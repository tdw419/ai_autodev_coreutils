"""task-split -- Break one spec into N independent parallel work items.

Like `split` but for specs: takes a markdown spec or plan and decomposes
it into independently executable work items with clear boundaries.

Input:  A markdown spec/plan (file or stdin)
Output: N work item files in .autodev/tasks/
State:  task_split_state.json with the decomposition

Usage:
    autodev-task-split roadmap.md --parallel 3
    autodev-task-split --from-spec plan --parallel 5
    cat spec.md | autodev-task-split --parallel 2
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from model_choice import query
except ImportError:
    query = None

from .contract import (
    make_parser, add_common_args, find_project, ensure_autodev_dir,
    write_state, output, error, read_spec, EXIT_FAILURE,
)


TASKS_DIR = "tasks"


def split_spec(spec_text: str, n: int, model: str = None, context: str = "") -> list[dict]:
    """Use an LLM to split a spec into N independent work items."""
    if query is None:
        error("model_choice not installed. Run: pip install model_choice")

    prompt = f"""You are a task decomposer. Break this specification into exactly {n} independent, parallelizable work items.

Rules:
- Each item must be independently executable by an AI coding agent
- Each item must have clear input/output boundaries
- Items should not depend on each other (they run in parallel)
- Include enough context in each item that an agent can work alone
- Use markdown format

{context}

SPECIFICATION:
{spec_text}

Output JSON array of objects with keys: id, title, description, files_likely_touched, estimated_complexity (small/medium/large), dependencies (should be empty for parallel items).
Output ONLY valid JSON, no markdown fences."""

    if model:
        resp = query(prompt, model=model)
    else:
        resp = query(prompt)

    # Parse the JSON response
    text = resp.strip()
    if text.startswith("```"):
        # Strip markdown fences
        lines = text.split("\n")
        text = "\n".join(lines[1:-1])

    try:
        tasks = json.loads(text)
    except json.JSONDecodeError:
        # Try to extract JSON from the text
        import re
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            tasks = json.loads(match.group())
        else:
            error(f"LLM did not return valid JSON. Got: {text[:200]}")

    if not isinstance(tasks, list):
        error(f"Expected list of tasks, got {type(tasks)}")

    return tasks


def format_task_md(task: dict, index: int) -> str:
    """Format a single task as markdown."""
    return f"""# Task {task.get('id', index)}: {task.get('title', 'Untitled')}

## Description
{task.get('description', 'No description')}

## Files Likely Touched
{chr(10).join(f'- {f}' for f in task.get('files_likely_touched', [])) or '- Unknown'}

## Estimated Complexity
{task.get('estimated_complexity', 'unknown')}

## Dependencies
{', '.join(task.get('dependencies', [])) or 'None (parallelizable)'}
"""


def main(argv=None):
    parser = make_parser("task-split", "Break a spec into N independent parallel work items")
    parser.add_argument(
        "spec_file", nargs="?", default=None,
        help="Markdown spec file to split (reads stdin if omitted)",
    )
    parser.add_argument(
        "--from-spec", dest="from_spec",
        help="Read spec from .autodev/<name>.md",
    )
    parser.add_argument(
        "-n", "--parallel", type=int, default=3,
        help="Number of parallel work items to produce (default: 3)",
    )
    parser.add_argument(
        "-m", "--model", default=None,
        help="LLM model to use (via model_choice)",
    )
    parser.add_argument(
        "--context-files", nargs="*", default=[],
        help="Extra files to include as context",
    )

    args = parser.parse_args(argv)
    project = find_project(args.workdir)
    ad = ensure_autodev_dir(project)

    # Read spec
    spec_text = ""
    if args.spec_file:
        spec_text = Path(args.spec_file).read_text()
    elif args.from_spec:
        spec_text = read_spec(project, args.from_spec)
        if not spec_text:
            error(f"Spec '{args.from_spec}' not found in .autodev/")
    elif not sys.stdin.isatty():
        spec_text = sys.stdin.read()
    else:
        error("No spec provided. Use: task-split <file> or --from-spec <name> or pipe stdin")

    # Read context files
    context = ""
    for cf in args.context_files:
        p = Path(cf)
        if p.exists():
            context += f"\n--- {cf} ---\n{p.read_text()}\n"

    # Split
    tasks = split_spec(spec_text, args.parallel, args.model, context)

    # Write task files
    tasks_dir = ad / TASKS_DIR
    tasks_dir.mkdir(exist_ok=True)

    # Clean old tasks
    for old in tasks_dir.glob("task_*.md"):
        old.unlink()

    written = []
    for i, task in enumerate(tasks):
        md = format_task_md(task, i)
        task_file = tasks_dir / f"task_{i:03d}.md"
        task_file.write_text(md)
        task["_file"] = str(task_file.relative_to(project))
        written.append(task)

    # Write state
    write_state(project, "task_split", {
        "source": args.spec_file or args.from_spec or "stdin",
        "count": len(written),
        "tasks": written,
    })

    if args.json_output:
        output({"tasks": written, "count": len(written)}, json_mode=True)
    elif not args.quiet:
        output(f"Split into {len(written)} tasks:")
        for t in written:
            output(f"  [{t.get('id', '?')}] {t.get('title', 'Untitled')} ({t.get('estimated_complexity', '?')})")

    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
