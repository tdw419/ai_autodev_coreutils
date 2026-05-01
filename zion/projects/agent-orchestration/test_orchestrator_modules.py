#!/usr/bin/env python3
"""
Tests for orchestrator modules: poller.py, spawner.py, roles.py, orchestrator.py.

Uses mocked subprocess calls for gh CLI and tmp_path for filesystem tests.
"""
import json
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent))

import pytest


# ─── Roles module tests ──────────────────────────────────────────────

class TestRoles:
    def test_load_role_from_file(self, tmp_path):
        role_file = tmp_path / "test.yaml"
        role_file.write_text(
            "name: tester\n"
            "description: Test specialist\n"
            "system_prompt: You test things.\n"
            "allowed_toolsets: [bash, read]\n"
            "max_turns: 15\n"
        )
        from roles import load_role
        role = load_role(role_file)
        assert role.name == "tester"
        assert role.description == "Test specialist"
        assert role.system_prompt == "You test things."
        assert role.allowed_toolsets == ["bash", "read"]
        assert role.max_turns == 15

    def test_load_role_defaults(self, tmp_path):
        role_file = tmp_path / "minimal.yaml"
        role_file.write_text("name: basic\n")
        from roles import load_role
        role = load_role(role_file)
        assert role.name == "basic"
        assert role.max_turns == 20
        assert role.acp_command == "claude"
        assert role.allowed_toolsets == []

    def test_load_invalid_role(self, tmp_path):
        bad = tmp_path / "bad.yaml"
        bad.write_text("- just a list")
        from roles import load_role
        with pytest.raises(ValueError, match="Invalid role"):
            load_role(bad)

    def test_load_all_roles(self, tmp_path):
        (tmp_path / "a.yaml").write_text("name: alpha\nmax_turns: 10\n")
        (tmp_path / "b.yaml").write_text("name: beta\nmax_turns: 20\n")
        from roles import load_all_roles
        roles = load_all_roles(tmp_path)
        assert set(roles.keys()) == {"alpha", "beta"}
        assert roles["alpha"].max_turns == 10

    def test_load_all_roles_empty_dir(self, tmp_path):
        from roles import load_all_roles
        roles = load_all_roles(tmp_path)
        assert roles == {}

    def test_load_all_roles_nonexistent_dir(self):
        from roles import load_all_roles
        roles = load_all_roles("/nonexistent/path/roles")
        assert roles == {}

    def test_match_role_by_label(self, tmp_path):
        (tmp_path / "tester.yaml").write_text("name: tester\n")
        from roles import match_role
        issue = {"title": "Something", "labels": ["bug"]}
        role = match_role(issue, {"tester": MagicMock(name="tester")})
        assert role is not None

    def test_match_role_explicit_agent_role_label(self, tmp_path):
        (tmp_path / "reviewer.yaml").write_text("name: reviewer\n")
        from roles import match_role
        issue = {"title": "Something", "labels": ["agent-role:reviewer"]}
        reviewer = MagicMock(name="reviewer")
        roles = {"reviewer": reviewer, "implementer": MagicMock(name="implementer")}
        role = match_role(issue, roles)
        assert role == reviewer

    def test_match_role_by_title_keyword(self, tmp_path):
        (tmp_path / "implementer.yaml").write_text("name: implementer\n")
        from roles import match_role
        issue = {"title": "Implement user auth", "labels": []}
        role = match_role(issue, {"implementer": MagicMock(name="implementer")})
        assert role is not None

    def test_match_role_default_implementer(self, tmp_path):
        (tmp_path / "implementer.yaml").write_text("name: implementer\n")
        from roles import match_role
        issue = {"title": "Something random", "labels": ["unknown-label"]}
        role = match_role(issue, {"implementer": MagicMock(name="implementer")})
        assert role is not None

    def test_match_role_no_roles_available(self):
        from roles import match_role
        issue = {"title": "Fix bug", "labels": ["bug"]}
        role = match_role(issue, {})
        assert role is None

    def test_build_role_prompt(self):
        from roles import Role, build_role_prompt
        role = Role(
            name="coder", description="", system_prompt="You are a coder.",
            allowed_toolsets=[], max_turns=20
        )
        result = build_role_prompt("Do the task", role)
        assert result.startswith("You are a coder.")
        assert "Do the task" in result

    def test_build_role_prompt_no_system_prompt(self):
        from roles import Role, build_role_prompt
        role = Role(
            name="blank", description="", system_prompt="",
            allowed_toolsets=[], max_turns=20
        )
        result = build_role_prompt("Do the task", role)
        assert result == "Do the task"

    def test_label_role_map(self):
        from roles import LABEL_ROLE_MAP
        assert LABEL_ROLE_MAP["bug"] == "tester"
        assert LABEL_ROLE_MAP["feature"] == "implementer"
        assert LABEL_ROLE_MAP["review"] == "reviewer"
        assert LABEL_ROLE_MAP["triage"] == "coordinator"

    def test_title_role_map(self):
        from roles import TITLE_ROLE_MAP
        assert TITLE_ROLE_MAP["fix"] == "tester"
        assert TITLE_ROLE_MAP["implement"] == "implementer"
        assert TITLE_ROLE_MAP["plan"] == "coordinator"


