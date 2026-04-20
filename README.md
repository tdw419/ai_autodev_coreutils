# autodev_coreutils

Linux coreutils for AI development automation.

Small, single-purpose CLI tools that share a common data contract,
composable via pipes and the filesystem.

## The Contract

Every tool:
1. Reads a **project directory** (`-w .` by default)
2. Reads/writes **markdown specs** as the universal interchange format
3. Writes state to `.autodev/` in the project dir
4. Exits **0** on success, **non-zero** on failure
5. Accepts `--json` for machine-readable output
6. Accepts `-q` / `--quiet` for piped composition (errors only)

## Install

```bash
pip install -e .
```

## Tools

### New Coreutils (this package)

| Command | Analogy | Purpose |
|---------|---------|---------|
| `autodev-task-split` | `split` | Break a spec into N independent parallel work items |
| `autodev-context-pack` | `tar` | Bundle only the files an agent needs for a task |
| `autodev-verify` | `test` | Verify agent claims against actual codebase state |
| `autodev-snapshot` | `checkpoint` | Capture or restore workflow state for resume |
| `autodev-watchdog` | `watch` | Monitor a running agent, intervene on stall |

### Pipe Adapters

Bridge between existing tool formats:

| Adapter | From | To | Purpose |
|---------|------|----|---------|
| `possibilities:roadmap` | tree.json | roadmap.yaml | Top paths become phases |
| `roadmap:tasks` | roadmap.yaml | markdown spec | Roadmap becomes task-split input |
| `tasks:rfl-seeds` | task_*.md | seed_*.txt | Tasks become RFL --from-file prompts |

```bash
autodev pipe possibilities:roadmap tree.json -o .autodev/roadmap.yaml
autodev pipe roadmap:tasks .autodev/roadmap.yaml | autodev-task-split - -n 3
autodev pipe tasks:rfl-seeds .autodev/tasks/ --json
```

### Flow (One-Shot Pipeline)

Chains the entire pipeline end-to-end:

```bash
autodev flow --question "What should we build next?" -w ./project
```

Runs: explore -> roadmap -> split -> pack -> seed in one command.

### Existing Tools (external, must be installed separately)

| Command | Purpose |
|---------|---------|
| `possibilities` | Explore branching possibilities for any project |
| `roadmap` | Parse specs into structured engineering roadmaps |
| `rfl` | Recursive Feedback Loop -- AI self-feeding conversation engine |
| `model-choice` | LLM provider selection and fallback chains |

## Quick Start

```bash
# Initialize a project
autodev init

# Check status
autodev status

# List all tools
autodev list

# Full pipeline from question to RFL seeds
autodev flow --question "What should we build next?" -w . --skip-pack

# Or step by step:
possibilities explore "What next?" -w . -o .autodev/tree.json
autodev pipe possibilities:roadmap .autodev/tree.json -o .autodev/roadmap.yaml
autodev-task-split .autodev/roadmap.yaml -n 3 --json
autodev pipe tasks:rfl-seeds .autodev/tasks/

# Verify after agent work
autodev-verify --claim "Added error handling to parser.py"

# Snapshot before risky changes
autodev-snapshot --tag "before-refactor"
```

## The `.autodev/` Directory

```
.autodev/
  tasks/                  # task-split output (task_000.md, ...)
  snapshots/              # snapshot archives (snap_<tag>.tar.gz)
  pack/                   # context-pack output (minimal file bundles)
  possibility_tree.json   # raw exploration tree
  roadmap.yaml            # generated roadmap
  *_state.json            # per-tool state files
  seed_task_*.txt         # RFL seed prompts
```

## Why

Linux coreutils work because every tool reads stdin, writes stdout,
exits 0/1. That contract enables `grep foo | sort | uniq -c | sort -rn`.

AI dev automation needs the same: tools that share a contract so they
compose. The contract is: project directory + markdown specs + exit codes.

## Tests

```bash
python3 -m pytest tests/ -v
```

22 tests, all passing.
