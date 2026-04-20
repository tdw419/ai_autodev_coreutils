"""Roadmap Builder -- renderers.

Converts a Roadmap model into Markdown, JSON, or YAML output.
"""

from __future__ import annotations

import json
from typing import Any

import yaml

from .models import (
    DeliverableStatus,
    PhaseStatus,
    Roadmap,
    TaskStatus,
)

# Status emoji/sigils for markdown
_PHASE_SIGIL = {
    PhaseStatus.COMPLETE: "[x]",
    PhaseStatus.IN_PROGRESS: "[~]",
    PhaseStatus.PLANNED: "[ ]",
    PhaseStatus.FUTURE: "[?]",
}

_DELIV_SIGIL = {
    DeliverableStatus.DONE: "[x]",
    DeliverableStatus.IN_PROGRESS: "[~]",
    DeliverableStatus.TODO: "[ ]",
}

_TASK_SIGIL = {
    TaskStatus.DONE: "[x]",
    TaskStatus.IN_PROGRESS: "[~]",
    TaskStatus.TODO: "[ ]",
}

_PHASE_BADGE = {
    PhaseStatus.COMPLETE: "COMPLETE",
    PhaseStatus.IN_PROGRESS: "IN PROGRESS",
    PhaseStatus.PLANNED: "PLANNED",
    PhaseStatus.FUTURE: "FUTURE",
}


def render_markdown(roadmap: Roadmap) -> str:
    """Render a Roadmap model as a GitHub-flavored Markdown document."""
    lines: list[str] = []

    # Header
    lines.append(f"# {roadmap.title}")
    lines.append("")
    if roadmap.description:
        lines.append(roadmap.description)
        lines.append("")

    # Progress summary
    total_phases = len(roadmap.phases)
    done = sum(1 for p in roadmap.phases if p.status == PhaseStatus.COMPLETE)
    in_prog = sum(1 for p in roadmap.phases if p.status == PhaseStatus.IN_PROGRESS)
    lines.append(f"**Progress:** {done}/{total_phases} phases complete, {in_prog} in progress")
    lines.append("")

    # Total deliverables
    all_deliverables = [d for p in roadmap.phases for d in p.deliverables]
    total_d = len(all_deliverables)
    done_d = sum(1 for d in all_deliverables if d.status == DeliverableStatus.DONE)
    if total_d > 0:
        lines.append(f"**Deliverables:** {done_d}/{total_d} complete")
        lines.append("")

    # Total tasks
    all_tasks = [t for p in roadmap.phases for d in p.deliverables for t in d.tasks]
    total_t = len(all_tasks)
    done_t = sum(1 for t in all_tasks if t.status == TaskStatus.DONE)
    if total_t > 0:
        lines.append(f"**Tasks:** {done_t}/{total_t} complete")
        lines.append("")

    # Scope summary table
    lines.append("## Scope Summary")
    lines.append("")
    lines.append("| Phase | Status | Deliverables | LOC Target | Tests |")
    lines.append("|-------|--------|-------------|-----------|-------|")
    for phase in roadmap.phases:
        d_done = sum(1 for d in phase.deliverables if d.status == DeliverableStatus.DONE)
        d_total = len(phase.deliverables)
        badge = _PHASE_BADGE.get(phase.status, "?")
        loc = f"{phase.scope_lines_total:,}" if phase.scope_lines_total else "-"
        tests = str(phase.test_target) if phase.test_target else "-"
        lines.append(f"| {phase.id} {phase.title} | {badge} | {d_done}/{d_total} | {loc} | {tests} |")
    lines.append("")

    # Dependencies
    all_deps = [d for p in roadmap.phases for d in p.dependencies]
    if all_deps:
        lines.append("## Dependencies")
        lines.append("")
        lines.append("| From | To | Type | Reason |")
        lines.append("|------|----|------|--------|")
        for dep in all_deps:
            lines.append(f"| {dep.source_phase} | {dep.target_phase} | {dep.dep_type.value} | {dep.reason} |")
        lines.append("")

    # Phase details
    for phase in roadmap.phases:
        sigil = _PHASE_SIGIL.get(phase.status, "[ ]")
        badge = _PHASE_BADGE.get(phase.status, "?")
        lines.append(f"## {sigil} {phase.id}: {phase.title} ({badge})")
        lines.append("")

        if phase.goal:
            lines.append(f"**Goal:** {phase.goal}")
            lines.append("")

        if phase.description:
            lines.append(phase.description)
            lines.append("")

        if phase.deliverables:
            lines.append("### Deliverables")
            lines.append("")
            for d in phase.deliverables:
                dsigil = _DELIV_SIGIL.get(d.status, "[ ]")
                lines.append(f"- {dsigil} **{d.name}** -- {d.description}")
                if d.tasks:
                    for t in d.tasks:
                        tsigil = _TASK_SIGIL.get(t.status, "[ ]")
                        dep_str = f" (depends: {', '.join(t.dependencies)})" if t.dependencies else ""
                        assignee_str = f" [{t.assignee}]" if t.assignee else ""
                        lines.append(f"  - {tsigil} `{t.id}` {t.title}{assignee_str}{dep_str}")
                        if t.description:
                            for line in t.description.strip().split("\n"):
                                lines.append(f"    > {line}")
                        for ac in t.acceptance_criteria:
                            lines.append(f"    - {ac}")
                        if t.files:
                            lines.append(f"    _Files: {', '.join(t.files)}_")
                if d.acceptance_criteria:
                    for ac in d.acceptance_criteria:
                        check = "x" if ac.met else " "
                        lines.append(f"  - [{check}] {ac.description}")
                        if ac.validation:
                            lines.append(f"    _Validation: {ac.validation}_")
                if d.scope_lines:
                    lines.append(f"  _~{d.scope_lines} LOC_")
                if d.notes:
                    lines.append(f"  _Note: {d.notes}_")
            lines.append("")

        if phase.technical_notes:
            lines.append("### Technical Notes")
            lines.append("")
            lines.append(phase.technical_notes)
            lines.append("")

        if phase.risks:
            lines.append("### Risks")
            lines.append("")
            for r in phase.risks:
                lines.append(f"- {r}")
            lines.append("")

    # Global risks
    if roadmap.global_risks:
        lines.append("## Global Risks")
        lines.append("")
        for r in roadmap.global_risks:
            lines.append(f"- {r}")
        lines.append("")

    # Conventions
    if roadmap.conventions:
        lines.append("## Conventions")
        lines.append("")
        for c in roadmap.conventions:
            lines.append(f"- {c}")
        lines.append("")

    return "\n".join(lines)


