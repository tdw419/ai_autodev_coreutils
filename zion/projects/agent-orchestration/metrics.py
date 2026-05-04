#!/usr/bin/env python3
"""
Baseline metrics collection for the Hermes Agent Orchestrator.

Collects and aggregates operational metrics from across the system:
- Pipeline execution stats (runs, success rate, duration)
- Workspace lifecycle metrics (creation rate, stuck workspaces, completion rate)
- Cost tracking summaries (per-repo, daily, period)
- Health monitor integration (alerts, resource usage)

Metrics are stored as JSON files and can be queried via CLI or imported
as a module for dashboarding and alerting.

Usage:
    python3 metrics.py snapshot                  # Take a metrics snapshot
    python3 metrics.py snapshot --json           # JSON output
    python3 metrics.py trend --days 7            # Show 7-day trend
    python3 metrics.py export --format prometheus # Export for Prometheus
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Direct imports from orchestrator modules
from execution_log import get_stats, list_runs
from workspace_manager import get_report, list_workspaces, WorkspaceStatus
from health_monitor import (
    check_stuck_workspaces,
    check_failed_workspaces,
    check_resource_usage,
    check_pipeline_health,
    generate_alerts,
)
from cost_tracker import (
    get_all_repos,
    get_period_cost,
    check_budget,
    record_usage,
)

METRICS_DIR = Path(os.path.expanduser("~/.orchestrator/metrics"))


def _ensure_dir():
    """Ensure metrics directory exists."""
    METRICS_DIR.mkdir(parents=True, exist_ok=True)


def take_snapshot() -> dict:
    """
    Take a comprehensive metrics snapshot.

    Returns a dict with all current metrics, suitable for
    storage, display, or export.
    """
    snapshot = {
        "timestamp": datetime.now().isoformat(),
        "pipelines": _pipeline_metrics(),
        "workspaces": _workspace_metrics(),
        "costs": _cost_metrics(),
        "health": _health_metrics(),
    }
    return snapshot


def save_snapshot(snapshot: dict | None = None) -> Path:
    """
    Save a metrics snapshot to disk.

    Args:
        snapshot: Snapshot dict. If None, takes a fresh snapshot.

    Returns:
        Path to the saved snapshot file.
    """
    _ensure_dir()
    if snapshot is None:
        snapshot = take_snapshot()

    filename = f"snapshot-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    path = METRICS_DIR / filename
    path.write_text(json.dumps(snapshot, indent=2))
    return path


def load_recent_snapshots(count: int = 10) -> list[dict]:
    """Load the most recent snapshots from disk."""
    if not METRICS_DIR.exists():
        return []

    snapshots = []
    for f in sorted(METRICS_DIR.glob("snapshot-*.json"), reverse=True)[:count]:
        try:
            snapshots.append(json.loads(f.read_text()))
        except (json.JSONDecodeError, OSError):
            continue
    return snapshots


def _pipeline_metrics() -> dict:
    """Collect pipeline execution metrics."""
    stats = get_stats()
    health = check_pipeline_health()

    return {
        "total_runs": stats.get("total_runs", 0),
        "by_status": stats.get("by_status", {}),
        "success_rate": health.get("success_rate", 0.0),
        "recent_runs": health.get("recent", [])[:5],
        "avg_duration_seconds": _compute_avg_duration(list_runs(limit=20)),
    }


def _workspace_metrics() -> dict:
    """Collect workspace lifecycle metrics."""
    report = get_report()
    stuck = check_stuck_workspaces()
    failed = check_failed_workspaces()

    # Compute completion rate
    total = report.get("total", 0)
    completed = report.get("completed", 0)
    completion_rate = completed / total if total > 0 else 0.0

    return {
        "total": total,
        "active": report.get("active", 0),
        "completed": completed,
        "completion_rate": round(completion_rate, 3),
        "by_status": report.get("by_status", {}),
        "stuck_count": len(stuck),
        "stuck_details": stuck[:5],
        "failed_count": len(failed),
        "failed_details": failed[:5],
    }


def _cost_metrics() -> dict:
    """Collect cost tracking metrics."""
    repos = get_all_repos()
    repo_costs = {}

    for repo in repos:
        daily = get_period_cost(repo, days=1)
        weekly = get_period_cost(repo, days=7)
        repo_costs[repo] = {
            "daily_tokens": daily.get("total_tokens", 0),
            "daily_cost": daily.get("total_cost", 0.0),
            "weekly_tokens": weekly.get("total_tokens", 0),
            "weekly_cost": weekly.get("total_cost", 0.0),
        }

    total_weekly = sum(r["weekly_cost"] for r in repo_costs.values())

    return {
        "tracked_repos": len(repos),
        "repos": repo_costs,
        "total_weekly_cost": round(total_weekly, 4),
    }


def _health_metrics() -> dict:
    """Collect health monitoring metrics."""
    resources = check_resource_usage()
    alerts = generate_alerts()

    return {
        "resources": resources,
        "alert_count": len(alerts),
        "alerts_by_severity": {
            "critical": sum(1 for a in alerts if a["severity"] == "critical"),
            "warning": sum(1 for a in alerts if a["severity"] == "warning"),
            "info": sum(1 for a in alerts if a["severity"] == "info"),
        },
        "recent_alerts": alerts[:5],
    }


def _compute_avg_duration(runs: list[dict]) -> float:
    """Compute average duration from recent runs."""
    if not runs:
        return 0.0
    durations = [r.get("duration_seconds", 0) for r in runs if r.get("duration_seconds", 0) > 0]
    if not durations:
        return 0.0
    return round(sum(durations) / len(durations), 2)


def format_summary(snapshot: dict) -> str:
    """Format a snapshot as a human-readable summary."""
    lines = [
        f"{'='*60}",
        f"  Orchestrator Metrics — {snapshot['timestamp']}",
        f"{'='*60}",
        "",
        "📊 Pipelines",
        f"   Total runs:      {snapshot['pipelines']['total_runs']}",
        f"   Success rate:    {snapshot['pipelines']['success_rate']:.1%}",
        f"   Avg duration:    {snapshot['pipelines']['avg_duration_seconds']}s",
        f"   By status:       {snapshot['pipelines']['by_status']}",
        "",
        "📁 Workspaces",
        f"   Total:           {snapshot['workspaces']['total']}",
        f"   Active:          {snapshot['workspaces']['active']}",
        f"   Completed:       {snapshot['workspaces']['completed']}",
        f"   Completion rate: {snapshot['workspaces']['completion_rate']:.1%}",
        f"   Stuck:           {snapshot['workspaces']['stuck_count']}",
        f"   Failed:          {snapshot['workspaces']['failed_count']}",
        "",
        "💰 Costs",
        f"   Tracked repos:   {snapshot['costs']['tracked_repos']}",
        f"   Weekly total:    ${snapshot['costs']['total_weekly_cost']:.4f}",
    ]

    for repo, cost in snapshot["costs"]["repos"].items():
        lines.append(f"     {repo}: ${cost['weekly_cost']:.4f}/wk")

    lines.extend([
        "",
        "🏥 Health",
        f"   Alerts:          {snapshot['health']['alert_count']}",
        f"   Critical:        {snapshot['health']['alerts_by_severity']['critical']}",
        f"   Warning:         {snapshot['health']['alerts_by_severity']['warning']}",
    ])

    resources = snapshot["health"]["resources"]
    if "workspaces_bytes" in resources:
        ws_mb = resources["workspaces_bytes"] / (1024 * 1024)
        lines.append(f"   Workspace disk:  {ws_mb:.1f}MB")

    return "\n".join(lines)


def export_prometheus(snapshot: dict) -> str:
    """
    Export metrics in Prometheus text exposition format.

    Returns a string suitable for a /metrics endpoint.
    """
    lines = [
        "# HELP orch_pipeline_total Total pipeline runs",
        "# TYPE orch_pipeline_total counter",
        f"orch_pipeline_total {snapshot['pipelines']['total_runs']}",
        "",
        "# HELP orch_pipeline_success_rate Pipeline success rate (0-1)",
        "# TYPE orch_pipeline_success_rate gauge",
        f"orch_pipeline_success_rate {snapshot['pipelines']['success_rate']}",
        "",
        "# HELP orch_pipeline_avg_duration_seconds Average pipeline duration",
        "# TYPE orch_pipeline_avg_duration_seconds gauge",
        f"orch_pipeline_avg_duration_seconds {snapshot['pipelines']['avg_duration_seconds']}",
        "",
        "# HELP orch_workspace_total Total workspaces",
        "# TYPE orch_workspace_total gauge",
        f"orch_workspace_total {snapshot['workspaces']['total']}",
        "",
        "# HELP orch_workspace_active Active workspaces",
        "# TYPE orch_workspace_active gauge",
        f"orch_workspace_active {snapshot['workspaces']['active']}",
        "",
        "# HELP orch_workspace_completion_rate Workspace completion rate (0-1)",
        "# TYPE orch_workspace_completion_rate gauge",
        f"orch_workspace_completion_rate {snapshot['workspaces']['completion_rate']}",
        "",
        "# HELP orch_workspace_stuck_count Stuck workspaces",
        "# TYPE orch_workspace_stuck_count gauge",
        f"orch_workspace_stuck_count {snapshot['workspaces']['stuck_count']}",
        "",
        "# HELP orch_cost_weekly_total Weekly cost in dollars",
        "# TYPE orch_cost_weekly_total gauge",
        f"orch_cost_weekly_total {snapshot['costs']['total_weekly_cost']}",
        "",
        "# HELP orch_health_alerts_total Total active alerts",
        "# TYPE orch_health_alerts_total gauge",
        f"orch_health_alerts_total {snapshot['health']['alert_count']}",
        "",
        "# HELP orch_health_alerts_critical Critical alerts",
        "# TYPE orch_health_alerts_critical gauge",
        f"orch_health_alerts_critical {snapshot['health']['alerts_by_severity']['critical']}",
        "",
    ]

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Orchestrator metrics collection")
    sub = parser.add_subparsers(dest="command")

    # snapshot
    snap = sub.add_parser("snapshot", help="Take and display a metrics snapshot")
    snap.add_argument("--save", action="store_true", help="Save snapshot to disk")
    snap.add_argument("--json", action="store_true", help="Output as JSON")

    # trend
    trend = sub.add_parser("trend", help="Show metrics trend from saved snapshots")
    trend.add_argument("--days", type=int, default=7, help="Days to look back")

    # export
    export = sub.add_parser("export", help="Export metrics")
    export.add_argument("--format", choices=["prometheus", "json"], default="json",
                        help="Export format")

    # history
    hist = sub.add_parser("history", help="List saved snapshots")
    hist.add_argument("--count", type=int, default=10, help="Number of snapshots")

    args = parser.parse_args()

    if args.command == "snapshot":
        snapshot = take_snapshot()

        if args.save:
            path = save_snapshot(snapshot)
            print(f"Snapshot saved to {path}")

        if args.json:
            print(json.dumps(snapshot, indent=2))
        else:
            print(format_summary(snapshot))

    elif args.command == "trend":
        snapshots = load_recent_snapshots(count=20)
        if not snapshots:
            print("No saved snapshots found. Run 'metrics.py snapshot --save' first.")
            return

        # Show trend summary
        print(f"{'Timestamp':<22} {'Runs':>6} {'Success':>8} {'Active':>7} {'Stuck':>6} {'Alerts':>7}")
        print("-" * 60)
        for s in snapshots:
            ts = s["timestamp"][:19]
            runs = s["pipelines"]["total_runs"]
            rate = f"{s['pipelines']['success_rate']:.1%}"
            active = s["workspaces"]["active"]
            stuck = s["workspaces"]["stuck_count"]
            alerts = s["health"]["alert_count"]
            print(f"{ts:<22} {runs:>6} {rate:>8} {active:>7} {stuck:>6} {alerts:>7}")

    elif args.command == "export":
        snapshot = take_snapshot()

        if args.format == "prometheus":
            print(export_prometheus(snapshot))
        else:
            print(json.dumps(snapshot, indent=2))

    elif args.command == "history":
        snapshots = load_recent_snapshots(count=args.count)
        if not snapshots:
            print("No saved snapshots found.")
            return

        for s in snapshots:
            ts = s["timestamp"][:19]
            runs = s["pipelines"]["total_runs"]
            alerts = s["health"]["alert_count"]
            print(f"  {ts}  runs={runs}  alerts={alerts}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
