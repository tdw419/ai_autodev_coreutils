"""Roadmap Builder -- YAML parser.

Reads a structured YAML file and produces a Roadmap model.
See templates/ for example input formats.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

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

_STATUS_MAP_PHASE = {e.value: e for e in PhaseStatus}
_STATUS_MAP_DELIV = {e.value: e for e in DeliverableStatus}
_STATUS_MAP_TASK = {e.value: e for e in TaskStatus}
_DEP_TYPE_MAP = {e.value: e for e in DependencyType}


def _parse_acceptance(raw: dict[str, Any] | str) -> AcceptanceCriterion:
    if isinstance(raw, str):
        return AcceptanceCriterion(description=raw, validation="", met=True)
    return AcceptanceCriterion(
        description=raw.get("description", ""),
        validation=raw.get("validation", ""),
        met=raw.get("met", False),
    )


def _parse_deliverable(raw: dict[str, Any]) -> Deliverable:
    status_str = raw.get("status", "todo")
    status = _STATUS_MAP_DELIV.get(status_str, DeliverableStatus.TODO)
    criteria = [_parse_acceptance(c) for c in raw.get("acceptance_criteria", [])]
    tasks = [_parse_task(t) for t in raw.get("tasks", [])]
    return Deliverable(
        name=raw.get("name", ""),
        description=raw.get("description", ""),
        status=status,
        acceptance_criteria=criteria,
        tasks=tasks,
        scope_lines=raw.get("scope_lines", 0),
        scope_files=raw.get("scope_files", []),
        notes=raw.get("notes", ""),
    )


def _parse_task(raw: dict[str, Any]) -> Task:
    status_str = raw.get("status", "todo")
    status = _STATUS_MAP_TASK.get(status_str, TaskStatus.TODO)
    return Task(
        id=raw.get("id", ""),
        title=raw.get("title", ""),
        status=status,
        description=raw.get("description", ""),
        assignee=raw.get("assignee", ""),
        dependencies=raw.get("dependencies", []),
        acceptance_criteria=raw.get("acceptance_criteria", []),
        files=raw.get("files", []),
    )


def _parse_dependency(raw: dict[str, Any]) -> Dependency:
    dep_str = raw.get("type", "hard")
    return Dependency(
        source_phase=raw.get("source", ""),
        target_phase=raw.get("target", ""),
        dep_type=_DEP_TYPE_MAP.get(dep_str, DependencyType.HARD),
        reason=raw.get("reason", ""),
    )


def _parse_phase(raw: dict[str, Any]) -> Phase:
    status_str = raw.get("status", "planned")
    status = _STATUS_MAP_PHASE.get(status_str, PhaseStatus.PLANNED)
    deliverables = [_parse_deliverable(d) for d in raw.get("deliverables", [])]
    deps = [_parse_dependency(d) for d in raw.get("dependencies", [])]
    return Phase(
        id=raw.get("id", ""),
        title=raw.get("title", ""),
        status=status,
        description=raw.get("description", ""),
        goal=raw.get("goal", ""),
        deliverables=deliverables,
        dependencies=deps,
        technical_notes=raw.get("technical_notes", ""),
        risks=raw.get("risks", []),
        scope_lines_total=raw.get("scope_lines_total", 0),
        scope_files_total=raw.get("scope_files_total", 0),
        test_target=raw.get("test_target", 0),
    )


def parse_yaml(path: str | Path) -> Roadmap:
    """Parse a YAML roadmap file into a Roadmap model."""
    with open(path) as f:
        data = yaml.safe_load(f)

    phases = [_parse_phase(p) for p in data.get("phases", [])]

    return Roadmap(
        title=data.get("title", "Untitled Roadmap"),
        version=data.get("version", "0.1.0"),
        description=data.get("description", ""),
        project_url=data.get("project_url", ""),
        phases=phases,
        global_risks=data.get("global_risks", []),
        conventions=data.get("conventions", []),
        meta=data.get("meta", {}),
    )


def parse_dict(data: dict[str, Any]) -> Roadmap:
    """Parse a dict (already loaded YAML/JSON) into a Roadmap model."""
    phases = [_parse_phase(p) for p in data.get("phases", [])]
    return Roadmap(
        title=data.get("title", "Untitled Roadmap"),
        version=data.get("version", "0.1.0"),
        description=data.get("description", ""),
        project_url=data.get("project_url", ""),
        phases=phases,
        global_risks=data.get("global_risks", []),
        conventions=data.get("conventions", []),
        meta=data.get("meta", {}),
    )
