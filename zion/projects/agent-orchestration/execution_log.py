#!/usr/bin/env python3
"""
Execution log storage for the Hermes Agent Orchestrator.

Records every pipeline run as a JSON file in ~/.orchestrator/logs/runs/.
Each file is named by timestamp and contains the full execution result
including node results, duration, context, and final status.

Also provides JSON Lines logging for orchestrator loop iterations in
~/.orchestrator/logs/loops/YYYY-MM-DD.jsonl.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any


LOG_DIR = Path(os.path.expanduser("~/.orchestrator/logs"))
RUNS_DIR = LOG_DIR / "runs"
LOOPS_DIR = LOG_DIR / "loops"


def _ensure_dirs():
    """Create log directories if they don't exist."""
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    LOOPS_DIR.mkdir(parents=True, exist_ok=True)


def log_pipeline_run(result_dict: dict) -> str:
    """
    Log a pipeline execution result to a JSON file.

    Args:
        result_dict: The ExecutionResult.to_dict() output.

    Returns:
        The run ID (filename without extension).
    """
    _ensure_dirs()
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    log_path = RUNS_DIR / f"{run_id}.json"

    # Enrich with log metadata
    result_dict["_logged_at"] = datetime.now().isoformat()
    result_dict["_run_id"] = run_id

    with open(log_path, "w") as f:
        json.dump(result_dict, f, indent=2)

    return run_id


def log_loop_iteration(summary: dict) -> None:
    """
    Append an orchestrator loop iteration summary to the daily log.

    Args:
        summary: The run_loop() return dict.
    """
    _ensure_dirs()
    today = datetime.now().strftime("%Y-%m-%d")
    log_path = LOOPS_DIR / f"{today}.jsonl"

    entry = {
        "_logged_at": datetime.now().isoformat(),
        **summary,
    }

    with open(log_path, "a") as f:
        f.write(json.dumps(entry) + "\n")


def list_runs(limit: int = 20, status: str | None = None) -> list[dict]:
    """
    List recent pipeline runs from the log directory.

    Args:
        limit: Max number of runs to return.
        status: Optional filter by status (completed, failed, partial).

    Returns:
        List of run summary dicts, newest first.
    """
    if not RUNS_DIR.exists():
        return []

    runs = []
    for f in sorted(RUNS_DIR.glob("*.json"), reverse=True)[:limit]:
        try:
            data = json.loads(f.read_text())
            if status and data.get("status") != status:
                continue
            runs.append({
                "run_id": data.get("_run_id", f.stem),
                "pipeline_name": data.get("pipeline_name", "unknown"),
                "status": data.get("status", "unknown"),
                "total_nodes": data.get("total_nodes", 0),
                "completed_nodes": data.get("completed_nodes", 0),
                "failed_nodes": data.get("failed_nodes", 0),
                "duration_seconds": data.get("duration_seconds", 0),
                "logged_at": data.get("_logged_at", ""),
            })
        except (json.JSONDecodeError, KeyError):
            continue

    return runs


def get_run(run_id: str) -> dict | None:
    """
    Load a specific run's full details.

    Args:
        run_id: The run ID (filename without .json).

    Returns:
        The full run data dict, or None if not found.
    """
    log_path = RUNS_DIR / f"{run_id}.json"
    if not log_path.exists():
        return None

    try:
        return json.loads(log_path.read_text())
    except json.JSONDecodeError:
        return None


def get_stats() -> dict:
    """Get summary statistics across all logged runs."""
    if not RUNS_DIR.exists():
        return {"total_runs": 0}

    runs = list(RUNS_DIR.glob("*.json"))
    if not runs:
        return {"total_runs": 0}

    statuses = {"completed": 0, "failed": 0, "partial": 0}
    total_duration = 0.0
    total_nodes = 0

    for f in runs:
        try:
            data = json.loads(f.read_text())
            s = data.get("status", "unknown")
            if s in statuses:
                statuses[s] += 1
            total_duration += data.get("duration_seconds", 0)
            total_nodes += data.get("total_nodes", 0)
        except (json.JSONDecodeError, KeyError):
            continue

    return {
        "total_runs": len(runs),
        "by_status": statuses,
        "total_duration_seconds": round(total_duration, 2),
        "avg_duration_seconds": round(total_duration / len(runs), 2) if runs else 0,
        "total_nodes_executed": total_nodes,
    }


def get_loop_history(date: str | None = None, limit: int = 50) -> list[dict]:
    """
    Read orchestrator loop iteration logs.

    Args:
        date: Optional date string (YYYY-MM-DD). Defaults to today.
        limit: Max entries to return.

    Returns:
        List of loop iteration dicts.
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    log_path = LOOPS_DIR / f"{date}.jsonl"
    if not log_path.exists():
        return []

    entries = []
    with open(log_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    return entries[-limit:]


def prune_old_runs(keep_days: int = 30) -> int:
    """
    Remove run log files older than keep_days.

    Returns:
        Number of files removed.
    """
    import time
    cutoff = time.time() - (keep_days * 86400)
    removed = 0

    for f in RUNS_DIR.glob("*.json"):
        if f.stat().st_mtime < cutoff:
            f.unlink()
            removed += 1

    for f in LOOPS_DIR.glob("*.jsonl"):
        if f.stat().st_mtime < cutoff:
            f.unlink()
            removed += 1

    return removed
