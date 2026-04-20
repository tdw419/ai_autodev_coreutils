"""autodev -- Meta command for all autodev coreutils.

Lists available tools, shows tool status, provides help.

Usage:
    autodev list          # Show all available coreutils
    autodev status        # Show .autodev/ state for current project
    autodev init          # Initialize .autodev/ directory
    autodev help <tool>   # Show help for a specific tool
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

from . import __version__
from .contract import (
    find_project, ensure_autodev_dir, read_state,
    output, error, EXIT_SUCCESS,
)


# All coreutils and their descriptions
COREUTILS = {
    # New tools in this package
    "task-split": {
        "cmd": "autodev-task-split",
        "desc": "Break a spec into N independent parallel work items",
        "module": "autodev_coreutils.task_split",
        "new": True,
    },
    "context-pack": {
        "cmd": "autodev-context-pack",
        "desc": "Bundle only the files an agent needs for a task",
        "module": "autodev_coreutils.context_pack",
        "new": True,
    },
    "verify": {
        "cmd": "autodev-verify",
        "desc": "Verify agent claims against actual codebase state",
        "module": "autodev_coreutils.verify",
        "new": True,
    },
    "snapshot": {
        "cmd": "autodev-snapshot",
        "desc": "Capture or restore autodev workflow state",
        "module": "autodev_coreutils.snapshot",
        "new": True,
    },
    "watchdog": {
        "cmd": "autodev-watchdog",
        "desc": "Monitor a running agent and intervene on stall",
        "module": "autodev_coreutils.watchdog",
        "new": True,
    },
    # Existing tools (external CLIs)
    "possibilities": {
        "cmd": "possibilities",
        "desc": "Explore branching possibilities for any project",
        "module": "possibilities.cli",
        "new": False,
    },
    "roadmap": {
        "cmd": "roadmap",
        "desc": "Parse specs into structured engineering roadmaps",
        "module": "roadmap_builder.cli",
        "new": False,
    },
    "rfl": {
        "cmd": "rfl",
        "desc": "Recursive Feedback Loop -- AI self-feeding conversation engine",
        "module": "recursive_feedback_loop.cli",
        "new": False,
    },
    "model-choice": {
        "cmd": "model-choice",
        "desc": "LLM provider selection and fallback chains",
        "module": "model_choice.cli",
        "new": False,
    },
}

# Hermes skills (not CLIs, but part of the ecosystem)
SKILLS = {
    "carry-forward": "Bouncer/gate for autonomous session loops",
    "keep-or-revert": "Atomic git commit or rollback wrapper",
    "learnings": "Accumulate project knowledge across sessions",
    "strategist": "Prioritize next work from audit data and history",
    "session-chain": "Self-chaining Hermes session loop",
    "delegate-dispatch": "Route tasks to the right AI agent",
    "ai-guide": "Generate AI_GUIDE.md for a codebase",
    "autodev": "Autonomous development loop (build-audit-fix-advance)",
}


def list_tools(json_mode=False, quiet=False):
    """List all available coreutils."""
    if json_mode:
        output({"coreutils": COREUTILS, "skills": SKILLS}, json_mode=True)
        return

    output("Autodev Coreutils v" + __version__)
    output("")
    output("CLI Tools:")
    for name, info in COREUTILS.items():
        marker = "+" if info["new"] else " "
        status = ""
        # Check if installed
        try:
            result = subprocess.run(
                ["which", info["cmd"]], capture_output=True, timeout=5,
            )
            if result.returncode != 0:
                status = " [NOT INSTALLED]"
        except (subprocess.TimeoutExpired, FileNotFoundError):
            status = " [?]"
        output(f"  {marker} {name:16s} {info['desc']}{status}")

    output("")
    output("Hermes Skills (loaded via skill_view):")
    for name, desc in SKILLS.items():
        output(f"    {name:16s} {desc}")


def show_status(project: Path, json_mode=False, quiet=False):
    """Show .autodev/ state for current project."""
    ad = project / ".autodev"
    if not ad.exists():
        if not quiet:
            output("No .autodev/ directory. Run: autodev init")
        return

    # Read all state files
    states = {}
    for state_file in sorted(ad.glob("*_state.json")):
        tool = state_file.stem.replace("_state", "")
        states[tool] = json.loads(state_file.read_text())

    if json_mode:
        output(states, json_mode=True)
    elif not quiet:
        output(f"Project: {project}")
        output(f"State files: {len(states)}")
        for tool, state in states.items():
            updated = state.get("updated_at", "unknown")
            output(f"  {tool}: updated {updated}")

    # Check for tasks
    tasks_dir = ad / "tasks"
    if tasks_dir.exists():
        tasks = list(tasks_dir.glob("task_*.md"))
        if not quiet:
            output(f"  Tasks: {len(tasks)}")


def init_project(project: Path, quiet=False):
    """Initialize .autodev/ directory with standard structure."""
    ad = ensure_autodev_dir(project)
    (ad / "tasks").mkdir(exist_ok=True)
    (ad / "snapshots").mkdir(exist_ok=True)
    (ad / "pack").mkdir(exist_ok=True)

    # Create .gitignore for autodev state
    gitignore = ad / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text("# Autodev state -- check this in for team sharing\n# or ignore for solo projects\n")

    if not quiet:
        output(f"Initialized .autodev/ in {project}")


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="autodev",
        description="Autodev Coreutils -- Linux coreutils for AI development automation",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "-w", "--workdir", default=".",
        help="Project directory (default: current directory)",
    )
    parser.add_argument(
        "--json", action="store_true", dest="json_output",
        help="Output in JSON format",
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true",
        help="Suppress output",
    )

    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="List all available coreutils")
    sub.add_parser("status", help="Show .autodev/ state for current project")
    sub.add_parser("init", help="Initialize .autodev/ directory")

    args = parser.parse_args(argv)
    project = find_project(args.workdir)

    if args.command == "list" or args.command is None:
        list_tools(args.json_output, args.quiet)
    elif args.command == "status":
        show_status(project, args.json_output, args.quiet)
    elif args.command == "init":
        init_project(project, args.quiet)
    else:
        parser.print_help()

    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
