#!/usr/bin/env python3
"""
Hermes Agent Orchestrator - main loop.

Polls GitHub Issues for agent-ready tasks, manages worker concurrency,
spawns workspace environments, and outputs instructions for the Hermes
cron agent to execute via delegate_task.

Usage:
    python3 orchestrator.py                      # run one loop iteration
    python3 orchestrator.py --status             # show worker status only
    python3 orchestrator.py --config config.yaml # use custom config

Config (orchestrator.yaml or env vars):
    repo: GitHub repo (ORCH_REPO)
    label: Issue label to filter (ORCH_LABEL, default: agent-ready)
    max_concurrent: Max parallel workers (ORCH_MAX_CONCURRENT, default: 2)
    project_dir: Target project for work (ORCH_PROJECT_DIR)
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add project dir to path for imports
PROJECT_DIR = Path(os.environ.get(
    "ORCH_PROJECT_DIR",
    os.path.expanduser("~/zion/projects/agent-orchestration"),
))
WORKSPACES_DIR = PROJECT_DIR / "workspaces"

sys.path.insert(0, str(PROJECT_DIR))
from poller import poll_issues
from spawner import spawn_worker


def load_config(config_path: str | None = None) -> dict:
    """Load orchestrator configuration from YAML or environment."""
    defaults = {
        "repo": os.environ.get("ORCH_REPO", ""),
        "label": os.environ.get("ORCH_LABEL", "agent-ready"),
        "max_concurrent": int(os.environ.get("ORCH_MAX_CONCURRENT", "2")),
        "project_dir": str(PROJECT_DIR),
        "pipeline": os.environ.get("ORCH_PIPELINE", ""),
    }

    if config_path and os.path.exists(config_path):
        import yaml
        with open(config_path) as f:
            file_config = yaml.safe_load(f) or {}
        for k, v in file_config.items():
            if v is not None:
                defaults[k] = v

    return defaults


def get_active_workers() -> list[dict]:
    """Read workspace metadata to find in-progress workers."""
    if not WORKSPACES_DIR.exists():
        return []

    workers = []
    for ws in sorted(WORKSPACES_DIR.iterdir()):
        meta_path = ws / "meta.json"
        if not meta_path.exists():
            continue
        try:
            meta = json.loads(meta_path.read_text())
            if meta.get("status") == "in-progress":
                workers.append(meta)
        except (json.JSONDecodeError, KeyError):
            continue

    return workers


def get_worker_count() -> int:
    """Count currently active (in-progress) workers."""
    return len(get_active_workers())


def update_issue_status(issue_number: int, status: str, repo: str):
    """Update GitHub issue with a comment indicating worker status."""
    import subprocess
    if status == "in-progress":
        comment = "🤖 Agent orchestrator picked up this issue. Workspace is being prepared."
    elif status == "completed":
        comment = "✅ Agent completed work on this issue. Please review the changes."
    elif status == "failed":
        comment = "❌ Agent failed to complete this issue. Manual intervention needed."
    else:
        return

    subprocess.run(
        ["gh", "issue", "comment", str(issue_number),
         "--repo", repo, "--body", comment],
        capture_output=True, text=True,
        env={**os.environ, "GH_PAGER": "cat"},
    )


def run_loop(config: dict, dry_run: bool = False) -> dict:
    """
    Run one orchestrator loop iteration.

    Returns a summary dict with actions taken.
    """
    repo = config["repo"]
    if not repo:
        return {"error": "No repo configured. Set ORCH_REPO or use --repo."}

    # Check current worker count
    active = get_active_workers()
    active_count = len(active)
    max_concurrent = config["max_concurrent"]
    available_slots = max(0, max_concurrent - active_count)

    summary = {
        "timestamp": datetime.now().isoformat(),
        "repo": repo,
        "label": config["label"],
        "active_workers": active_count,
        "max_concurrent": max_concurrent,
        "available_slots": available_slots,
        "active_issues": [w["issue_number"] for w in active],
        "polled": 0,
        "spawned": [],
        "skipped_full": False,
    }

    if available_slots == 0:
        summary["skipped_full"] = True
        print(f"All {max_concurrent} worker slots occupied. Skipping poll.", file=sys.stderr)
        return summary

    # Poll for issues
    issues = poll_issues(repo=repo, label=config["label"])
    summary["polled"] = len(issues)

    if not issues:
        print("No agent-ready issues found.", file=sys.stderr)
        return summary

    # Filter out issues already being worked on
    active_issue_nums = {w["issue_number"] for w in active}
    new_issues = [i for i in issues if i["number"] not in active_issue_nums]

    if not new_issues:
        print(f"All {len(issues)} polled issues are already in-progress.", file=sys.stderr)
        return summary

    # Spawn workers for new issues (up to available slots)
    to_spawn = new_issues[:available_slots]
    for issue in to_spawn:
        print(f"Spawning worker for issue #{issue['number']}: {issue['title']}", file=sys.stderr)

        if not dry_run:
            result = spawn_worker(
                issue=issue,
                project_dir=Path(config["project_dir"]) if config.get("project_dir") else None,
                pipeline=config.get("pipeline"),
            )
            # Comment on the issue
            update_issue_status(issue["number"], "in-progress", repo)
            summary["spawned"].append({
                "issue_number": issue["number"],
                "workspace": result["workspace_path"],
                "execution_mode": result["execution_mode"],
            })
        else:
            summary["spawned"].append({
                "issue_number": issue["number"],
                "workspace": str(WORKSPACES_DIR / str(issue["number"])),
            })

    return summary


def show_status():
    """Display current orchestrator status."""
    workers = get_active_workers()
    completed = []
    failed = []

    if WORKSPACES_DIR.exists():
        for ws in sorted(WORKSPACES_DIR.iterdir()):
            meta_path = ws / "meta.json"
            if not meta_path.exists():
                continue
            try:
                meta = json.loads(meta_path.read_text())
                status = meta.get("status")
                if status == "completed":
                    completed.append(meta)
                elif status == "failed":
                    failed.append(meta)
            except (json.JSONDecodeError, KeyError):
                continue

    print(f"{'Active Workers':<20} {len(workers)}")
    print(f"{'Completed':<20} {len(completed)}")
    print(f"{'Failed':<20} {len(failed)}")
    print()

    if workers:
        print("Active workers:")
        for w in workers:
            print(f"  #{w['issue_number']:>4}  {w['title']}")
            print(f"        spawned: {w.get('spawned_at', 'unknown')}")

    if failed:
        print("\nFailed workers:")
        for w in failed:
            print(f"  #{w['issue_number']:>4}  {w['title']}")


def main():
    parser = argparse.ArgumentParser(
        description="Hermes Agent Orchestrator - poll, spawn, manage workers",
    )
    parser.add_argument(
        "--config", "-C",
        default=os.path.join(str(PROJECT_DIR), "orchestrator.yaml"),
        help="Path to config YAML",
    )
    parser.add_argument(
        "--repo", "-r",
        default=None,
        help="GitHub repo (overrides config)",
    )
    parser.add_argument(
        "--label", "-l",
        default=None,
        help="Label to filter (overrides config)",
    )
    parser.add_argument(
        "--max-concurrent", "-m",
        type=int,
        default=None,
        help="Max parallel workers (overrides config)",
    )
    parser.add_argument(
        "--status", "-s",
        action="store_true",
        help="Show worker status and exit",
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Show what would happen without creating workspaces",
    )

    args = parser.parse_args()

    if args.status:
        show_status()
        return

    config = load_config(
        config_path=args.config if os.path.exists(args.config) else None,
    )
    if args.repo:
        config["repo"] = args.repo
    if args.label:
        config["label"] = args.label
    if args.max_concurrent is not None:
        config["max_concurrent"] = args.max_concurrent

    summary = run_loop(config, dry_run=args.dry_run)
    json.dump(summary, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
