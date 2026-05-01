#!/usr/bin/env python3
"""Tests for multi-repo orchestration (Phase 16)."""

import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))


class TestCostTracker:
    """Tests for cost_tracker.py module."""

    def test_record_usage_basic(self, tmp_path, monkeypatch):
        from cost_tracker import record_usage, COSTS_DIR
        monkeypatch.setattr("cost_tracker.COSTS_DIR", tmp_path / "costs")

        daily = record_usage(repo="owner/repo", tokens=10000)
        assert daily["total_tokens"] == 10000
        assert daily["total_cost"] > 0
        assert len(daily["entries"]) == 1
        assert daily["entries"][0]["tokens"] == 10000

    def test_record_usage_accumulates(self, tmp_path, monkeypatch):
        from cost_tracker import record_usage, COSTS_DIR
        monkeypatch.setattr("cost_tracker.COSTS_DIR", tmp_path / "costs")

        record_usage(repo="owner/repo", tokens=10000)
        record_usage(repo="owner/repo", tokens=5000)

        daily_path = tmp_path / "costs" / "owner__repo" / f"{__import__('datetime').date.today().isoformat()}.json"
        assert daily_path.exists()
        data = json.loads(daily_path.read_text())
        assert data["total_tokens"] == 15000

    def test_estimate_pipeline_cost(self):
        from cost_tracker import estimate_pipeline_cost

        result = estimate_pipeline_cost(["ai", "bash", "ai", "review"])
        assert result["estimated_tokens"] > 0
        assert result["estimated_cost"] > 0
        # bash nodes should not add cost
        result_bash_only = estimate_pipeline_cost(["bash", "dependency"])
        assert result_bash_only["estimated_tokens"] == 0
        assert result_bash_only["estimated_cost"] == 0

    def test_check_budget_ok(self, tmp_path, monkeypatch):
        from cost_tracker import record_usage, check_budget, COSTS_DIR
        monkeypatch.setattr("cost_tracker.COSTS_DIR", tmp_path / "costs")

        record_usage(repo="owner/repo", tokens=1000)  # small amount
        result = check_budget("owner/repo", budget_daily=100.0)
        assert result["status"] == "ok"
        assert result["remaining"] > 0

    def test_check_budget_exceeded(self, tmp_path, monkeypatch):
        from cost_tracker import record_usage, check_budget, COSTS_DIR
        monkeypatch.setattr("cost_tracker.COSTS_DIR", tmp_path / "costs")

        # Record enough tokens to exceed budget
        # $0.003 per 1K tokens. Budget of $0.01 = ~3333 tokens
        record_usage(repo="owner/repo", tokens=10000)
        result = check_budget("owner/repo", budget_daily=0.01)
        assert result["status"] == "exceeded"

    def test_check_budget_warning(self, tmp_path, monkeypatch):
        from cost_tracker import record_usage, check_budget, COSTS_DIR
        monkeypatch.setattr("cost_tracker.COSTS_DIR", tmp_path / "costs")

        # Record ~85% of budget
        # $0.003 per 1K * 8500 tokens = $0.0255. Budget $0.03 = 85%
        record_usage(repo="owner/repo", tokens=8500)
        result = check_budget("owner/repo", budget_daily=0.03)
        assert result["status"] == "warning"

    def test_get_period_cost(self, tmp_path, monkeypatch):
        from cost_tracker import record_usage, get_period_cost, COSTS_DIR
        monkeypatch.setattr("cost_tracker.COSTS_DIR", tmp_path / "costs")

        record_usage(repo="owner/repo", tokens=10000)
        result = get_period_cost("owner/repo", days=7)
        assert result["total_tokens"] == 10000
        assert result["total_cost"] > 0
        assert len(result["daily"]) == 1

    def test_get_all_repos(self, tmp_path, monkeypatch):
        from cost_tracker import record_usage, get_all_repos, COSTS_DIR
        monkeypatch.setattr("cost_tracker.COSTS_DIR", tmp_path / "costs")

        record_usage(repo="owner/repo1", tokens=1000)
        record_usage(repo="owner/repo2", tokens=2000)

        repos = get_all_repos()
        assert "owner/repo1" in repos
        assert "owner/repo2" in repos


