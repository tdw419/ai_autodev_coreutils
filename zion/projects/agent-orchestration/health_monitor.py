#!/usr/bin/env python3
"""
Agent Health Monitoring (Deacon Pattern) for the Hermes Agent Orchestrator.

A lightweight watchdog that monitors orchestrator health, detects stuck/failed
agents, and triggers recovery actions. The "Deacon" watches over the flock.

Monitors:
- Stuck workspaces (in-progress too long)
- Failed pipeline runs (repeated failures)
- Resource usage (disk, memory)
- Pipeline success rate trends
- Agent spawn failures

Usage:
    python3 health_monitor.py --check
    python3 health_monitor.py --watch --interval 60
    python3 health_monitor.py --report
    python3 health_monitor.py --alerts
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

PROJECT_DIR = Path(os.environ.get(
    "ORCH_PROJECT_DIR",
    os.path.expanduser("~/zion/projects/agent-orchestration"),
))
WORKSPACES_DIR = PROJECT_DIR / "workspaces"
ORCH_DIR = Path(os.path.expanduser("~/.orchestrator"))
LOGS_DIR = ORCH_DIR / "logs"
HEALTH_DIR = LOGS_DIR / "health"

# Thresholds
DEFAULT_STUCK_THRESHOLD_HOURS = 4
DEFAULT_MAX_FAILURES = 3
DEFAULT_SUCCESS_RATE_FLOOR = 0.5  # Alert if success rate drops below 50%


def _ensure_dirs():
    HEALTH_DIR.mkdir(parents=True, exist_ok=True)


# --- Health Checks ---

def check_stuck_workspaces(threshold_hours: int = DEFAULT_STUCK_THRESHOLD_HOURS) -> list[dict]:
    """Find workspaces stuck in-progress beyond threshold."""
    if not WORKSPACES_DIR.exists():
        return []

    stuck = []
    cutoff = datetime.now() - timedelta(hours=threshold_hours)

    for ws in sorted(WORKSPACES_DIR.iterdir()):
        if not ws.is_dir():
            continue
        meta_path = ws / "meta.json"
        if not meta_path.exists():
            continue
        try:
            meta = json.loads(meta_path.read_text())
        except json.JSONDecodeError:
            continue

        if meta.get("status") == "in-progress":
            updated = meta.get("updated_at")
            if updated:
                updated_dt = datetime.fromisoformat(updated)
                if updated_dt < cutoff:
                    stuck.append({
                        "issue_number": meta.get("issue_number"),
                        "title": meta.get("title", ""),
                        "status": meta["status"],
                        "updated_at": updated,
                        "stuck_hours": (datetime.now() - updated_dt).total_seconds() / 3600,
                        "attempts": meta.get("attempts", 0),
                    })

    return stuck


def check_failed_workspaces(max_failures: int = DEFAULT_MAX_FAILURES) -> list[dict]:
    """Find workspaces with too many failed attempts."""
    if not WORKSPACES_DIR.exists():
        return []

    failed = []
    for ws in sorted(WORKSPACES_DIR.iterdir()):
        if not ws.is_dir():
            continue
        meta_path = ws / "meta.json"
        if not meta_path.exists():
            continue
        try:
            meta = json.loads(meta_path.read_text())
        except json.JSONDecodeError:
            continue

        if meta.get("status") == "failed" or meta.get("attempts", 0) >= max_failures:
            failed.append({
                "issue_number": meta.get("issue_number"),
                "title": meta.get("title", ""),
                "status": meta.get("status"),
                "attempts": meta.get("attempts", 0),
                "fail_note": meta.get("fail_note", ""),
            })

    return failed


def check_resource_usage() -> dict:
    """Check disk and memory usage for the orchestrator."""
    usage = {}

    # Disk usage of workspaces
    if WORKSPACES_DIR.exists():
        du = subprocess.run(
            ["du", "-sb", str(WORKSPACES_DIR)],
            capture_output=True, text=True,
        )
        if du.returncode == 0 and du.stdout.strip():
            usage["workspaces_bytes"] = int(du.stdout.split()[0])

    # Disk usage of logs
    if LOGS_DIR.exists():
        du = subprocess.run(
            ["du", "-sb", str(LOGS_DIR)],
            capture_output=True, text=True,
        )
        if du.returncode == 0 and du.stdout.strip():
            usage["logs_bytes"] = int(du.stdout.split()[0])

    # Workspace count
    if WORKSPACES_DIR.exists():
        usage["workspace_count"] = sum(1 for d in WORKSPACES_DIR.iterdir() if d.is_dir())

    # Active workspace count
    active = 0
    if WORKSPACES_DIR.exists():
        for ws in WORKSPACES_DIR.iterdir():
            meta_path = ws / "meta.json"
            if meta_path.exists():
                try:
                    meta = json.loads(meta_path.read_text())
                    if meta.get("status") in ("in-progress", "claimed"):
                        active += 1
                except json.JSONDecodeError:
                    pass
    usage["active_workspaces"] = active

    return usage


def check_pipeline_health() -> dict:
    """Analyze recent pipeline run success rate."""
    runs_dir = LOGS_DIR / "runs"
    if not runs_dir.exists():
        return {"total_runs": 0, "success_rate": 0, "recent": []}

    runs = []
    for f in sorted(runs_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)[:50]:
        try:
            data = json.loads(f.read_text())
            runs.append(data)
        except json.JSONDecodeError:
            continue

    if not runs:
        return {"total_runs": 0, "success_rate": 0, "recent": []}

    completed = sum(1 for r in runs if r.get("status") == "completed")
    failed = sum(1 for r in runs if r.get("status") == "failed")
    success_rate = completed / max(len(runs), 1)

    # Last 10 runs detail
    recent = []
    for r in runs[:10]:
        recent.append({
            "run_id": r.get("run_id", f.stem),
            "status": r.get("status"),
            "pipeline": r.get("pipeline_name"),
            "duration": r.get("duration_seconds"),
        })

    return {
        "total_runs": len(runs),
        "completed": completed,
        "failed": failed,
        "success_rate": round(success_rate, 3),
        "recent": recent,
    }


# --- Alert Generation ---

def generate_alerts(
    stuck_threshold: int = DEFAULT_STUCK_THRESHOLD_HOURS,
    max_failures: int = DEFAULT_MAX_FAILURES,
    success_rate_floor: float = DEFAULT_SUCCESS_RATE_FLOOR,
) -> list[dict]:
    """Generate health alerts based on all checks."""
    alerts = []
    severity_counts = {"critical": 0, "warning": 0, "info": 0}

    # Check stuck workspaces
    stuck = check_stuck_workspaces(stuck_threshold)
    for ws in stuck:
        alert = {
            "type": "stuck_workspace",
            "severity": "critical" if ws["stuck_hours"] > stuck_threshold * 2 else "warning",
            "message": f"Issue #{ws['issue_number']} stuck in-progress for {ws['stuck_hours']:.1f}h",
            "detail": ws,
        }
        alerts.append(alert)
        severity_counts[alert["severity"]] += 1

    # Check failed workspaces
    failed = check_failed_workspaces(max_failures)
    for ws in failed:
        alert = {
            "type": "failed_workspace",
            "severity": "critical" if ws["attempts"] >= max_failures * 2 else "warning",
            "message": f"Issue #{ws['issue_number']} failed after {ws['attempts']} attempts",
            "detail": ws,
        }
        alerts.append(alert)
        severity_counts[alert["severity"]] += 1

    # Check pipeline health
    health = check_pipeline_health()
    if health["total_runs"] > 5 and health["success_rate"] < success_rate_floor:
        alert = {
            "type": "low_success_rate",
            "severity": "warning",
            "message": f"Pipeline success rate {health['success_rate']:.1%} below {success_rate_floor:.1%} floor",
            "detail": health,
        }
        alerts.append(alert)
        severity_counts[alert["severity"]] += 1

    # Check resources
    resources = check_resource_usage()
    ws_bytes = resources.get("workspaces_bytes", 0)
    if ws_bytes > 10 * 1024 * 1024 * 1024:  # 10GB
        alert = {
            "type": "high_disk_usage",
            "severity": "warning",
            "message": f"Workspaces using {ws_bytes / (1024**3):.1f}GB",
            "detail": resources,
        }
        alerts.append(alert)
        severity_counts[alert["severity"]] += 1

    return alerts


# --- Full Health Check ---

def run_health_check() -> dict:
    """Run all health checks and return a comprehensive report."""
    _ensure_dirs()

    stuck = check_stuck_workspaces()
    failed = check_failed_workspaces()
    resources = check_resource_usage()
    pipeline = check_pipeline_health()
    alerts = generate_alerts()

    report = {
        "timestamp": datetime.now().isoformat(),
        "status": "healthy" if not any(a["severity"] == "critical" for a in alerts) else "degraded",
        "stuck_workspaces": stuck,
        "failed_workspaces": failed,
        "resources": resources,
        "pipeline_health": pipeline,
        "alerts": alerts,
        "alert_counts": {
            "critical": sum(1 for a in alerts if a["severity"] == "critical"),
            "warning": sum(1 for a in alerts if a["severity"] == "warning"),
            "info": sum(1 for a in alerts if a["severity"] == "info"),
        },
    }

    # Save report
    report_path = HEALTH_DIR / f"{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    report_path.write_text(json.dumps(report, indent=2))

    return report


def get_recent_reports(count: int = 10) -> list[dict]:
    """Get recent health check reports."""
    if not HEALTH_DIR.exists():
        return []

    reports = []
    for f in sorted(HEALTH_DIR.glob("*.json"), reverse=True)[:count]:
        try:
            reports.append(json.loads(f.read_text()))
        except json.JSONDecodeError:
            continue
    return reports


def main():
    parser = argparse.ArgumentParser(description="Agent health monitoring")
    parser.add_argument("--check", action="store_true", help="Run health check")
    parser.add_argument("--watch", action="store_true", help="Watch mode (continuous)")
    parser.add_argument("--interval", type=int, default=60, help="Watch interval in seconds")
    parser.add_argument("--report", action="store_true", help="Show health report")
    parser.add_argument("--alerts", action="store_true", help="Show alerts only")

    args = parser.parse_args()

    if args.check or args.report:
        result = run_health_check()
        print(json.dumps(result, indent=2))
    elif args.alerts:
        alerts = generate_alerts()
        if alerts:
            print(json.dumps(alerts, indent=2))
        else:
            print("No alerts.")
    elif args.watch:
        print(f"Watching health every {args.interval}s (Ctrl+C to stop)...")
        try:
            while True:
                result = run_health_check()
                status = result["status"].upper()
                alert_count = result["alert_counts"]["critical"]
                ts = datetime.now().strftime("%H:%M:%S")
                print(f"[{ts}] Status: {status} | Critical alerts: {alert_count}")
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\nStopped.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
