# AI Guide for autodev_coreutils

## What This Is

Linux coreutils for AI dev automation. One package with 7 consolidated tools
+ 5 new tools + pipe adapters + flow pipeline. 601 tests.

## Source Layout

```
autodev_coreutils/          # NEW tools
  contract.py               # Shared contract (all tools import from here)
  cli.py                    # `autodev` meta command
  adapters.py               # Pipe adapters between tool formats
  flow.py                   # One-shot pipeline
  task_split.py             # autodev-task-split
  context_pack.py           # autodev-context-pack
  verify.py                 # autodev-verify
  snapshot.py               # autodev-snapshot
  watchdog.py               # autodev-watchdog

model_choice/               # CONSOLIDATED from ~/zion/projects/model_choice
possibilities/              # CONSOLIDATED from ~/zion/projects/ai_possibilities
roadmap_builder/            # CONSOLIDATED from ~/zion/projects/roadmap_builder
recursive_feedback_loop/    # CONSOLIDATED from ~/zion/projects/recursive_feedback_loop
carry_forward/              # CONSOLIDATED from ~/zion/projects/carry_forward
autodev/                    # CONSOLIDATED from ~/zion/projects/autodev
session_relay/              # CONSOLIDATED from ~/zion/projects/session_relay
```

## Key Patterns

- Each consolidated package keeps its original module name
- Cross-package imports work: possibilities imports model_choice, etc.
- carry_forward uses a re-export __init__.py (original was flat module)
- All CLI entry points in pyproject.toml
- autodev_coreutils.contract provides shared infra for NEW tools only

## Build & Test

```bash
pip install -e . --break-system-packages
python3 -m pytest tests/ possibilities/tests/ recursive_feedback_loop/tests/ carry_forward/tests/ -q
# 601 tests
```

## Adding a New Coreutil

1. Create `autodev_coreutils/<name>.py`
2. Import from `contract.py`
3. Implement `main(argv=None)`
4. Add entry point to `pyproject.toml`
5. Register in `cli.py` COREUTILS dict
6. Add tests in `tests/test_<name>.py`

## Consolidating Another Tool

1. Copy package dir into this source tree
2. Add to `pyproject.toml` [tool.setuptools.packages.find] include list
3. Add CLI entry point to `pyproject.scripts`
4. Fix any import path issues (relative imports, conftest targets)
5. Run tests