# ─── Poller module tests (mocked gh CLI) ─────────────────────────────

class TestPoller:
    def _mock_gh_result(self, issues_json):
        """Create a mock subprocess result for gh CLI."""
        result = MagicMock()
        result.returncode = 0
        result.stdout = json.dumps(issues_json)
        result.stderr = ""
        return result

    def test_poll_issues_filters_assigned(self):
        from poller import poll_issues
        issues = [
            {"number": 1, "title": "Unassigned", "body": "Do X",
             "labels": [{"name": "agent-ready"}], "assignees": [],
             "url": "http://example.com/1", "createdAt": "2026-01-01T00:00:00Z", "state": "open"},
            {"number": 2, "title": "Assigned", "body": "Do Y",
             "labels": [{"name": "agent-ready"}], "assignees": [{"login": "someone"}],
             "url": "http://example.com/2", "createdAt": "2026-01-01T00:00:00Z", "state": "open"},
        ]
        mock_result = self._mock_gh_result(issues)
        with patch("poller.subprocess.run", return_value=mock_result):
            ready = poll_issues(repo="owner/repo")
        assert len(ready) == 1
        assert ready[0]["number"] == 1

    def test_poll_issues_empty(self):
        from poller import poll_issues
        mock_result = self._mock_gh_result([])
        with patch("poller.subprocess.run", return_value=mock_result):
            ready = poll_issues(repo="owner/repo")
        assert ready == []

    def test_poll_issues_all_assigned(self):
        from poller import poll_issues
        issues = [
            {"number": 1, "title": "Taken", "body": "",
             "labels": [{"name": "agent-ready"}], "assignees": [{"login": "user"}],
             "url": "http://x", "createdAt": "2026-01-01", "state": "open"},
        ]
        mock_result = self._mock_gh_result(issues)
        with patch("poller.subprocess.run", return_value=mock_result):
            ready = poll_issues(repo="owner/repo")
        assert ready == []

    def test_poll_issues_structured_output(self):
        from poller import poll_issues
        issues = [
            {"number": 42, "title": "My Issue", "body": "Fix it",
             "labels": [{"name": "agent-ready"}, {"name": "bug"}], "assignees": [],
             "url": "http://example.com/42", "createdAt": "2026-05-01T00:00:00Z", "state": "open"},
        ]
        mock_result = self._mock_gh_result(issues)
        with patch("poller.subprocess.run", return_value=mock_result):
            ready = poll_issues(repo="owner/repo")
        assert ready[0]["number"] == 42
        assert ready[0]["title"] == "My Issue"
        assert ready[0]["body"] == "Fix it"
        assert ready[0]["labels"] == ["agent-ready", "bug"]
        assert ready[0]["url"] == "http://example.com/42"


