#!/usr/bin/env python3
"""
Automated Garbage Collection and Remediation for the Hermes Agent Orchestrator.

Scans for stale workspaces, leaked resources, and code convention violations.
Provides cleanup and remediation capabilities.

Usage:
    python3 gc.py --scan
    python3 gc.py --run [--force]
    python3 gc.py --workspace PATH --delete
    python3 gc.py --conventions /path/to/project
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import time
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(os.environ.get(
    "ORCH_PROJECT_DIR",
    os.path.expanduser("~/zion/projects/agent-orchestration"),
))
WORKSPACES_DIR = PROJECT_DIR / "workspaces"
ORCH_DIR = Path(os.path.expanduser("~/.orchestrator"))
LOGS_DIR = ORCH_DIR / "logs"
GC_DIR = LOGS_DIR / "gc"


def _ensure_dirs():
    GC_DIR.mkdir(parents=True, exist_ok=True)


# --- Stale Workspace Scanner ---

def scan_stale_workspaces(max_age_hours: int = 72) -> list[dict]:
    """
    Find workspaces not modified in N hours.

    Args:
        max_age_hours: Maximum age in hours before a workspace is considered stale.

    Returns:
        List of stale workspace info dicts.
    """
    if not WORKSPACES_DIR.exists():
        return []

    cutoff = time.time() - (max_age_hours * 3600)
    stale = []

    for ws in sorted(WORKSPACES_DIR.iterdir()):
        if not ws.is_dir():
            continue
        meta_path = ws / "meta.json"
        meta = {}
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text())
            except json.JSONDecodeError:
                pass

        # Check last modification time of any file in workspace
        latest_mtime = 0
        for f in ws.rglob("*"):
            if f.is_file():
                latest_mtime = max(latest_mtime, f.stat().st_mtime)

        if latest_mtime < cutoff:
            age_hours = (time.time() - latest_mtime) / 3600
            du = subprocess.run(
                ["du", "-sb", str(ws)], capture_output=True, text=True
            )
            size_bytes = int(du.stdout.split()[0]) if du.stdout.strip() else 0

            stale.append({
                "path": str(ws),
                "issue_number": meta.get("issue_number"),
                "title": meta.get("title", ""),
                "status": meta.get("status", "unknown"),
                "age_hours": round(age_hours, 1),
                "size_bytes": size_bytes,
                "last_modified": datetime.fromtimestamp(latest_mtime).isoformat(),
            })

    return stale


# --- Dead Branch Scanner ---

def scan_dead_branches(repo: str | None = None) -> list[dict]:
    """
    Find git branches associated with workspaces that are not merged.

    Args:
        repo: GitHub repo (owner/repo). If None, uses local git in workspaces.

    Returns:
        List of dead branch info dicts.
    """
    if not WORKSPACES_DIR.exists():
        return []

    dead = []
    active_issues = set()

    # Collect active issue numbers
    for ws in WORKSPACES_DIR.iterdir():
        meta_path = ws / "meta.json"
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text())
                if meta.get("status") in ("in-progress",):
                    active_issues.add(str(meta.get("issue_number", "")))
            except json.JSONDecodeError:
                pass

    for ws in sorted(WORKSPACES_DIR.iterdir()):
        meta_path = ws / "meta.json"
        if not meta_path.exists():
            continue
        try:
            meta = json.loads(meta_path.read_text())
        except json.JSONDecodeError:
            continue

        issue_num = str(meta.get("issue_number", ""))
        if issue_num in active_issues:
            continue

        # Check for a git worktree/branch
        git_dir = ws / ".git"
        if not git_dir.exists():
            continue

        result = subprocess.run(
            ["git", "-C", str(ws), "branch", "--show-current"],
            capture_output=True, text=True,
        )
        branch = result.stdout.strip()
        if branch:
            # Check if branch is merged into main
            merged = subprocess.run(
                ["git", "-C", str(ws), "branch", "--merged", "main"],
                capture_output=True, text=True,
            )
            if branch not in merged.stdout:
                dead.append({
                    "workspace": str(ws),
                    "issue_number": issue_num,
                    "branch": branch,
                    "title": meta.get("title", ""),
                    "status": meta.get("status", "unknown"),
                })

    return dead


# --- Leaked Resources Scanner ---

def scan_leaked_resources() -> dict:
    """
    Find orphaned files in ~/.orchestrator/ that may be leaked resources.

    Returns:
        Dict with categories of leaked resources.
    """
    leaked = {
        "incomplete_logs": [],
        "empty_dirs": [],
        "temp_files": [],
        "orphaned_reviews": [],
    }

    # Check for incomplete run logs (files that are empty or < 10 bytes)
    runs_dir = LOGS_DIR / "runs"
    if runs_dir.exists():
        for f in runs_dir.glob("*.json"):
            if f.stat().st_size < 10:
                leaked["incomplete_logs"].append(str(f))

    # Check for empty directories in workspaces
    if WORKSPACES_DIR.exists():
        for ws in WORKSPACES_DIR.iterdir():
            if ws.is_dir():
                files = list(ws.rglob("*"))
                if len(files) <= 1:  # Just the directory itself (or empty)
                    leaked["empty_dirs"].append(str(ws))

    # Check for temp files
    for pattern in ["*.tmp", "*.bak", "*.swp"]:
        for f in ORCH_DIR.rglob(pattern):
            leaked["temp_files"].append(str(f))

    # Check for reviews without corresponding runs
    reviews_dir = LOGS_DIR / "reviews"
    runs_dir = LOGS_DIR / "runs"
    if reviews_dir.exists() and runs_dir.exists():
        run_ids = {f.stem for f in runs_dir.glob("*.json")}
        for f in reviews_dir.glob("*.json"):
            if f.stem not in run_ids:
                leaked["orphaned_reviews"].append(str(f))

    return leaked


# --- Workspace Cleanup ---

def cleanup_workspace(workspace_path: str, mode: str = "archive") -> dict:
    """
    Archive or delete a workspace.

    Args:
        workspace_path: Path to the workspace directory.
        mode: "archive" (compress to tar.gz), "delete" (remove), "dry_run" (report only).

    Returns:
        Dict with cleanup result.
    """
    ws = Path(workspace_path)
    if not ws.exists():
        return {"error": f"Workspace not found: {ws}", "path": workspace_path}

    size_bytes = sum(f.stat().st_size for f in ws.rglob("*") if f.is_file())

    result = {
        "path": str(ws),
        "mode": mode,
        "size_bytes": size_bytes,
        "timestamp": datetime.now().isoformat(),
    }

    if mode == "dry_run":
        result["action"] = "would_cleanup"
        return result

    if mode == "archive":
        archive_dir = WORKSPACES_DIR / "archive"
        archive_dir.mkdir(parents=True, exist_ok=True)
        archive_name = f"{ws.name}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.tar.gz"
        archive_path = archive_dir / archive_name

        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(ws, arcname=ws.name)

        shutil.rmtree(ws)
        result["action"] = "archived"
        result["archive_path"] = str(archive_path)
        result["archive_size"] = archive_path.stat().st_size

    elif mode == "delete":
        shutil.rmtree(ws)
        result["action"] = "deleted"

    return result


# --- Convention Scanner ---

def scan_conventions(project_dir: str) -> dict:
    """
    Scan Python files for convention violations.

    Checks for:
    - Missing docstrings on public functions/classes
    - TODO/FIXME/HACK markers
    - Inconsistent naming (mixed camelCase/snake_case)

    Args:
        project_dir: Path to the project directory to scan.

    Returns:
        Dict with scan results: files_scanned, issues list.
    """
    proj = Path(project_dir)
    if not proj.exists():
        return {"error": f"Directory not found: {project_dir}"}

    issues = []
    files_scanned = 0

    for py_file in proj.rglob("*.py"):
        # Skip test files, __pycache__, venv
        rel = py_file.relative_to(proj)
        parts = str(rel).split(os.sep)
        if any(p in ("__pycache__", "venv", ".venv", "node_modules") for p in parts):
            continue
        if "test_" in py_file.name:
            continue

        files_scanned += 1
        try:
            source = py_file.read_text()
        except (UnicodeDecodeError, PermissionError):
            continue

        lines = source.split("\n")

        # Check for TODO/FIXME/HACK markers
        for i, line in enumerate(lines, 1):
            for marker in ["TODO", "FIXME", "HACK", "XXX"]:
                if re.search(rf'\b{marker}\b', line, re.IGNORECASE):
                    issues.append({
                        "file": str(rel),
                        "line": i,
                        "issue_type": marker.lower(),
                        "severity": "info",
                        "content": line.strip(),
                    })

        # Parse AST for docstring checks
        try:
            tree = ast.parse(source)
        except SyntaxError:
            issues.append({
                "file": str(rel),
                "line": 0,
                "issue_type": "syntax_error",
                "severity": "error",
                "content": "File has syntax errors",
            })
            continue

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Skip private methods (start with _)
                if node.name.startswith("_"):
                    continue
                # Check for docstring
                docstring = ast.get_docstring(node)
                if not docstring:
                    issues.append({
                        "file": str(rel),
                        "line": node.lineno,
                        "issue_type": "missing_docstring",
                        "severity": "warning",
                        "content": f"Public function '{node.name}' has no docstring",
                    })
            elif isinstance(node, ast.ClassDef):
                if node.name.startswith("_"):
                    continue
                docstring = ast.get_docstring(node)
                if not docstring:
                    issues.append({
                        "file": str(rel),
                        "line": node.lineno,
                        "issue_type": "missing_docstring",
                        "severity": "warning",
                        "content": f"Public class '{node.name}' has no docstring",
                    })

    # Check for naming inconsistencies within each file
    for py_file in proj.rglob("*.py"):
        rel = py_file.relative_to(proj)
        parts = str(rel).split(os.sep)
        if any(p in ("__pycache__", "venv", ".venv", "node_modules") for p in parts):
            continue
        if "test_" in py_file.name:
            continue

        try:
            tree = ast.parse(py_file.read_text())
        except (SyntaxError, UnicodeDecodeError):
            continue

        names = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                names.append(node.name)
            elif isinstance(node, ast.ClassDef):
                names.append(node.name)

        has_camel = any(re.match(r'^[a-z]+[A-Z]', n) for n in names if not n.startswith("_"))
        has_snake = any("_" in n for n in names if not n.startswith("_"))
        if has_camel and has_snake and len(names) > 2:
            issues.append({
                "file": str(rel),
                "line": 0,
                "issue_type": "naming_inconsistency",
                "severity": "warning",
                "content": f"File mixes camelCase and snake_case names: {', '.join(names[:5])}",
            })

    return {
        "files_scanned": files_scanned,
        "total_issues": len(issues),
        "by_severity": {
            s: sum(1 for i in issues if i["severity"] == s)
            for s in ("error", "warning", "info")
        },
        "issues": issues[:100],  # Cap at 100 issues
    }


# --- Full GC Run ---

def run_gc(dry_run: bool = True, max_age_hours: int = 72) -> dict:
    """
    Run full garbage collection scan and cleanup.

    Args:
        dry_run: If True, report what would be cleaned without doing it.
        max_age_hours: Age threshold for stale workspaces.

    Returns:
        Full GC report dict.
    """
    _ensure_dirs()

    report = {
        "timestamp": datetime.now().isoformat(),
        "dry_run": dry_run,
        "max_age_hours": max_age_hours,
        "stale_workspaces": [],
        "dead_branches": [],
        "leaked_resources": {},
        "cleaned": [],
        "bytes_freed": 0,
    }

    # Scan stale workspaces
    stale = scan_stale_workspaces(max_age_hours)
    report["stale_workspaces"] = stale

    # Scan dead branches
    dead = scan_dead_branches()
    report["dead_branches"] = dead

    # Scan leaked resources
    leaked = scan_leaked_resources()
    report["leaked_resources"] = leaked

    if not dry_run:
        # Clean stale workspaces
        for ws in stale:
            result = cleanup_workspace(ws["path"], mode="archive")
            report["cleaned"].append(result)
            report["bytes_freed"] += result.get("size_bytes", 0)

        # Clean leaked resources
        for f in leaked.get("incomplete_logs", []):
            Path(f).unlink(missing_ok=True)
            report["cleaned"].append({"action": "deleted", "path": f, "reason": "incomplete_log"})
        for f in leaked.get("temp_files", []):
            Path(f).unlink(missing_ok=True)
            report["cleaned"].append({"action": "deleted", "path": f, "reason": "temp_file"})

    # Save report
    report_path = GC_DIR / f"{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    report_path.write_text(json.dumps(report, indent=2))

    return report


def main():
    parser = argparse.ArgumentParser(description="Garbage collection for orchestrator")
    parser.add_argument("--scan", action="store_true", help="Scan only, no cleanup")
    parser.add_argument("--run", action="store_true", help="Run full GC")
    parser.add_argument("--force", action="store_true", help="Actually delete (not dry-run)")
    parser.add_argument("--workspace", help="Clean a specific workspace")
    parser.add_argument("--delete", action="store_true", help="Delete (not archive) workspace")
    parser.add_argument("--conventions", help="Scan project for convention violations")
    parser.add_argument("--max-age", type=int, default=72, help="Max workspace age in hours")

    args = parser.parse_args()

    if args.conventions:
        result = scan_conventions(args.conventions)
        print(json.dumps(result, indent=2))
        return

    if args.workspace:
        mode = "delete" if args.delete else "archive"
        result = cleanup_workspace(args.workspace, mode=mode)
        print(json.dumps(result, indent=2))
        return

    if args.run:
        result = run_gc(dry_run=not args.force, max_age_hours=args.max_age)
        print(json.dumps(result, indent=2))
        return

    if args.scan:
        stale = scan_stale_workspaces(args.max_age)
        dead = scan_dead_branches()
        leaked = scan_leaked_resources()
        print(json.dumps({
            "stale_workspaces": stale,
            "dead_branches": dead,
            "leaked_resources": leaked,
        }, indent=2))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
