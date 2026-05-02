#!/usr/bin/env python3
"""
Merge Queue Manager for the Hermes Agent Orchestrator (Refinery Pattern).

Ordered queue that sequences PR merges to minimize conflicts. PRs are added
to a JSON Lines-backed queue, ordered by safety (no-conflict first), then
by fewest conflicts, then by age (oldest first). Before dequeuing, runs
conflict_detector to verify the merge is still safe.

Queue file: ~/.orchestrator/merge-queue.jsonl

Usage:
    python3 merge_queue.py enqueue --pr 42 --branch feature-xyz --repo owner/repo
    python3 merge_queue.py dequeue
    python3 merge_queue.py status
    python3 merge_queue.py reorder
    python3 merge_queue.py list
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

PROJECT_DIR = Path(os.environ.get(
    "ORCH_PROJECT_DIR",
    os.path.expanduser("~/zion/projects/agent-orchestration"),
))
ORCH_DIR = Path(os.path.expanduser("~/.orchestrator"))
QUEUE_FILE = ORCH_DIR / "merge-queue.jsonl"

# PR states
STATE_QUEUED = "queued"
STATE_READY = "ready"
STATE_NEEDS_REBASE = "needs-rebase"
STATE_MERGED = "merged"
STATE_FAILED = "failed"


def _ensure_queue_file():
    """Create queue directory and file if they don't exist."""
    ORCH_DIR.mkdir(parents=True, exist_ok=True)
    if not QUEUE_FILE.exists():
        QUEUE_FILE.write_text("")


def _read_queue() -> list[dict]:
    """Read all entries from the queue file."""
    _ensure_queue_file()
    entries = []
    for line in QUEUE_FILE.read_text().strip().split("\n"):
        line = line.strip()
        if line:
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                pass  # Skip malformed lines
    return entries


def _write_queue(entries: list[dict]):
    """Write all entries to the queue file."""
    _ensure_queue_file()
    lines = [json.dumps(e) for e in entries]
    QUEUE_FILE.write_text("\n".join(lines) + "\n" if lines else "")


def _conflict_score(entry: dict) -> int:
    """Get conflict count for sorting (0 = no conflicts = highest priority)."""
    return entry.get("conflict_count", 0)


def _enqueue_time(entry: dict) -> float:
    """Get enqueue time for sorting (older = higher priority)."""
    return entry.get("enqueued_at", time.time())


def _sort_queue(entries: list[dict]) -> list[dict]:
    """Sort queue: no-conflict first, then fewest conflicts, then oldest."""
    active = [e for e in entries if e.get("state") in (STATE_QUEUED, STATE_READY, STATE_NEEDS_REBASE)]
    inactive = [e for e in entries if e.get("state") not in (STATE_QUEUED, STATE_READY, STATE_NEEDS_REBASE)]

    # Sort active entries: READY first (no conflicts), then by conflict count, then by age
    def sort_key(e):
        state_priority = 0 if e.get("state") == STATE_READY else (1 if e.get("state") == STATE_QUEUED else 2)
        return (state_priority, _conflict_score(e), _enqueue_time(e))

    active.sort(key=sort_key)
    return active + inactive


def enqueue(pr: int, branch: str, repo: str = "", workspace: str = "") -> dict:
    """
    Add a PR to the merge queue.

    Returns:
        The created queue entry.
    """
    entries = _read_queue()

    # Check if PR is already in queue
    for e in entries:
        if e.get("pr") == pr and e.get("state") not in (STATE_MERGED, STATE_FAILED):
            return {"error": f"PR #{pr} is already in the queue (state: {e['state']})", "entry": e}

    # Run conflict detector
    conflict_count = 0
    conflict_files = []
    try:
        sys.path.insert(0, str(PROJECT_DIR))
        from conflict_detector import check_conflicts
        report = check_conflicts(branch)
        conflict_count = len(report.get("conflict_files", []))
        conflict_files = report.get("conflict_files", [])
        initial_state = STATE_NEEDS_REBASE if report.get("has_conflicts") else STATE_QUEUED
    except Exception:
        initial_state = STATE_QUEUED

    entry = {
        "pr": pr,
        "branch": branch,
        "repo": repo,
        "workspace": workspace,
        "state": initial_state,
        "conflict_count": conflict_count,
        "conflict_files": conflict_files,
        "enqueued_at": time.time(),
        "enqueued_at_iso": datetime.utcnow().isoformat() + "Z",
        "updated_at": time.time(),
        "updated_at_iso": datetime.utcnow().isoformat() + "Z",
        "merge_attempts": 0,
        "last_check_at": None,
    }

    entries.append(entry)
    entries = _sort_queue(entries)
    _write_queue(entries)
    return entry


