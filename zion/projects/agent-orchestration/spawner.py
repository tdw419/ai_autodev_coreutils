#!/usr/bin/env python3
"""
Worker spawner for the Hermes Agent Orchestrator.

Takes an issue (from poller output) and prepares an isolated workspace
for a delegate_task worker. Builds a structured prompt from the issue
context and any project AI_GUIDE.md, then outputs the parameters needed
to spawn the worker.

Supports role-based specialization: when a role is matched (from issue
labels or heuristics), the role's system prompt is prepended and its
allowed toolsets / max_turns are applied.

Multi-repo support: workspaces are organized as workspaces/{repo_name}/{issue_number}
to avoid collisions between repos. Pass repo_name to select the layout.

The orchestrator (Hermes cron agent) reads this output and calls
delegate_task with the prepared workspace and prompt.
"""

import argparse
import json
import os
import sys
from pathlib import Path

from roles import load_all_roles, match_role, build_role_prompt

PROJECT_DIR = Path(os.environ.get("ORCH_PROJECT_DIR", os.path.expanduser("~/zion/projects/agent-orchestration")))
WORKSPACES_DIR = PROJECT_DIR / "workspaces"


def get_workspace_dir(issue_number: int, repo_name: str | None = None) -> Path:
    """
    Get workspace directory path for an issue.

    Multi-repo layout: workspaces/{repo_name}/{issue_number}
    Single-repo layout: workspaces/{issue_number}
    """
    if repo_name:
        return WORKSPACES_DIR / repo_name / str(issue_number)
    return WORKSPACES_DIR / str(issue_number)


def find_project_dir(issue: dict) -> Path | None:
    """Try to determine the target project directory from issue context."""
    body = issue.get("body", "")
    if not body:
        return None

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


def read_ai_guide(project_dir: Path | None = None, ai_guide_path: str = "") -> str:
    """Read AI_GUIDE.md from a project directory or explicit path."""
    if ai_guide_path:
        p = Path(os.path.expanduser(ai_guide_path))
        if p.exists():
            return p.read_text()
    if project_dir:
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
    pipeline: str | None = None,
    role_name: str | None = None,
    repo_name: str | None = None,
    ai_guide_path: str = "",
    dry_run: bool = False,
) -> dict:
    """
    Prepare workspace and prompt for a worker task.

    If a pipeline YAML is provided, the worker will execute via the DAG
    executor instead of a raw delegate_task call. Each issue becomes a
    DAG execution with the task context injected as {{task}}.

    If role_name is provided (or matched from issue labels), the role's
    system prompt is prepended and its toolsets/max_turns are applied.

    If repo_name is provided, workspace is organized under
    workspaces/{repo_name}/{issue_number}.

    Returns a dict with workspace_path, prompt_path, prompt, and
    project_dir that the orchestrator can use.
    """
    issue_num = issue["number"]
    workspace = get_workspace_dir(issue_num, repo_name)

    if workspace.exists():
        print(f"Warning: workspace {workspace} already exists (issue may be in-progress)", file=sys.stderr)

    # Load roles and match to this issue
    roles = load_all_roles()
    role = None
    if role_name and role_name in roles:
        role = roles[role_name]
    elif not role_name:
        role = match_role(issue, roles)

    if not dry_run:
        workspace.mkdir(parents=True, exist_ok=True)

        # Save issue metadata
        meta = {
            "issue_number": issue_num,
            "title": issue["title"],
            "labels": issue.get("labels", []),
            "url": issue.get("url", ""),
            "status": "in-progress",
            "pipeline": pipeline,
            "role": role.name if role else None,
            "repo_name": repo_name,
            "spawned_at": __import__("datetime").datetime.now().isoformat(),
        }
        (workspace / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")

    # Find project directory for AI_GUIDE.md context
    resolved_project = project_dir or find_project_dir(issue)
    ai_guide = read_ai_guide(resolved_project, ai_guide_path)

    # Build the task description
    task_desc = build_prompt(issue, ai_guide)

    # Apply role system prompt if matched
    if role:
        task_desc = build_role_prompt(task_desc, role)

    # Build execution instructions based on mode (pipeline vs direct)
    if pipeline:
        pipeline_path = Path(pipeline)
        if not pipeline_path.is_absolute():
            pipeline_path = PROJECT_DIR / pipeline
        execution_mode = "dag"
        exec_instructions = {
            "mode": "dag",
            "pipeline": str(pipeline_path),
            "workdir": str(workspace),
            "context": {"task": task_desc},
            "command": f"python3 {PROJECT_DIR}/executor.py {pipeline_path} --workdir {workspace} --context task=@{workspace}/task.json",
        }
    else:
        execution_mode = "direct"
        exec_instructions = {
            "mode": "direct",
            "workdir": str(workspace),
            "prompt": task_desc,
            "acp_command": role.acp_command if role else "claude",
        }
        # Apply role-specific constraints
        if role:
            exec_instructions["allowed_toolsets"] = role.allowed_toolsets
            exec_instructions["max_turns"] = role.max_turns

    if not dry_run:
        # Save prompt to workspace
        prompt_path = workspace / "prompt.md"
        prompt_path.write_text(task_desc)
        # Save task as JSON for DAG executor context
        (workspace / "task.json").write_text(json.dumps({"task": task_desc}))
    else:
        prompt_path = workspace / "prompt.md"

    result = {
        "issue_number": issue_num,
        "workspace_path": str(workspace),
        "prompt_path": str(prompt_path),
        "execution_mode": execution_mode,
        "project_dir": str(resolved_project) if resolved_project else None,
        "role": role.to_dict() if role else None,
        "repo_name": repo_name,
        "exec_instructions": exec_instructions,
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
        "--pipeline", "-P",
        default=os.environ.get("ORCH_PIPELINE", ""),
        help="Pipeline YAML to use (enables DAG mode). Default: ORCH_PIPELINE env var",
    )
    parser.add_argument(
        "--role", "-r",
        default=None,
        help="Role profile to use (e.g. implementer, reviewer, tester, coordinator). Default: auto-match from labels",
    )
    parser.add_argument(
        "--repo-name",
        default=None,
        help="Repo name for workspace organization (workspaces/{repo_name}/{issue})",
    )
    parser.add_argument(
        "--ai-guide",
        default="",
        help="Explicit path to AI_GUIDE.md (overrides project dir lookup)",
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
        ai_guide = read_ai_guide(
            Path(args.project_dir) if args.project_dir else None,
            args.ai_guide,
        )
        print(build_prompt(issue, ai_guide))
        return

    result = spawn_worker(
        issue=issue,
        project_dir=Path(args.project_dir) if args.project_dir else None,
        pipeline=args.pipeline or None,
        role_name=args.role or None,
        repo_name=args.repo_name or None,
        ai_guide_path=args.ai_guide,
        dry_run=args.dry_run,
    )

    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
