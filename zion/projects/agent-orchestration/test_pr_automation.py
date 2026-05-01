#!/usr/bin/env python3
"""Tests for Phase 13: Pull Request Automation."""

import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).parent))

from pr_automation import (
    _run_gh,
    _read_workspace_meta,
    _get_branch_name,
    create_pr,
    list_prs,
    get_pr_status,
    merge_pr,
    close_pr,
    update_pr,
    WORKSPACES_DIR,
)


@pytest.fixture(autouse=True)
def setup_dirs(tmp_path, monkeypatch):
    """Redirect directories to tmp_path."""
    monkeypatch.setattr("pr_automation.WORKSPACES_DIR", tmp_path / "workspaces")


def _setup_workspace(tmp_path, issue=42, title="Fix bug", status="completed"):
    """Create a test workspace with meta.json."""
    ws_dir = tmp_path / "workspaces" / str(issue)
    ws_dir.mkdir(parents=True)
    meta = {
        "issue_number": issue,
        "title": title,
        "description": "This is a test issue",
        "status": status,
        "attempts": 1,
        "last_run_id": "run-abc",
    }
    (ws_dir / "meta.json").write_text(json.dumps(meta))
    return ws_dir


# --- Helper functions ---

def test_get_branch_name():
    assert _get_branch_name(42) == "issue-42"
    assert _get_branch_name("99") == "issue-99"


def test_read_workspace_meta(tmp_path):
    ws_dir = _setup_workspace(tmp_path)
    meta = _read_workspace_meta(42)
    assert meta is not None
    assert meta["title"] == "Fix bug"


def test_read_workspace_meta_not_found():
    assert _read_workspace_meta(999) is None


# --- gh CLI wrapper ---

@patch("pr_automation.subprocess.run")
def test_run_gh_success(mock_run):
    mock_run.return_value = MagicMock(
        returncode=0,
        stdout='{"number": 1}',
        stderr="",
    )
    result = _run_gh(["pr", "list"])
    assert result["exit_code"] == 0
    assert result["data"]["number"] == 1


@patch("pr_automation.subprocess.run")
def test_run_gh_json_parse_error(mock_run):
    mock_run.return_value = MagicMock(
        returncode=0,
        stdout="not json",
        stderr="",
    )
    result = _run_gh(["pr", "view"])
    assert result["exit_code"] == 0
    assert result["data"] is None
    assert result["stdout"] == "not json"


@patch("pr_automation.subprocess.run", side_effect=FileNotFoundError)
def test_run_gh_not_found(mock_run):
    result = _run_gh(["pr", "list"])
    assert result["exit_code"] == -1
    assert "not found" in result["stderr"]


@patch("pr_automation.subprocess.run", side_effect=subprocess.TimeoutExpired(cmd="gh", timeout=30))
def test_run_gh_timeout(mock_run):
    import subprocess
    result = _run_gh(["pr", "list"], timeout=5)
    assert result["exit_code"] == -1
    assert result["stderr"] == "timeout"


# --- PR Creation ---

@patch("pr_automation._run_gh")
def test_create_pr_success(mock_gh, tmp_path):
    _setup_workspace(tmp_path)

    # Default branch query
    mock_gh.side_effect = [
        {"exit_code": 0, "data": {"defaultBranchRef": {"name": "main"}}, "stdout": "", "stderr": ""},
        # Push branch (can fail, ignored)
        {"exit_code": 1, "data": None, "stdout": "", "stderr": "already exists"},
        # PR create
        {"exit_code": 0, "data": {"number": 123, "html_url": "https://github.com/owner/repo/pull/123"}, "stdout": "", "stderr": ""},
    ]

    result = create_pr(42, "owner/repo")

    assert result["pr_number"] == 123
    assert result["pr_url"] == "https://github.com/owner/repo/pull/123"
    assert result["status"] == "created"
    assert "Fix #42" in result["title"]

    # Meta should be updated with PR info
    meta = json.loads((tmp_path / "workspaces" / "42" / "meta.json").read_text())
    assert meta["pr_number"] == 123


