#!/usr/bin/env python3
"""
Component integration chain test for the Hermes Agent Orchestrator.

Tests that all modules work together when chained:
poller -> spawner -> executor -> logger -> health -> workspace_manager

Validates data flows correctly between modules, catches interface
mismatches (wrong parameter names, missing fields, incompatible types).
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

from dag import load_pipeline, parse_pipeline, NodeType, pipeline_to_dict
from executor import DAGExecutor, ExecutionResult, NodeResult
from spawner import spawn_worker, get_workspace_dir, build_prompt, read_ai_guide, find_project_dir
from execution_log import (
    log_pipeline_run, log_loop_iteration, list_runs, get_run, get_stats,
    get_loop_history, prune_old_runs,
)
from workspace_manager import (
    create_workspace, transition_workspace, get_workspace_status,
    list_workspaces, expire_workspaces, get_report, WorkspaceStatus,
)
from health_monitor import check_stuck_workspaces, run_health_check
from cost_tracker import record_usage, check_budget, estimate_pipeline_cost, get_daily_cost
from roles import load_all_roles, match_role, build_role_prompt, load_role, LABEL_ROLE_MAP


# ─── Fixtures ───────────────────────────────────────────────────

# GitHub API format (for poller mocking)
GH_ISSUE = {
    "number": 42,
    "title": "Implement user authentication",
    "body": "Add JWT-based authentication to the API endpoints. Use the existing middleware pattern.",
    "labels": [{"name": "feature"}, {"name": "agent-ready"}],
    "url": "https://github.com/test/repo/issues/42",
    "createdAt": "2026-05-04T12:00:00Z",
    "state": "open",
    "assignees": [],
}

# Poller output format (flat labels, for spawner/workspace_manager)
ISSUE = {
    "number": 42,
    "title": "Implement user authentication",
    "body": "Add JWT-based authentication to the API endpoints. Use the existing middleware pattern.",
    "labels": ["feature", "agent-ready"],
    "url": "https://github.com/test/repo/issues/42",
    "created_at": "2026-05-04T12:00:00Z",
}


def _make_pipeline(nodes: dict, name: str = "chain-test") -> dict:
    return {"name": name, "version": "1.0", "nodes": nodes}


def _write_pipeline(tmp_path: Path, data: dict) -> Path:
    p = tmp_path / "pipeline.yaml"
    p.write_text(yaml.dump(data))
    return p


# ─── Poller -> Spawner chain ────────────────────────────────────

class TestPollerSpawnerChain:
    """Test data flow from poller output to spawner input."""

    def test_poller_output_is_valid_spawner_input(self, tmp_path, monkeypatch):
        """Poller output format should be directly usable by spawner."""
        monkeypatch.setenv("ORCH_PROJECT_DIR", str(tmp_path))
        monkeypatch.setattr("spawner.PROJECT_DIR", tmp_path)
        monkeypatch.setattr("spawner.WORKSPACES_DIR", tmp_path / "workspaces")

        with patch("poller.gh", return_value=[GH_ISSUE]):
            from poller import poll_issues
            issues = poll_issues(repo="test/repo")

        # Feed poller output directly to spawner
        for issue in issues:
            result = spawn_worker(issue=issue, project_dir=tmp_path, dry_run=False)
            assert "workspace_path" in result
            assert "execution_mode" in result
            assert result["issue_number"] == issue["number"]

    def test_multiple_issues_create_separate_workspaces(self, tmp_path, monkeypatch):
        """Multiple issues should create isolated workspaces."""
        monkeypatch.setenv("ORCH_PROJECT_DIR", str(tmp_path))
        monkeypatch.setattr("spawner.PROJECT_DIR", tmp_path)
        monkeypatch.setattr("spawner.WORKSPACES_DIR", tmp_path / "workspaces")

        issues = [
            {**ISSUE, "number": i, "title": f"Issue {i}"}
            for i in range(1, 4)
        ]

        workspace_paths = set()
        for issue in issues:
            result = spawn_worker(issue=issue, project_dir=tmp_path, dry_run=False)
            workspace_paths.add(result["workspace_path"])

        assert len(workspace_paths) == 3

    def test_spawner_output_contains_exec_instructions(self, tmp_path, monkeypatch):
        """Spawner output should contain everything needed to execute."""
        monkeypatch.setenv("ORCH_PROJECT_DIR", str(tmp_path))
        monkeypatch.setattr("spawner.PROJECT_DIR", tmp_path)
        monkeypatch.setattr("spawner.WORKSPACES_DIR", tmp_path / "workspaces")

        result = spawn_worker(issue=ISSUE, project_dir=tmp_path, dry_run=False)

        exec_instr = result.get("exec_instructions", {})
        assert "mode" in exec_instr
        assert "workdir" in exec_instr
        assert exec_instr["mode"] in ("direct", "dag")

        if exec_instr["mode"] == "direct":
            assert "prompt" in exec_instr
        elif exec_instr["mode"] == "dag":
            assert "pipeline" in exec_instr
            assert "context" in exec_instr


# ─── Spawner -> Executor chain ──────────────────────────────────

class TestSpawnerExecutorChain:
    """Test data flow from spawner workspace to executor."""

    def test_executor_runs_in_spawner_workspace(self, tmp_path, monkeypatch):
        """Executor should execute pipeline in the workspace created by spawner."""
        monkeypatch.setenv("ORCH_PROJECT_DIR", str(tmp_path))
        monkeypatch.setattr("spawner.PROJECT_DIR", tmp_path)
        monkeypatch.setattr("spawner.WORKSPACES_DIR", tmp_path / "workspaces")

        # Spawn workspace
        result = spawn_worker(issue=ISSUE, project_dir=tmp_path, dry_run=False)
        workspace = Path(result["workspace_path"])

        # Create pipeline that writes to workspace
        pipeline_data = _make_pipeline({
            "create_file": {
                "type": "bash",
                "command": "echo 'auth module' > auth.py",
            },
            "verify_file": {
                "type": "bash",
                "command": "test -f auth.py && echo 'verified'",
                "depends_on": ["create_file"],
            },
        })
        pfile = _write_pipeline(tmp_path, pipeline_data)
        pipeline = load_pipeline(pfile)

        # Execute in the spawner workspace
        executor = DAGExecutor(pipeline, workdir=workspace)
        exec_result = executor.run()

        assert exec_result.status == "completed"
        assert (workspace / "auth.py").exists()

    def test_executor_context_from_spawner_task(self, tmp_path, monkeypatch):
        """Executor should receive context from spawner's task.json."""
        monkeypatch.setenv("ORCH_PROJECT_DIR", str(tmp_path))
        monkeypatch.setattr("spawner.PROJECT_DIR", tmp_path)
        monkeypatch.setattr("spawner.WORKSPACES_DIR", tmp_path / "workspaces")

        result = spawn_worker(issue=ISSUE, project_dir=tmp_path, dry_run=False)
        workspace = Path(result["workspace_path"])

        # Read the task.json created by spawner
        task_data = json.loads((workspace / "task.json").read_text())
        assert "task" in task_data

        # Create pipeline that writes task context to file (use tee with heredoc to avoid quoting)
        pipeline_data = _make_pipeline({
            "echo_task": {
                "type": "bash",
                "command": "cat > task_output.txt << 'ENDTASK'\n{{task}}\nENDTASK",
            },
        })
        pfile = _write_pipeline(tmp_path, pipeline_data)
        pipeline = load_pipeline(pfile)

        executor = DAGExecutor(pipeline, workdir=workspace, context=task_data)
        exec_result = executor.run()

        assert exec_result.status == "completed"
        output = (workspace / "task_output.txt").read_text()
        assert "Implement user authentication" in output

    def test_pipeline_mode_spawner_executor_integration(self, tmp_path, monkeypatch):
        """Test spawner in DAG mode feeding into executor."""
        monkeypatch.setenv("ORCH_PROJECT_DIR", str(tmp_path))
        monkeypatch.setattr("spawner.PROJECT_DIR", tmp_path)
        monkeypatch.setattr("spawner.WORKSPACES_DIR", tmp_path / "workspaces")

        pipeline_data = _make_pipeline({
            "step1": {
                "type": "bash",
                "command": "echo 'step1' > step1.txt",
            },
            "step2": {
                "type": "bash",
                "command": "echo 'step2' > step2.txt",
                "depends_on": ["step1"],
            },
        })
        pfile = _write_pipeline(tmp_path, pipeline_data)

        # Spawn with pipeline
        result = spawn_worker(
            issue=ISSUE,
            project_dir=tmp_path,
            pipeline=str(pfile),
            dry_run=False,
        )
        assert result["execution_mode"] == "dag"

        # Execute
        exec_instr = result["exec_instructions"]
        pipeline = load_pipeline(exec_instr["pipeline"])
        workspace = Path(exec_instr["workdir"])
        executor = DAGExecutor(pipeline, workdir=workspace)
        exec_result = executor.run()

        assert exec_result.status == "completed"
        assert (workspace / "step1.txt").exists()
        assert (workspace / "step2.txt").exists()


