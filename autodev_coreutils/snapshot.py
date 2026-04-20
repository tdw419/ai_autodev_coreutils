"""snapshot -- Capture the full state of a multi-tool workflow.

Like a checkpoint/save-state. Captures what's done, what's in progress,
what's queued, and the state of every autodev tool. Can be restored later.

Input:  Project directory with .autodev/ state
Output: A snapshot file (tar + manifest)
State:  snapshot_state.json

Usage:
    autodev-snapshot --tag "before-refactor"
    autodev-snapshot --list
    autodev-snapshot --restore before-refactor
"""

import argparse
import json
import shutil
import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path

from .contract import (
    make_parser, find_project, ensure_autodev_dir,
    write_state, output, error,
)


def take_snapshot(project: Path, tag: str = None) -> dict:
    """Capture current state of all autodev tools."""
    ad = project / ".autodev"
    if not ad.exists():
        return {"error": "No .autodev/ directory found"}

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    snap_tag = tag or timestamp

    # Collect all state
    state = {
        "tag": snap_tag,
        "timestamp": timestamp,
        "project": str(project),
        "files": [],
        "tool_states": {},
    }

    # Read all JSON state files
    for state_file in ad.glob("*_state.json"):
        tool_name = state_file.stem.replace("_state", "")
        state["tool_states"][tool_name] = json.loads(state_file.read_text())

    # List all files in .autodev/
    for f in ad.rglob("*"):
        if f.is_file():
            state["files"].append(str(f.relative_to(ad)))

    # Create snapshot archive
    snapshots_dir = ad / "snapshots"
    snapshots_dir.mkdir(exist_ok=True)
    snap_file = snapshots_dir / f"snap_{snap_tag}.tar.gz"

    with tarfile.open(snap_file, "w:gz") as tar:
        for f in ad.rglob("*"):
            if f.is_file() and "snapshots" not in str(f):
                tar.add(f, arcname=str(f.relative_to(project)))

    state["snapshot_file"] = str(snap_file.relative_to(project))

    # Also save manifest
    manifest = snapshots_dir / f"snap_{snap_tag}_manifest.json"
    manifest.write_text(json.dumps(state, indent=2))

    return state


def list_snapshots(project: Path) -> list[dict]:
    """List all snapshots."""
    snapshots_dir = project / ".autodev" / "snapshots"
    if not snapshots_dir.exists():
        return []

    snapshots = []
    for manifest in sorted(snapshots_dir.glob("*_manifest.json")):
        try:
            data = json.loads(manifest.read_text())
            snapshots.append(data)
        except (json.JSONDecodeError, OSError):
            continue

    return snapshots


def restore_snapshot(project: Path, tag: str) -> dict:
    """Restore a snapshot by tag."""
    snapshots_dir = project / ".autodev" / "snapshots"
    snap_file = snapshots_dir / f"snap_{tag}.tar.gz"

    if not snap_file.exists():
        # Try partial match
        matches = list(snapshots_dir.glob(f"snap_*{tag}*.tar.gz"))
        if not matches:
            return {"error": f"Snapshot '{tag}' not found"}
        snap_file = matches[0]

    ad = project / ".autodev"

    # Backup current state
    backup_dir = ad / "snapshots" / "_pre_restore_backup"
    if ad.exists():
        if backup_dir.exists():
            shutil.rmtree(backup_dir)
        shutil.copytree(ad, backup_dir, dirs_exist_ok=True)
        # Remove the backup dir from itself (nested)
        if (backup_dir / "snapshots" / "_pre_restore_backup").exists():
            shutil.rmtree(backup_dir / "snapshots" / "_pre_restore_backup")

    # Extract snapshot
    with tarfile.open(snap_file, "r:gz") as tar:
        tar.extractall(path=project)

    return {
        "restored": tag,
        "from": str(snap_file),
        "backup": str(backup_dir),
    }


def main(argv=None):
    parser = make_parser("snapshot", "Capture or restore autodev workflow state")
    parser.add_argument(
        "--tag", default=None,
        help="Tag for this snapshot (default: timestamp)",
    )
    parser.add_argument(
        "--list", action="store_true",
        help="List all snapshots",
    )
    parser.add_argument(
        "--restore", default=None,
        help="Restore a snapshot by tag",
    )

    args = parser.parse_args(argv)
    project = find_project(args.workdir)

    if args.list:
        snaps = list_snapshots(project)
        if args.json_output:
            output(snaps, json_mode=True)
        elif not args.quiet:
            if not snaps:
                output("No snapshots found")
            for s in snaps:
                output(f"  [{s.get('tag', '?')}] {s.get('timestamp', '?')} - {len(s.get('files', []))} files, {len(s.get('tool_states', {}))} tool states")
        return 0

    if args.restore:
        result = restore_snapshot(project, args.restore)
        if "error" in result:
            if not args.json_output:
                error(result["error"])
            output(result, json_mode=True)
            return 1
        write_state(project, "snapshot", result)
        if args.json_output:
            output(result, json_mode=True)
        elif not args.quiet:
            output(f"Restored snapshot: {result['restored']}")
            output(f"  Backup at: {result['backup']}")
        return 0

    # Take snapshot
    result = take_snapshot(project, args.tag)
    if "error" in result:
        if not args.json_output:
            error(result["error"])
        output(result, json_mode=True)
        return 1

    write_state(project, "snapshot", result)

    if args.json_output:
        output(result, json_mode=True)
    elif not args.quiet:
        output(f"Snapshot '{result['tag']}' saved")
        output(f"  {len(result['files'])} files, {len(result['tool_states'])} tool states")
        output(f"  -> {result['snapshot_file']}")

    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
