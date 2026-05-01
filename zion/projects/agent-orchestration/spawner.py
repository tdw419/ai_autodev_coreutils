#!/usr/bin/env python3
"""
Worker spawner for the Hermes Agent Orchestrator.

Takes an issue (from poller output) and prepares an isolated workspace
for a delegate_task worker. Builds a structured prompt from the issue
context and any project AI_GUIDE.md, then outputs the parameters needed
to spawn the worker.

The orchestrator (Hermes cron agent) reads this output and calls
delegate_task with the prepared workspace and prompt.
"""

import argparse
import json
import os
import sys
from pathlib import Path

PROJECT_DIR = Path(os.environ.get("ORCH_PROJECT_DIR", os.path.expanduser("~/zion/projects/agent-orchestration")))
WORKSPACES_DIR = PROJECT_DIR / "workspaces"


def find_project_dir(issue: dict) -> Path | None:
    """Try to determine the target project directory from issue context."""
    # Check if issue body mentions a project path
    body = issue.get("body", "")
    if not body:
        return None

    # Look for patterns like ~/zion/projects/NAME or project: NAME
    import re
    # Match ~/zion/projects/something
    m = re.search(r'~/zion/projects/([a-zA-Z0-9_-]+)', body)
    if m:
        return Path(os.path.expanduser(f"~/zion/projects/{m.group(1)}"))

    # Match project: or repo: mentions
    m = re.search(r'(?:project|repo|directory)[:\s]+([a-zA-Z0-9_-]+)', body, re.IGNORECASE)
    if m:
        return Path(os.path.expanduser(f"~/zion/projects/{m.group(1)}"))

    return None


def read_ai_guide(project_dir: Path) -> str:
    """Read AI_GUIDE.md from a project directory if it exists."""
    guide_path = project_dir / "AI_GUIDE.md"
    if guide_path.exists():
        return guide_path.read_text()
    return ""


def build_prompt(issue: dict, ai_guide: str = "") -> str:
    """Build the worker prompt from issue context and project guide."""
    parts = [
        f"## Task from GitHub Issue #{issue['number']}",
        "",
        f"**Title:** {issue['title']}",
        "",
        "**Description:**",
        issue.get("body", "(no description)"),
        "",
        f"**Labels:** {', '.join(issue.get('labels', []))}",
        f"**Issue URL:** {issue.get('url', '')}",
    ]

    if ai_guide:
        parts.extend([
            "",
            "## Project Guidelines (AI_GUIDE.md)",
            "",
            "Follow these project conventions:",
            "",
            ai_guide,
        ])

    parts.extend([
        "",
        "## Instructions",
        "",
        "1. Read and understand the task above",
        "2. Implement the changes described in the issue",
        "3. Run tests to verify your changes",
        "4. Commit with a descriptive message",
        "",
        "When done, summarize what you changed and any issues encountered.",
    ])

    return "\n".join(parts)


def spawn_worker(
    issue: dict,
    project_dir: Path | None = None,
    dry_run: bool = False,
) -> dict:
    """
    Prepare workspace and prompt for a worker task.

    Returns a dict with workspace_path, prompt_path, prompt, and
    project_dir that the orchestrator can use to call delegate_task.
    """
    issue_num = issue["number"]
    workspace = WORKSPACES_DIR / str(issue_num)

    if workspace.exists():
        print(f"Warning: workspace {workspace} already exists (issue may be in-progress)", file=sys.stderr)

    if not dry_run:
        workspace.mkdir(parents=True, exist_ok=True)

        # Save issue metadata
        meta = {
            "issue_number": issue_num,
            "title": issue["title"],
            "labels": issue.get("labels", []),
            "url": issue.get("url", ""),
            "status": "in-progress",
            "spawned_at": __import__("datetime").datetime.now().isoformat(),
        }
        (workspace / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")

    # Find project directory for AI_GUIDE.md context
    resolved_project = project_dir or find_project_dir(issue)
    ai_guide = read_ai_guide(resolved_project) if resolved_project else ""

    # Build the prompt
    prompt = build_prompt(issue, ai_guide)

    if not dry_run:
        # Save prompt to workspace
        prompt_path = workspace / "prompt.md"
        prompt_path.write_text(prompt)
    else:
        prompt_path = workspace / "prompt.md"

    result = {
        "issue_number": issue_num,
        "workspace_path": str(workspace),
        "prompt_path": str(prompt_path),
        "prompt": prompt,
        "project_dir": str(resolved_project) if resolved_project else None,
        "delegate_params": {
            "workdir": str(workspace),
            "prompt": prompt,
            "acp_command": "claude",
        },
    }

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Prepare workspace for an orchestrator worker task",
    )
    parser.add_argument(
        "--issue", "-i",
        required=True,
        help="Issue JSON (object with number, title, body, labels, url) or path to JSON file",
    )
    parser.add_argument(
        "--project-dir", "-p",
        default=None,
        help="Target project directory (for AI_GUIDE.md context)",
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Show what would be done without creating files",
    )
    parser.add_argument(
        "--prompt-only",
        action="store_true",
        help="Only output the prompt text (no workspace setup)",
    )

    args = parser.parse_args()

    # Parse issue input
    issue_input = args.issue
    if os.path.exists(issue_input):
        with open(issue_input) as f:
            issue = json.load(f)
    else:
        try:
            issue = json.loads(issue_input)
        except json.JSONDecodeError:
            parser.error(f"Invalid JSON for --issue: {issue_input}")

    # Validate required fields
    for field in ("number", "title"):
        if field not in issue:
            parser.error(f"Issue missing required field: {field}")

    if args.prompt_only:
        ai_guide = ""
        if args.project_dir:
            ai_guide = read_ai_guide(Path(args.project_dir))
        print(build_prompt(issue, ai_guide))
        return

    result = spawn_worker(
        issue=issue,
        project_dir=Path(args.project_dir) if args.project_dir else None,
        dry_run=args.dry_run,
    )

    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
