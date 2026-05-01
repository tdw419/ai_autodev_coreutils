#!/usr/bin/env python3
"""
Issue poller for the Hermes Agent Orchestrator.

Polls GitHub Issues via gh CLI, filtering for issues labeled 'agent-ready'
that are open and unassigned. Returns structured JSON suitable for downstream
worker spawner consumption.

Modeled on the Symphony polling daemon pattern (issue tracker as control plane).
"""

import argparse
import json
import subprocess
import sys
import os


def gh(args: list[str]) -> dict:
    """Run a gh CLI command and return parsed JSON output."""
    result = subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
        env={**os.environ, "GH_PAGER": "cat"},
    )
    if result.returncode != 0:
        print(f"gh error: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return json.loads(result.stdout)


def poll_issues(
    repo: str,
    label: str = "agent-ready",
    state: str = "open",
    limit: int = 30,
) -> list[dict]:
    """
    Poll GitHub Issues for actionable tasks.

    Filters issues by label and state, then excludes any that are already
    assigned to someone (indicating work-in-progress).

    Returns list of dicts with: number, title, body, labels, url, created_at.
    """
    raw = gh([
        "issue", "list",
        "--repo", repo,
        "--label", label,
        "--state", state,
        "--limit", str(limit),
        "--json", "number,title,body,labels,assignees,url,createdAt,state",
    ])

    ready = []
    for issue in raw:
        # Skip issues that already have assignees (work-in-progress)
        if issue.get("assignees"):
            continue
        # Skip closed issues (safety check, should be filtered by --state)
        if issue.get("state") != "open":
            continue
        ready.append({
            "number": issue["number"],
            "title": issue["title"],
            "body": issue.get("body") or "",
            "labels": [lbl["name"] for lbl in issue.get("labels", [])],
            "url": issue["url"],
            "created_at": issue["createdAt"],
        })

    return ready


def main():
    parser = argparse.ArgumentParser(
        description="Poll GitHub Issues for agent-ready tasks",
    )
    parser.add_argument(
        "--repo", "-r",
        default=os.environ.get("ORCH_REPO", ""),
        help="GitHub repo (e.g. owner/repo). Default: ORCH_REPO env var",
    )
    parser.add_argument(
        "--label", "-l",
        default=os.environ.get("ORCH_LABEL", "agent-ready"),
        help="Label to filter issues by. Default: agent-ready",
    )
    parser.add_argument(
        "--limit", "-n",
        type=int,
        default=30,
        help="Max issues to fetch. Default: 30",
    )
    parser.add_argument(
        "--count-only", "-c",
        action="store_true",
        help="Only print the count of ready issues",
    )

    args = parser.parse_args()

    if not args.repo:
        parser.error("repo is required (set ORCH_REPO env var or use --repo)")

    issues = poll_issues(
        repo=args.repo,
        label=args.label,
        limit=args.limit,
    )

    if args.count_only:
        print(len(issues))
    else:
        json.dump(issues, sys.stdout, indent=2)
        print()  # trailing newline


if __name__ == "__main__":
    main()