def render_json(roadmap: Roadmap) -> str:
    """Render a Roadmap model as JSON."""
    return json.dumps(_to_dict(roadmap), indent=2)


def render_yaml(roadmap: Roadmap) -> str:
    """Render a Roadmap model as YAML."""
    return yaml.dump(_to_dict(roadmap), default_flow_style=False, sort_keys=False)


def _to_dict(roadmap: Roadmap) -> dict[str, Any]:
    """Convert roadmap to a serializable dict."""
    return {
        "title": roadmap.title,
        "version": roadmap.version,
        "description": roadmap.description,
        "project_url": roadmap.project_url,
        "phases": [
            {
                "id": p.id,
                "title": p.title,
                "status": p.status.value,
                "description": p.description,
                "goal": p.goal,
                "deliverables": [
                    {
                        "name": d.name,
                        "description": d.description,
                        "status": d.status.value,
                        "acceptance_criteria": [
                            {
                                "description": ac.description,
                                "validation": ac.validation,
                                "met": ac.met,
                            }
                            for ac in d.acceptance_criteria
                        ],
                        "tasks": [
                            {
                                "id": t.id,
                                "title": t.title,
                                "status": t.status.value,
                                "description": t.description,
                                "assignee": t.assignee,
                                "dependencies": t.dependencies,
                                "acceptance_criteria": t.acceptance_criteria,
                                "files": t.files,
                            }
                            for t in d.tasks
                        ],
                        "scope_lines": d.scope_lines,
                        "scope_files": d.scope_files,
                        "notes": d.notes,
                    }
                    for d in p.deliverables
                ],
                "dependencies": [
                    {
                        "source": dep.source_phase,
                        "target": dep.target_phase,
                        "type": dep.dep_type.value,
                        "reason": dep.reason,
                    }
                    for dep in p.dependencies
                ],
                "technical_notes": p.technical_notes,
                "risks": p.risks,
                "scope_lines_total": p.scope_lines_total,
                "scope_files_total": p.scope_files_total,
                "test_target": p.test_target,
            }
            for p in roadmap.phases
        ],
        "global_risks": roadmap.global_risks,
        "conventions": roadmap.conventions,
        "meta": roadmap.meta,
    }