@patch("pr_automation._run_gh")
def test_create_pr_custom_title_body(mock_gh, tmp_path):
    _setup_workspace(tmp_path)

    mock_gh.side_effect = [
        {"exit_code": 0, "data": {"defaultBranchRef": {"name": "main"}}, "stdout": "", "stderr": ""},
        {"exit_code": 1, "data": None, "stdout": "", "stderr": "already exists"},
        {"exit_code": 0, "data": {"number": 456, "html_url": "https://github.com/owner/repo/pull/456"}, "stdout": "", "stderr": ""},
    ]

    result = create_pr(42, "owner/repo", title="Custom Title", body="Custom Body")

    assert result["pr_number"] == 456
    # The custom title should be used
    assert result["title"] == "Custom Title"


@patch("pr_automation._run_gh")
def test_create_pr_draft(mock_gh, tmp_path):
    _setup_workspace(tmp_path)

    mock_gh.side_effect = [
        {"exit_code": 0, "data": {"defaultBranchRef": {"name": "main"}}, "stdout": "", "stderr": ""},
        {"exit_code": 1, "data": None, "stdout": "", "stderr": "already exists"},
        {"exit_code": 0, "data": {"number": 789, "html_url": "https://github.com/owner/repo/pull/789"}, "stdout": "", "stderr": ""},
    ]

    result = create_pr(42, "owner/repo", draft=True)
    assert result["pr_number"] == 789

    # Check that --draft was in the args (3rd call is pr create)
    create_call = mock_gh.call_args_list[2]
    assert "--draft" in create_call[0][0]


def test_create_pr_no_workspace():
    result = create_pr(999, "owner/repo")
    assert "error" in result


@patch("pr_automation._run_gh")
def test_create_pr_gh_failure(mock_gh, tmp_path):
    _setup_workspace(tmp_path)

    mock_gh.side_effect = [
        {"exit_code": 0, "data": {"defaultBranchRef": {"name": "main"}}, "stdout": "", "stderr": ""},
        {"exit_code": 1, "data": None, "stdout": "", "stderr": "already exists"},
        {"exit_code": 1, "data": None, "stdout": "", "stderr": "Branch not found"},
    ]

    result = create_pr(42, "owner/repo")
    assert "error" in result


# --- PR Listing ---

@patch("pr_automation._run_gh")
def test_list_prs(mock_gh):
    mock_gh.return_value = {
        "exit_code": 0,
        "data": [
            {"number": 1, "title": "First", "state": "OPEN"},
            {"number": 2, "title": "Second", "state": "OPEN"},
        ],
        "stdout": "", "stderr": "",
    }

    result = list_prs("owner/repo")
    assert len(result) == 2
    assert result[0]["number"] == 1


@patch("pr_automation._run_gh")
def test_list_prs_empty(mock_gh):
    mock_gh.return_value = {"exit_code": 0, "data": [], "stdout": "", "stderr": ""}
    result = list_prs("owner/repo")
    assert result == []


@patch("pr_automation._run_gh")
def test_list_prs_error(mock_gh):
    mock_gh.return_value = {"exit_code": 1, "data": None, "stdout": "", "stderr": "auth error"}
    result = list_prs("owner/repo")
    assert result == []


# --- PR Status ---

@patch("pr_automation._run_gh")
def test_get_pr_status_ready(mock_gh):
    mock_gh.return_value = {
        "exit_code": 0,
        "data": {
            "number": 42,
            "title": "Fix bug",
            "state": "OPEN",
            "url": "https://github.com/owner/repo/pull/42",
            "mergeable": True,
            "reviewDecision": "APPROVED",
            "statusCheckRollup": [
                {"status": "COMPLETED", "conclusion": "SUCCESS"},
                {"status": "COMPLETED", "conclusion": "SUCCESS"},
            ],
            "labels": [{"name": "bug"}],
        },
        "stdout": "", "stderr": "",
    }

    result = get_pr_status("owner/repo", 42)

    assert result["number"] == 42
    assert result["mergeable"] is True
    assert result["review_decision"] == "APPROVED"
    assert result["checks"]["passing"] == 2
    assert result["checks"]["failing"] == 0
    assert result["ready_to_merge"] is True
    assert result["labels"] == ["bug"]


