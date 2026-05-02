#!/usr/bin/env python3
"""
Conflict Detector for the Hermes Agent Orchestrator (Refinery Pattern).

Predicts merge conflicts between workspace branches and the main branch.
Uses git internals (merge-tree, diff) to detect potential conflicts before
they happen, enabling the merge queue to sequence PRs safely.

Usage:
    python3 conflict_detector.py --check --branch feature-xyz --repo owner/repo
    python3 conflict_detector.py --check --workspace 42
    python3 conflict_detector.py --batch
    python3 conflict_detector.py --status
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

PROJECT_DIR = Path(os.environ.get(
    "ORCH_PROJECT_DIR",
    os.path.expanduser("~/zion/projects/agent-orchestration"),
))
WORKSPACES_DIR = PROJECT_DIR / "workspaces"


def _run_git(args: list[str], cwd: Optional[str] = None, timeout: int = 30) -> dict:
    """Run a git command and return parsed result."""
    cmd = ["git"] + args
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, cwd=cwd,
        )
        return {
            "exit_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
    except subprocess.TimeoutExpired:
        return {"exit_code": -1, "stdout": "", "stderr": "timeout"}
    except FileNotFoundError:
        return {"exit_code": -1, "stdout": "", "stderr": "git not found"}


def _get_workspace_branch(workspace_id: str) -> Optional[str]:
    """Get the branch name for a workspace."""
    meta_path = WORKSPACES_DIR / workspace_id / "meta.json"
    if not meta_path.exists():
        return None
    try:
        meta = json.loads(meta_path.read_text())
        return meta.get("branch")
    except (json.JSONDecodeError, OSError):
        return None


def _get_changed_files(branch: str, base: str = "main", repo: Optional[str] = None) -> list[str]:
    """Get files changed on a branch vs base."""
    result = _run_git(["diff", "--name-only", f"{base}...{branch}"])
    if result["exit_code"] != 0:
        return []
    return [f for f in result["stdout"].split("\n") if f]


def _get_changed_files_on_base(branch: str, base: str = "main") -> list[str]:
    """Get files changed on base since branching point."""
    result = _run_git(["log", "--oneline", f"{branch}..{base}", "--name-only", "--pretty=format:"])
    if result["exit_code"] != 0:
        return []
    return list({f for f in result["stdout"].split("\n") if f})


def _check_merge_tree_conflicts(branch: str, base: str = "main") -> dict:
    """
    Use git merge-tree --write-tree to dry-run a merge and detect conflicts.
    Returns dict with conflict info. Requires git 2.36+.
    """
    # Check if base branch exists
    base_check = _run_git(["rev-parse", "--verify", base])
    if base_check["exit_code"] != 0:
        return {"has_conflicts": None, "conflict_files": [], "tree_sha": None,
                "error": f"Base branch '{base}' does not exist"}

    # Check if branch exists
    branch_check = _run_git(["rev-parse", "--verify", branch])
    if branch_check["exit_code"] != 0:
        return {"has_conflicts": None, "conflict_files": [], "tree_sha": None,
                "error": f"Branch '{branch}' does not exist"}

    result = _run_git(["merge-tree", "--write-tree", base, branch])
    if result["exit_code"] == 0:
        # Clean merge - exit code 0 means no conflicts
        return {"has_conflicts": False, "conflict_files": [], "tree_sha": result["stdout"]}
    elif result["exit_code"] == 1:
        # exit code 1 can mean conflicts OR an error like "not something we can merge"
        stderr = result.get("stderr", "")
        if "not something we can merge" in stderr or "fatal" in stderr.lower():
            return {"has_conflicts": None, "conflict_files": [], "tree_sha": None,
                    "error": stderr}
        # Conflicts detected - parse the output for conflict markers
        conflict_files = _parse_merge_tree_output(result["stdout"])
        return {"has_conflicts": True, "conflict_files": conflict_files, "tree_sha": None}
    else:
        # git error (maybe old version) - fall back to diff-based check
        return {"has_conflicts": None, "conflict_files": [], "tree_sha": None, "error": result["stderr"]}


def _parse_merge_tree_output(output: str) -> list[str]:
    """Parse git merge-tree output to extract conflicted file paths."""
    conflicts = []
    lines = output.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        # Newer merge-tree format: CONFLICT markers in merge output
        if "CONFLICT" in line:
            # Extract file path from conflict line
            parts = line.split("\t")
            if len(parts) >= 2:
                # Take the last part, strip "CONFLICT (...)" prefix
                fname = parts[-1].rsplit(": ", 1)[-1].strip()
                if fname:
                    conflicts.append(fname)
        elif "Auto-merging " in line:
            # "Auto-merging <path>" indicates a file that needed merging
            # Only include if followed by a CONFLICT line
            fname = line.replace("Auto-merging ", "").strip()
            if i + 1 < len(lines) and "CONFLICT" in lines[i + 1]:
                if fname and not fname.startswith("Auto-merging"):
                    conflicts.append(fname)
        # Skip git object hashes (40-char hex)
        elif line.strip() and len(line.strip()) == 40:
            pass  # Skip SHA lines
        # Skip mode lines (100644, 100755, etc.)
        elif line.strip() and any(line.strip().startswith(m) for m in ["100644", "100755", "120000", "160000"]):
            pass
        i += 1
    return list(set(f for f in conflicts if f))


def _check_overlap_conflicts(branch: str, base: str = "main") -> list[str]:
    """
    Fallback conflict detection: find files changed on both branch and base.
    Less accurate than merge-tree but works on older git versions.
    """
    branch_files = set(_get_changed_files(branch, base))
    base_files = set(_get_changed_files_on_base(branch, base))
    overlap = branch_files & base_files
    return sorted(overlap)


def _classify_conflict(file_path: str) -> str:
    """Classify conflict type based on file extension."""
    ext = Path(file_path).suffix.lower()
    structural_exts = {".yaml", ".yml", ".json", ".toml", ".xml", ".lock", ".csv"}
    if ext in structural_exts:
        return "structural"
    return "content"


def _compute_severity(conflict_files: list[str], total_changed: int) -> str:
    """Compute conflict severity based on ratio of conflicting files."""
    if not conflict_files:
        return "none"
    if total_changed == 0:
        return "high"
    ratio = len(conflict_files) / total_changed
    if ratio > 0.5:
        return "high"
    elif ratio > 0.2:
        return "medium"
    return "low"


def _suggest_action(severity: str, has_conflicts: bool, conflict_count: int) -> str:
    """Suggest an action based on conflict analysis."""
    if not has_conflicts:
        return "proceed"
    if severity == "high" or conflict_count > 5:
        return "wait"
    return "rebase"


def check_conflicts(
    branch: str,
    base: str = "main",
    repo: Optional[str] = None,
) -> dict:
    """
    Check for merge conflicts between a branch and base.

    Returns:
        Dict with:
            - branch: the branch name checked
            - base: the base branch
            - has_conflicts: bool or None if detection failed
            - conflict_files: list of conflicting file paths
            - conflict_types: dict mapping file -> conflict type
            - severity: none/low/medium/high
            - suggested_action: proceed/rebase/wait
            - overlap_files: files changed on both sides (fallback)
            - detection_method: merge-tree or overlap
            - checked_at: ISO timestamp
    """
    checked_at = datetime.utcnow().isoformat() + "Z"

    # Try merge-tree first (more accurate)
    merge_result = _check_merge_tree_conflicts(branch, base)

    if merge_result["has_conflicts"] is not None:
        conflict_files = merge_result["conflict_files"]
        has_conflicts = merge_result["has_conflicts"]
        detection_method = "merge-tree"
    elif merge_result.get("error") and "does not exist" in merge_result.get("error", ""):
        # Base or branch doesn't exist - can't check conflicts
        conflict_files = []
        has_conflicts = False
        detection_method = "unavailable"
    else:
        # Fall back to overlap detection
        conflict_files = _check_overlap_conflicts(branch, base)
        has_conflicts = len(conflict_files) > 0
        detection_method = "overlap"

    total_changed = len(_get_changed_files(branch, base))
    severity = _compute_severity(conflict_files, total_changed)
    suggested_action = _suggest_action(severity, has_conflicts, len(conflict_files))
    conflict_types = {f: _classify_conflict(f) for f in conflict_files}

    return {
        "branch": branch,
        "base": base,
        "has_conflicts": has_conflicts,
        "conflict_files": conflict_files,
        "conflict_types": conflict_types,
        "severity": severity,
        "suggested_action": suggested_action,
        "total_changed_files": total_changed,
        "detection_method": detection_method,
        "checked_at": checked_at,
    }


def check_workspace(workspace_id: str, base: str = "main") -> dict:
    """Check conflicts for a workspace by its ID."""
    branch = _get_workspace_branch(workspace_id)
    if not branch:
        return {
            "workspace": workspace_id,
            "error": f"No branch found for workspace {workspace_id}",
            "has_conflicts": None,
            "checked_at": datetime.utcnow().isoformat() + "Z",
        }
    result = check_conflicts(branch, base)
    result["workspace"] = workspace_id
    return result


def check_all_workspaces(base: str = "main") -> list[dict]:
    """Check conflicts for all active workspaces."""
    results = []
    if not WORKSPACES_DIR.exists():
        return results
    for ws_dir in sorted(WORKSPACES_DIR.iterdir()):
        if ws_dir.is_dir():
            meta_path = ws_dir / "meta.json"
            if meta_path.exists():
                result = check_workspace(ws_dir.name, base)
                results.append(result)
    return results


def print_report(report: dict):
    """Print a human-readable conflict report."""
    if "error" in report:
        print(f"ERROR: {report['error']}")
        return

    workspace = report.get("workspace", "")
    prefix = f"Workspace {workspace}: " if workspace else ""
    branch = report["branch"]

    if report["has_conflicts"]:
        print(f"{prefix}{branch}: CONFLICTS DETECTED")
        print(f"  Severity: {report['severity']}")
        print(f"  Conflicting files ({len(report['conflict_files'])}):")
        for f in report["conflict_files"]:
            ctype = report["conflict_types"].get(f, "content")
            print(f"    - {f} ({ctype})")
        print(f"  Suggested action: {report['suggested_action']}")
    else:
        print(f"{prefix}{branch}: no conflicts (clean merge)")
    print(f"  Detection method: {report['detection_method']}")
    print(f"  Total changed files: {report['total_changed_files']}")
    print(f"  Checked at: {report['checked_at']}")


def main():
    parser = argparse.ArgumentParser(description="Conflict detector (Refinery pattern)")
    parser.add_argument("--check", action="store_true", help="Check for conflicts")
    parser.add_argument("--branch", type=str, help="Branch name to check")
    parser.add_argument("--workspace", type=str, help="Workspace ID to check")
    parser.add_argument("--batch", action="store_true", help="Check all workspaces")
    parser.add_argument("--base", type=str, default="main", help="Base branch (default: main)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--status", action="store_true", help="Show git and detector status")
    args = parser.parse_args()

    if args.status:
        # Show git version and available methods
        git_ver = _run_git(["--version"])
        print(f"Git: {git_ver['stdout']}")
        mt_result = _run_git(["merge-tree", "--write-tree", "--help"])
        has_merge_tree = mt_result["exit_code"] == 0
        print(f"merge-tree --write-tree: {'available' if has_merge_tree else 'not available (will use overlap fallback)'}")

        # Show active workspaces
        if WORKSPACES_DIR.exists():
            workspaces = [d.name for d in WORKSPACES_DIR.iterdir() if d.is_dir() and (d / "meta.json").exists()]
            print(f"Active workspaces: {len(workspaces)}")
            for ws in workspaces:
                branch = _get_workspace_branch(ws)
                print(f"  - {ws}: {branch or 'no branch'}")
        return

    if args.batch:
        results = check_all_workspaces(args.base)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            if not results:
                print("No active workspaces found.")
            for r in results:
                print_report(r)
                print()
        return

    if args.workspace:
        report = check_workspace(args.workspace, args.base)
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print_report(report)
        return

    if args.branch:
        report = check_conflicts(args.branch, args.base)
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print_report(report)
        return

    parser.print_help()
    sys.exit(1)


if __name__ == "__main__":
    main()
