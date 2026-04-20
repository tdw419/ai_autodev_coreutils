"""Roadmap Builder -- CLI interface."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .parser import parse_yaml
from .markdown_parser import parse_auto, parse_markdown
from .renderer import render_json, render_markdown, render_yaml


def cmd_build(args: argparse.Namespace) -> None:
    """Build a roadmap from a YAML spec and render it."""
    roadmap = parse_auto(args.input)

    fmt = args.format
    if fmt == "markdown":
        output = render_markdown(roadmap)
    elif fmt == "json":
        output = render_json(roadmap)
    elif fmt == "yaml":
        output = render_yaml(roadmap)
    else:
        print(f"Unknown format: {fmt}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        Path(args.output).write_text(output)
        print(f"Wrote {len(output)} bytes to {args.output}")
    else:
        print(output)


def cmd_validate(args: argparse.Namespace) -> None:
    """Validate a YAML roadmap spec."""
    try:
        roadmap = parse_auto(args.input)
        issues = []

        if not roadmap.title:
            issues.append("Missing roadmap title")

        phase_ids = set()
        for phase in roadmap.phases:
            if phase.id in phase_ids:
                issues.append(f"Duplicate phase id: {phase.id}")
            phase_ids.add(phase.id)

            if not phase.title:
                issues.append(f"Phase {phase.id} missing title")

            for dep in phase.dependencies:
                if dep.source_phase not in phase_ids:
                    issues.append(f"Dependency source '{dep.source_phase}' not found in phases")
                if dep.target_phase not in phase_ids:
                    issues.append(f"Dependency target '{dep.target_phase}' not found in phases")

        if issues:
            print("Validation issues:")
            for issue in issues:
                print(f"  - {issue}")
            sys.exit(1)
        else:
            n_phases = len(roadmap.phases)
            n_delivs = sum(len(p.deliverables) for p in roadmap.phases)
            n_tasks = sum(len(t) for p in roadmap.phases for d in p.deliverables for t in [d.tasks])
            msg = f"OK: {n_phases} phases, {n_delivs} deliverables"
            if n_tasks:
                msg += f", {n_tasks} tasks"
            msg += ", no issues"
            print(msg)


    except Exception as e:
        print(f"Parse error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_init(args: argparse.Namespace) -> None:
    """Create a starter roadmap YAML file."""
    starter = f"""title: "{args.title}"
version: "0.1.0"
description: "Product roadmap for {args.title}"
project_url: ""

phases:
  - id: "phase-1"
    title: "Foundation"
    status: "in_progress"
    goal: "Get the core working end-to-end"
    description: "Build the minimum viable version."
    deliverables:
      - name: "Core module"
        description: "The main module"
        status: "in_progress"
        acceptance_criteria:
          - description: "All tests pass"
            validation: "pytest"
            met: false
        tasks:
          - id: "p1.d1.t1"
            title: "Set up project structure"
            status: "done"
            description: "Create package layout with pyproject.toml"
            acceptance_criteria:
              - "Package installs cleanly"
            files: ["pyproject.toml", "src/__init__.py"]
          - id: "p1.d1.t2"
            title: "Implement core logic"
            status: "todo"
            dependencies: ["p1.d1.t1"]
            acceptance_criteria:
              - "Unit tests pass"
            files: ["src/core.py"]
    technical_notes: ""
    risks: []
    scope_lines_total: 1000
    test_target: 50

global_risks:
  - "Scope creep"

conventions:
  - "All code goes through PR review"
"""
    output_path = args.output or "roadmap.yaml"
    Path(output_path).write_text(starter)
    print(f"Created {output_path}")


def cmd_next_task(args: argparse.Namespace) -> None:
    """Print the next actionable task from a roadmap."""
    roadmap = parse_auto(args.input)
    task = roadmap.next_task()
    if task is None:
        print("No actionable tasks remaining.")
        sys.exit(0)

    # Find which deliverable/phase this task belongs to
    phase_info = ""
    deliv_info = ""
    for phase in roadmap.phases:
        for deliv in phase.deliverables:
            for t in deliv.tasks:
                if t.id == task.id:
                    phase_info = f"{phase.id}: {phase.title}"
                    deliv_info = f"{deliv.name}"
                    break

    lines = [
        f"Task: {task.title}",
        f"ID: {task.id}",
        f"Status: {task.status.value}",
        f"Phase: {phase_info}",
        f"Deliverable: {deliv_info}",
    ]
    if task.assignee:
        lines.append(f"Assignee: {task.assignee}")
    if task.dependencies:
        lines.append(f"Dependencies: {', '.join(task.dependencies)}")
    if task.description:
        lines.append("")
        lines.append(task.description)
    if task.acceptance_criteria:
        lines.append("")
        lines.append("Acceptance Criteria:")
        for ac in task.acceptance_criteria:
            lines.append(f"  - {ac}")
    if task.files:
        lines.append("")
        lines.append(f"Target Files: {', '.join(task.files)}")

    print("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="roadmap",
        description="Roadmap Builder -- parse specs into structured engineering roadmaps",
    )
    sub = parser.add_subparsers(dest="command")

    # build
    p_build = sub.add_parser("build", help="Build roadmap from YAML spec")
    p_build.add_argument("input", help="Input YAML roadmap spec")
    p_build.add_argument("-o", "--output", help="Output file path (stdout if omitted)")
    p_build.add_argument("-f", "--format", default="markdown",
                         choices=["markdown", "json", "yaml"], help="Output format")
    p_build.set_defaults(func=cmd_build)

    # validate
    p_validate = sub.add_parser("validate", help="Validate a roadmap YAML spec")
    p_validate.add_argument("input", help="Input YAML roadmap spec")
    p_validate.set_defaults(func=cmd_validate)

    # init
    p_init = sub.add_parser("init", help="Create a starter roadmap YAML")
    p_init.add_argument("title", help="Roadmap title")
    p_init.add_argument("-o", "--output", help="Output file path (default: roadmap.yaml)")
    p_init.set_defaults(func=cmd_init)

    # next-task
    p_next = sub.add_parser("next-task", help="Show the next actionable task")
    p_next.add_argument("input", help="Input YAML roadmap spec")
    p_next.set_defaults(func=cmd_next_task)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