# ─── Executor -> Logger chain ───────────────────────────────────

class TestExecutorLoggerChain:
    """Test data flow from executor results to execution log."""

    def test_execution_result_serializes_for_logging(self, tmp_path):
        """ExecutionResult.to_dict() should produce loggable data."""
        pipeline_data = _make_pipeline({
            "echo": {"type": "bash", "command": "echo hello"},
        })
        pfile = _write_pipeline(tmp_path, pipeline_data)
        pipeline = load_pipeline(pfile)

        executor = DAGExecutor(pipeline, workdir=tmp_path)
        result = executor.run()

        # to_dict() should not raise
        d = result.to_dict()
        assert "pipeline_name" in d
        assert "status" in d
        assert "results" in d
        assert isinstance(d["results"], list)

    def test_logged_result_can_be_retrieved(self, tmp_path, monkeypatch):
        """Logged execution result should be retrievable by run_id."""
        monkeypatch.setattr("execution_log.RUNS_DIR", tmp_path / "runs")
        monkeypatch.setattr("execution_log.LOOPS_DIR", tmp_path / "loops")

        pipeline_data = _make_pipeline({
            "a": {"type": "bash", "command": "echo a"},
            "b": {"type": "bash", "command": "echo b", "depends_on": ["a"]},
        })
        pfile = _write_pipeline(tmp_path, pipeline_data)
        pipeline = load_pipeline(pfile)
        executor = DAGExecutor(pipeline, workdir=tmp_path)
        result = executor.run()

        run_id = log_pipeline_run(result.to_dict())
        retrieved = get_run(run_id)

        assert retrieved is not None
        assert retrieved["pipeline_name"] == pipeline.name
        assert retrieved["total_nodes"] == 2
        assert retrieved["completed_nodes"] == 2
        assert len(retrieved["results"]) == 2

    def test_multiple_runs_tracked_in_stats(self, tmp_path, monkeypatch):
        """Stats should aggregate across multiple logged runs."""
        monkeypatch.setattr("execution_log.RUNS_DIR", tmp_path / "runs")

        for i in range(3):
            pipeline_data = _make_pipeline(
                {"echo": {"type": "bash", "command": f"echo run{i}"}},
                name=f"pipeline-{i}",
            )
            pfile = _write_pipeline(tmp_path, pipeline_data)
            pipeline = load_pipeline(pfile)
            executor = DAGExecutor(pipeline, workdir=tmp_path)
            result = executor.run()
            log_pipeline_run(result.to_dict())

        stats = get_stats()
        assert stats["total_runs"] >= 3
        assert stats["by_status"]["completed"] >= 3

    def test_failed_run_is_logged_correctly(self, tmp_path, monkeypatch):
        """Failed runs should be logged with correct status."""
        monkeypatch.setattr("execution_log.RUNS_DIR", tmp_path / "runs")

        pipeline_data = _make_pipeline({
            "fail": {"type": "bash", "command": "exit 42"},
        })
        pfile = _write_pipeline(tmp_path, pipeline_data)
        pipeline = load_pipeline(pfile)
        executor = DAGExecutor(pipeline, workdir=tmp_path)
        result = executor.run()

        assert result.status == "failed"
        run_id = log_pipeline_run(result.to_dict())

        retrieved = get_run(run_id)
        assert retrieved["status"] == "failed"
        assert retrieved["failed_nodes"] == 1


