# Roadmap Builder -- Task Guide for AI Agents

This document explains how to use the Task model in roadmap YAML files.
If you are an AI agent picking up work from a roadmap, read this first.

## The Hierarchy

```
Roadmap
  └─ Phase          (major milestone -- "Foundation", "MVP", "v2.0")
       └─ Deliverable    (concrete output -- "Core module", "REST API")
            └─ Task          (actionable step -- "Create register file", "Write tests")
```

Tasks are the unit of work an agent can pick up. A deliverable like "Core module"
is too coarse to just start on. Its tasks break it into ordered, verifiable steps.

## Task Fields

| Field | Required | Description |
|-------|----------|-------------|
| id | yes | Unique identifier. Convention: `p<phase>.d<deliv>.t<task>` (e.g. `p1.d1.t3`) |
| title | yes | Short description of the work |
| status | yes | `todo`, `in_progress`, or `done` |
| description | no | Step-by-step instructions or context |
| assignee | no | Agent name that should do this (advisory, not enforced) |
| dependencies | no | List of task IDs that must be `done` before this can start |
| acceptance_criteria | no | List of strings -- how to verify this task is complete |
| files | no | List of file paths to create or modify |

## YAML Example

```yaml
deliverables:
  - name: "Register file"
    description: "32 general-purpose registers for the VM"
    status: "todo"
    tasks:
      - id: "p1.d1.t1"
        title: "Define Register enum"
        status: "done"
        description: "Create src/registers.rs with the Register enum (R0-R31)"
        acceptance_criteria:
          - "File compiles without errors"
          - "All 32 register variants exist"
        files: ["src/registers.rs"]

      - id: "p1.d1.t2"
        title: "Implement register file struct"
        status: "todo"
        dependencies: ["p1.d1.t1"]
        description: "Create RegisterFile struct backed by [u32; 32]"
        acceptance_criteria:
          - "get() and set() methods work"
          - "Unit tests pass"
        files: ["src/registers.rs"]

      - id: "p1.d1.t3"
        title: "Write tests"
        status: "todo"
        dependencies: ["p1.d1.t2"]
        acceptance_criteria:
          - "Edge cases tested (R0 always 0, overflow wraps)"
        files: ["src/registers.rs", "tests/register_tests.rs"]
```

## How to Pick Up Work

### CLI: `roadmap next-task`

```bash
roadmap next-task roadmap.yaml
```

Returns the next actionable task: the first task with `status: todo` and all
dependencies satisfied. Output looks like:

```
Task: Implement register file struct
ID: p1.d1.t2
Status: todo
Phase: phase-1: Core VM
Deliverable: Register file
Dependencies: p1.d1.t1

Create RegisterFile struct backed by [u32; 32]

Acceptance Criteria:
  - get() and set() methods work
  - Unit tests pass

Target Files: src/registers.rs
```

If all tasks are done or blocked, it prints "No actionable tasks remaining."

### Python API: `roadmap.next_task()`

```python
from roadmap_builder import parse_yaml, TaskStatus

roadmap = parse_yaml("roadmap.yaml")
task = roadmap.next_task()

if task:
    print(f"Work on: {task.id} -- {task.title}")
    print(f"Files: {task.files}")
    print(f"Acceptance criteria: {task.acceptance_criteria}")
```

### How `next_task()` Picks

It walks the roadmap in order:
1. Skip phases with status `complete`
2. Skip deliverables with status `done`
3. Skip tasks that are not `todo`
4. Skip tasks whose dependencies are not all `done`
5. Return the first task that passes all filters

This means task order in the YAML matters. Put tasks in the order they should
be done. Use `dependencies` only when tasks are not sequential within a
deliverable (e.g. parallel tasks that converge, or cross-deliverable deps).

## How to Mark Work Done

Edit the YAML file. Change the task status:

```yaml
# Before
- id: "p1.d1.t2"
  title: "Implement register file struct"
  status: "todo"

# After
- id: "p1.d1.t2"
  title: "Implement register file struct"
  status: "done"
```

Then regenerate the markdown:

```bash
roadmap build roadmap.yaml -o ROADMAP.md -f markdown
```

Optionally move to `in_progress` first if the work will span multiple sessions.

## Dependency Rules

- Dependencies are task IDs (e.g. `["p1.d1.t1", "p1.d2.t4"]`)
- A task with no `dependencies` field (or empty list) is always actionable when `todo`
- A task with dependencies is only actionable when ALL of them are `done`
- Dependencies on tasks in other deliverables or other phases are valid
- Circular dependencies are not detected -- avoid them

## When to Mark the Deliverable Done

When ALL tasks in a deliverable are `done`, consider marking the deliverable
itself as `done`. This is not automatic -- the agent or human should verify the
deliverable's acceptance_criteria (the structured ones with validation methods).

## Carrying Forward

The carry_forward system (`suggest_next`) surfaces tasks from roadmaps. When a
project has a `roadmap.yaml` with tasks, carry_forward will show the next
actionable task at confidence 0.6 in the `context` command output.

For chain loops (autonomous coding), the preflight script can call
`roadmap next-task roadmap.yaml` to determine what to work on.

## Full Workflow for an Agent

1. Read this document
2. Run `roadmap next-task roadmap.yaml` to find what to work on
3. Read the task's description, acceptance_criteria, and files
4. Read any referenced files to understand the current state
5. Do the work
6. Run tests to verify acceptance criteria
7. Edit roadmap.yaml: change task status to `done`
8. If all tasks in a deliverable are done, mark deliverable `done`
9. Regenerate: `roadmap build roadmap.yaml -o ROADMAP.md -f markdown`
10. Commit all changes

## Backwards Compatibility

Roadmaps that don't use tasks still work. Tasks default to an empty list.
The `next_task()` method returns `None` when there are no tasks, and agents
should fall back to deliverable-level tracking.
