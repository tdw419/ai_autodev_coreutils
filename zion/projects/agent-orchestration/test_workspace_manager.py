#!/usr/bin/env python3
"""Tests for Phase 11: Workspace Lifecycle Management."""

import json
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

from workspace_manager import (
    WorkspaceStatus,
    VALID_TRANSITIONS,
    ACTIVE_STATUSES,
    create_workspace,
    transition_workspace,
    get_workspace_status,
    list_workspaces,
    expire_workspaces,
    get_report,
    WORKSPACES_DIR,
)


@pytest.fixture(autouse=True)
def setup_dirs(tmp_path, monkeypatch):
    """Redirect workspace directory to tmp_path."""
    monkeypatch.setattr("workspace_manager.WORKSPACES_DIR", tmp_path / "workspaces")


# --- WorkspaceStatus Enum ---

def test_status_values():
    """All expected statuses exist."""
    expected = {"created", "claimed", "in-progress", "completed", "merged", "failed", "abandoned", "archived"}
    actual = set(WorkspaceStatus.values())
    assert actual == expected


def test_valid_transitions_completeness():
    """Every status has an entry in VALID_TRANSITIONS."""
    for status in WorkspaceStatus:
        assert status in VALID_TRANSITIONS, f"Missing transition for {status.value}"


def test_terminal_state():
    """Archived is a terminal state with no transitions."""
    assert VALID_TRANSITIONS[WorkspaceStatus.ARCHIVED] == []


def test_active_statuses():
    """Active statuses exclude completed/merged/failed/abandoned/archived."""
    for s in ACTIVE_STATUSES:
        assert s in {WorkspaceStatus.CREATED, WorkspaceStatus.CLAIMED, WorkspaceStatus.IN_PROGRESS}


# --- Create Workspace ---

def test_create_workspace(tmp_path):
    """Workspace is created with correct metadata."""
    meta = create_workspace(42, title="Fix login bug")

    assert meta["issue_number"] == 42
    assert meta["title"] == "Fix login bug"
    assert meta["status"] == "created"
    assert meta["attempts"] == 0
    assert meta["created_at"] is not None

    # File exists
    ws_dir = tmp_path / "workspaces" / "42"
    assert ws_dir.exists()
    meta_file = ws_dir / "meta.json"
    assert meta_file.exists()
    stored = json.loads(meta_file.read_text())
    assert stored["issue_number"] == 42


def test_create_workspace_duplicate(tmp_path):
    """Creating a duplicate workspace returns error."""
    create_workspace(42, title="First")
    result = create_workspace(42, title="Second")

    assert "error" in result
    assert "already exists" in result["error"]


def test_create_workspace_with_labels():
    """Labels are stored in metadata."""
    meta = create_workspace(10, title="Test", labels=["bug", "p1"])
    assert meta["labels"] == ["bug", "p1"]


# --- State Transitions ---

def test_transition_created_to_claimed(tmp_path):
    """created -> claimed is valid."""
    create_workspace(1)
    result = transition_workspace(1, "claimed")

    assert result["status"] == "claimed"
    assert result["claimed_at"] is not None


def test_transition_claimed_to_in_progress(tmp_path):
    """claimed -> in-progress increments attempts."""
    create_workspace(2)
    transition_workspace(2, "claimed")
    result = transition_workspace(2, "in-progress")

    assert result["status"] == "in-progress"
    assert result["attempts"] == 1


def test_transition_failed_to_in_progress_retries(tmp_path):
    """failed -> in-progress does NOT increment attempts (retry)."""
    create_workspace(3)
    transition_workspace(3, "claimed")
    transition_workspace(3, "in-progress")
    transition_workspace(3, "failed", note="tests failed")
    result = transition_workspace(3, "in-progress")

    assert result["status"] == "in-progress"
    assert result["attempts"] == 1  # Not incremented on retry
    assert "fail_note" not in result


