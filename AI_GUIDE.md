# AI Guide for autodev_coreutils

## What This Is

Linux coreutils for AI development automation. Small CLI tools that
share a common contract: project dir + markdown specs + exit codes.

## Project Structure

```
autodev_coreutils/
  contract.py      # Shared contract (all tools import from here)
  cli.py           # `autodev` meta command (list/status/init/pipe/flow)
  adapters.py      # Pipe adapters between tool formats
  flow.py          # One-shot pipeline (explore->roadmap->split->pack->seed)
  task_split.py    # `autodev-task-split`
  context_pack.py  # `autodev-context-pack`
  verify.py        # `autodev-verify`
  snapshot.py      # `autodev-snapshot`
  watchdog.py      # `autodev-watchdog`
tests/
  test_contract.py     # 9 tests
  test_adapters.py     # 6 tests
  test_task_split.py   # 3 tests
  test_snapshot.py     # 4 tests
```

22 tests total, all passing.

## Key Patterns

- **contract.py** is imported by every tool. It provides:
  `find_project()`, `ensure_autodev_dir()`, `write_state()`,
  `read_state()`, `write_spec()`, `read_spec()`, `make_parser()`
- **adapters.py** bridges tool formats. Each adapter reads one tool's
  output and produces input for the next. Registered in ADAPTERS dict.
- **flow.py** chains the full pipeline. Each step is a separate function
  that can succeed or fail independently.
- Every tool's `main()` takes `argv=None` so it's testable
- State goes to `.autodev/<tool>_state.json`
- Specs go to `.autodev/<name>.md`
- Tasks go to `.autodev/tasks/task_NNN.md`
- LLM calls go through `model_choice.query()`

## Build & Test

```bash
pip install -e . --break-system-packages  # system Python
python3 -m pytest tests/ -v               # 22 tests
```

## Adding a New Coreutil

1. Create `<name>.py` in `autodev_coreutils/`
2. Import from `contract.py`: `make_parser`, `find_project`, etc.
3. Implement `main(argv=None)` that returns 0 or non-zero
4. Add entry point to `pyproject.toml`: `autodev-<name> = "..."`
5. Register in `cli.py` COREUTILS dict
6. Add tests in `tests/test_<name>.py`

## Adding a New Pipe Adapter

1. Add function to `adapters.py` (takes input, produces output)
2. Register in ADAPTERS dict with `"source:dest"` key
3. Add test in `tests/test_adapters.py`

## External Dependencies

- `model_choice` -- LLM provider selection (required for LLM-using tools)
- `pyyaml` -- YAML parsing (needed by adapters)
- `rich` -- Terminal formatting