class TestMultiRepoConfig:
    """Tests for multi-repo configuration loading and validation."""

    def test_single_repo_mode(self, tmp_path):
        from orchestrator import load_config

        config_path = tmp_path / "config.yaml"
        config_path.write_text("repo: owner/repo\nlabel: agent-ready\nmax_concurrent: 3\n")
        config = load_config(str(config_path))
        assert len(config["repos"]) == 1
        assert config["repos"][0]["url"] == "owner/repo"
        assert config["repos"][0]["labels"] == ["agent-ready"]
        assert config["repos"][0]["max_concurrent"] == 3

    def test_multi_repo_mode(self, tmp_path):
        from orchestrator import load_config

        config_path = tmp_path / "config.yaml"
        config_path.write_text("""
repos:
  - name: repo1
    url: owner/repo1
    labels: [agent-ready, bug]
    max_concurrent: 2
    budget_daily: 10.0
  - name: repo2
    url: owner/repo2
    labels: [agent-ready]
    max_concurrent: 1
""")
        config = load_config(str(config_path))
        assert len(config["repos"]) == 2
        assert config["repos"][0]["url"] == "owner/repo1"
        assert config["repos"][0]["labels"] == ["agent-ready", "bug"]
        assert config["repos"][0]["budget_daily"] == 10.0
        assert config["repos"][1]["max_concurrent"] == 1

    def test_validate_config_valid(self, tmp_path):
        from orchestrator import load_config, validate_config

        config_path = tmp_path / "config.yaml"
        config_path.write_text("""
repos:
  - name: repo1
    url: owner/repo1
    max_concurrent: 2
""")
        config = load_config(str(config_path))
        errors = validate_config(config)
        assert errors == []

    def test_validate_config_no_repos(self):
        from orchestrator import validate_config

        errors = validate_config({"repos": []})
        assert len(errors) == 1
        assert "No repos configured" in errors[0]

    def test_validate_config_missing_url(self):
        from orchestrator import validate_config

        errors = validate_config({
            "repos": [{"name": "test", "max_concurrent": 2}]
        })
        assert any("'url' is required" in e for e in errors)

    def test_validate_config_negative_max_concurrent(self):
        from orchestrator import validate_config

        errors = validate_config({
            "repos": [{"name": "test", "url": "o/r", "max_concurrent": 0}]
        })
        assert any("max_concurrent" in e for e in errors)

    def test_validate_config_negative_budget(self):
        from orchestrator import validate_config

        errors = validate_config({
            "repos": [{"name": "test", "url": "o/r", "max_concurrent": 2, "budget_daily": -1}]
        })
        assert any("budget_daily" in e for e in errors)

    def test_multi_repo_defaults_applied(self, tmp_path):
        from orchestrator import load_config

        config_path = tmp_path / "config.yaml"
        config_path.write_text("""
repos:
  - name: repo1
    url: owner/repo1
""")
        config = load_config(str(config_path))
        repo = config["repos"][0]
        assert repo["labels"] == ["agent-ready"]
        assert repo["max_concurrent"] == 2
        assert repo["pipeline"] == ""
        assert repo["approval_mode"] == "never"
        assert repo["budget_daily"] is None


class TestMultiRepoWorkspaceLayout:
    """Tests for per-repo workspace organization."""

    def test_single_repo_workspace_path(self):
        from spawner import get_workspace_dir

        ws = get_workspace_dir(42, repo_name=None)
        assert ws.name == "42"
        assert ws.parent.name == "workspaces"

    def test_multi_repo_workspace_path(self):
        from spawner import get_workspace_dir

        ws = get_workspace_dir(42, repo_name="owner__repo1")
        assert ws.name == "42"
        assert ws.parent.name == "owner__repo1"
        assert ws.parent.parent.name == "workspaces"

    def test_spawn_worker_with_repo_name(self, tmp_path, monkeypatch):
        from spawner import spawn_worker, WORKSPACES_DIR
        monkeypatch.setattr("spawner.WORKSPACES_DIR", tmp_path / "workspaces")
        monkeypatch.setattr("spawner.PROJECT_DIR", tmp_path)

        issue = {
            "number": 123,
            "title": "Test issue",
            "body": "Fix something",
            "labels": ["bug"],
            "url": "https://github.com/owner/repo1/issues/123",
        }

        result = spawn_worker(
            issue=issue,
            repo_name="owner__repo1",
            dry_run=False,
        )

        assert result["repo_name"] == "owner__repo1"
        assert "owner__repo1" in result["workspace_path"]
        assert "123" in result["workspace_path"]

        # Verify meta.json has repo_name
        meta_path = Path(result["workspace_path"]) / "meta.json"
        meta = json.loads(meta_path.read_text())
        assert meta["repo_name"] == "owner__repo1"

    def test_read_ai_guide_explicit_path(self, tmp_path):
        from spawner import read_ai_guide

        guide = tmp_path / "custom" / "AI_GUIDE.md"
        guide.parent.mkdir(parents=True)
        guide.write_text("# Custom Guide\nUse tabs, not spaces.")

        result = read_ai_guide(ai_guide_path=str(guide))
        assert "Use tabs" in result

    def test_read_ai_guide_falls_back_to_project_dir(self, tmp_path):
        from spawner import read_ai_guide

        project = tmp_path / "project"
        project.mkdir()
        (project / "AI_GUIDE.md").write_text("# Project Guide\nPython 3.12+")

        result = read_ai_guide(project_dir=project)
        assert "Python 3.12" in result

    def test_read_ai_guide_explicit_takes_priority(self, tmp_path):
        from spawner import read_ai_guide

        project = tmp_path / "project"
        project.mkdir()
        (project / "AI_GUIDE.md").write_text("# Project Guide")

        explicit = tmp_path / "explicit" / "AI_GUIDE.md"
        explicit.parent.mkdir(parents=True)
        explicit.write_text("# Explicit Guide")

        result = read_ai_guide(project_dir=project, ai_guide_path=str(explicit))
        assert "Explicit Guide" in result
        assert "Project Guide" not in result


