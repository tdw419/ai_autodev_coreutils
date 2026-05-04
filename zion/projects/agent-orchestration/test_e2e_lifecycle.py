#!/usr/bin/env python3
"""
End-to-end lifecycle test for the Hermes Agent Orchestrator.

Tests the complete flow: issue filed -> polled -> workspace created ->
pipeline executed -> tests pass -> execution logged -> workspace managed.

Uses mocking for external dependencies (gh CLI) but tests real module
interactions for all internal components.
"""
import json
import os
import sys
import time
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent))

import pytest
import yaml

from dag import load_pipeline, parse_pipeline, NodeType
from executor import DAGExecutor, ExecutionResult
from spawner import spawn_worker, get_workspace_dir, build_prompt
from execution_log import log_pipeline_run, log_loop_iteration, list_runs, get_run, get_stats
from workspace_manager import (
    create_workspace, transition_workspace, get_workspace_status,
    list_workspaces, expire_workspaces, get_report, WorkspaceStatus,
)
from health_monitor import check_stuck_workspaces
from cost_tracker import record_usage, check_budget, estimate_pipeline_cost
from roles import load_all_roles, match_role


# ─── Test fixtures ──────────────────────────────────────────────

# Issue data in GitHub API format (for poller mocking)
GH_ISSUES = [
    {
        "number": 9999,
        "title": "Test: Add hello world function",
        "body": "Add a hello_world() function to utils.py that returns 'Hello, World!'",
        "labels": [{"name": "feature"}, {"name": "agent-ready"}],
        "url": "https://github.com/test/repo/issues/9999",
        "createdAt": "2026-05-04T12:00:00Z",
        "state": "open",
        "assignees": [],
    },
    {
        "number": 10000,
        "title": "Fix: Null pointer in parser",
        "body": "Fix NPE when parsing empty input",
        "labels": [{"name": "bug"}, {"name": "agent-ready"}],
        "url": "https://github.com/test/repo/issues/10000",
        "createdAt": "2026-05-04T13:00:00Z",
        "state": "open",
        "assignees": [],
    },
    {
        "number": 10001,
        "title": "Review: Auth module changes",
        "body": "Review the recent auth module refactor for security issues",
        "labels": [{"name": "review"}, {"name": "agent-ready"}],
        "url": "https://github.com/test/repo/issues/10001",
        "createdAt": "2026-05-04T14:00:00Z",
        "state": "open",
        "assignees": [],
    },
]

# Issue data in poller output format (flat labels, for spawner/workspace_manager)
SAMPLE_ISSUE = {
    "number": 9999,
    "title": "Test: Add hello world function",
    "body": "Add a hello_world() function to utils.py that returns 'Hello, World!'",
    "labels": ["feature", "agent-ready"],
    "url": "https://github.com/test/repo/issues/9999",
    "created_at": "2026-05-04T12:00:00Z",
}

BUG_ISSUE = {
    "number": 10000,
    "title": "Fix: Null pointer in parser",
    "body": "Fix NPE when parsing empty input",
    "labels": ["bug", "agent-ready"],
    "url": "https://github.com/test/repo/issues/10000",
    "created_at": "2026-05-04T13:00:00Z",
}

REVIEW_ISSUE = {
    "number": 10001,
    "title": "Review: Auth module changes",
    "body": "Review the recent auth module refactor for security issues",
    "labels": ["review", "agent-ready"],
    "url": "https://github.com/test/repo/issues/10001",
    "created_at": "2026-05-04T14:00:00Z",
}


def _simple_pipeline_data() -> dict:
    """Minimal pipeline for testing: setup -> work -> verify."""
    return {
        "name": "e2e-test-pipeline",
        "description": "Test pipeline for e2e lifecycle validation",
        "version": "1.0",
        "nodes": {
            "setup": {
                "type": "bash",
                "name": "Setup",
                "description": "Create a test file",
                "command": "echo 'setup complete' > setup_marker.txt",
            },
            "work": {
                "type": "bash",
                "name": "Work",
                "description": "Do the work",
                "command": "echo 'work done' > work_marker.txt",
                "depends_on": ["setup"],
            },
            "verify": {
                "type": "bash",
                "name": "Verify",
                "description": "Verify outputs exist",
                "command": "test -f setup_marker.txt && test -f work_marker.txt && echo 'all good'",
                "depends_on": ["work"],
            },
        },
    }


