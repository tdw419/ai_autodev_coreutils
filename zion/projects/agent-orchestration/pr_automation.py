#!/usr/bin/env python3
"""
Pull Request Automation for the Hermes Agent Orchestrator.

Creates, updates, and manages GitHub PRs from workspace branches.
Automates the PR lifecycle: create, label, add reviewers, check status,
and handle merge/close.

Usage:
    python3 pr_automation.py --create ISSUE_NUMBER --repo owner/repo
    python3 pr_automation.py --list --repo owner/repo
    python3 pr_automation.py --status PR_NUMBER --repo owner/repo
    python3 pr_automation.py --merge PR_NUMBER --repo owner/repo
    python3 pr_automation.py --close PR_NUMBER --repo owner/repo
"""

from __future__ import annotations

import argparse
import json
import os
import re
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


def _run_gh(args: list[str], timeout: int = 30) -> dict:
    """
    Run a gh CLI command and return parsed output.

    Args:
        args: Command arguments (after 'gh').
        timeout: Command timeout in seconds.

    Returns:
        Dict with 'exit_code', 'stdout', 'stderr', 'data' (parsed JSON if available).
    """
    cmd = ["gh"] + args
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout,
        )
        data = None
        if result.stdout.strip():
            try:
                data = json.loads(result.stdout)
            except json.JSONDecodeError:
                pass
        return {
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "data": data,
        }
    except subprocess.TimeoutExpired:
        return {"exit_code": -1, "stdout": "", "stderr": "timeout", "data": None}
    except FileNotFoundError:
        return {"exit_code": -1, "stdout": "", "stderr": "gh not found", "data": None}


def _read_workspace_meta(issue_number: int | str) -> dict | None:
    """Read workspace metadata."""
    meta_path = WORKSPACES_DIR / str(issue_number) / "meta.json"
    if not meta_path.exists():
        return None
    try:
        return json.loads(meta_path.read_text())
    except json.JSONDecodeError:
        return None


def _get_branch_name(issue_number: int | str) -> str:
    """Get the expected branch name for an issue."""
    return f"issue-{issue_number}"


# --- PR Creation ---

def create_pr(
    issue_number: int | str,
    repo: str,
    title: str | None = None,
    body: str | None = None,
    labels: list[str] | None = None,
    reviewers: list[str] | None = None,
    draft: bool = False,
) -> dict:
    """
    Create a PR for a workspace branch.

    Args:
        issue_number: GitHub issue number.
        repo: GitHub repo (owner/repo).
        title: PR title. Auto-generated from issue if None.
        body: PR body. Auto-generated from issue if None.
        labels: Labels to add.
        reviewers: Reviewers to assign.
        draft: Create as draft PR.

    Returns:
        Dict with PR creation result.
    """
    meta = _read_workspace_meta(issue_number)
    if meta is None:
        return {"error": f"No workspace found for issue #{issue_number}"}

    branch = _get_branch_name(issue_number)
    ws_dir = WORKSPACES_DIR / str(issue_number)

    # Generate title/body from issue if not provided
    if title is None:
        title = f"Fix #{issue_number}: {meta.get('title', 'Automated PR')}"

    if body is None:
        body = f"Closes #{issue_number}\n\n"
        body += f"**Issue:** {meta.get('title', 'N/A')}\n\n"
        body += f"**Description:**\n{meta.get('description', 'No description')}\n\n"

        # Add execution summary if available
        if meta.get("last_run_id"):
            body += f"**Last Run:** {meta['last_run_id']}\n"
        if meta.get("attempts", 0) > 1:
            body += f"**Attempts:** {meta['attempts']}\n"

    # Push branch and create PR
    push_result = _run_gh([
        "repo", "view", repo, "--json", "defaultBranchRef",
    ])
    if push_result.get("data"):
        default_branch = push_result["data"].get("defaultBranchRef", {}).get("name", "main")
    else:
        default_branch = "main"

    # Push the branch
    push_cmd = _run_gh([
        "api",
        f"repos/{repo}/git/refs",
        "--method", "POST",
        "-f", f"ref=refs/heads/{branch}",
        "-f", f"sha={default_branch}",
    ])
    # If branch already exists, that's fine
    if push_result["exit_code"] != 0 and "already exists" not in push_result.get("stderr", ""):
        pass  # Continue anyway, might already be pushed

    # Create the PR
    pr_args = [
        "pr", "create",
        "--repo", repo,
        "--head", branch,
        "--base", default_branch,
        "--title", title,
        "--body", body,
    ]
    if draft:
        pr_args.append("--draft")
    if labels:
        pr_args.extend(["--label", ",".join(labels)])
    if reviewers:
        pr_args.extend(["--reviewer", ",".join(reviewers)])

    result = _run_gh(pr_args)

    if result["exit_code"] == 0 and result["data"]:
        pr_number = result["data"].get("number")
        pr_url = result["data"].get("html_url", "")

        # Update workspace meta with PR info
        meta["pr_number"] = pr_number
        meta["pr_url"] = pr_url
        meta_path = ws_dir / "meta.json"
        meta_path.write_text(json.dumps(meta, indent=2))

        return {
            "pr_number": pr_number,
            "pr_url": pr_url,
            "status": "created",
            "title": title,
        }
    else:
        return {
            "error": result.get("stderr", "Unknown error"),
            "exit_code": result["exit_code"],
        }


