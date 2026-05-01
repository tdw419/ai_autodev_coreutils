#!/usr/bin/env python3
"""Tests for Phase 10: Automated Garbage Collection and Remediation."""

import json
import os
import sys
import time
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).parent))

from garbage_collector import (
    scan_stale_workspaces,
    scan_dead_branches,
    scan_leaked_resources,
    cleanup_workspace,
    scan_conventions,
    run_gc,
    GC_DIR,
    ORCH_DIR,
    LOGS_DIR,
    WORKSPACES_DIR,
    PROJECT_DIR,
)

import garbage_collector as gc_mod


@pytest.fixture(autouse=True)
def setup_dirs(tmp_path, monkeypatch):
    """Redirect all GC directories to tmp_path."""
    monkeypatch.setattr("garbage_collector.WORKSPACES_DIR", tmp_path / "workspaces")
    monkeypatch.setattr("garbage_collector.ORCH_DIR", tmp_path / ".orchestrator")
    monkeypatch.setattr("garbage_collector.LOGS_DIR", tmp_path / ".orchestrator" / "logs")
    monkeypatch.setattr("garbage_collector.GC_DIR", tmp_path / ".orchestrator" / "logs" / "gc")
    monkeypatch.setattr("garbage_collector.PROJECT_DIR", tmp_path / "project")


# --- Stale Workspace Scanner ---

def test_scan_stale_workspaces_empty(tmp_path):
    """No workspaces returns empty list."""
    result = scan_stale_workspaces(max_age_hours=72)
    assert result == []


def test_scan_stale_workspaces_fresh(tmp_path):
    """Recently modified workspace is not stale."""
    ws_dir = tmp_path / "workspaces" / "42"
    ws_dir.mkdir(parents=True)
    (ws_dir / "meta.json").write_text(json.dumps({
        "issue_number": 42,
        "status": "in-progress",
    }))
    (ws_dir / "main.py").write_text("print('hello')")

    result = scan_stale_workspaces(max_age_hours=72)
    assert len(result) == 0


def test_scan_stale_workspaces_old(tmp_path):
    """Old workspace is detected as stale."""
    ws_dir = tmp_path / "workspaces" / "99"
    ws_dir.mkdir(parents=True)
    (ws_dir / "meta.json").write_text(json.dumps({
        "issue_number": 99,
        "status": "completed",
    }))
    old_file = ws_dir / "output.txt"
    old_file.write_text("old data")
    # Backdate ALL files in workspace
    old_time = time.time() - (100 * 3600)  # 100 hours ago
    for f in ws_dir.rglob("*"):
        if f.is_file():
            os.utime(f, (old_time, old_time))

    result = scan_stale_workspaces(max_age_hours=72)
    assert len(result) == 1
    assert result[0]["issue_number"] == 99
    assert result[0]["age_hours"] > 72


# --- Dead Branch Scanner ---

def test_scan_dead_branches_no_workspaces(tmp_path):
    """No workspaces returns empty list."""
    result = scan_dead_branches()
    assert result == []


def test_scan_dead_branches_active_not_dead(tmp_path):
    """Active workspace is not reported as dead."""
    ws_dir = tmp_path / "workspaces" / "42"
    ws_dir.mkdir(parents=True)
    (ws_dir / "meta.json").write_text(json.dumps({
        "issue_number": 42,
        "status": "in-progress",
    }))
    # Simulate git repo
    git_dir = ws_dir / ".git"
    git_dir.mkdir()
    (git_dir / "HEAD").write_text("ref: refs/heads/feature-42")

    result = scan_dead_branches()
    assert len(result) == 0


def test_scan_dead_branches_no_git(tmp_path):
    """Workspace without git is not reported."""
    ws_dir = tmp_path / "workspaces" / "50"
    ws_dir.mkdir(parents=True)
    (ws_dir / "meta.json").write_text(json.dumps({
        "issue_number": 50,
        "status": "completed",
    }))

    result = scan_dead_branches()
    assert len(result) == 0


# --- Leaked Resources Scanner ---

def test_scan_leaked_resources_empty(tmp_path):
    """No leaks in clean state."""
    result = scan_leaked_resources()
    assert all(len(v) == 0 for v in result.values())


def test_scan_leaked_resources_incomplete_logs(tmp_path):
    """Small log files are flagged as incomplete."""
    logs_dir = tmp_path / ".orchestrator" / "logs" / "runs"
    logs_dir.mkdir(parents=True)
    (logs_dir / "run-tiny.json").write_text("{}")  # 2 bytes, < 10 threshold

    result = scan_leaked_resources()
    assert len(result["incomplete_logs"]) == 1