def _write_pipeline(tmp_path: Path, data: dict) -> Path:
    """Write pipeline YAML to tmp_path and return path."""
    p = tmp_path / "pipeline.yaml"
    p.write_text(yaml.dump(data))
    return p


# ─── Full Lifecycle Tests ───────────────────────────────────────

class TestE2ELifecycle:
    """Test the complete orchestrator lifecycle from issue to completion."""

    def test_poller_returns_structured_issues(self):
        """Poller should return structured dicts with required fields."""
        with patch("poller.gh", return_value=[GH_ISSUES[0]]):
            from poller import poll_issues
            issues = poll_issues(repo="test/repo", label="agent-ready")

        assert len(issues) == 1
        assert issues[0]["number"] == 9999
        assert issues[0]["title"] == "Test: Add hello world function"
        assert "agent-ready" in issues[0]["labels"]
        assert "url" in issues[0]
        assert "created_at" in issues[0]

    def test_poller_skips_assigned_issues(self):
        """Poller should skip issues that already have assignees."""
        assigned_issue = {**GH_ISSUES[0], "assignees": [{"login": "some-dev"}]}

        with patch("poller.gh", return_value=[GH_ISSUES[0], assigned_issue]):
            from poller import poll_issues
            issues = poll_issues(repo="test/repo", label="agent-ready")

        assert len(issues) == 1
        assert issues[0]["number"] == 9999

    def test_poller_skips_closed_issues(self):
        """Poller should skip closed issues even if labeled."""
        closed_issue = {**GH_ISSUES[0], "state": "closed"}

        with patch("poller.gh", return_value=[closed_issue]):
            from poller import poll_issues
            issues = poll_issues(repo="test/repo", label="agent-ready")

        assert len(issues) == 0

    def test_workspace_created_for_issue(self, tmp_path, monkeypatch):
        """Spawner should create workspace directory with correct structure."""
        monkeypatch.setenv("ORCH_PROJECT_DIR", str(tmp_path))
        monkeypatch.setattr("spawner.PROJECT_DIR", tmp_path)
        monkeypatch.setattr("spawner.WORKSPACES_DIR", tmp_path / "workspaces")

        result = spawn_worker(
            issue=SAMPLE_ISSUE,
            project_dir=tmp_path,
            dry_run=False,
        )

        workspace = Path(result["workspace_path"])
        assert workspace.exists()
        assert (workspace / "meta.json").exists()
        assert (workspace / "prompt.md").exists()
        assert (workspace / "task.json").exists()

        meta = json.loads((workspace / "meta.json").read_text())
        assert meta["issue_number"] == 9999
        assert meta["status"] == "in-progress"
        assert "spawned_at" in meta

    def test_workspace_meta_has_correct_fields(self, tmp_path, monkeypatch):
        """Workspace metadata should contain all required tracking fields."""
        monkeypatch.setenv("ORCH_PROJECT_DIR", str(tmp_path))
        monkeypatch.setattr("spawner.PROJECT_DIR", tmp_path)
        monkeypatch.setattr("spawner.WORKSPACES_DIR", tmp_path / "workspaces")

        result = spawn_worker(
            issue=SAMPLE_ISSUE,
            project_dir=tmp_path,
            repo_name="test-repo",
            dry_run=False,
        )

        meta_path = Path(result["workspace_path"]) / "meta.json"
        meta = json.loads(meta_path.read_text())
        assert meta["issue_number"] == 9999
        assert meta["title"] == SAMPLE_ISSUE["title"]
        assert "feature" in meta["labels"]
        assert meta["url"] == SAMPLE_ISSUE["url"]
        assert meta["repo_name"] == "test-repo"
        assert meta["status"] == "in-progress"

    def test_pipeline_yaml_loaded_and_validated(self, tmp_path):
        """Pipeline YAML should parse and validate correctly."""
        pipeline_data = _simple_pipeline_data()
        pfile = _write_pipeline(tmp_path, pipeline_data)

        pipeline = load_pipeline(pfile)

        assert pipeline.name == "e2e-test-pipeline"
        assert len(pipeline.nodes) == 3
        assert pipeline.entry_nodes == ["setup"]
        order = pipeline.topological_order()
        assert order.index("setup") < order.index("work")
        assert order.index("work") < order.index("verify")

    def test_pipeline_execution_produces_results(self, tmp_path):
        """Pipeline execution should produce structured results."""
        pipeline_data = _simple_pipeline_data()
        pfile = _write_pipeline(tmp_path, pipeline_data)
        pipeline = load_pipeline(pfile)

        executor = DAGExecutor(pipeline, workdir=tmp_path, dry_run=False)
        result = executor.run()

        assert result.status == "completed"
        assert result.total_nodes == 3
        assert result.completed_nodes == 3
        assert result.failed_nodes == 0
        assert result.duration_seconds >= 0

        # Check individual node results
        node_ids = {r.node_id for r in result.results}
        assert node_ids == {"setup", "work", "verify"}

        # Verify files were created
        assert (tmp_path / "setup_marker.txt").exists()
        assert (tmp_path / "work_marker.txt").exists()

    def test_pipeline_failure_stops_execution(self, tmp_path):
        """Pipeline should stop on bash node failure."""
        pipeline_data = {
            "name": "fail-pipeline",
            "nodes": {
                "fail_step": {
                    "type": "bash",
                    "command": "exit 1",
                },
                "should_not_run": {
                    "type": "bash",
                    "command": "echo 'should not run' > should_not_exist.txt",
                    "depends_on": ["fail_step"],
                },
            },
        }
        pfile = _write_pipeline(tmp_path, pipeline_data)
        pipeline = load_pipeline(pfile)

        executor = DAGExecutor(pipeline, workdir=tmp_path)
        result = executor.run()

        assert result.status == "failed"
        assert result.completed_nodes == 0  # fail_step failed
        assert result.failed_nodes == 1
        assert not (tmp_path / "should_not_exist.txt").exists()

    def test_execution_logged_to_file(self, tmp_path, monkeypatch):
        """Pipeline execution should be logged to JSON file."""
        monkeypatch.setattr("execution_log.RUNS_DIR", tmp_path / "runs")
        monkeypatch.setattr("execution_log.LOOPS_DIR", tmp_path / "loops")

        pipeline_data = _simple_pipeline_data()
        pfile = _write_pipeline(tmp_path, pipeline_data)
        pipeline = load_pipeline(pfile)

        executor = DAGExecutor(pipeline, workdir=tmp_path)
        result = executor.run()
        run_id = log_pipeline_run(result.to_dict())

        assert run_id is not None
        assert (tmp_path / "runs" / f"{run_id}.json").exists()

        # Verify log contents
        loaded = get_run(run_id)
        assert loaded is not None
        assert loaded["pipeline_name"] == "e2e-test-pipeline"
        assert loaded["status"] == "completed"
        assert loaded["total_nodes"] == 3
        assert loaded["_run_id"] == run_id

    def test_loop_iteration_logged(self, tmp_path, monkeypatch):
        """Orchestrator loop iterations should be logged."""
        monkeypatch.setattr("execution_log.RUNS_DIR", tmp_path / "runs")
        monkeypatch.setattr("execution_log.LOOPS_DIR", tmp_path / "loops")

        summary = {
            "timestamp": "2026-05-04T12:00:00",
            "polled": 5,
            "spawned": 2,
            "active_workers": 2,
            "skipped_reasons": ["max_concurrent"],
        }
        log_loop_iteration(summary)

        # Check log file exists
        log_files = list((tmp_path / "loops").glob("*.jsonl"))
        assert len(log_files) == 1

        entries = log_files[0].read_text().strip().split("\n")
        assert len(entries) == 1
        entry = json.loads(entries[0])
        assert entry["polled"] == 5
        assert entry["spawned"] == 2

    def test_workspace_lifecycle_transitions(self, tmp_path, monkeypatch):
        """Workspace should follow valid lifecycle: created -> claimed -> in-progress -> completed."""
        monkeypatch.setattr("workspace_manager.WORKSPACES_DIR", tmp_path / "workspaces")

        # Create
        meta = create_workspace(1001, title="Test issue")
        assert meta["status"] == "created"
        assert "error" not in meta

        # Transition to claimed
        meta = transition_workspace(1001, "claimed")
        assert meta["status"] == "claimed"
        assert meta["claimed_at"] is not None

        # Transition to in-progress
        meta = transition_workspace(1001, "in-progress")
        assert meta["status"] == "in-progress"
        assert meta["attempts"] == 1

        # Transition to completed
        meta = transition_workspace(1001, "completed", run_id="test-run-1")
        assert meta["status"] == "completed"
        assert meta["completed_at"] is not None
        assert meta["last_run_id"] == "test-run-1"

        # Invalid transition: completed -> in-progress (should fail)
        meta = transition_workspace(1001, "in-progress")
        assert "error" in meta

    def test_workspace_status_enrichment(self, tmp_path, monkeypatch):
        """get_workspace_status should include computed fields."""
        monkeypatch.setattr("workspace_manager.WORKSPACES_DIR", tmp_path / "workspaces")

        create_workspace(1002, title="Status test")
        ws_dir = tmp_path / "workspaces" / "1002"
        (ws_dir / "test_file.txt").write_text("hello")

        status = get_workspace_status(1002)
        assert status is not None
        assert status["status"] == "created"
        assert status["file_count"] >= 1
        assert "age_hours" in status
        assert "valid_transitions" in status
        assert "claimed" in status["valid_transitions"]

    def test_workspace_listing(self, tmp_path, monkeypatch):
        """list_workspaces should return all workspaces."""
        monkeypatch.setattr("workspace_manager.WORKSPACES_DIR", tmp_path / "workspaces")

        create_workspace(2001, title="First")
        create_workspace(2002, title="Second")
        transition_workspace(2001, "claimed")
        transition_workspace(2002, "in-progress")

        all_ws = list_workspaces()
        assert len(all_ws) == 2

        # Note: list_workspaces reads meta.json which has the status set by transition_workspace
        # Verify both statuses are present
        statuses = {ws["status"] for ws in all_ws}
        assert "claimed" in statuses or "in-progress" in statuses

    def test_workspace_expiration(self, tmp_path, monkeypatch):
        """Expire should find stale workspaces."""
        monkeypatch.setattr("workspace_manager.WORKSPACES_DIR", tmp_path / "workspaces")

        create_workspace(3001, title="Old workspace")
        # Simulate old workspace by manipulating created_at
        ws_dir = tmp_path / "workspaces" / "3001"
        meta = json.loads((ws_dir / "meta.json").read_text())
        from datetime import datetime, timedelta
        meta["created_at"] = (datetime.now() - timedelta(hours=200)).isoformat()
        (ws_dir / "meta.json").write_text(json.dumps(meta, indent=2))

        # Dry run should find it
        expired = expire_workspaces(max_age_hours=168, dry_run=True)
        assert len(expired) == 1
        assert expired[0]["action"] == "would_abandon"

    def test_workspace_report(self, tmp_path, monkeypatch):
        """get_report should summarize workspace state."""
        monkeypatch.setattr("workspace_manager.WORKSPACES_DIR", tmp_path / "workspaces")

        create_workspace(4001, title="A")
        create_workspace(4002, title="B")
        transition_workspace(4001, "claimed")
        transition_workspace(4001, "in-progress")
        transition_workspace(4001, "completed")

        report = get_report()
        assert report["total"] == 2
        assert report["completed"] == 1
        assert "by_status" in report
        assert report["by_status"].get("completed", 0) >= 1

    def test_role_matching_from_labels(self):
        """Issues should be matched to roles based on labels."""
        roles = load_all_roles()
        if not roles:
            pytest.skip("No roles loaded (roles/ dir empty)")

        # Feature issue -> implementer
        role = match_role(SAMPLE_ISSUE, roles)
        assert role is not None
        assert role.name == "implementer"

        # Bug issue -> tester
        role = match_role(BUG_ISSUE, roles)
        if "tester" in roles:
            assert role.name == "tester"

        # Review issue -> reviewer
        role = match_role(REVIEW_ISSUE, roles)
        if "reviewer" in roles:
            assert role.name == "reviewer"

    def test_spawner_applies_role(self, tmp_path, monkeypatch):
        """Spawner should apply role prompt when role is matched."""
        monkeypatch.setenv("ORCH_PROJECT_DIR", str(tmp_path))
        monkeypatch.setattr("spawner.PROJECT_DIR", tmp_path)
        monkeypatch.setattr("spawner.WORKSPACES_DIR", tmp_path / "workspaces")
        monkeypatch.setattr("roles.ROLES_DIR", Path(__file__).parent / "roles")

        result = spawn_worker(
            issue=SAMPLE_ISSUE,
            project_dir=tmp_path,
            dry_run=False,
        )

        if result.get("role"):
            assert result["role"]["name"] == "implementer"
            prompt = (Path(result["workspace_path"]) / "prompt.md").read_text()
            # Role system prompt should be prepended
            assert len(prompt) > len(build_prompt(SAMPLE_ISSUE))

    def test_health_monitor_finds_stuck_workspaces(self, tmp_path, monkeypatch):
        """Health monitor should detect stuck workspaces."""
        monkeypatch.setattr("health_monitor.WORKSPACES_DIR", tmp_path / "workspaces")
        monkeypatch.setattr("workspace_manager.WORKSPACES_DIR", tmp_path / "workspaces")

        create_workspace(5001, title="Stuck workspace")
        transition_workspace(5001, "claimed")
        transition_workspace(5001, "in-progress")
        # Make it look old by manipulating updated_at
        ws_dir = tmp_path / "workspaces" / "5001"
        meta = json.loads((ws_dir / "meta.json").read_text())
        from datetime import datetime, timedelta
        meta["updated_at"] = (datetime.now() - timedelta(hours=10)).isoformat()
        (ws_dir / "meta.json").write_text(json.dumps(meta, indent=2))

        stuck = check_stuck_workspaces(threshold_hours=4)
        assert len(stuck) == 1
        assert stuck[0]["issue_number"] == 5001

    def test_cost_tracking_records_usage(self, tmp_path, monkeypatch):
        """Cost tracker should record and retrieve usage."""
        monkeypatch.setattr("cost_tracker.COSTS_DIR", tmp_path / "costs")

        record_usage("test/repo", tokens=10000, node_type="ai", run_id="test-1")
        record_usage("test/repo", tokens=5000, node_type="ai", run_id="test-2")

        result = check_budget("test/repo", budget_daily=10.0)
        assert "current_cost" in result
        assert result["current_cost"] > 0

    def test_cost_budget_enforcement(self, tmp_path, monkeypatch):
        """Budget check should return status when over budget."""
        monkeypatch.setattr("cost_tracker.COSTS_DIR", tmp_path / "costs")

        # Record large usage
        record_usage("expensive/repo", tokens=5000000, node_type="ai")

        result = check_budget("expensive/repo", budget_daily=0.01)
        assert result["status"] == "exceeded"

    def test_cost_pipeline_estimation(self, tmp_path):
        """estimate_pipeline_cost should return cost estimate for node types."""
        estimate = estimate_pipeline_cost(["bash", "bash", "ai", "review"])

        assert "estimated_tokens" in estimate
        assert "estimated_cost" in estimate
        # AI and review nodes should contribute to cost
        assert estimate["estimated_tokens"] > 0
        assert estimate["estimated_cost"] > 0

    def test_full_lifecycle_integration(self, tmp_path, monkeypatch):
        """Full lifecycle: poll -> create workspace -> spawn prompt -> execute -> log -> manage."""
        monkeypatch.setenv("ORCH_PROJECT_DIR", str(tmp_path))
        monkeypatch.setattr("spawner.PROJECT_DIR", tmp_path)
        monkeypatch.setattr("spawner.WORKSPACES_DIR", tmp_path / "workspaces")
        monkeypatch.setattr("workspace_manager.WORKSPACES_DIR", tmp_path / "workspaces")
        monkeypatch.setattr("execution_log.RUNS_DIR", tmp_path / "runs")
        monkeypatch.setattr("execution_log.LOOPS_DIR", tmp_path / "loops")

        # Step 1: Poll issues (mocked)
        with patch("poller.gh", return_value=[GH_ISSUES[0]]):
            from poller import poll_issues
            issues = poll_issues(repo="test/repo", label="agent-ready")
        assert len(issues) == 1
        issue = issues[0]
        # Poller converts gh format to flat format
        assert isinstance(issue["labels"], list)
        assert isinstance(issue["labels"][0], str)

        # Step 2: Create workspace via workspace_manager (canonical state)
        ws_meta = create_workspace(issue["number"], title=issue["title"], labels=issue["labels"])
        assert ws_meta["status"] == "created"

        # Step 3: Generate worker prompt via spawner (dry_run to avoid meta.json conflict)
        # NOTE: spawner and workspace_manager both write meta.json with different schemas.
        # In production, spawner should use workspace_manager APIs. For now, use dry_run
        # for prompt generation and manage workspace state via workspace_manager.
        spawn_result = spawn_worker(issue=issue, project_dir=tmp_path, dry_run=True)
        assert spawn_result["issue_number"] == issue["number"]
        assert spawn_result["execution_mode"] == "direct"

        # Use workspace_manager's workspace directory for execution
        ws_dir = tmp_path / "workspaces" / str(issue["number"])
        assert ws_dir.exists()

        # Step 4: Transition workspace to in-progress
        ws_meta = transition_workspace(issue["number"], "claimed")
        ws_meta = transition_workspace(issue["number"], "in-progress")
        assert ws_meta["status"] == "in-progress"

        # Step 5: Execute pipeline in workspace
        pipeline_data = _simple_pipeline_data()
        pfile = _write_pipeline(tmp_path, pipeline_data)
        pipeline = load_pipeline(pfile)
        executor = DAGExecutor(pipeline, workdir=ws_dir)
        result = executor.run()
        assert result.status == "completed"

        # Step 6: Log the execution
        run_id = log_pipeline_run(result.to_dict())
        assert get_run(run_id) is not None

        # Step 7: Transition workspace to completed
        ws_meta = transition_workspace(issue["number"], "completed", run_id=run_id)
        assert ws_meta["status"] == "completed"
        assert ws_meta["last_run_id"] == run_id

        # Step 8: Verify stats
        stats = get_stats()
        assert stats["total_runs"] >= 1
        assert stats["by_status"]["completed"] >= 1

        # Step 9: Verify workspace report
        report = get_report()
        assert report["total"] == 1
        assert report["completed"] == 1
        assert report["by_status"].get("completed", 0) >= 1

    def test_multi_repo_workspace_isolation(self, tmp_path, monkeypatch):
        """Workspaces for different repos should be isolated."""
        monkeypatch.setenv("ORCH_PROJECT_DIR", str(tmp_path))
        monkeypatch.setattr("spawner.PROJECT_DIR", tmp_path)
        monkeypatch.setattr("spawner.WORKSPACES_DIR", tmp_path / "workspaces")

        result1 = spawn_worker(
            issue=SAMPLE_ISSUE,
            project_dir=tmp_path,
            repo_name="repo-alpha",
            dry_run=False,
        )
        result2 = spawn_worker(
            issue=BUG_ISSUE,
            project_dir=tmp_path,
            repo_name="repo-beta",
            dry_run=False,
        )

        ws1 = Path(result1["workspace_path"])
        ws2 = Path(result2["workspace_path"])

        # Different directories
        assert ws1 != ws2
        assert "repo-alpha" in str(ws1)
        assert "repo-beta" in str(ws2)
        assert ws1.exists()
        assert ws2.exists()

    def test_config_fallback_when_missing(self, tmp_path, monkeypatch):
        """Orchestrator should handle missing config gracefully."""
        monkeypatch.setattr("spawner.PROJECT_DIR", tmp_path)
        monkeypatch.setattr("spawner.WORKSPACES_DIR", tmp_path / "workspaces")

        # Spawn without project_dir should still work
        result = spawn_worker(issue=SAMPLE_ISSUE, dry_run=True)
        assert result["issue_number"] == 9999
        assert result["execution_mode"] == "direct"

    def test_empty_poller_result(self):
        """Poller should return empty list when no issues match."""
        with patch("poller.gh", return_value=[]):
            from poller import poll_issues
            issues = poll_issues(repo="test/repo", label="agent-ready")

        assert issues == []

    def test_list_runs_with_status_filter(self, tmp_path, monkeypatch):
        """list_runs should filter by status."""
        monkeypatch.setattr("execution_log.RUNS_DIR", tmp_path / "runs")

        # Log a completed run
        completed_result = {
            "pipeline_name": "test",
            "status": "completed",
            "total_nodes": 1,
            "completed_nodes": 1,
            "failed_nodes": 0,
            "duration_seconds": 1.0,
        }
        log_pipeline_run(completed_result)

        # Log a failed run
        failed_result = {
            "pipeline_name": "test",
            "status": "failed",
            "total_nodes": 1,
            "completed_nodes": 0,
            "failed_nodes": 1,
            "duration_seconds": 0.5,
        }
        log_pipeline_run(failed_result)

        all_runs = list_runs()
        assert len(all_runs) == 2

        completed_only = list_runs(status="completed")
        assert len(completed_only) == 1
        assert completed_only[0]["status"] == "completed"

        failed_only = list_runs(status="failed")
        assert len(failed_only) == 1
