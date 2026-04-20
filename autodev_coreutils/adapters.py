"""Pipe adapters for composing autodev coreutils with each other.

The problem: existing tools (possibilities, roadmap, rfl) each have
their own CLI interface, output format, and file conventions. They
don't share stdin/stdout or a common data format.

The solution: adapter functions that bridge between tool outputs.
Each adapter reads one tool's output and produces input for the next.

Usage in Python:
    from autodev_coreutils.adapters import (
        possibilities_to_roadmap,
        roadmap_to_tasks,
        tasks_to_rfl_seeds,
    )

Usage from shell:
    autodev pipe possibilities:roadmap tree.json -o roadmap.yaml
    autodev pipe roadmap:tasks roadmap.yaml -n 3
    autodev pipe tasks:rfl-seeds --dir .autodev/tasks/
"""

import json
import sys
from pathlib import Path
from typing import Optional


def possibilities_to_roadmap(tree_json: str | Path, output: str | Path = None) -> str:
    """Convert a possibilities tree JSON into a roadmap YAML skeleton.

    Takes the top-ranked paths from a possibilities tree and generates
    a roadmap YAML with one phase per top path.

    Args:
        tree_json: Path to possibilities tree JSON file
        output: Optional output path for roadmap YAML

    Returns:
        Roadmap YAML string
    """
    if isinstance(tree_json, str) and not Path(tree_json).exists():
        data = json.loads(tree_json)
    else:
        data = json.loads(Path(tree_json).read_text())

    # Extract paths from the tree
    paths = _extract_paths(data)

    yaml_parts = [
        'title: "Generated from Possibility Tree"',
        'version: "0.1.0"',
        'description: "Auto-generated roadmap from possibility exploration"',
        'project_url: ""',
        '',
        'phases:',
    ]

    for i, path in enumerate(paths[:5]):  # Cap at 5 phases
        phase_id = f"phase-{i+1}"
        title = path.get("name", f"Phase {i+1}")
        description = path.get("description", "")

        yaml_parts.append(f'  - id: "{phase_id}"')
        yaml_parts.append(f'    title: "{title}"')
        yaml_parts.append(f'    status: "planned"')
        yaml_parts.append(f'    goal: "{description}"')
        yaml_parts.append(f'    description: "{description}"')
        yaml_parts.append(f'    deliverables:')
        yaml_parts.append(f'      - name: "Implementation"')
        yaml_parts.append(f'        description: "Implement {title}"')
        yaml_parts.append(f'        status: "planned"')
        yaml_parts.append(f'        acceptance_criteria:')
        yaml_parts.append(f'          - description: "Tests pass"')
        yaml_parts.append(f'            validation: "pytest"')
        yaml_parts.append(f'            met: false')
        yaml_parts.append('')

    result = "\n".join(yaml_parts)

    if output:
        Path(output).write_text(result)

    return result


def _extract_paths(tree_data: dict) -> list[dict]:
    """Extract ranked paths from a possibility tree."""
    paths = []

    def walk(node, current_path=None):
        if current_path is None:
            current_path = []

        name = node.get("description", node.get("name", ""))
        desc = node.get("rationale", "")
        current_path.append({"name": name, "description": desc})

        children = node.get("children", [])
        if not children:
            # Leaf node -- this is a complete path
            paths.append({
                "name": " -> ".join(p["name"] for p in current_path),
                "description": " | ".join(
                    p["description"] for p in current_path if p["description"]
                )[:200],
                "depth": len(current_path),
                "fertility": node.get("fertility", 0),
            })
        else:
            for child in children:
                walk(child, list(current_path))

    walk(tree_data)
    # Sort by fertility descending
    paths.sort(key=lambda p: p.get("fertility", 0), reverse=True)
    return paths


def roadmap_to_task_spec(roadmap_yaml: str | Path) -> str:
    """Convert a roadmap YAML into a single markdown spec suitable for task-split.

    The markdown spec lists all phases, deliverables, and tasks from the
    roadmap in a format task-split can decompose into parallel work items.
    """
    import yaml

    if isinstance(roadmap_yaml, Path) or Path(roadmap_yaml).exists():
        text = Path(roadmap_yaml).read_text()
    else:
        text = roadmap_yaml

    data = yaml.safe_load(text)

    lines = [f"# {data.get('title', 'Roadmap')}", ""]

    if data.get("description"):
        lines.append(data["description"])
        lines.append("")

    phases = data.get("phases", [])
    for phase in phases:
        lines.append(f"## Phase: {phase.get('title', phase.get('id', '?'))}")
        if phase.get("goal"):
            lines.append(f"**Goal:** {phase['goal']}")
        if phase.get("description"):
            lines.append(phase["description"])
        lines.append("")

        for deliv in phase.get("deliverables", []):
            lines.append(f"### Deliverable: {deliv.get('name', '?')}")
            if deliv.get("description"):
                lines.append(deliv["description"])
            lines.append("")

            for task in deliv.get("tasks", []):
                status = task.get("status", "planned")
                if status != "done":
                    lines.append(f"- [ ] {task.get('title', '?')}")
                    if task.get("description"):
                        lines.append(f"      {task['description']}")

        lines.append("")

    return "\n".join(lines)


def tasks_to_rfl_seeds(tasks_dir: str | Path, output_dir: str | Path = None) -> list[Path]:
    """Convert task markdown files into RFL seed prompts.

    Each task_NNN.md becomes a seed prompt that RFL can use with
    --from-file. The seed includes the task description plus context
    about what the agent should accomplish.

    Args:
        tasks_dir: Directory containing task_*.md files
        output_dir: Directory to write seed files (default: tasks_dir)

    Returns:
        List of seed file paths
    """
    tasks_path = Path(tasks_dir)
    out_path = Path(output_dir) if output_dir else tasks_path

    seeds = []
    for task_file in sorted(tasks_path.glob("task_*.md")):
        task_text = task_file.read_text()

        seed_text = f"""You are an AI coding agent executing a specific task.
Read the project's AI_GUIDE.md first to understand the codebase, then complete the task below.

# Task

{task_text}

# Instructions

1. Read AI_GUIDE.md in the project root
2. Understand the task requirements above
3. Implement the changes
4. Run tests to verify
5. Report what you did and what tests pass

When done, write a brief summary to .autodev/outcome_{task_file.stem}.md
"""
        seed_file = out_path / f"seed_{task_file.stem}.txt"
        seed_file.write_text(seed_text)
        seeds.append(seed_file)

    return seeds


def outcome_to_learnings(outcome_file: str | Path) -> str:
    """Convert an agent outcome file into a learnings entry.

    Extracts what worked, what didn't, and conventions discovered.
    """
    text = Path(outcome_file).read_text()

    return f"""## From {Path(outcome_file).name}

{text}

---
"""


# Adapter registry for CLI dispatch
ADAPTERS = {
    "possibilities:roadmap": possibilities_to_roadmap,
    "roadmap:tasks": roadmap_to_task_spec,
    "tasks:rfl-seeds": tasks_to_rfl_seeds,
}
