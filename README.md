# autodev_coreutils

Linux coreutils for AI development automation. One package, 7 tools, 601 tests.

Like GNU coreutils -- `ls`, `cat`, `grep`, `sort`, `wc` all live in one source
tree, share build infra, and ship as one package. Same idea, but for AI dev.

## Install

```bash
pip install -e .
```

One install gives you all of these commands:

| Command | Analogy | Source | Purpose |
|---------|---------|--------|---------|
| `possibilities` | `ls` | consolidated | Explore branching possibilities for any project |
| `roadmap` | `mkdir -p` | consolidated | Structure plans into phases/milestones |
| `rfl` | `while` | consolidated | Recursive self-feeding refinement loop |
| `model-choice` | `env` | consolidated | LLM provider selection and routing |
| `autodev-loop` | `for` | consolidated | Build-audit-fix-advance development loop |
| `carry-forward` | `nohup` | consolidated | Session continuity gate for loops |
| `autodev` | meta | new | Meta command: list, status, init, pipe, flow |
| `autodev-task-split` | `split` | new | Break a spec into N parallel work items |
| `autodev-context-pack` | `tar` | new | Bundle only files an agent needs |
| `autodev-verify` | `test` | new | Verify agent claims against codebase |
| `autodev-snapshot` | `checkpoint` | new | Capture/restore workflow state |
| `autodev-watchdog` | `watch` | new | Monitor agent, intervene on stall |

## The Contract

Every tool:
1. Reads a **project directory** (`-w .` by default)
2. Reads/writes **markdown specs** as the universal interchange format
3. Writes state to `.autodev/` in the project dir
4. Exits **0** on success, **non-zero** on failure
5. Accepts `--json` for machine-readable output
6. Accepts `-q` / `--quiet` for piped composition

## Quick Start

```bash
# Full pipeline: question -> RFL seeds in one command
autodev flow --question "What should we build next?" -w .

# Or step by step
possibilities explore "What next?" -w . -o .autodev/tree.json
autodev pipe possibilities:roadmap .autodev/tree.json -o .autodev/roadmap.yaml
autodev-task-split .autodev/roadmap.yaml -n 3 --json
autodev pipe tasks:rfl-seeds .autodev/tasks/
```

## Source Layout

```
autodev_coreutils/          # New tools (contract, adapters, flow, task-split, etc.)
model_choice/               # LLM provider routing (was ~/zion/projects/model_choice)
possibilities/              # Branching idea explorer (was ~/zion/projects/ai_possibilities)
roadmap_builder/            # Plan structuring (was ~/zion/projects/roadmap_builder)
recursive_feedback_loop/    # Iterative refinement (was ~/zion/projects/recursive_feedback_loop)
carry_forward/              # Session continuity (was ~/zion/projects/carry_forward)
autodev/                    # Build-audit-fix loop (was ~/zion/projects/autodev)
session_relay/              # Session handoff (was ~/zion/projects/session_relay)
```

Each keeps its own module namespace. Cross-package imports work because
they're all in one source tree now.

## Tests

```bash
python3 -m pytest tests/ possibilities/tests/ recursive_feedback_loop/tests/ carry_forward/tests/ -q
```

601 tests, all passing.