def test_scan_leaked_resources_temp_files(tmp_path):
    """Temp files are detected."""
    orch_dir = tmp_path / ".orchestrator"
    orch_dir.mkdir(parents=True)
    (orch_dir / "cache.tmp").write_text("temp data")
    (orch_dir / "backup.bak").write_text("backup data")

    result = scan_leaked_resources()
    assert len(result["temp_files"]) == 2


def test_scan_leaked_resources_orphaned_reviews(tmp_path):
    """Reviews without corresponding runs are orphaned."""
    logs_dir = tmp_path / ".orchestrator" / "logs"
    reviews_dir = logs_dir / "reviews"
    runs_dir = logs_dir / "runs"
    reviews_dir.mkdir(parents=True)
    runs_dir.mkdir(parents=True)

    (reviews_dir / "orphan-review.json").write_text('{"verdict": "pass"}')

    result = scan_leaked_resources()
    assert len(result["orphaned_reviews"]) == 1


def test_scan_leaked_resources_valid_pair_not_orphaned(tmp_path):
    """Review with matching run is not orphaned."""
    logs_dir = tmp_path / ".orchestrator" / "logs"
    reviews_dir = logs_dir / "reviews"
    runs_dir = logs_dir / "runs"
    reviews_dir.mkdir(parents=True)
    runs_dir.mkdir(parents=True)

    run_id = "run-123"
    (runs_dir / f"{run_id}.json").write_text('{"status": "completed"}')
    (reviews_dir / f"{run_id}.json").write_text('{"verdict": "pass"}')

    result = scan_leaked_resources()
    assert len(result["orphaned_reviews"]) == 0


# --- Workspace Cleanup ---

def test_cleanup_workspace_archive(tmp_path):
    """Workspace is archived to tar.gz."""
    ws_dir = tmp_path / "workspaces" / "77"
    ws_dir.mkdir(parents=True)
    (ws_dir / "file.txt").write_text("content")

    original = gc_mod.WORKSPACES_DIR
    gc_mod.WORKSPACES_DIR = tmp_path / "workspaces"

    try:
        result = cleanup_workspace(str(ws_dir), mode="archive")
        assert result["action"] == "archived"
        assert "archive_path" in result
        assert not ws_dir.exists()
        assert Path(result["archive_path"]).exists()
    finally:
        gc_mod.WORKSPACES_DIR = original


def test_cleanup_workspace_delete(tmp_path):
    """Workspace is deleted."""
    ws_dir = tmp_path / "workspaces" / "88"
    ws_dir.mkdir(parents=True)
    (ws_dir / "file.txt").write_text("content")

    result = cleanup_workspace(str(ws_dir), mode="delete")
    assert result["action"] == "deleted"
    assert not ws_dir.exists()


def test_cleanup_workspace_dry_run(tmp_path):
    """Dry run doesn't delete anything."""
    ws_dir = tmp_path / "workspaces" / "99"
    ws_dir.mkdir(parents=True)
    (ws_dir / "file.txt").write_text("content")

    result = cleanup_workspace(str(ws_dir), mode="dry_run")
    assert result["action"] == "would_cleanup"
    assert ws_dir.exists()


def test_cleanup_workspace_not_found():
    """Non-existent workspace returns error."""
    result = cleanup_workspace("/nonexistent/path/123", mode="archive")
    assert "error" in result


# --- Convention Scanner ---

def test_scan_conventions_missing_dir():
    """Missing directory returns error."""
    result = scan_conventions("/nonexistent/project")
    assert "error" in result


def test_scan_conventions_clean(tmp_path):
    """Clean Python files have no issues."""
    (tmp_path / "clean.py").write_text('''
def hello():
    """Say hello."""
    return "hello"

class Greeter:
    """A friendly greeter."""

    def greet(self):
        """Greet someone."""
        pass
''')

    result = scan_conventions(str(tmp_path))
    assert result["files_scanned"] == 1
    assert result["total_issues"] == 0


def test_scan_conventions_missing_docstrings(tmp_path):
    """Public functions without docstrings are flagged."""
    (tmp_path / "sloppy.py").write_text('''
def public_func():
    return 42

class PublicClass:
    def method(self):
        pass
''')

    result = scan_conventions(str(tmp_path))
    assert result["total_issues"] == 3
    missing = [i for i in result["issues"] if i["issue_type"] == "missing_docstring"]
    assert len(missing) == 3


