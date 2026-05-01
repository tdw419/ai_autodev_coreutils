#!/usr/bin/env python3
"""
Workspace Lifecycle Management for the Hermes Agent Orchestrator.

Manages workspace creation, state transitions, expiration, and cleanup.
Each workspace corresponds to a GitHub issue and follows a defined lifecycle:

  created -> claimed -> in-progress -> completed -> merged -> archived
             -> abandoned -> archived
             -> failed -> retried (-> in-progress)

Usage:
    python3 workspace_manager.py --create ISSUE_NUMBER --title "Fix bug"
    python3 workspace_manager.py --status ISSUE_NUMBER
    python3 workspace_manager.py --transition ISSUE_NUMBER --to in-progress
    python3 workspace_manager.py --list [--status STATUS]
    python3 workspace_manager.py --expire --max-age HOURS
    python3 workspace_manager.py --report
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional

PROJECT_DIR = Path(os.environ.get(
    "ORCH_PROJECT_DIR",
    os.path.expanduser("~/zion/projects/agent-orchestration"),
))
WORKSPACES_DIR = PROJECT_DIR / "workspaces"


class WorkspaceStatus(str, Enum):
    """Valid workspace lifecycle states."""
    CREATED = "created"
    CLAIMED = "claimed"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    MERGED = "merged"
    FAILED = "failed"
    ABANDONED = "abandoned"
    ARCHIVED = "archived"

    @classmethod
    def values(cls):
        return [s.value for s in cls]


# Valid state transitions: from_state -> [to_states]
VALID_TRANSITIONS = {
    WorkspaceStatus.CREATED: [WorkspaceStatus.CLAIMED, WorkspaceStatus.ABANDONED],
    WorkspaceStatus.CLAIMED: [WorkspaceStatus.IN_PROGRESS, WorkspaceStatus.ABANDONED],
    WorkspaceStatus.IN_PROGRESS: [WorkspaceStatus.COMPLETED, WorkspaceStatus.FAILED, WorkspaceStatus.ABANDONED],
    WorkspaceStatus.COMPLETED: [WorkspaceStatus.MERGED, WorkspaceStatus.ARCHIVED],
    WorkspaceStatus.FAILED: [WorkspaceStatus.IN_PROGRESS, WorkspaceStatus.ABANDONED],
    WorkspaceStatus.MERGED: [WorkspaceStatus.ARCHIVED],
    WorkspaceStatus.ABANDONED: [WorkspaceStatus.ARCHIVED],
    WorkspaceStatus.ARCHIVED: [],  # Terminal state
}

# States considered "active" (not eligible for auto-cleanup)
ACTIVE_STATUSES = {
    WorkspaceStatus.CREATED,
    WorkspaceStatus.CLAIMED,
    WorkspaceStatus.IN_PROGRESS,
}

# Default workspace TTL in hours
DEFAULT_TTL_HOURS = 168  # 1 week


def _workspace_dir(issue_number: int | str) -> Path:
    """Get the workspace directory for an issue number."""
    return WORKSPACES_DIR / str(issue_number)


def _meta_path(issue_number: int | str) -> Path:
    """Get the meta.json path for an issue number."""
    return _workspace_dir(issue_number) / "meta.json"


def _read_meta(issue_number: int | str) -> dict | None:
    """Read workspace metadata. Returns None if not found."""
    path = _meta_path(issue_number)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return None


def _write_meta(issue_number: int | str, meta: dict) -> None:
    """Write workspace metadata."""
    ws_dir = _workspace_dir(issue_number)
    ws_dir.mkdir(parents=True, exist_ok=True)
    _meta_path(issue_number).write_text(json.dumps(meta, indent=2))


# --- Workspace Creation ---

def create_workspace(
    issue_number: int | str,
    title: str = "",
    description: str = "",
    labels: list[str] | None = None,
    pipeline: str = "default",
) -> dict:
    """
    Create a new workspace for an issue.

    Args:
        issue_number: GitHub issue number.
        title: Issue title.
        description: Issue description/body.
        labels: GitHub labels.
        pipeline: Pipeline name to use.

    Returns:
        Workspace metadata dict.
    """
    ws_dir = _workspace_dir(issue_number)
    if ws_dir.exists():
        meta = _read_meta(issue_number)
        if meta:
            return {"error": f"Workspace already exists for issue #{issue_number}", "meta": meta}

    ws_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now().isoformat()

    meta = {
        "issue_number": int(issue_number),
        "title": title,
        "description": description,
        "labels": labels or [],
        "status": WorkspaceStatus.CREATED.value,
        "pipeline": pipeline,
        "created_at": now,
        "updated_at": now,
        "claimed_at": None,
        "completed_at": None,
        "merged_at": None,
        "attempts": 0,
        "last_run_id": None,
    }

    _write_meta(issue_number, meta)
    return meta


# --- State Transitions ---

def transition_workspace(
    issue_number: int | str,
    to_status: str,
    run_id: str | None = None,
    note: str = "",
) -> dict:
    """
    Transition a workspace to a new status.

    Args:
        issue_number: GitHub issue number.
        to_status: Target status (must be a valid WorkspaceStatus value).
        run_id: Optional pipeline run ID.
        note: Optional note about the transition.

    Returns:
        Updated metadata dict, or error dict.
    """
    meta = _read_meta(issue_number)
    if meta is None:
        return {"error": f"No workspace found for issue #{issue_number}"}

    current = WorkspaceStatus(meta["status"])
    target = WorkspaceStatus(to_status)

    valid_targets = VALID_TRANSITIONS.get(current, [])
    if target not in valid_targets:
        return {
            "error": f"Invalid transition: {current.value} -> {target.value}",
            "valid": [t.value for t in valid_targets],
        }

    now = datetime.now().isoformat()
    meta["updated_at"] = now

    if target == WorkspaceStatus.CLAIMED:
        meta["claimed_at"] = now
    elif target == WorkspaceStatus.IN_PROGRESS:
        if current != WorkspaceStatus.FAILED:
            meta["attempts"] += 1
        meta["status"] = target.value
    elif target == WorkspaceStatus.COMPLETED:
        meta["completed_at"] = now
    elif target == WorkspaceStatus.MERGED:
        meta["merged_at"] = now
    elif target == WorkspaceStatus.FAILED:
        pass  # Just update status

    if target == WorkspaceStatus.FAILED:
        meta["fail_note"] = note
    elif "fail_note" in meta:
        del meta["fail_note"]

    meta["status"] = target.value

    if run_id:
        meta["last_run_id"] = run_id

    _write_meta(issue_number, meta)
    return meta


# --- Workspace Status ---

def get_workspace_status(issue_number: int | str) -> dict | None:
    """Get workspace status and metadata."""
    meta = _read_meta(issue_number)
    if meta is None:
        return None

    # Add computed fields
    ws_dir = _workspace_dir(issue_number)
    if ws_dir.exists():
        file_count = sum(1 for f in ws_dir.rglob("*") if f.is_file())
        size_bytes = sum(f.stat().st_size for f in ws_dir.rglob("*") if f.is_file())
    else:
        file_count = 0
        size_bytes = 0

    meta["file_count"] = file_count
    meta["size_bytes"] = size_bytes

    # Compute age
    if meta.get("created_at"):
        created = datetime.fromisoformat(meta["created_at"])
        age_hours = (datetime.now() - created).total_seconds() / 3600
        meta["age_hours"] = round(age_hours, 1)

    # Compute valid next transitions
    current = WorkspaceStatus(meta["status"])
    meta["valid_transitions"] = [t.value for t in VALID_TRANSITIONS.get(current, [])]

    return meta


# --- Workspace Listing ---

def list_workspaces(status: str | None = None) -> list[dict]:
    """
    List all workspaces, optionally filtered by status.

    Args:
        status: Filter by status. If None, list all.

    Returns:
        List of workspace metadata dicts.
    """
    if not WORKSPACES_DIR.exists():
        return []

    workspaces = []
    for ws_dir in sorted(WORKSPACES_DIR.iterdir()):
        if not ws_dir.is_dir():
            continue
        meta_path = ws_dir / "meta.json"
        if not meta_path.exists():
            continue
        try:
            meta = json.loads(meta_path.read_text())
        except json.JSONDecodeError:
            continue

        if status and meta.get("status") != status:
            continue

        workspaces.append(meta)

    return workspaces


# --- Expiration ---

def expire_workspaces(max_age_hours: int = DEFAULT_TTL_HOURS, dry_run: bool = True) -> list[dict]:
    """
    Find and optionally expire stale workspaces.

    Workspaces that are in non-terminal states past their TTL get
    transitioned to ABANDONED.

    Args:
        max_age_hours: Age threshold in hours.
        dry_run: If True, report without transitioning.

    Returns:
        List of expired workspace actions.
    """
    actions = []

    for ws_dir in sorted(WORKSPACES_DIR.iterdir()):
        if not ws_dir.is_dir():
            continue
        meta = _read_meta(str(ws_dir.name))
        if meta is None:
            continue

        status = WorkspaceStatus(meta.get("status", "created"))
        if status in ACTIVE_STATUSES or status == WorkspaceStatus.FAILED:
            created_at = meta.get("created_at")
            if not created_at:
                continue
            created = datetime.fromisoformat(created_at)
            age_hours = (datetime.now() - created).total_seconds() / 3600

            if age_hours > max_age_hours:
                action = {
                    "issue_number": meta.get("issue_number"),
                    "title": meta.get("title", ""),
                    "current_status": status.value,
                    "age_hours": round(age_hours, 1),
                    "action": "would_abandon" if dry_run else "abandoned",
                }

                if not dry_run:
                    transition_workspace(
                        str(ws_dir.name),
                        WorkspaceStatus.ABANDONED.value,
                        note=f"Auto-expired after {round(age_hours)} hours",
                    )

                actions.append(action)

    return actions


# --- Summary Report ---

def get_report() -> dict:
    """Generate a summary report of all workspaces."""
    workspaces = list_workspaces()
    if not workspaces:
        return {"total": 0, "by_status": {}, "active": 0, "completed": 0}

    by_status = {}
    active = 0
    completed = 0

    for ws in workspaces:
        status = ws.get("status", "unknown")
        by_status[status] = by_status.get(status, 0) + 1
        if WorkspaceStatus(status) in ACTIVE_STATUSES:
            active += 1
        elif WorkspaceStatus(status) == WorkspaceStatus.COMPLETED:
            completed += 1

    return {
        "total": len(workspaces),
        "by_status": by_status,
        "active": active,
        "completed": completed,
        "workspaces": workspaces,
    }


def main():
    parser = argparse.ArgumentParser(description="Workspace lifecycle management")
    parser.add_argument("--create", type=int, help="Create workspace for issue number")
    parser.add_argument("--title", help="Issue title (for --create)")
    parser.add_argument("--status", type=int, help="Get workspace status")
    parser.add_argument("--transition", type=int, help="Transition workspace for issue")
    parser.add_argument("--to", help="Target status (for --transition)")
    parser.add_argument("--list", action="store_true", help="List workspaces")
    parser.add_argument("--filter-status", help="Filter by status (for --list)")
    parser.add_argument("--expire", action="store_true", help="Expire stale workspaces")
    parser.add_argument("--max-age", type=int, default=DEFAULT_TTL_HOURS, help="Max age in hours")
    parser.add_argument("--force", action="store_true", help="Actually expire (not dry-run)")
    parser.add_argument("--report", action="store_true", help="Summary report")

    args = parser.parse_args()

    if args.create:
        result = create_workspace(args.create, title=args.title or "")
        print(json.dumps(result, indent=2))
    elif args.status:
        result = get_workspace_status(args.status)
        if result is None:
            print(json.dumps({"error": "Workspace not found"}))
        else:
            print(json.dumps(result, indent=2))
    elif args.transition:
        if not args.to:
            parser.error("--to is required with --transition")
        result = transition_workspace(args.transition, args.to)
        print(json.dumps(result, indent=2))
    elif args.list:
        result = list_workspaces(status=args.filter_status)
        print(json.dumps(result, indent=2))
    elif args.expire:
        result = expire_workspaces(max_age_hours=args.max_age, dry_run=not args.force)
        print(json.dumps(result, indent=2))
    elif args.report:
        result = get_report()
        print(json.dumps(result, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