# --- PR Listing ---

def list_prs(repo: str, state: str = "open", limit: int = 30) -> list[dict]:
    """
    List PRs for a repository.

    Args:
        repo: GitHub repo (owner/repo).
        state: PR state filter (open, closed, all).
        limit: Max PRs to return.

    Returns:
        List of PR info dicts.
    """
    result = _run_gh([
        "pr", "list",
        "--repo", repo,
        "--state", state,
        "--limit", str(limit),
        "--json", "number,title,state,url,headRefName,createdAt,labels",
    ])

    if result["exit_code"] == 0 and result["data"]:
        return result["data"]
    return []


# --- PR Status ---

def get_pr_status(repo: str, pr_number: int) -> dict | None:
    """
    Get detailed PR status including checks and reviews.

    Args:
        repo: GitHub repo (owner/repo).
        pr_number: PR number.

    Returns:
        Dict with PR status info, or None on error.
    """
    result = _run_gh([
        "pr", "view", str(pr_number),
        "--repo", repo,
        "--json", "number,title,state,url,mergeable,reviewDecision,statusCheckRollup,labels",
    ])

    if result["exit_code"] == 0 and result["data"]:
        data = result["data"]

        # Summarize check status
        checks = data.get("statusCheckRollup", [])
        passing = sum(1 for c in checks if c.get("status") == "COMPLETED" and c.get("conclusion") == "SUCCESS")
        failing = sum(1 for c in checks if c.get("status") == "COMPLETED" and c.get("conclusion") in ("FAILURE", "TIMED_OUT"))
        pending = sum(1 for c in checks if c.get("status") == "IN_PROGRESS" or c.get("status") == "QUEUED")

        return {
            "number": data["number"],
            "title": data["title"],
            "state": data["state"],
            "url": data["url"],
            "mergeable": data.get("mergeable"),
            "review_decision": data.get("reviewDecision"),
            "checks": {"passing": passing, "failing": failing, "pending": pending},
            "labels": [l.get("name") for l in data.get("labels", [])],
            "ready_to_merge": (
                data.get("mergeable") is True
                and data.get("reviewDecision") == "APPROVED"
                and failing == 0
                and pending == 0
            ),
        }

    return None


# --- PR Merge ---