def test_scan_conventions_private_ignored(tmp_path):
    """Private functions/classes are not flagged."""
    (tmp_path / "private.py").write_text('''
def _internal():
    return 1

class _Helper:
    def _secret(self):
        pass
''')

    result = scan_conventions(str(tmp_path))
    missing = [i for i in result["issues"] if i["issue_type"] == "missing_docstring"]
    assert len(missing) == 0


def test_scan_conventions_todo_markers(tmp_path):
    """TODO/FIXME markers are detected."""
    (tmp_path / "todo_file.py").write_text('''
def func():
    """Has a docstring."""
    # TODO: implement this
    # FIXME: this is broken
    return None
''')

    result = scan_conventions(str(tmp_path))
    todos = [i for i in result["issues"] if i["issue_type"] == "todo"]
    fixes = [i for i in result["issues"] if i["issue_type"] == "fixme"]
    assert len(todos) == 1
    assert len(fixes) == 1


def test_scan_conventions_skips_tests(tmp_path):
    """Test files are skipped."""
    (tmp_path / "test_stuff.py").write_text('''
def no_docstring():
    return 1
''')

    result = scan_conventions(str(tmp_path))
    assert result["files_scanned"] == 0


def test_scan_conventions_skips_venv(tmp_path):
    """venv directories are skipped."""
    venv = tmp_path / "venv" / "lib" / "site.py"
    venv.parent.mkdir(parents=True)
    venv.write_text('def no_doc(): pass')

    result = scan_conventions(str(tmp_path))
    assert result["files_scanned"] == 0


# --- Full GC Run ---

def test_run_gc_dry_run(tmp_path):
    """Dry run GC scans but doesn't clean."""
    ws_dir = tmp_path / "workspaces" / "100"
    ws_dir.mkdir(parents=True)
    (ws_dir / "meta.json").write_text('{"issue_number": 100, "status": "completed"}')
    old_file = ws_dir / "old.txt"
    old_file.write_text("old")
    old_time = time.time() - 200 * 3600
    for f in ws_dir.rglob("*"):
        if f.is_file():
            os.utime(f, (old_time, old_time))

    result = run_gc(dry_run=True, max_age_hours=72)

    assert result["dry_run"] is True
    assert len(result["stale_workspaces"]) == 1
    assert len(result["cleaned"]) == 0
    assert result["bytes_freed"] == 0


def test_run_gc_actual_cleanup(tmp_path):
    """Non-dry-run GC cleans stale workspaces."""
    original = gc_mod.WORKSPACES_DIR
    gc_mod.WORKSPACES_DIR = tmp_path / "workspaces"

    try:
        ws_dir = tmp_path / "workspaces" / "101"
        ws_dir.mkdir(parents=True)
        (ws_dir / "meta.json").write_text('{"issue_number": 101, "status": "completed"}')
        old_file = ws_dir / "old.txt"
        old_file.write_text("stale data here")
        old_time = time.time() - 200 * 3600
        for f in ws_dir.rglob("*"):
            if f.is_file():
                os.utime(f, (old_time, old_time))

        result = run_gc(dry_run=False, max_age_hours=72)

        assert result["dry_run"] is False
        assert len(result["stale_workspaces"]) == 1
        assert len(result["cleaned"]) == 1
        assert result["cleaned"][0]["action"] == "archived"
        assert result["bytes_freed"] > 0
        assert not ws_dir.exists()
    finally:
        gc_mod.WORKSPACES_DIR = original


def test_run_gc_saves_report(tmp_path):
    """GC run saves a report file."""
    run_gc(dry_run=True)

    reports = list((tmp_path / ".orchestrator" / "logs" / "gc").glob("*.json"))
    assert len(reports) == 1
    report = json.loads(reports[0].read_text())
    assert "timestamp" in report
    assert "stale_workspaces" in report


# --- GC Pipeline YAML ---

def test_gc_pipeline_loads():
    """GC pipeline YAML is valid and loadable."""
    from dag import load_pipeline
    pipeline = load_pipeline(str(Path(__file__).parent / "pipelines" / "gc-pipeline.yaml"))

    assert pipeline.name == "gc-pipeline"
    assert "implement" in pipeline.nodes
    assert "gc_scan" in pipeline.nodes
    assert "convention_check" in pipeline.nodes

    gc_node = pipeline.nodes["gc_scan"]
    assert "test" in gc_node.depends_on
