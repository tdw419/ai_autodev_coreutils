"""Roadmap Builder -- Markdown parser.

Parses the Geometry OS style ROADMAP.md format into the Roadmap model.

Format:
    # Title

    description text

    ## [x] phase-N: Title (STATUS)

    **Goal:** text

    description

    ### Deliverables

    - [x] **Name** -- description
      - [x] sub-task text
      - [ ] unchecked sub-task
    - [ ] **Name** -- description

    ### Technical Notes

    text

    ## Dependencies

    | From | To | Type | Reason |
    ...

    ## Global Risks

    - risk text

    ## Conventions

    - convention text
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from .models import (
    AcceptanceCriterion,
    Deliverable,
    DeliverableStatus,
    Dependency,
    DependencyType,
    Phase,
    PhaseStatus,
    Roadmap,
    Task,
    TaskStatus,
)


_PHASE_RE = re.compile(
    r"^##\s+\[([ xX])\]\s+"
    r"(phase-\d+)"
    r":\s+(.+?)"
    r"\s*\((COMPLETE|PLANNED|IN_PROGRESS|FUTURE)\)\s*$"
)

_GOAL_RE = re.compile(r"^\*\*Goal:\*\*\s*(.+)$")

_DELIVERABLE_RE = re.compile(
    r"^-\s+\[([ xX])\]\s+\*\*(.+?)\*\*\s*(?:--\s*(.+))?$"
)

_SUBTASK_RE = re.compile(r"^  -\s+\[([ xX])\]\s+(.+)$")

_DEP_TABLE_SEP = re.compile(r"^\|[-\s|:]+\|$")


def _phase_status(check: str, label: str) -> PhaseStatus:
    """Determine phase status from checkbox and label."""
    if check.lower() == "x":
        return PhaseStatus.COMPLETE
    mapping = {
        "COMPLETE": PhaseStatus.COMPLETE,
        "IN_PROGRESS": PhaseStatus.IN_PROGRESS,
        "PLANNED": PhaseStatus.PLANNED,
        "FUTURE": PhaseStatus.FUTURE,
    }
    return mapping.get(label, PhaseStatus.PLANNED)


def _deliverable_status(check: str) -> DeliverableStatus:
    if check.lower() == "x":
        return DeliverableStatus.DONE
    return DeliverableStatus.TODO


def _task_status(check: str) -> TaskStatus:
    if check.lower() == "x":
        return TaskStatus.DONE
    return TaskStatus.TODO


def _parse_dependencies(lines: list[str]) -> list[Dependency]:
    """Parse the dependency table (Markdown pipe format)."""
    deps = []
    in_table = False
    for line in lines:
        line = line.strip()
        if not line.startswith("|"):
            if in_table:
                break
            continue
        if _DEP_TABLE_SEP.match(line):
            in_table = True
            continue
        if not in_table:
            continue
        cells = [c.strip() for c in line.split("|")]
        # | from | to | type | reason |
        # cells: ['', from, to, type, reason, '']
        if len(cells) >= 5:
            dep_type_str = cells[3].strip().lower()
            dep_type_map = {
                "hard": DependencyType.HARD,
                "soft": DependencyType.SOFT,
                "informs": DependencyType.INFORMS,
            }
            deps.append(Dependency(
                source_phase=cells[1].strip(),
                target_phase=cells[2].strip(),
                dep_type=dep_type_map.get(dep_type_str, DependencyType.HARD),
                reason=cells[4].strip() if len(cells) > 4 else "",
            ))
    return deps


def _parse_global_section(lines: list[str], header: str) -> list[str]:
    """Parse a bullet-list section (Global Risks or Conventions)."""
    items = []
    in_section = False
    for line in lines:
        stripped = line.strip()
        if stripped == f"## {header}":
            in_section = True
            continue
        if in_section:
            if stripped.startswith("## "):
                break
            if stripped.startswith("- "):
                items.append(stripped[2:])
    return items


def _parse_deliverables(lines: list[str], phase_idx: int) -> list[Deliverable]:
    """Parse deliverables from lines within a phase section."""
    deliverables = []
    current_deliv = None
    task_counter = 0

    for line in lines:
        m = _DELIVERABLE_RE.match(line)
        if m:
            # Save previous deliverable
            if current_deliv is not None:
                deliverables.append(current_deliv)
            check, name, desc = m.group(1), m.group(2), m.group(3) or ""
            task_counter += 1
            task_id = f"p{phase_idx}.d{len(deliverables)+1}.t{task_counter}"
            current_deliv = Deliverable(
                name=name,
                description=desc,
                status=_deliverable_status(check),
                tasks=[],
            )
            continue

        sm = _SUBTASK_RE.match(line)
        if sm and current_deliv is not None:
            task_counter += 1
            task_id = f"p{phase_idx}.d{len(deliverables)+1}.t{task_counter}"
            current_deliv.tasks.append(Task(
                id=task_id,
                title=sm.group(2),
                status=_task_status(sm.group(1)),
            ))
            continue

    if current_deliv is not None:
        deliverables.append(current_deliv)

    return deliverables


def parse_markdown(path: str | Path) -> Roadmap:
    """Parse a Markdown roadmap (Geometry OS format) into a Roadmap model."""
    text = Path(path).read_text()
    lines = text.split("\n")

    # Extract title from first # heading
    title = "Untitled Roadmap"
    description = ""
    for line in lines:
        if line.startswith("# ") and not line.startswith("## "):
            title = line[2:].strip()
            break

    # Extract description (between title and first phase)
    desc_lines = []
    in_desc = False
    for line in lines:
        if line.startswith("# ") and not line.startswith("## "):
            in_desc = True
            continue
        if in_desc:
            if _PHASE_RE.match(line) or line.startswith("## "):
                break
            if line.strip():
                desc_lines.append(line.strip())
    description = " ".join(desc_lines)

    # Find all phase boundaries
    phase_starts = []
    for i, line in enumerate(lines):
        m = _PHASE_RE.match(line)
        if m:
            phase_starts.append((i, m))

    # Parse each phase
    phases = []
    for idx, (start, match) in enumerate(phase_starts):
        check, phase_id, phase_title, status_label = (
            match.group(1), match.group(2), match.group(3), match.group(4)
        )

        # Find end of this phase (next phase or end of file)
        if idx + 1 < len(phase_starts):
            end = phase_starts[idx + 1][0]
        else:
            # Go until ## Dependencies or ## Global Risks or EOF
            end = len(lines)
            for j in range(start + 1, len(lines)):
                if lines[j].strip().startswith("## Dependencies") or \
                   lines[j].strip().startswith("## Global Risks") or \
                   lines[j].strip().startswith("## Conventions"):
                    end = j
                    break

        phase_lines = lines[start:end]

        # Extract goal
        goal = ""
        for pl in phase_lines:
            gm = _GOAL_RE.match(pl)
            if gm:
                goal = gm.group(1)
                break

        # Extract description (text between goal and ### Deliverables)
        desc_parts = []
        found_goal = False
        for pl in phase_lines[1:]:  # skip the phase header
            if pl.startswith("### Deliverables"):
                break
            if found_goal:
                if pl.strip() and not pl.startswith("**") and not pl.startswith("##"):
                    desc_parts.append(pl.strip())
            if _GOAL_RE.match(pl):
                found_goal = True
        phase_desc = " ".join(desc_parts)

        # Find ### Deliverables section
        deliv_start = None
        deliv_end = len(phase_lines)
        for di, pl in enumerate(phase_lines):
            if pl.strip() == "### Deliverables":
                deliv_start = di + 1
            elif deliv_start is not None and (
                pl.startswith("### ") or pl.startswith("## ")
            ):
                deliv_end = di
                break

        deliverables = []
        if deliv_start is not None:
            deliverables = _parse_deliverables(
                phase_lines[deliv_start:deliv_end], idx + 1
            )

        phase_num = idx + 1
        phases.append(Phase(
            id=phase_id,
            title=phase_title,
            status=_phase_status(check, status_label),
            description=phase_desc,
            goal=goal,
            deliverables=deliverables,
        ))

    # Parse dependencies section
    dependencies = _parse_dependencies(lines)

    # Parse global risks and conventions
    global_risks = _parse_global_section(lines, "Global Risks")
    conventions = _parse_global_section(lines, "Conventions")

    return Roadmap(
        title=title,
        version="1.0.0",
        description=description,
        phases=phases,
        global_risks=global_risks,
        conventions=conventions,
        meta={"format": "markdown", "source": str(path)},
    )


def parse_auto(path: str | Path) -> Roadmap:
    """Auto-detect format (YAML or Markdown) and parse."""
    text = Path(path).read_text()
    stripped = text.lstrip()

    if stripped.startswith("---") or stripped.startswith("title:"):
        # YAML format
        import yaml
        data = yaml.safe_load(text)
        from .parser import parse_dict
        return parse_dict(data)
    elif stripped.startswith("#"):
        # Markdown format
        return parse_markdown(path)
    else:
        # Try YAML first, fall back to Markdown
        try:
            import yaml
            data = yaml.safe_load(text)
            if isinstance(data, dict) and "phases" in data:
                from .parser import parse_dict
                return parse_dict(data)
        except Exception:
            pass
        return parse_markdown(path)