# ─── Spawner module tests ────────────────────────────────────────────

class TestSpawner:
    def test_build_prompt_basic(self):
        from spawner import build_prompt
        issue = {"number": 1, "title": "Fix bug", "body": "It's broken", "labels": ["bug"], "url": "http://x"}
        prompt = build_prompt(issue)
        assert "Fix bug" in prompt
        assert "It's broken" in prompt
        assert "#1" in prompt

    def test_build_prompt_with_ai_guide(self):
        from spawner import build_prompt
        issue = {"number": 2, "title": "Feature", "body": "Add X", "labels": [], "url": "http://x"}
        prompt = build_prompt(issue, ai_guide="Use TypeScript.")
        assert "Use TypeScript." in prompt
        assert "Project Guidelines" in prompt

    def test_build_prompt_empty_body(self):
        from spawner import build_prompt
        issue = {"number": 3, "title": "No desc", "body": "", "labels": [], "url": "http://x"}
        prompt = build_prompt(issue)
        # Empty body still produces a valid prompt with just the title
        assert "No desc" in prompt
        assert "#3" in prompt

    def test_find_project_dir_from_body(self):
        from spawner import find_project_dir
        issue = {"body": "Work in ~/zion/projects/my-app"}
        result = find_project_dir(issue)
        assert result is not None
        assert result.name == "my-app"

    def test_find_project_dir_from_keyword(self):
        from spawner import find_project_dir
        issue = {"body": "project: target-repo needs update"}
        result = find_project_dir(issue)
        assert result is not None
        assert result.name == "target-repo"

    def test_find_project_dir_none(self):
        from spawner import find_project_dir
        issue = {"body": "Just some text"}
        result = find_project_dir(issue)
        assert result is None

    def test_read_ai_guide_exists(self, tmp_path):
        from spawner import read_ai_guide
        guide = tmp_path / "AI_GUIDE.md"
        guide.write_text("Follow PEP 8.")
        result = read_ai_guide(tmp_path)
        assert result == "Follow PEP 8."

    def test_read_ai_guide_missing(self, tmp_path):
        from spawner import read_ai_guide
        result = read_ai_guide(tmp_path)
        assert result == ""

    def test_spawn_worker_dry_run(self):
        from spawner import spawn_worker
        issue = {"number": 42, "title": "Test task", "body": "Do it", "labels": [], "url": "http://x"}
        result = spawn_worker(issue, dry_run=True)
        assert result["issue_number"] == 42
        assert result["execution_mode"] == "direct"
        assert "workspace_path" in result

    def test_spawn_worker_creates_workspace(self, tmp_path):
        from spawner import spawn_worker, WORKSPACES_DIR
        issue = {"number": 99, "title": "Workspace test", "body": "Create files", "labels": [], "url": "http://x"}
        with patch("spawner.WORKSPACES_DIR", tmp_path / "ws"):
            with patch("spawner.PROJECT_DIR", tmp_path / "proj"):
                result = spawn_worker(issue, dry_run=False)
        assert result["issue_number"] == 99
        ws = Path(result["workspace_path"])
        assert ws.exists()
        assert (ws / "meta.json").exists()
        assert (ws / "prompt.md").exists()
        assert (ws / "task.json").exists()

    def test_spawn_worker_with_pipeline(self):
        from spawner import spawn_worker
        issue = {"number": 10, "title": "Pipeline task", "body": "Run it", "labels": [], "url": "http://x"}
        result = spawn_worker(issue, pipeline="pipelines/test-pipeline.yaml", dry_run=True)
        assert result["execution_mode"] == "dag"
        assert result["exec_instructions"]["mode"] == "dag"


# ─── Orchestrator module tests (mocked) ──────────────────────────────