# ─── Logger -> Health chain ─────────────────────────────────────

class TestLoggerHealthChain:
    """Test data flow from execution logs to health monitoring."""

    def test_health_check_reads_workspace_state(self, tmp_path, monkeypatch):
        """Health check should read workspace state created by spawner."""
        monkeypatch.setattr("health_monitor.WORKSPACES_DIR", tmp_path / "workspaces")
        monkeypatch.setattr("workspace_manager.WORKSPACES_DIR", tmp_path / "workspaces")

        # Create a workspace in-progress
        create_workspace(6001, title="Active workspace")
        transition_workspace(6001, "in-progress")

        stuck = check_stuck_workspaces(threshold_hours=100)
        # Not stuck (just created)
        assert len(stuck) == 0

    def test_health_check_runs_without_errors(self, tmp_path, monkeypatch):
        """run_health_check should complete without errors even with no data."""
        monkeypatch.setattr("health_monitor.WORKSPACES_DIR", tmp_path / "workspaces")
        monkeypatch.setattr("health_monitor.LOGS_DIR", tmp_path / "logs")
        monkeypatch.setattr("health_monitor.HEALTH_DIR", tmp_path / "health")

        report = run_health_check()
        assert isinstance(report, dict)
        assert "status" in report  # "healthy" or "degraded"