def test_transition_in_progress_to_completed(tmp_path):
    """in-progress -> completed sets completed_at."""
    create_workspace(4)
    transition_workspace(4, "claimed")
    transition_workspace(4, "in-progress")
    result = transition_workspace(4, "completed")

    assert result["status"] == "completed"
    assert result["completed_at"] is not None


def test_transition_completed_to_merged(tmp_path):
    """completed -> merged sets merged_at."""
    create_workspace(5)
    transition_workspace(5, "claimed")
    transition_workspace(5, "in-progress")
    transition_workspace(5, "completed")
    result = transition_workspace(5, "merged")

    assert result["status"] == "merged"
    assert result["merged_at"] is not None


def test_transition_invalid(tmp_path):
    """Invalid transition returns error."""
    create_workspace(6)
    result = transition_workspace(6, "completed")

    assert "error" in result
    assert "Invalid transition" in result["error"]


def test_transition_from_terminal(tmp_path):
    """Cannot transition from archived."""
    create_workspace(7)
    transition_workspace(7, "claimed")
    transition_workspace(7, "in-progress")
    transition_workspace(7, "completed")
    transition_workspace(7, "merged")
    transition_workspace(7, "archived")
    result = transition_workspace(7, "in-progress")

    assert "error" in result
    assert VALID_TRANSITIONS[WorkspaceStatus.ARCHIVED] == []


def test_transition_not_found():
    """Transition on non-existent workspace returns error."""
    result = transition_workspace(999, "claimed")
    assert "error" in result
    assert "No workspace found" in result["error"]


def test_transition_with_run_id(tmp_path):
    """Transition stores run_id."""
    create_workspace(8)
    transition_workspace(8, "claimed")
    transition_workspace(8, "in-progress")
    result = transition_workspace(8, "completed", run_id="run-abc-123")

    assert result["last_run_id"] == "run-abc-123"


def test_transition_failed_stores_note(tmp_path):
    """Failed transition stores fail_note."""
    create_workspace(9)
    transition_workspace(9, "claimed")
    transition_workspace(9, "in-progress")
    result = transition_workspace(9, "failed", note="Tests timed out")

    assert result["status"] == "failed"
    assert result["fail_note"] == "Tests timed out"


def test_transition_recovering_clears_fail_note(tmp_path):
    """Recovering from failure clears fail_note."""
    create_workspace(10)
    transition_workspace(10, "claimed")
    transition_workspace(10, "in-progress")
    transition_workspace(10, "failed", note="broken")
    result = transition_workspace(10, "in-progress")

    assert "fail_note" not in result


# --- Get Status ---

def test_get_status(tmp_path):
    """get_workspace_status returns enriched metadata."""
    create_workspace(11, title="Status test")
    ws_dir = tmp_path / "workspaces" / "11"
    (ws_dir / "code.py").write_text("print('hello')")

    result = get_workspace_status(11)

    assert result is not None
    assert result["issue_number"] == 11
    assert result["file_count"] == 2  # meta.json + code.py
    assert result["size_bytes"] > 0
    assert result["age_hours"] is not None
    assert result["valid_transitions"] == ["claimed", "abandoned"]


def test_get_status_not_found():
    """Non-existent workspace returns None."""
    result = get_workspace_status(999)
    assert result is None


# --- List Workspaces ---

def test_list_all(tmp_path):
    """List returns all workspaces."""
    create_workspace(1, title="First")
    create_workspace(2, title="Second")
    create_workspace(3, title="Third")

    result = list_workspaces()
    assert len(result) == 3


def test_list_filter_by_status(tmp_path):
    """List can filter by status."""
    create_workspace(1)
    create_workspace(2)
    transition_workspace(2, "claimed")

    result = list_workspaces(status="created")
    assert len(result) == 1
    assert result[0]["issue_number"] == 1

    result = list_workspaces(status="claimed")
    assert len(result) == 1
    assert result[0]["issue_number"] == 2


def test_list_empty(tmp_path):
    """Empty directory returns empty list."""
    result = list_workspaces()
    assert result == []