class TestMultiRepoOrchestratorLoop:
    """Tests for multi-repo orchestrator run_loop."""

    def test_run_loop_multi_repo(self, tmp_path, monkeypatch):
        from orchestrator import run_loop
        monkeypatch.setattr("orchestrator.WORKSPACES_DIR", tmp_path / "workspaces")
        monkeypatch.setattr("orchestrator.PROJECT_DIR", tmp_path)

        mock_poll = MagicMock(return_value=[
            {"number": 1, "title": "Issue 1", "body": "", "labels": [], "url": ""},
        ])
        monkeypatch.setattr("orchestrator.poll_issues", mock_poll)

        mock_spawn = MagicMock(return_value={
            "workspace_path": str(tmp_path / "ws"),
            "execution_mode": "direct",
        })
        monkeypatch.setattr("orchestrator.spawn_worker", mock_spawn)
        monkeypatch.setattr("orchestrator.update_issue_status", MagicMock())
        monkeypatch.setattr("orchestrator.log_loop_iteration", MagicMock())
        monkeypatch.setattr("orchestrator.record_usage", MagicMock())
        monkeypatch.setattr("orchestrator.estimate_pipeline_cost", MagicMock(return_value={"estimated_tokens": 0}))

        config = {
            "repos": [
                {"name": "repo1", "url": "owner/repo1", "labels": ["agent-ready"],
                 "pipeline": "", "max_concurrent": 2, "budget_daily": None,
                 "roles_dir": "roles/", "ai_guide_path": "", "approval_mode": "never"},
                {"name": "repo2", "url": "owner/repo2", "labels": ["agent-ready"],
                 "pipeline": "", "max_concurrent": 1, "budget_daily": None,
                 "roles_dir": "roles/", "ai_guide_path": "", "approval_mode": "never"},
            ],
            "max_concurrent": 10,
            "project_dir": str(tmp_path),
        }

        summary = run_loop(config, dry_run=False)
        assert "repos" in summary
        assert "repo1" in summary["repos"]
        assert "repo2" in summary["repos"]
        assert summary["repos"]["repo1"]["polled"] == 1
        assert summary["repos"]["repo2"]["polled"] == 1

    def test_run_loop_budget_exceeded_skips_repo(self, tmp_path, monkeypatch):
        from orchestrator import run_loop
        monkeypatch.setattr("orchestrator.WORKSPACES_DIR", tmp_path / "workspaces")
        monkeypatch.setattr("orchestrator.PROJECT_DIR", tmp_path)

        mock_check = MagicMock(return_value={
            "status": "exceeded", "current_cost": 15.0,
            "remaining": -5.0, "usage_ratio": 1.5, "budget_daily": 10.0,
        })
        monkeypatch.setattr("orchestrator.check_budget", mock_check)
        monkeypatch.setattr("orchestrator.poll_issues", MagicMock(return_value=[]))
        monkeypatch.setattr("orchestrator.log_loop_iteration", MagicMock())

        config = {
            "repos": [{
                "name": "repo1", "url": "owner/repo1", "labels": ["agent-ready"],
                "pipeline": "", "max_concurrent": 2, "budget_daily": 10.0,
                "roles_dir": "roles/", "ai_guide_path": "", "approval_mode": "never",
            }],
            "max_concurrent": 10,
            "project_dir": str(tmp_path),
        }

        summary = run_loop(config, dry_run=False)
        assert summary["repos"]["repo1"]["skipped"] == "budget_exceeded"

    def test_run_loop_filter_repo(self, tmp_path, monkeypatch):
        from orchestrator import run_loop
        monkeypatch.setattr("orchestrator.WORKSPACES_DIR", tmp_path / "workspaces")
        monkeypatch.setattr("orchestrator.PROJECT_DIR", tmp_path)

        mock_poll = MagicMock(return_value=[])
        monkeypatch.setattr("orchestrator.poll_issues", mock_poll)
        monkeypatch.setattr("orchestrator.log_loop_iteration", MagicMock())

        config = {
            "repos": [
                {"name": "repo1", "url": "owner/repo1", "labels": ["agent-ready"],
                 "pipeline": "", "max_concurrent": 2, "budget_daily": None,
                 "roles_dir": "roles/", "ai_guide_path": "", "approval_mode": "never"},
                {"name": "repo2", "url": "owner/repo2", "labels": ["agent-ready"],
                 "pipeline": "", "max_concurrent": 1, "budget_daily": None,
                 "roles_dir": "roles/", "ai_guide_path": "", "approval_mode": "never"},
            ],
            "max_concurrent": 10,
            "project_dir": str(tmp_path),
        }

        summary = run_loop(config, dry_run=False, filter_repo="owner/repo2")
        assert "repo2" in summary["repos"]
        assert "repo1" not in summary["repos"]

    def test_run_loop_no_repos_returns_error(self):
        from orchestrator import run_loop

        summary = run_loop({"repos": [], "max_concurrent": 2})
        assert "error" in summary

    def test_run_loop_per_repo_concurrency_limit(self, tmp_path, monkeypatch):
        from orchestrator import run_loop, WORKSPACES_DIR
        ws_dir = tmp_path / "workspaces" / "repo1"
        ws_dir.mkdir(parents=True)

        # Create 2 in-progress workers for repo1
        for i in [1, 2]:
            meta_path = ws_dir / str(i)
            meta_path.mkdir()
            (meta_path / "meta.json").write_text(json.dumps({
                "issue_number": i, "title": f"Issue {i}",
                "status": "in-progress", "repo_name": "repo1",
            }))

        monkeypatch.setattr("orchestrator.WORKSPACES_DIR", tmp_path / "workspaces")
        monkeypatch.setattr("orchestrator.PROJECT_DIR", tmp_path)
        monkeypatch.setattr("orchestrator.poll_issues", MagicMock(return_value=[
            {"number": 3, "title": "Issue 3", "body": "", "labels": [], "url": ""},
        ]))
        monkeypatch.setattr("orchestrator.spawn_worker", MagicMock(return_value={
            "workspace_path": str(tmp_path / "ws"), "execution_mode": "direct",
        }))
        monkeypatch.setattr("orchestrator.update_issue_status", MagicMock())
        monkeypatch.setattr("orchestrator.log_loop_iteration", MagicMock())
        monkeypatch.setattr("orchestrator.record_usage", MagicMock())
        monkeypatch.setattr("orchestrator.estimate_pipeline_cost", MagicMock(return_value={"estimated_tokens": 0}))

        config = {
            "repos": [{
                "name": "repo1", "url": "owner/repo1", "labels": ["agent-ready"],
                "pipeline": "", "max_concurrent": 2, "budget_daily": None,
                "roles_dir": "roles/", "ai_guide_path": "", "approval_mode": "never",
            }],
            "max_concurrent": 10,
            "project_dir": str(tmp_path),
        }

        summary = run_loop(config, dry_run=False)
        # Should skip because repo has max_concurrent=2 and 2 are active
        assert summary["repos"]["repo1"]["skipped"] == "full"

    def test_get_active_workers_with_repo_filter(self, tmp_path, monkeypatch):
        from orchestrator import get_active_workers
        monkeypatch.setattr("orchestrator.WORKSPACES_DIR", tmp_path / "workspaces")

        # Create workers in two repos
        for repo, issue in [("repo1", 1), ("repo1", 2), ("repo2", 3)]:
            ws_dir = tmp_path / "workspaces" / repo / str(issue)
            ws_dir.mkdir(parents=True)
            (ws_dir / "meta.json").write_text(json.dumps({
                "issue_number": issue, "title": f"Issue {issue}",
                "status": "in-progress", "repo_name": repo,
            }))

        all_workers = get_active_workers()
        assert len(all_workers) == 3

        repo1_workers = get_active_workers(repo_name="repo1")
        assert len(repo1_workers) == 2

        repo2_workers = get_active_workers(repo_name="repo2")
        assert len(repo2_workers) == 1

        nonexistent = get_active_workers(repo_name="repo3")
        assert len(nonexistent) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
