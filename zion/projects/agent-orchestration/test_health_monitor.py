#!/usr/bin/env python3
"""Tests for Phase 14: Agent Health Monitoring (Deacon Pattern)."""

import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).parent))

from health_monitor import (
    check_stuck_workspaces,
    check_failed_workspaces,
    check_resource_usage,
    check_pipeline_health,
    generate_alerts,
    run_health_check,
    get_recent_reports,
    HEALTH_DIR,
    WORKSPACES_DIR,
    LOGS_DIR,
    PROJECT_DIR,
    ORCH_DIR,
)


@pytest.fixture(autouse=True)
def setup_dirs(tmp_path, monkeypatch):
    """Redirect all directories to tmp_path."""
    monkeypatch.setattr("health_monitor.WORKSPACES_DIR", tmp_path / "workspaces")
    monkeypatch.setattr("health_monitor.ORCH_DIR", tmp_path / ".orchestrator")
    monkeypatch.setattr("health_monitor.LOGS_DIR", tmp_path / ".orchestrator" / "logs")
    monkeypatch.setattr("health_monitor.HEALTH_DIR", tmp_path / ".orchestrator" / "logs" / "health")
    monkeypatch.setattr("health_monitor.PROJECT_DIR", tmp_path / "project")


def _make_workspace(tmp_path, issue, status="in-progress", attempts=1, updated_hours_ago=0):
    """Create a test workspace."""
    ws_dir = tmp_path / "workspaces" / str(issue)
    ws_dir.mkdir(parents=True)
    updated = datetime.now() - timedelta(hours=updated_hours_ago)
    meta = {
        "issue_number": issue,
        "title": f"Issue {issue}",
        "status": status,
        "attempts": attempts,
        "updated_at": updated.isoformat(),
    }
    (ws_dir / "meta.json").write_text(json.dumps(meta))
    return ws_dir


# --- Stuck Workspace Check ---

def test_check_stuck_none(tmp_path):
    """No workspaces returns empty."""
    assert check_stuck_workspaces() == []


def test_check_stuck_fresh(tmp_path):
    """Recent in-progress workspace is not stuck."""
    _make_workspace(tmp_path, 1, updated_hours_ago=1)
    assert check_stuck_workspaces(threshold_hours=4) == []


def test_check_stuck_old(tmp_path):
    """Old in-progress workspace is detected."""
    _make_workspace(tmp_path, 2, updated_hours_ago=10)
    result = check_stuck_workspaces(threshold_hours=4)
    assert len(result) == 1
    assert result[0]["issue_number"] == 2
    assert result[0]["stuck_hours"] > 4


def test_check_stuck_completed_not_flagged(tmp_path):
    """Completed workspace is not flagged as stuck."""
    _make_workspace(tmp_path, 3, status="completed", updated_hours_ago=100)
    assert check_stuck_workspaces(threshold_hours=4) == []


# --- Failed Workspace Check ---

def test_check_failed_none(tmp_path):
    assert check_failed_workspaces() == []


def test_check_failed_status(tmp_path):
    """Workspace with failed status is detected."""
    _make_workspace(tmp_path, 10, status="failed", attempts=2)
    result = check_failed_workspaces(max_failures=3)
    assert len(result) == 1
    assert result[0]["issue_number"] == 10


def test_check_failed_too_many_attempts(tmp_path):
    """Workspace with many attempts is detected even if not failed."""
    _make_workspace(tmp_path, 11, status="in-progress", attempts=5)
    result = check_failed_workspaces(max_failures=3)
    assert len(result) == 1


def test_check_failed_ok(tmp_path):
    """Workspace with few attempts is not flagged."""
    _make_workspace(tmp_path, 12, status="in-progress", attempts=1)
    assert check_failed_workspaces(max_failures=3) == []


# --- Resource Usage ---

def test_check_resource_usage_empty(tmp_path):
    """Empty state returns minimal info."""
    result = check_resource_usage()
    assert "active_workspaces" in result


def test_check_resource_usage_with_workspaces(tmp_path):
    """Resource usage counts workspaces correctly."""
    _make_workspace(tmp_path, 1, status="in-progress")
    _make_workspace(tmp_path, 2, status="completed")
    _make_workspace(tmp_path, 3, status="claimed")

    result = check_resource_usage()
    assert result["workspace_count"] == 3
    assert result["active_workspaces"] == 2  # in-progress + claimed


