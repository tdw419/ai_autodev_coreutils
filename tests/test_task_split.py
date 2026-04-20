"""Tests for task-split coreutil."""

import json
from pathlib import Path
from unittest.mock import patch, MagicMock

from autodev_coreutils.contract import ensure_autodev_dir
from autodev_coreutils.task_split import format_task_md, main


def test_format_task_md():
    """format_task_md produces valid markdown."""
    task = {
        "id": "T1",
        "title": "Add logging",
        "description": "Add structured logging to all modules",
        "files_likely_touched": ["src/main.py", "src/utils.py"],
        "estimated_complexity": "small",
        "dependencies": [],
    }
    md = format_task_md(task, 0)
    assert "# Task T1: Add logging" in md
    assert "src/main.py" in md
    assert "small" in md
    assert "None (parallelizable)" in md


def test_format_task_md_empty_deps():
    """format_task_md handles empty fields gracefully."""
    task = {"id": "T2", "title": "Fix bug"}
    md = format_task_md(task, 1)
    assert "# Task T2: Fix bug" in md
    assert "Unknown" in md


def test_main_reads_file(tmp_path):
    """task-split reads a spec file."""
    ensure_autodev_dir(tmp_path)
    spec = tmp_path / "spec.md"
    spec.write_text("# Spec\nAdd feature X")

    mock_tasks = [
        {"id": "T1", "title": "Part 1", "description": "Do A", "files_likely_touched": [], "estimated_complexity": "small", "dependencies": []},
        {"id": "T2", "title": "Part 2", "description": "Do B", "files_likely_touched": [], "estimated_complexity": "medium", "dependencies": []},
    ]

    with patch("autodev_coreutils.task_split.split_spec", return_value=mock_tasks):
        result = main(["-w", str(tmp_path), str(spec), "--json"])

    # Check tasks were written
    ad = tmp_path / ".autodev"
    tasks_dir = ad / "tasks"
    assert tasks_dir.exists()
    task_files = list(tasks_dir.glob("task_*.md"))
    assert len(task_files) == 2

    # Check state
    state = json.loads((ad / "task_split_state.json").read_text())
    assert state["count"] == 2