def dequeue() -> Optional[dict]:
    """
    Pop the next PR from the queue (highest priority, active).

    Before returning, verifies the merge is still safe using conflict_detector.
    If new conflicts detected, moves PR to needs-rebase and returns the next one.

    Returns:
        The queue entry to merge, or None if queue is empty.
    """
    entries = _read_queue()
    active = [e for e in entries if e.get("state") in (STATE_QUEUED, STATE_READY)]

    if not active:
        return None

    # Sort to get the best candidate
    active = _sort_queue(active)

    for candidate in active:
        # Verify merge is still safe
        try:
            sys.path.insert(0, str(PROJECT_DIR))
            from conflict_detector import check_conflicts
            report = check_conflicts(candidate["branch"])
            candidate["last_check_at"] = datetime.utcnow().isoformat() + "Z"

            if report.get("has_conflicts"):
                # Conflict detected - move to needs-rebase
                candidate["state"] = STATE_NEEDS_REBASE
                candidate["conflict_count"] = len(report.get("conflict_files", []))
                candidate["conflict_files"] = report.get("conflict_files", [])
                candidate["updated_at"] = time.time()
                candidate["updated_at_iso"] = datetime.utcnow().isoformat() + "Z"
                _write_queue(entries)
                continue  # Try next candidate
            else:
                # Safe to merge - remove from queue
                candidate["state"] = STATE_READY
                candidate["updated_at"] = time.time()
                candidate["updated_at_iso"] = datetime.utcnow().isoformat() + "Z"
                candidate["conflict_count"] = 0
                candidate["conflict_files"] = []
                # Remove from queue
                entries = [e for e in entries if e is not candidate]
                _write_queue(entries)
                return candidate
        except Exception:
            # Conflict detector failed - still return candidate (optimistic)
            entries = [e for e in entries if e is not candidate]
            _write_queue(entries)
            return candidate

    # All candidates had conflicts
    _write_queue(entries)
    return None


def status() -> dict:
    """Get queue status summary."""
    entries = _read_queue()
    active = [e for e in entries if e.get("state") in (STATE_QUEUED, STATE_READY, STATE_NEEDS_REBASE)]
    queued = [e for e in active if e.get("state") == STATE_QUEUED]
    ready = [e for e in active if e.get("state") == STATE_READY]
    needs_rebase = [e for e in active if e.get("state") == STATE_NEEDS_REBASE]
    merged = [e for e in entries if e.get("state") == STATE_MERGED]
    failed = [e for e in entries if e.get("state") == STATE_FAILED]

    return {
        "total": len(entries),
        "active": len(active),
        "queued": len(queued),
        "ready": len(ready),
        "needs_rebase": len(needs_rebase),
        "merged": len(merged),
        "failed": len(failed),
        "next_pr": ready[0]["pr"] if ready else (queued[0]["pr"] if queued else None),
        "entries": active,
    }


def reorder():
    """Re-sort the queue based on current conflict status."""
    entries = _read_queue()
    entries = _sort_queue(entries)
    _write_queue(entries)
    return {"reordered": True, "active_count": len([e for e in entries if e.get("state") in (STATE_QUEUED, STATE_READY, STATE_NEEDS_REBASE)])}


def mark_merged(pr: int) -> bool:
    """Mark a PR as merged (archive it)."""
    entries = _read_queue()
    found = False
    for e in entries:
        if e.get("pr") == pr:
            e["state"] = STATE_MERGED
            e["updated_at"] = time.time()
            e["updated_at_iso"] = datetime.utcnow().isoformat() + "Z"
            found = True
    if found:
        _write_queue(entries)
    return found


def mark_failed(pr: int, reason: str = "") -> bool:
    """Mark a PR as failed."""
    entries = _read_queue()
    found = False
    for e in entries:
        if e.get("pr") == pr:
            e["state"] = STATE_FAILED
            e["failure_reason"] = reason
            e["updated_at"] = time.time()
            e["updated_at_iso"] = datetime.utcnow().isoformat() + "Z"
            found = True
    if found:
        _write_queue(entries)
    return found


def remove(pr: int) -> bool:
    """Remove a PR from the queue entirely."""
    entries = _read_queue()
    original_len = len(entries)
    entries = [e for e in entries if e.get("pr") != pr]
    if len(entries) < original_len:
        _write_queue(entries)
        return True
    return False