# --- Pipeline Health ---

def test_check_pipeline_health_no_runs(tmp_path):
    """No runs returns zeros."""
    result = check_pipeline_health()
    assert result["total_runs"] == 0
    assert result["success_rate"] == 0


def test_check_pipeline_health_with_runs(tmp_path):
    """Pipeline health computes success rate."""
    runs_dir = tmp_path / ".orchestrator" / "logs" / "runs"
    runs_dir.mkdir(parents=True)

    for i in range(8):
        run = {
            "run_id": f"run-{i}",
            "status": "completed" if i < 6 else "failed",
            "pipeline_name": "test",
            "duration_seconds": 5.0,
        }
        (runs_dir / f"run-{i}.json").write_text(json.dumps(run))

    result = check_pipeline_health()

    assert result["total_runs"] == 8
    assert result["completed"] == 6
    assert result["failed"] == 2
    assert result["success_rate"] == 0.75
    assert len(result["recent"]) == 8


# --- Alert Generation ---

def test_generate_alerts_healthy(tmp_path):
    """Healthy system has no alerts."""
    _make_workspace(tmp_path, 1, updated_hours_ago=1)
    alerts = generate_alerts()
    assert len(alerts) == 0


def test_generate_alerts_stuck(tmp_path):
    """Stuck workspace generates warning (not critical)."""
    _make_workspace(tmp_path, 1, updated_hours_ago=6)  # Between 4 and 8 (2x threshold)
    alerts = generate_alerts(stuck_threshold=4)
    stuck_alerts = [a for a in alerts if a["type"] == "stuck_workspace"]
    assert len(stuck_alerts) == 1
    assert stuck_alerts[0]["severity"] == "warning"


def test_generate_alerts_very_stuck_is_critical(tmp_path):
    """Very stuck workspace generates critical alert."""
    _make_workspace(tmp_path, 1, updated_hours_ago=20)
    alerts = generate_alerts(stuck_threshold=4)
    stuck_alerts = [a for a in alerts if a["type"] == "stuck_workspace"]
    assert len(stuck_alerts) == 1
    assert stuck_alerts[0]["severity"] == "critical"


def test_generate_alerts_failed(tmp_path):
    """Failed workspace generates warning."""
    _make_workspace(tmp_path, 1, status="failed", attempts=4)
    alerts = generate_alerts(max_failures=3)
    failed_alerts = [a for a in alerts if a["type"] == "failed_workspace"]
    assert len(failed_alerts) == 1


def test_generate_alerts_low_success_rate(tmp_path):
    """Low pipeline success rate generates warning."""
    runs_dir = tmp_path / ".orchestrator" / "logs" / "runs"
    runs_dir.mkdir(parents=True)
    for i in range(10):
        run = {
            "run_id": f"run-{i}",
            "status": "failed",
            "pipeline_name": "test",
            "duration_seconds": 5.0,
        }
        (runs_dir / f"run-{i}.json").write_text(json.dumps(run))

    alerts = generate_alerts(success_rate_floor=0.5)
    rate_alerts = [a for a in alerts if a["type"] == "low_success_rate"]
    assert len(rate_alerts) == 1
    assert rate_alerts[0]["severity"] == "warning"


# --- Full Health Check ---

def test_run_health_check_healthy(tmp_path):
    """Healthy system returns healthy status."""
    result = run_health_check()

    assert result["status"] == "healthy"
    assert result["alert_counts"]["critical"] == 0


def test_run_health_check_degraded(tmp_path):
    """Degraded system returns degraded status."""
    _make_workspace(tmp_path, 1, updated_hours_ago=20)
    result = run_health_check()

    assert result["status"] == "degraded"
    assert result["alert_counts"]["critical"] >= 1


def test_run_health_check_saves_report(tmp_path):
    """Health check saves a report file."""
    run_health_check()

    reports = list((tmp_path / ".orchestrator" / "logs" / "health").glob("*.json"))
    assert len(reports) == 1
    report = json.loads(reports[0].read_text())
    assert "timestamp" in report
    assert "status" in report


# --- Recent Reports ---

def test_get_recent_reports(tmp_path):
    """Recent reports are returned in order."""
    run_health_check()
    time.sleep(1.1)  # Ensure different filenames
    run_health_check()

    reports = get_recent_reports(count=5)
    assert len(reports) == 2


def test_get_recent_reports_empty(tmp_path):
    assert get_recent_reports() == []