@patch("pr_automation._run_gh")
def test_get_pr_status_not_ready(mock_gh):
    mock_gh.return_value = {
        "exit_code": 0,
        "data": {
            "number": 43,
            "title": "WIP",
            "state": "OPEN",
            "url": "https://github.com/owner/repo/pull/43",
            "mergeable": False,
            "reviewDecision": "PENDING",
            "statusCheckRollup": [
                {"status": "IN_PROGRESS"},
                {"status": "COMPLETED", "conclusion": "FAILURE"},
            ],
            "labels": [],
        },
        "stdout": "", "stderr": "",
    }

    result = get_pr_status("owner/repo", 43)

    assert result["ready_to_merge"] is False
    assert result["checks"]["failing"] == 1
    assert result["checks"]["pending"] == 1


@patch("pr_automation._run_gh")
def test_get_pr_status_error(mock_gh):
    mock_gh.return_value = {"exit_code": 1, "data": None, "stdout": "", "stderr": "not found"}
    result = get_pr_status("owner/repo", 999)
    assert result is None


# --- PR Merge ---

@patch("workspace_manager.transition_workspace")
@patch("pr_automation._run_gh")
def test_merge_pr_success(mock_gh, mock_transition, tmp_path):
    _setup_workspace(tmp_path)

    mock_gh.side_effect = [
        # Merge command
        {"exit_code": 0, "data": None, "stdout": "Merged", "stderr": ""},
        # Get branch name
        {"exit_code": 0, "data": {"headRefName": "issue-42"}, "stdout": "", "stderr": ""},
    ]

    result = merge_pr("owner/repo", 42)

    assert result["status"] == "merged"
    mock_transition.assert_called_once_with("42", "merged")


@patch("pr_automation._run_gh")
def test_merge_pr_failure(mock_gh):
    mock_gh.return_value = {"exit_code": 1, "data": None, "stdout": "", "stderr": "merge conflict"}
    result = merge_pr("owner/repo", 42)
    assert "error" in result


# --- PR Close ---

@patch("pr_automation._run_gh")
def test_close_pr(mock_gh):
    mock_gh.return_value = {"exit_code": 0, "data": None, "stdout": "", "stderr": ""}
    result = close_pr("owner/repo", 42)
    assert result["status"] == "closed"


@patch("pr_automation._run_gh")
def test_close_pr_with_comment(mock_gh):
    mock_gh.return_value = {"exit_code": 0, "data": None, "stdout": "", "stderr": ""}
    result = close_pr("owner/repo", 42, comment="Closing due to inactivity")

    assert result["status"] == "closed"
    # Should have called gh twice: comment + close
    assert mock_gh.call_count == 2


@patch("pr_automation._run_gh")
def test_close_pr_failure(mock_gh):
    mock_gh.return_value = {"exit_code": 1, "data": None, "stdout": "", "stderr": "error"}
    result = close_pr("owner/repo", 42)
    assert "error" in result


# --- PR Update ---

@patch("pr_automation._run_gh")
def test_update_pr_title(mock_gh):
    mock_gh.return_value = {"exit_code": 0, "data": None, "stdout": "", "stderr": ""}
    result = update_pr("owner/repo", 42, title="New Title")
    assert result["status"] == "updated"

    call_args = mock_gh.call_args[0][0]
    assert "--title" in call_args
    assert "New Title" in call_args


@patch("pr_automation._run_gh")
def test_update_pr_labels(mock_gh):
    mock_gh.return_value = {"exit_code": 0, "data": None, "stdout": "", "stderr": ""}
    result = update_pr("owner/repo", 42, labels=["bug", "p1"])
    assert result["status"] == "updated"

    call_args = mock_gh.call_args[0][0]
    assert "--add-label" in call_args
    assert "bug,p1" in call_args
