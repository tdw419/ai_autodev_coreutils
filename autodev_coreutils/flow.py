"""flow -- One-shot pipeline that chains coreutils end-to-end.

The dream composition, made real:

  possibilities -> roadmap -> task-split -> context-pack -> rfl seeds

Usage:
    autodev flow --question "What should we build next?" -w ./project
    autodev flow --from-tree tree.json -w ./project
    autodev flow --from-roadmap roadmap.yaml -w ./project -n 3
"""

import json
import subprocess
import sys
from pathlib import Path

from .contract import (
    find_project, ensure_autodev_dir, write_state, output, error,
)


def run_cmd(cmd: str, timeout: int = 600) -> tuple[int, str, str]:
    """Run a shell command, return (exit_code, stdout, stderr)."""
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


def flow_explore(question: str, project: Path, model: str = None, complexity: str = "fast",
                 max_nodes: int = 25) -> Path | None:
    """Step 1: Run possibilities explore."""
    ad = ensure_autodev_dir(project)
    tree_file = ad / "possibility_tree.json"

    cmd = f'possibilities explore "{question}" -w "{project}" --max-nodes {max_nodes} -c {complexity} -o "{tree_file}"'
    if model:
        cmd += f' -m {model}'

    output(f"  [1/5] Exploring possibilities...")
    code, stdout, stderr = run_cmd(cmd, timeout=300)

    if code != 0 or not tree_file.exists():
        output(f"  [1/5] FAILED: {stderr[:200]}")
        return None

    # Count nodes
    data = json.loads(tree_file.read_text())
    node_count = _count_nodes(data)
    output(f"  [1/5] OK: {node_count} nodes explored -> {tree_file.name}")
    return tree_file


def flow_roadmap(tree_file: Path, project: Path) -> Path | None:
    """Step 2: Convert possibility tree to roadmap."""
    from .adapters import possibilities_to_roadmap

    ad = ensure_autodev_dir(project)
    roadmap_file = ad / "roadmap.yaml"

    output(f"  [2/5] Building roadmap...")
    try:
        possibilities_to_roadmap(tree_file, roadmap_file)
        output(f"  [2/5] OK: roadmap -> {roadmap_file.name}")
        return roadmap_file
    except Exception as e:
        output(f"  [2/5] FAILED: {e}")
        return None


def flow_split(roadmap_file: Path, project: Path, n: int = 3) -> bool:
    """Step 3: Split roadmap into tasks."""
    from .adapters import roadmap_to_task_spec
    from .task_split import split_spec, format_task_md

    ad = ensure_autodev_dir(project)
    tasks_dir = ad / "tasks"
    tasks_dir.mkdir(exist_ok=True)

    output(f"  [3/5] Splitting into {n} tasks...")
    try:
        spec = roadmap_to_task_spec(roadmap_file)
        tasks = split_spec(spec, n)

        # Write task files
        for i, task in enumerate(tasks):
            md = format_task_md(task, i)
            (tasks_dir / f"task_{i:03d}.md").write_text(md)
            task["_file"] = f".autodev/tasks/task_{i:03d}.md"

        write_state(project, "task_split", {
            "source": str(roadmap_file),
            "count": len(tasks),
            "tasks": tasks,
        })
        output(f"  [3/5] OK: {len(tasks)} tasks -> .autodev/tasks/")
        return True
    except Exception as e:
        output(f"  [3/5] FAILED: {e}")
        return False


def flow_pack(project: Path) -> int:
    """Step 4: Pack context for each task."""
    from .context_pack import select_files, pack_files

    ad = ensure_autodev_dir(project)
    tasks_dir = ad / "tasks"
    pack_dir = ad / "pack"

    task_files = sorted(tasks_dir.glob("task_*.md"))
    if not task_files:
        output(f"  [4/5] SKIP: no tasks to pack")
        return 0

    output(f"  [4/5] Packing context for {len(task_files)} tasks...")
    total_files = 0

    for task_file in task_files:
        task_text = task_file.read_text()
        try:
            files = select_files(project, task_text)
            task_pack = pack_dir / task_file.stem
            pack_files(project, files, task_pack)
            total_files += len(files)
        except Exception:
            # Packing is best-effort
            pass

    output(f"  [4/5] OK: {total_files} files packed across {len(task_files)} tasks")
    return len(task_files)


def flow_seeds(project: Path) -> list[Path]:
    """Step 5: Generate RFL seeds from tasks."""
    from .adapters import tasks_to_rfl_seeds

    ad = ensure_autodev_dir(project)
    tasks_dir = ad / "tasks"

    output(f"  [5/5] Generating RFL seeds...")
    seeds = tasks_to_rfl_seeds(tasks_dir)
    output(f"  [5/5] OK: {len(seeds)} seed files generated")

    for seed in seeds:
        output(f"        rfl run --from-file {seed}")

    return seeds


def _count_nodes(data: dict) -> int:
    """Count nodes in a possibility tree."""
    count = 1
    for child in data.get("children", []):
        count += _count_nodes(child)
    return count


def main_flow(
    question: str = None,
    tree_file: str = None,
    roadmap_file: str = None,
    project_path: str = ".",
    parallel: int = 3,
    skip_explore: bool = False,
    skip_pack: bool = False,
    json_mode: bool = False,
    quiet: bool = False,
    model: str = None,
):
    """Run the full exploration -> roadmap -> split -> pack -> seed pipeline."""
    project = find_project(project_path)
    ad = ensure_autodev_dir(project)

    if not quiet:
        output(f"Autodev Flow: {project.name}")
        output(f"")

    results = {"steps": {}, "status": "running"}

    # Step 1: Explore (or load existing tree)
    if tree_file:
        tree_path = Path(tree_file)
        if not tree_path.exists():
            error(f"Tree file not found: {tree_file}")
        if not quiet:
            output(f"  [1/5] Using existing tree: {tree_path.name}")
    elif roadmap_file:
        skip_explore = True
    elif question:
        tree_path = flow_explore(question, project, model)
        if not tree_path:
            results["status"] = "failed"
            results["failed_at"] = "explore"
            write_state(project, "flow", results)
            return 1
    else:
        error("Provide --question, --from-tree, or --from-roadmap")

    # Step 2: Build roadmap (or use existing)
    if roadmap_file:
        roadmap_path = Path(roadmap_file)
        if not roadmap_path.exists():
            error(f"Roadmap file not found: {roadmap_file}")
        if not quiet:
            output(f"  [2/5] Using existing roadmap: {roadmap_path.name}")
    elif not skip_explore:
        roadmap_path = flow_roadmap(tree_path, project)
        if not roadmap_path:
            results["status"] = "failed"
            results["failed_at"] = "roadmap"
            write_state(project, "flow", results)
            return 1
    else:
        roadmap_path = None

    # Step 3: Split into tasks
    if roadmap_path:
        if not flow_split(roadmap_path, project, parallel):
            results["status"] = "failed"
            results["failed_at"] = "split"
            write_state(project, "flow", results)
            return 1

    # Step 4: Pack context (optional, can be slow)
    if not skip_pack:
        flow_pack(project)

    # Step 5: Generate seeds
    seeds = flow_seeds(project)

    results["status"] = "success"
    results["seeds"] = [str(s) for s in seeds]
    write_state(project, "flow", results)

    if json_mode:
        output(results, json_mode=True)
    elif not quiet:
        output(f"")
        output(f"Done. To execute tasks:")
        for seed in seeds:
            output(f"  rfl run --from-file {seed}")

    return 0