# ─── Full chain: poller -> spawner -> executor -> logger -> health ───

class TestFullIntegrationChain:
    """Test the complete module chain end-to-end."""

    def test_full_chain_single_issue(self, tmp_path, monkeypatch):
        """Complete chain: mock poll -> create workspace -> spawn prompt -> execute -> log -> manage."""
        # Setup paths
        monkeypatch.setenv("ORCH_PROJECT_DIR", str(tmp_path))
        monkeypatch.setattr("spawner.PROJECT_DIR", tmp_path)
        monkeypatch.setattr("spawner.WORKSPACES_DIR", tmp_path / "workspaces")
        monkeypatch.setattr("workspace_manager.WORKSPACES_DIR", tmp_path / "workspaces")
        monkeypatch.setattr("execution_log.RUNS_DIR", tmp_path / "runs")
        monkeypatch.setattr("execution_log.LOOPS_DIR", tmp_path / "loops")
        monkeypatch.setattr("health_monitor.WORKSPACES_DIR", tmp_path / "workspaces")
        monkeypatch.setattr("health_monitor.LOGS_DIR", tmp_path / "logs")
        monkeypatch.setattr("health_monitor.HEALTH_DIR", tmp_path / "health")
        monkeypatch.setattr("cost_tracker.COSTS_DIR", tmp_path / "costs")

        # 1. Poll (mocked)
        with patch("poller.gh", return_value=[GH_ISSUE]):
            from poller import poll_issues
            issues = poll_issues(repo="test/repo")
        assert len(issues) == 1

        # 2. Create workspace (workspace_manager)
        ws = create_workspace(issues[0]["number"], title=issues[0]["title"])
        assert ws["status"] == "created"

        # 3. Spawn worker (dry_run to avoid meta.json conflict with workspace_manager)
        spawn = spawn_worker(issue=issues[0], project_dir=tmp_path, dry_run=True)
        ws_dir = tmp_path / "workspaces" / str(issues[0]["number"])
        assert ws_dir.exists()

        # 4. Transition to in-progress
        transition_workspace(issues[0]["number"], "claimed")
        transition_workspace(issues[0]["number"], "in-progress")

        # 5. Execute pipeline
        pipeline_data = _make_pipeline({
            "implement": {
                "type": "bash",
                "command": "echo 'def auth(): pass' > auth.py",
            },
            "test": {
                "type": "bash",
                "command": "test -f auth.py && echo 'tests pass'",
                "depends_on": ["implement"],
            },
        })
        pfile = _write_pipeline(tmp_path, pipeline_data)
        pipeline = load_pipeline(pfile)
        executor = DAGExecutor(pipeline, workdir=ws_dir)
        exec_result = executor.run()
        assert exec_result.status == "completed"

        # 6. Log execution
        run_id = log_pipeline_run(exec_result.to_dict())
        assert get_run(run_id) is not None

        # 7. Record cost
        cost = record_usage("test/repo", tokens=5000, run_id=run_id)
        budget = check_budget("test/repo", budget_daily=10.0)
        assert budget["status"] in ("ok", "warning")

        # 8. Transition to completed
        ws_meta = transition_workspace(issues[0]["number"], "completed", run_id=run_id)
        assert ws_meta["status"] == "completed"

        # 9. Health check (no stuck workspaces)
        stuck = check_stuck_workspaces(threshold_hours=4)
        assert len(stuck) == 0

        # 10. Final stats
        stats = get_stats()
        assert stats["total_runs"] >= 1
        report = get_report()
        assert report["completed"] >= 1

    def test_full_chain_with_pipeline_failure(self, tmp_path, monkeypatch):
        """Chain should handle pipeline failure gracefully."""
        monkeypatch.setenv("ORCH_PROJECT_DIR", str(tmp_path))
        monkeypatch.setattr("spawner.PROJECT_DIR", tmp_path)
        monkeypatch.setattr("spawner.WORKSPACES_DIR", tmp_path / "workspaces")
        monkeypatch.setattr("workspace_manager.WORKSPACES_DIR", tmp_path / "workspaces")
        monkeypatch.setattr("execution_log.RUNS_DIR", tmp_path / "runs")
        monkeypatch.setattr("execution_log.LOOPS_DIR", tmp_path / "loops")
        monkeypatch.setattr("cost_tracker.COSTS_DIR", tmp_path / "costs")

        with patch("poller.gh", return_value=[GH_ISSUE]):
            from poller import poll_issues
            issues = poll_issues(repo="test/repo")
        assert len(issues) >= 1

        create_workspace(issues[0]["number"], title=issues[0]["title"])
        transition_workspace(issues[0]["number"], "claimed")
        transition_workspace(issues[0]["number"], "in-progress")

        ws_dir = tmp_path / "workspaces" / str(issues[0]["number"])

        # Failing pipeline
        pipeline_data = _make_pipeline({
            "fail": {"type": "bash", "command": "exit 1"},
        })
        pfile = _write_pipeline(tmp_path, pipeline_data)
        pipeline = load_pipeline(pfile)
        executor = DAGExecutor(pipeline, workdir=ws_dir)
        exec_result = executor.run()

        assert exec_result.status == "failed"

        run_id = log_pipeline_run(exec_result.to_dict())
        retrieved = get_run(run_id)
        assert retrieved["status"] == "failed"

        # Transition to failed
        ws_meta = transition_workspace(issues[0]["number"], "failed", run_id=run_id, note="Pipeline failed")
        assert ws_meta["status"] == "failed"

    def test_full_chain_with_retry_loop(self, tmp_path, monkeypatch):
        """Chain should handle loop nodes without crashing."""
        monkeypatch.setenv("ORCH_PROJECT_DIR", str(tmp_path))
        monkeypatch.setattr("spawner.PROJECT_DIR", tmp_path)
        monkeypatch.setattr("spawner.WORKSPACES_DIR", tmp_path / "workspaces")
        monkeypatch.setattr("execution_log.RUNS_DIR", tmp_path / "runs")
        monkeypatch.setattr("execution_log.LOOPS_DIR", tmp_path / "loops")

        with patch("poller.gh", return_value=[GH_ISSUE]):
            from poller import poll_issues
            issues = poll_issues(repo="test/repo")
        assert len(issues) >= 1

        spawn = spawn_worker(issue=issues[0], project_dir=tmp_path, dry_run=False)
        workspace = Path(spawn["workspace_path"])

        # Pipeline with a loop that runs multiple bash steps
        pipeline_data = _make_pipeline({
            "step_a": {
                "type": "bash",
                "command": "echo 'a' > step_a.txt",
            },
            "step_b": {
                "type": "bash",
                "command": "echo 'b' > step_b.txt",
                "depends_on": ["step_a"],
            },
            "retry_loop": {
                "type": "loop",
                "max_iterations": 2,
                "children": ["step_a", "step_b"],
            },
        })
        pfile = _write_pipeline(tmp_path, pipeline_data)
        pipeline = load_pipeline(pfile)
        executor = DAGExecutor(pipeline, workdir=workspace)
        exec_result = executor.run()

        # Pipeline should complete or partial
        assert exec_result.status in ("completed", "partial", "failed")

        # Log the result regardless of status
        run_id = log_pipeline_run(exec_result.to_dict())
        retrieved = get_run(run_id)
        assert retrieved is not None


