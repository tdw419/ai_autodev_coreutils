"""Roadmap Builder -- data models."""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Optional


class PhaseStatus(str, enum.Enum):
    COMPLETE = "complete"
    IN_PROGRESS = "in_progress"
    PLANNED = "planned"
    FUTURE = "future"


class DeliverableStatus(str, enum.Enum):
    DONE = "done"
    IN_PROGRESS = "in_progress"
    TODO = "todo"


class TaskStatus(str, enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class DependencyType(str, enum.Enum):
    HARD = "hard"       # cannot start without this
    SOFT = "soft"       # strongly recommended but not blocking
    INFORMS = "informs" # output feeds into downstream


@dataclass
class AcceptanceCriterion:
    """A single testable criterion for a deliverable."""
    description: str
    validation: str = ""  # how to verify (e.g. "cargo test passes", "347 tests green")
    met: bool = False


@dataclass
class Task:
    """An actionable work item within a deliverable."""
    id: str                       # e.g. "p1.d1.t1"
    title: str
    status: TaskStatus = TaskStatus.TODO
    description: str = ""         # step-by-step instructions
    assignee: str = ""            # optional agent name
    dependencies: list[str] = field(default_factory=list)  # other task ids
    acceptance_criteria: list[str] = field(default_factory=list)
    files: list[str] = field(default_factory=list)  # target files to create/modify


@dataclass
class Deliverable:
    """A concrete piece of work within a phase."""
    name: str
    description: str
    status: DeliverableStatus = DeliverableStatus.TODO
    acceptance_criteria: list[AcceptanceCriterion] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)
    scope_lines: int = 0          # estimated LOC
    scope_files: list[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class Dependency:
    """A dependency edge between phases."""
    source_phase: str
    target_phase: str
    dep_type: DependencyType = DependencyType.HARD
    reason: str = ""


@dataclass
class Phase:
    """A major phase of the roadmap."""
    id: str
    title: str
    status: PhaseStatus = PhaseStatus.PLANNED
    description: str = ""
    goal: str = ""
    deliverables: list[Deliverable] = field(default_factory=list)
    dependencies: list[Dependency] = field(default_factory=list)
    technical_notes: str = ""
    risks: list[str] = field(default_factory=list)
    scope_lines_total: int = 0     # cumulative LOC after this phase
    scope_files_total: int = 0
    test_target: int = 0           # target test count after this phase


@dataclass
class Roadmap:
    """Top-level roadmap document."""
    title: str
    version: str = "0.1.0"
    description: str = ""
    project_url: str = ""
    phases: list[Phase] = field(default_factory=list)
    global_risks: list[str] = field(default_factory=list)
    conventions: list[str] = field(default_factory=list)
    meta: dict = field(default_factory=dict)

    def next_task(self) -> Optional["Task"]:
        """Return the next actionable task (status=todo, all deps done).

        Walks phases in order, then deliverables in order, then tasks in order.
        Returns the first task whose dependencies are all satisfied (status=done).
        Returns None if no actionable task exists.
        """
        # Build a lookup of task_id -> TaskStatus for dependency checking
        task_status_map: dict[str, TaskStatus] = {}
        for phase in self.phases:
            for deliv in phase.deliverables:
                for task in deliv.tasks:
                    task_status_map[task.id] = task.status

        for phase in self.phases:
            if phase.status == PhaseStatus.COMPLETE:
                continue
            for deliv in phase.deliverables:
                if deliv.status == DeliverableStatus.DONE:
                    continue
                for task in deliv.tasks:
                    if task.status != TaskStatus.TODO:
                        continue
                    # Check all dependencies are done
                    deps_met = all(
                        task_status_map.get(dep_id) == TaskStatus.DONE
                        for dep_id in task.dependencies
                    )
                    if deps_met:
                        return task
        return None
