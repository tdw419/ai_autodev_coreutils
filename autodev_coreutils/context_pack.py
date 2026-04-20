"""context-pack -- Bundle exactly the files an agent needs for a task.

Like `tar` but smarter: reads a task spec, uses the LLM to figure out
which files in the project are relevant, and bundles only those.
Agents waste tokens reading irrelevant code.

Input:  A task spec (file or .autodev/tasks/<N>.md)
Output: A directory or tar of just the relevant files
State:  context_pack_state.json with the file list

Usage:
    autodev-context-pack .autodev/tasks/task_000.md
    autodev-context-pack --task 2
    autodev-context-pack --spec "Add error handling to the parser"
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

try:
    from model_choice import query
except ImportError:
    query = None

from .contract import (
    make_parser, find_project, ensure_autodev_dir,
    write_state, output, error, read_spec,
)


def select_files(project: Path, task_text: str, model: str = None) -> list[str]:
    """Use LLM to select relevant files from the project."""
    if query is None:
        error("model_choice not installed")

    # Build file listing
    all_files = []
    for p in project.rglob("*"):
        if p.is_file() and not any(skip in str(p) for skip in [
            ".git/", "__pycache__/", ".venv/", "node_modules/",
            "target/", ".autodev/", ".egg-info/", ".mypy_cache/",
        ]):
            rel = str(p.relative_to(project))
            # Skip binary-ish files
            if any(rel.endswith(ext) for ext in [
                ".png", ".jpg", ".jpeg", ".gif", ".ico", ".woff",
                ".ttf", ".eot", ".so", ".o", ".pyc", ".wasm",
            ]):
                continue
            all_files.append(rel)

    file_list = "\n".join(all_files[:500])  # Cap to avoid token blowout

    prompt = f"""Given this task:
{task_text}

And these files in the project:
{file_list}

Select ONLY the files that are directly relevant to completing this task.
Be conservative -- include only files that need to be read or modified.
Output a JSON array of file paths. Output ONLY the JSON array, nothing else."""

    if model:
        resp = query(prompt, model=model)
    else:
        resp = query(prompt)

    text = resp.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:-1])

    try:
        files = json.loads(text)
    except json.JSONDecodeError:
        import re
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            files = json.loads(match.group())
        else:
            error(f"LLM did not return valid JSON. Got: {text[:200]}")

    # Validate files exist
    valid = []
    for f in files:
        if (project / f).exists():
            valid.append(f)
        else:
            # Try to find close match
            import difflib
            matches = difflib.get_close_matches(f, all_files, n=1, cutoff=0.6)
            if matches:
                valid.append(matches[0])

    return valid


def pack_files(project: Path, files: list[str], output_dir: Path) -> Path:
    """Copy selected files to output dir preserving structure."""
    output_dir.mkdir(parents=True, exist_ok=True)

    for f in files:
        src = project / f
        dst = output_dir / f
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    return output_dir


def main(argv=None):
    parser = make_parser("context-pack", "Bundle only the files an agent needs for a task")
    parser.add_argument(
        "task_file", nargs="?", default=None,
        help="Task spec file to pack context for",
    )
    parser.add_argument(
        "--task", type=int, default=None,
        help="Pack context for .autodev/tasks/task_<NNN>.md",
    )
    parser.add_argument(
        "--spec", default=None,
        help="Ad-hoc spec string to pack context for",
    )
    parser.add_argument(
        "-m", "--model", default=None,
        help="LLM model to use (via model_choice)",
    )
    parser.add_argument(
        "-o", "--output", default=None,
        help="Output directory (default: .autodev/pack/)",
    )

    args = parser.parse_args(argv)
    project = find_project(args.workdir)
    ad = ensure_autodev_dir(project)

    # Read task text
    task_text = ""
    if args.task_file:
        task_text = Path(args.task_file).read_text()
    elif args.task is not None:
        task_file = ad / "tasks" / f"task_{args.task:03d}.md"
        if not task_file.exists():
            error(f"Task file not found: {task_file}")
        task_text = task_file.read_text()
    elif args.spec:
        task_text = args.spec
    else:
        error("No task specified. Use: context-pack <file> or --task <N> or --spec <text>")

    # Select files
    files = select_files(project, task_text, args.model)

    # Pack
    out_dir = Path(args.output) if args.output else ad / "pack"
    pack_files(project, files, out_dir)

    # Write state
    write_state(project, "context_pack", {
        "task": args.task_file or f"task_{args.task:03d}" if args.task is not None else "ad-hoc",
        "files_selected": len(files),
        "files": files,
        "output": str(out_dir),
    })

    if args.json_output:
        output({"files": files, "output": str(out_dir)}, json_mode=True)
    elif not args.quiet:
        output(f"Packed {len(files)} files -> {out_dir}/")
        for f in files[:20]:
            output(f"  {f}")
        if len(files) > 20:
            output(f"  ... and {len(files) - 20} more")

    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
