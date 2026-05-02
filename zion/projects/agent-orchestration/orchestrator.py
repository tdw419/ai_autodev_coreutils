#!/usr/bin/env python3
"""
Hermes Agent Orchestrator - main loop.

Polls GitHub Issues for agent-ready tasks, manages worker concurrency,
spawns workspace environments, and outputs instructions for the Hermes
cron agent to execute via delegate_task.

Supports both single-repo and multi-repo modes:
  - Single-repo: set "repo" in config (backward compatible)
  - Multi-repo: set "repos" list in config with per-repo settings

Usage:
    python3 orchestrator.py                      # run one loop iteration
    python3 orchestrator.py --status             # show worker status only
    python3 orchestrator.py --config config.yaml # use custom config
    python3 orchestrator.py --repo owner/repo    # filter to single repo

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
from execution_log import log_loop_iteration
from cost_tracker import check_budget, record_usage, estimate_pipeline_cost


def _get_merge_queue_status() -> dict:
    """Get merge queue status, returns empty dict if merge_queue unavailable."""
    try:
        from merge_queue import status as mq_status
        return mq_status()
    except Exception:
        return {}


def _check_workspace_in_merge_queue(workspace_id: str) -> bool:
    """Check if a workspace has a PR pending in the merge queue."""
    try:
        from merge_queue import _read_queue
        entries = _read_queue()
        return any(
            e.get("workspace") == workspace_id
            and e.get("state") in ("queued", "ready", "needs-rebase")
            for e in entries
        )
    except Exception:
        return False


def _get_conflicting_workspaces() -> set[str]:
    """Get set of workspace IDs that have conflicts in the merge queue."""
    try:
        from merge_queue import _read_queue
        entries = _read_queue()
        return {
            e["workspace"]
            for e in entries
            if e.get("workspace") and e.get("conflict_count", 0) > 0
            and e.get("state") in ("queued", "ready", "needs-rebase")
        }
    except Exception:
        return set()


# Default per-repo config keys
REPO_DEFAULTS = {
    "labels": ["agent-ready"],
    "pipeline": "",
    "roles_dir": "roles/",
    "ai_guide_path": "",
    "approval_mode": "never",
    "max_concurrent": 2,
    "budget_daily": None,
}


def load_config(config_path: str | None = None) -> dict:
    """Load orchestrator configuration from YAML or environment."""
    defaults = {
        "repo": os.environ.get("ORCH_REPO", ""),
        "label": os.environ.get("ORCH_LABEL", "agent-ready"),
        "max_concurrent": int(os.environ.get("ORCH_MAX_CONCURRENT", "2")),
        "project_dir": str(PROJECT_DIR),
        "pipeline": os.environ.get("ORCH_PIPELINE", ""),
        "repos": [],
    }

    if config_path and os.path.exists(config_path):
        import yaml
        with open(config_path) as f:
            file_config = yaml.safe_load(f) or {}
        for k, v in file_config.items():
            if v is not None:
                defaults[k] = v

    # Normalize: if "repos" is set, use multi-repo mode
    # if only "repo" is set, wrap it in a single-element repos list
    if defaults.get("repos"):
        # Multi-repo mode: validate each repo config
        for r in defaults["repos"]:
            for key, default_val in REPO_DEFAULTS.items():
                if key not in r or r[key] is None:
                    r[key] = default_val
            # Ensure name is derived from url if not set
            if "name" not in r:
                r["name"] = r.get("url", "unknown").replace("/", "__")
    elif defaults.get("repo"):
        # Single-repo mode: wrap in list for unified processing
        defaults["repos"] = [{
            "name": defaults["repo"].replace("/", "__"),
            "url": defaults["repo"],
            "labels": [defaults["label"]],
            "pipeline": defaults.get("pipeline", ""),
            "roles_dir": "roles/",
            "ai_guide_path": "",
            "approval_mode": "never",
            "max_concurrent": defaults["max_concurrent"],
            "budget_daily": None,
        }]

    return defaults


def validate_config(config: dict) -> list[str]:
    """
    Validate orchestrator configuration.

    Returns list of error strings (empty = valid).
    """
    errors = []
    repos = config.get("repos", [])

    if not repos:
        errors.append("No repos configured. Set 'repo' or 'repos' in config.")
        return errors

    for i, r in enumerate(repos):
        prefix = f"repos[{i}]"
        if not r.get("url"):
            errors.append(f"{prefix}: 'url' is required")
        if r.get("max_concurrent", 0) < 1:
            errors.append(f"{prefix}: 'max_concurrent' must be >= 1")
        if r.get("pipeline") and not Path(r["pipeline"]).exists():
            # Only warn, don't error (pipeline may be relative)
            pass
        if r.get("budget_daily") is not None and r["budget_daily"] < 0:
            errors.append(f"{prefix}: 'budget_daily' must be >= 0")

    return errors


def _scan_workspaces_for_status(search_dir: Path, target_status: str) -> list[dict]:
    """Recursively scan a directory for workspace metadata with a given status."""
    results = []
    if not search_dir.exists():
        return results

    for item in sorted(search_dir.iterdir()):
        if not item.is_dir():
            continue
        meta_path = item / "meta.json"
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text())
                if meta.get("status") == target_status:
                    results.append(meta)
            except (json.JSONDecodeError, KeyError):
                continue
        else:
            # Recurse into subdirectories (multi-repo layout: workspaces/repo_name/issue/)
            results.extend(_scan_workspaces_for_status(item, target_status))

    return results


def get_active_workers(repo_name: str | None = None) -> list[dict]:
    """Read workspace metadata to find in-progress workers."""
    if repo_name:
        return _scan_workspaces_for_status(WORKSPACES_DIR / repo_name, "in-progress")
    return _scan_workspaces_for_status(WORKSPACES_DIR, "in-progress")


def get_worker_count(repo_name: str | None = None) -> int:
    """Count currently active (in-progress) workers."""
    return len(get_active_workers(repo_name))


def update_issue_status(issue_number: int, status: str, repo_url: str):
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
         "--repo", repo_url, "--body", comment],
        capture_output=True, text=True,
        env={**os.environ, "GH_PAGER": "cat"},
    )


def run_loop(config: dict, dry_run: bool = False, filter_repo: str | None = None) -> dict:
    """
    Run one orchestrator loop iteration across all configured repos.

    Returns a summary dict with actions taken per repo.
    """
    repos = config.get("repos", [])
    if not repos:
        return {"error": "No repos configured. Set ORCH_REPO or 'repos' in config."}

    # Apply repo filter if specified
    if filter_repo:
        repos = [r for r in repos if r["url"] == filter_repo or r["name"] == filter_repo]
        if not repos:
            return {"error": f"No repo matching '{filter_repo}' found in config."}

    global_max = config.get("max_concurrent", 10)
    total_active = get_worker_count()
    global_available = max(0, global_max - total_active)

    summary = {
        "timestamp": datetime.now().isoformat(),
        "total_active_workers": total_active,
        "global_max_concurrent": global_max,
        "global_available_slots": global_available,
        "merge_queue": _get_merge_queue_status(),
        "repos": {},
    }

    if global_available == 0:
        summary["skipped_full"] = True
        print(f"All {global_max} global worker slots occupied. Skipping poll.", file=sys.stderr)
        return summary

    for repo_config in repos:
        repo_url = repo_config["url"]
        repo_name = repo_config["name"]
        labels = repo_config.get("labels", ["agent-ready"])
        repo_max = repo_config.get("max_concurrent", 2)
        pipeline = repo_config.get("pipeline", "")
        budget_daily = repo_config.get("budget_daily")

        # Check per-repo worker count
        repo_active = get_worker_count(repo_name)
        repo_available = max(0, min(repo_max - repo_active, global_available))

        repo_summary = {
            "repo": repo_url,
            "labels": labels,
            "active_workers": repo_active,
            "max_concurrent": repo_max,
            "available_slots": repo_available,
            "polled": 0,
            "spawned": [],
            "skipped": None,
        }

        # Check budget
        if budget_daily is not None:
            budget_status = check_budget(repo_url, budget_daily)
            if budget_status["status"] == "exceeded":
                repo_summary["skipped"] = "budget_exceeded"
                summary["repos"][repo_name] = repo_summary
                print(f"  {repo_url}: budget exceeded (${budget_status['current_cost']:.4f}/${budget_daily:.2f})", file=sys.stderr)
                continue

        if repo_available == 0:
            repo_summary["skipped"] = "full" if repo_active >= repo_max else "global_full"
            summary["repos"][repo_name] = repo_summary
            continue

        # Poll for issues across all configured labels
        all_issues = []
        for label in labels:
            issues = poll_issues(repo=repo_url, label=label)
            all_issues.extend(issues)

        # Deduplicate by issue number
        seen = set()
        unique_issues = []
        for issue in all_issues:
            if issue["number"] not in seen:
                seen.add(issue["number"])
                unique_issues.append(issue)

        repo_summary["polled"] = len(unique_issues)

        if not unique_issues:
            summary["repos"][repo_name] = repo_summary
            continue

        # Filter out issues already being worked on
        active_issue_nums = {w["issue_number"] for w in get_active_workers(repo_name)}
        new_issues = [i for i in unique_issues if i["number"] not in active_issue_nums]

        # Filter out issues whose workspaces have pending PRs in merge queue
        conflicting_ws = _get_conflicting_workspaces()
        mq_filtered = []
        for issue in new_issues:
            ws_id = str(issue["number"])
            if ws_id in conflicting_ws:
                print(f"  Skipping {repo_url} #{issue['number']}: workspace has conflicting merge queue entry", file=sys.stderr)
                continue
            mq_filtered.append(issue)
        new_issues = mq_filtered

        if not new_issues:
            repo_summary["skipped"] = "all_in_progress"
            summary["repos"][repo_name] = repo_summary
            continue

        # Spawn workers for new issues (up to available slots)
        to_spawn = new_issues[:repo_available]
        for issue in to_spawn:
            print(f"  Spawning worker for {repo_url} #{issue['number']}: {issue['title']}", file=sys.stderr)

            if not dry_run:
                result = spawn_worker(
                    issue=issue,
                    project_dir=Path(config["project_dir"]) if config.get("project_dir") else None,
                    pipeline=pipeline or None,
                    repo_name=repo_name,
                    ai_guide_path=repo_config.get("ai_guide_path", ""),
                )
                update_issue_status(issue["number"], "in-progress", repo_url)

                # Record estimated cost
                try:
                    from cost_tracker import record_usage
                    est = estimate_pipeline_cost(["ai", "ai", "bash", "bash", "ai"])
                    record_usage(
                        repo=repo_url,
                        tokens=est["estimated_tokens"],
                        node_type="ai",
                        issue_number=issue["number"],
                    )
                except Exception:
                    pass

                repo_summary["spawned"].append({
                    "issue_number": issue["number"],
                    "workspace": result["workspace_path"],
                    "execution_mode": result["execution_mode"],
                })
                global_available -= 1
            else:
                ws_path = str(WORKSPACES_DIR / repo_name / str(issue["number"]))
                repo_summary["spawned"].append({
                    "issue_number": issue["number"],
                    "workspace": ws_path,
                })
                global_available -= 1

        summary["repos"][repo_name] = repo_summary

    # Log the loop iteration
    try:
        log_loop_iteration(summary)
    except Exception:
        pass

    return summary


def show_status():
    """Display current orchestrator status across all repos."""
    all_workers = get_active_workers()
    completed = []
    failed = []

    if WORKSPACES_DIR.exists():
        for repo_dir in sorted(WORKSPACES_DIR.iterdir()):
            if not repo_dir.is_dir():
                continue
            meta_path = repo_dir / "meta.json"
            if not meta_path.exists():
                # Check if this is a repo subdirectory (multi-repo layout)
                if repo_dir.name.startswith("."):
                    continue
                # Recurse into repo subdirectories
                for ws in sorted(repo_dir.iterdir()):
                    if not ws.is_dir():
                        continue
                    meta_path = ws / "meta.json"
                    if not meta_path.exists():
                        continue
                    _process_workspace(ws, meta_path, completed, failed)
                continue
            _process_workspace(repo_dir, meta_path, completed, failed)

    print(f"{'Active Workers':<20} {len(all_workers)}")
    print(f"{'Completed':<20} {len(completed)}")
    print(f"{'Failed':<20} {len(failed)}")

    # Merge queue status
    mq_status = _get_merge_queue_status()
    if mq_status:
        print(f"{'Merge Queue':<20} {mq_status.get('active', 0)} active, {mq_status.get('ready', 0)} ready")
        if mq_status.get("needs_manual", 0):
            print(f"{'  Needs Manual':<20} {mq_status['needs_manual']}")
        if mq_status.get("next_pr"):
            print(f"{'  Next PR':<20} #{mq_status['next_pr']}")
    print()

    if all_workers:
        print("Active workers:")
        for w in all_workers:
            repo_tag = f" [{w.get('repo_name', '')}]" if w.get('repo_name') else ""
            print(f"  #{w['issue_number']:>4}  {w['title']}{repo_tag}")
            print(f"        spawned: {w.get('spawned_at', 'unknown')}")

    if failed:
        print("\nFailed workers:")
        for w in failed:
            print(f"  #{w['issue_number']:>4}  {w['title']}")


def _process_workspace(ws_path: Path, meta_path: Path, completed: list, failed: list):
    """Process a workspace metadata file."""
    try:
        meta = json.loads(meta_path.read_text())
        status = meta.get("status")
        if status == "completed":
            completed.append(meta)
        elif status == "failed":
            failed.append(meta)
    except (json.JSONDecodeError, KeyError):
        pass


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
        help="Filter to a single repo (name or url)",
    )
    parser.add_argument(
        "--label", "-l",
        default=None,
        help="Label to filter (overrides config, single-repo mode only)",
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
        "--validate", "-V",
        action="store_true",
        help="Validate config and exit",
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Show what would happen without creating workspaces",
    )

    args = parser.parse_args()

    config = load_config(
        config_path=args.config if os.path.exists(args.config) else None,
    )

    if args.validate:
        errors = validate_config(config)
        if errors:
            print("Configuration errors:", file=sys.stderr)
            for e in errors:
                print(f"  - {e}", file=sys.stderr)
            sys.exit(1)
        else:
            repos = config.get("repos", [])
            print(f"Config valid. {len(repos)} repo(s) configured:")
            for r in repos:
                budget = f", budget: ${r.get('budget_daily', 'unlimited')}/day" if r.get('budget_daily') else ""
                print(f"  - {r['url']} (max: {r['max_concurrent']}, pipeline: {r.get('pipeline') or 'direct'}{budget})")
            sys.exit(0)

    if args.status:
        show_status()
        return

    if args.label and len(config.get("repos", [])) == 1:
        config["repos"][0]["labels"] = [args.label]
    if args.max_concurrent is not None:
        config["max_concurrent"] = args.max_concurrent

    summary = run_loop(config, dry_run=args.dry_run, filter_repo=args.repo)
    json.dump(summary, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