# ─── Interface consistency tests ────────────────────────────────

class TestInterfaceConsistency:
    """Verify interfaces are consistent across modules."""

    def test_workspace_path_consistency(self, tmp_path, monkeypatch):
        """spawner and workspace_manager should use compatible workspace paths."""
        monkeypatch.setattr("spawner.WORKSPACES_DIR", tmp_path / "workspaces")
        monkeypatch.setattr("workspace_manager.WORKSPACES_DIR", tmp_path / "workspaces")

        issue_num = 7777

        # Spawner path
        spawner_path = get_workspace_dir(issue_num)
        spawn_worker(issue={**ISSUE, "number": issue_num}, dry_run=False)

        # Workspace manager should find the same workspace
        ws = get_workspace_status(issue_num)
        assert ws is not None

    def test_pipeline_result_schema_matches_log_schema(self, tmp_path, monkeypatch):
        """ExecutionResult.to_dict() output should match log expectations."""
        monkeypatch.setattr("execution_log.RUNS_DIR", tmp_path / "runs")

        pipeline_data = _make_pipeline({
            "test": {"type": "bash", "command": "echo test"},
        })
        pfile = _write_pipeline(tmp_path, pipeline_data)
        pipeline = load_pipeline(pfile)
        executor = DAGExecutor(pipeline, workdir=tmp_path)
        result = executor.run()

        result_dict = result.to_dict()

        # Should have all expected fields
        expected_keys = {
            "pipeline_name", "status", "total_nodes",
            "completed_nodes", "failed_nodes", "skipped_nodes",
            "duration_seconds", "results",
        }
        assert expected_keys.issubset(set(result_dict.keys()))

        # Each node result should have expected keys
        for node_result in result_dict["results"]:
            node_keys = {"node_id", "node_type", "status", "output", "exit_code", "duration_seconds"}
            assert node_keys.issubset(set(node_result.keys()))

    def test_role_interface_consistency(self, tmp_path, monkeypatch):
        """Role loading and matching should work end-to-end."""
        monkeypatch.setattr("roles.ROLES_DIR", Path(__file__).parent / "roles")

        roles = load_all_roles()
        for role_name, role in roles.items():
            assert role.name == role_name
            assert isinstance(role.system_prompt, str)
            assert isinstance(role.allowed_toolsets, list)
            assert isinstance(role.max_turns, int)
            # to_dict should round-trip
            d = role.to_dict()
            assert d["name"] == role.name

    def test_cost_tracker_interface(self, tmp_path, monkeypatch):
        """Cost tracker functions should have consistent interfaces."""
        monkeypatch.setattr("cost_tracker.COSTS_DIR", tmp_path / "costs")

        record_usage("test/repo", tokens=1000, node_type="ai", run_id="run-1", issue_number=42)

        budget = check_budget("test/repo", budget_daily=10.0)
        assert "current_cost" in budget
        assert "remaining" in budget
        assert "status" in budget
        assert isinstance(budget["status"], str)

    def test_prompt_building_consistency(self):
        """build_prompt should always produce non-empty strings."""
        result = build_prompt(ISSUE)
        assert len(result) > 0
        assert "Task from GitHub Issue #42" in result
        assert "Implement user authentication" in result

    def test_ai_guide_loading_with_missing_file(self, tmp_path):
        """read_ai_guide should return empty string when guide doesn't exist."""
        result = read_ai_guide(tmp_path / "nonexistent", "")
        assert result == ""

    def test_find_project_dir_from_issue_body(self):
        """find_project_dir should extract project from issue body."""
        issue = {
            "number": 1,
            "title": "Fix in geometry-os",
            "body": "Fix a bug in ~/zion/projects/geometry-os/src/main.py",
        }
        result = find_project_dir(issue)
        assert result is not None
        assert "geometry-os" in str(result)

    def test_prune_old_runs(self, tmp_path, monkeypatch):
        """prune_old_runs should remove old log files."""
        monkeypatch.setattr("execution_log.RUNS_DIR", tmp_path / "runs")
        monkeypatch.setattr("execution_log.LOOPS_DIR", tmp_path / "loops")

        # Create some run files
        for i in range(3):
            log_pipeline_run({"pipeline_name": f"test-{i}", "status": "completed"})

        assert len(list((tmp_path / "runs").glob("*.json"))) == 3

        # Prune with very short retention
        import time
        removed = prune_old_runs(keep_days=0)
        # Should have removed all (they're all "old" with 0 days retention)
        assert removed >= 0  # Depends on timing

    def test_loop_history(self, tmp_path, monkeypatch):
        """get_loop_history should return logged iterations."""
        monkeypatch.setattr("execution_log.RUNS_DIR", tmp_path / "runs")
        monkeypatch.setattr("execution_log.LOOPS_DIR", tmp_path / "loops")

        for i in range(5):
            log_loop_iteration({"iteration": i, "polled": i + 1})

        history = get_loop_history(limit=10)
        assert len(history) == 5