def _print_entry(entry: dict, index: int = -1):
    """Print a queue entry in human-readable format."""
    prefix = f"  [{index}]" if index >= 0 else "  "
    state_icon = {
        STATE_QUEUED: "⏳",
        STATE_READY: "✅",
        STATE_NEEDS_REBASE: "⚠️",
        STATE_MERGED: "✔️",
        STATE_FAILED: "❌",
    }.get(entry.get("state", ""), "?")

    print(f"{prefix} {state_icon} PR #{entry['pr']} ({entry.get('branch', '?')}) "
          f"[{entry.get('state', '?')}] "
          f"conflicts: {entry.get('conflict_count', 0)} "
          f"enqueued: {entry.get('enqueued_at_iso', '?')}")
    if entry.get("conflict_files"):
        print(f"      conflicting: {', '.join(entry['conflict_files'][:5])}")


def main():
    parser = argparse.ArgumentParser(description="Merge queue manager (Refinery pattern)")
    sub = parser.add_subparsers(dest="command")

    # enqueue
    p_enq = sub.add_parser("enqueue", help="Add PR to merge queue")
    p_enq.add_argument("--pr", type=int, required=True, help="PR number")
    p_enq.add_argument("--branch", type=str, required=True, help="Branch name")
    p_enq.add_argument("--repo", type=str, default="", help="Repo (owner/repo)")
    p_enq.add_argument("--workspace", type=str, default="", help="Workspace ID")

    # dequeue
    sub.add_parser("dequeue", help="Pop next mergeable PR from queue")

    # status
    sub.add_parser("status", help="Show queue status")

    # list
    sub.add_parser("list", help="List all queue entries")

    # reorder
    sub.add_parser("reorder", help="Re-sort queue by priority")

    # mark-merged
    p_mg = sub.add_parser("mark-merged", help="Mark PR as merged")
    p_mg.add_argument("--pr", type=int, required=True)

    # mark-failed
    p_mf = sub.add_parser("mark-failed", help="Mark PR as failed")
    p_mf.add_argument("--pr", type=int, required=True)
    p_mf.add_argument("--reason", type=str, default="")

    # remove
    p_rm = sub.add_parser("remove", help="Remove PR from queue")
    p_rm.add_argument("--pr", type=int, required=True)

    args = parser.parse_args()

    if args.command == "enqueue":
        result = enqueue(args.pr, args.branch, args.repo, args.workspace)
        if "error" in result:
            print(f"ERROR: {result['error']}")
            sys.exit(1)
        print(f"Enqueued PR #{args.pr} ({args.branch}) -> {result['state']}")
        print(f"  Conflicts: {result['conflict_count']}")
        if result.get("conflict_files"):
            print(f"  Files: {', '.join(result['conflict_files'])}")

    elif args.command == "dequeue":
        entry = dequeue()
        if entry:
            print(f"Next to merge: PR #{entry['pr']} ({entry.get('branch', '?')})")
            print(f"  State: {entry.get('state')}")
            print(f"  Conflicts: {entry.get('conflict_count', 0)}")
        else:
            print("Queue is empty or all PRs need rebase.")

    elif args.command == "status":
        s = status()
        print(f"Merge Queue Status:")
        print(f"  Active: {s['active']} (queued: {s['queued']}, ready: {s['ready']}, needs-rebase: {s['needs_rebase']})")
        print(f"  Archived: {s['merged']} merged, {s['failed']} failed")
        print(f"  Next PR: {s['next_pr']}")
        if s.get("entries"):
            print(f"  Entries:")
            for i, e in enumerate(s["entries"]):
                _print_entry(e, i)

    elif args.command == "list":
        entries = _read_queue()
        if not entries:
            print("Queue is empty.")
        for i, e in enumerate(entries):
            _print_entry(e, i)

    elif args.command == "reorder":
        result = reorder()
        print(f"Reordered queue ({result['active_count']} active entries)")

    elif args.command == "mark-merged":
        if mark_merged(args.pr):
            print(f"PR #{args.pr} marked as merged.")
        else:
            print(f"PR #{args.pr} not found in queue.")

    elif args.command == "mark-failed":
        if mark_failed(args.pr, args.reason):
            print(f"PR #{args.pr} marked as failed.")
        else:
            print(f"PR #{args.pr} not found in queue.")

    elif args.command == "remove":
        if remove(args.pr):
            print(f"PR #{args.pr} removed from queue.")
        else:
            print(f"PR #{args.pr} not found in queue.")

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