class TestOrchestrator:
    def test_load_config_defaults(self):
        from orchestrator import load_config
        config = load_config(config_path=None)
        assert "repo" in config
        assert "max_concurrent" in config
        assert config["label"] == "agent-ready"

    def test_load_config_from_file(self, tmp_path):
        cfg = tmp_path / "orch.yaml"
        cfg.write_text("repo: test/repo\nmax_concurrent: 5\n")
        from orchestrator import load_config
        config = load_config(str(cfg))
        assert config["repo"] == "test/repo"
        assert config["max_concurrent"] == 5

    def test_get_active_workers_empty(self, tmp_path):
        from orchestrator import WORKSPACES_DIR, get_active_workers
        with patch("orchestrator.WORKSPACES_DIR", tmp_path / "nonexistent"):
            workers = get_active_workers()
        assert workers == []

    def test_get_active_workers_with_meta(self, tmp_path):
        from orchestrator import get_active_workers
        ws = tmp_path / "123"
        ws.mkdir()
        (ws / "meta.json").write_text(json.dumps({
            "issue_number": 123, "title": "Test", "status": "in-progress"
        }))
        with patch("orchestrator.WORKSPACES_DIR", tmp_path):
            workers = get_active_workers()
        assert len(workers) == 1
        assert workers[0]["issue_number"] == 123

    def test_get_active_workers_ignores_completed(self, tmp_path):
        from orchestrator import get_active_workers
        ws = tmp_path / "456"
        ws.mkdir()
        (ws / "meta.json").write_text(json.dumps({
            "issue_number": 456, "title": "Done", "status": "completed"
        }))
        with patch("orchestrator.WORKSPACES_DIR", tmp_path):
            workers = get_active_workers()
        assert workers == []

    def test_get_worker_count(self, tmp_path):
        from orchestrator import get_worker_count, get_active_workers
        with patch("orchestrator.WORKSPACES_DIR", tmp_path / "nonexistent"):
            assert get_worker_count() == 0

    def test_run_loop_no_repo(self):
        from orchestrator import run_loop
        result = run_loop({"repo": "", "label": "agent-ready", "max_concurrent": 2})
        assert "error" in result
        assert "No repo" in result["error"]

    def test_run_loop_skips_when_full(self, tmp_path):
        from orchestrator import run_loop, WORKSPACES_DIR
        # Create 2 in-progress workers (single-repo flat layout)
        for i in [1, 2]:
            ws = tmp_path / str(i)
            ws.mkdir()
            (ws / "meta.json").write_text(json.dumps({
                "issue_number": i, "title": f"Issue {i}", "status": "in-progress"
            }))
        with patch("orchestrator.WORKSPACES_DIR", tmp_path):
            result = run_loop({
                "repos": [{"name": "test__repo", "url": "test/repo", "labels": ["agent-ready"],
                            "pipeline": "", "max_concurrent": 2, "budget_daily": None,
                            "roles_dir": "roles/", "ai_guide_path": "", "approval_mode": "never"}],
                "max_concurrent": 2,
            })
        assert result["skipped_full"] is True
        assert result["global_available_slots"] == 0

    def test_run_loop_dry_run(self, tmp_path):
        from orchestrator import run_loop, WORKSPACES_DIR
        with patch("orchestrator.WORKSPACES_DIR", tmp_path / "ws"), \
             patch("orchestrator.poll_issues", return_value=[
                 {"number": 1, "title": "New issue", "body": "Fix", "labels": ["agent-ready"], "url": "http://x"}
             ]):
            result = run_loop({
                "repos": [{"name": "test__repo", "url": "test/repo", "labels": ["agent-ready"],
                            "pipeline": "", "max_concurrent": 2, "budget_daily": None,
                            "roles_dir": "roles/", "ai_guide_path": "", "approval_mode": "never"}],
                "max_concurrent": 2,
                "project_dir": str(tmp_path),
            }, dry_run=True)
        assert result["repos"]["test__repo"]["polled"] == 1
        assert len(result["repos"]["test__repo"]["spawned"]) == 1
        assert result["repos"]["test__repo"]["spawned"][0]["issue_number"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