def merge_pr(
    repo: str,
    pr_number: int,
    method: str = "squash",
    delete_branch: bool = True,
) -> dict:
    """
    Merge a PR.

    Args:
        repo: GitHub repo (owner/repo).
        pr_number: PR number.
        method: Merge method (merge, squash, rebase).
        delete_branch: Delete the branch after merge.

    Returns:
        Dict with merge result.
    """
    result = _run_gh([
        "pr", "merge", str(pr_number),
        "--repo", repo,
        "--" + method,
        "--delete-branch" if delete_branch else "--no-delete-branch",
    ])

    if result["exit_code"] == 0:
        # Update workspace meta
        pr_info = _run_gh([
            "pr", "view", str(pr_number),
            "--repo", repo,
            "--json", "headRefName",
        ])
        branch_name = None
        if pr_info.get("data"):
            branch_name = pr_info["data"].get("headRefName", "")

        if branch_name:
            # Extract issue number from branch name
            match = re.match(r"issue-(\d+)", branch_name)
            if match:
                issue_num = match.group(1)
                from workspace_manager import transition_workspace
                transition_workspace(issue_num, "merged")

        return {"status": "merged", "pr_number": pr_number, "method": method}
    else:
        return {"error": result.get("stderr", "Merge failed"), "exit_code": result["exit_code"]}


# --- PR Close ---

def close_pr(repo: str, pr_number: int, comment: str | None = None) -> dict:
    """
    Close a PR without merging.

    Args:
        repo: GitHub repo (owner/repo).
        pr_number: PR number.
        comment: Optional closing comment.

    Returns:
        Dict with close result.
    """
    if comment:
        _run_gh([
            "pr", "comment", str(pr_number),
            "--repo", repo,
            "--body", comment,
        ])

    result = _run_gh([
        "pr", "close", str(pr_number),
        "--repo", repo,
    ])

    if result["exit_code"] == 0:
        return {"status": "closed", "pr_number": pr_number}
    else:
        return {"error": result.get("stderr", "Close failed"), "exit_code": result["exit_code"]}


# --- PR Update ---

def update_pr(
    repo: str,
    pr_number: int,
    title: str | None = None,
    body: str | None = None,
    labels: list[str] | None = None,
) -> dict:
    """
    Update PR title, body, or labels.

    Args:
        repo: GitHub repo.
        pr_number: PR number.
        title: New title (optional).
        body: New body (optional).
        labels: Replace labels (optional).

    Returns:
        Dict with update result.
    """
    args = ["pr", "edit", str(pr_number), "--repo", repo]
    if title:
        args.extend(["--title", title])
    if body:
        args.extend(["--body", body])
    if labels:
        args.extend(["--add-label", ",".join(labels)])

    result = _run_gh(args)
    if result["exit_code"] == 0:
        return {"status": "updated", "pr_number": pr_number}
    else:
        return {"error": result.get("stderr", "Update failed"), "exit_code": result["exit_code"]}


def main():
    parser = argparse.ArgumentParser(description="PR automation")
    parser.add_argument("--create", type=int, help="Create PR for issue number")
    parser.add_argument("--repo", required=True, help="GitHub repo (owner/repo)")
    parser.add_argument("--title", help="PR title")
    parser.add_argument("--body", help="PR body")
    parser.add_argument("--labels", help="Comma-separated labels")
    parser.add_argument("--reviewers", help="Comma-separated reviewers")
    parser.add_argument("--draft", action="store_true", help="Create as draft")
    parser.add_argument("--list", action="store_true", help="List PRs")
    parser.add_argument("--status", type=int, help="Get PR status")
    parser.add_argument("--merge", type=int, help="Merge PR")
    parser.add_argument("--close", type=int, help="Close PR")
    parser.add_argument("--close-comment", help="Comment when closing")
    parser.add_argument("--merge-method", default="squash", choices=["merge", "squash", "rebase"])

    args = parser.parse_args()

    if args.create:
        labels = args.labels.split(",") if args.labels else None
        reviewers = args.reviewers.split(",") if args.reviewers else None
        result = create_pr(
            args.create, args.repo,
            title=args.title, body=args.body,
            labels=labels, reviewers=reviewers,
            draft=args.draft,
        )
    elif args.list:
        result = list_prs(args.repo)
    elif args.status:
        result = get_pr_status(args.repo, args.status)
    elif args.merge:
        result = merge_pr(args.repo, args.merge, method=args.merge_method)
    elif args.close:
        result = close_pr(args.repo, args.close, comment=args.close_comment)
    else:
        parser.print_help()
        return

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