# --- Expiration ---

def test_expire_dry_run(tmp_path, monkeypatch):
    """Dry run finds expired workspaces but doesn't change them."""
    # Create a workspace and backdate it
    create_workspace(50, title="Old task")
    meta = json.loads((tmp_path / "workspaces" / "50" / "meta.json").read_text())
    old_time = time.time() - 200 * 3600
    meta["created_at"] = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(old_time))
    (tmp_path / "workspaces" / "50" / "meta.json").write_text(json.dumps(meta))

    result = expire_workspaces(max_age_hours=168, dry_run=True)

    assert len(result) == 1
    assert result[0]["action"] == "would_abandon"
    assert result[0]["issue_number"] == 50

    # Status unchanged
    current = get_workspace_status(50)
    assert current["status"] == "created"


def test_expire_actual(tmp_path, monkeypatch):
    """Actual expiration transitions workspaces to abandoned."""
    create_workspace(51, title="Stale task")
    meta = json.loads((tmp_path / "workspaces" / "51" / "meta.json").read_text())
    old_time = time.time() - 200 * 3600
    meta["created_at"] = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(old_time))
    (tmp_path / "workspaces" / "51" / "meta.json").write_text(json.dumps(meta))

    result = expire_workspaces(max_age_hours=168, dry_run=False)

    assert len(result) == 1
    assert result[0]["action"] == "abandoned"

    current = get_workspace_status(51)
    assert current["status"] == "abandoned"


def test_expire_fresh_not_expired(tmp_path):
    """Fresh workspaces are not expired."""
    create_workspace(52, title="New task")

    result = expire_workspaces(max_age_hours=168, dry_run=True)
    assert len(result) == 0


def test_expire_completed_not_expired(tmp_path, monkeypatch):
    """Completed workspaces are not expired."""
    create_workspace(53)
    transition_workspace(53, "claimed")
    transition_workspace(53, "in-progress")
    transition_workspace(53, "completed")

    # Backdate it
    meta = json.loads((tmp_path / "workspaces" / "53" / "meta.json").read_text())
    old_time = time.time() - 200 * 3600
    meta["created_at"] = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(old_time))
    (tmp_path / "workspaces" / "53" / "meta.json").write_text(json.dumps(meta))

    result = expire_workspaces(max_age_hours=168, dry_run=True)
    assert len(result) == 0  # Completed is not in ACTIVE_STATUSES


# --- Report ---

def test_report(tmp_path):
    """Report aggregates workspace statistics."""
    create_workspace(1)
    create_workspace(2)
    transition_workspace(2, "claimed")
    create_workspace(3)
    transition_workspace(3, "claimed")
    transition_workspace(3, "in-progress")
    transition_workspace(3, "completed")

    report = get_report()

    assert report["total"] == 3
    assert report["by_status"]["created"] == 1
    assert report["by_status"]["claimed"] == 1
    assert report["by_status"]["completed"] == 1
    assert report["active"] == 2  # created + claimed
    assert report["completed"] == 1


def test_report_empty(tmp_path):
    """Empty workspace report."""
    report = get_report()
    assert report["total"] == 0
    assert report["active"] == 0


# --- Pipeline YAML ---

def test_workspace_lifecycle_pipeline_loads():
    """Workspace lifecycle pipeline YAML is valid."""
    from dag import load_pipeline
    pipeline = load_pipeline(str(Path(__file__).parent / "pipelines" / "workspace-lifecycle-pipeline.yaml"))

    assert pipeline.name == "workspace-lifecycle-pipeline"
    assert "setup" in pipeline.nodes
    assert "implement" in pipeline.nodes
    assert "review" in pipeline.nodes
    assert "complete" in pipeline.nodes

    # Dependencies
    assert "setup" in pipeline.nodes["implement"].depends_on
    assert "implement" in pipeline.nodes["review"].depends_on
    assert "review" in pipeline.nodes["complete"].depends_on
