#!/usr/bin/env python3
"""Tests for onboard.py — Project Onboarding Bootstrap (phase-24)."""
from __future__ import annotations

import os
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest.mock import patch

from onboard import (
    detect_build_command,
    detect_existing_guide,
    detect_frameworks,
    detect_language,
    detect_linter,
    detect_project,
    detect_test_runner,
    generate_guide,
    generate_orchestrator_config,
    onboard_full,
)


def _make_repo(tmp: Path, files: dict[str, str] | None = None) -> Path:
    """Create a minimal fake repo with given files."""
    repo = tmp / "test_repo"
    repo.mkdir()
    for name, content in (files or {}).items():
        p = repo / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
    return repo


class TestDetectLanguage(unittest.TestCase):
    """D1.T1 validation — detect at least 5 project types."""

    def test_python_pip(self):
        with tempfile.TemporaryDirectory() as td:
            repo = _make_repo(Path(td), {"requirements.txt": "flask\n"})
            self.assertEqual(detect_language(repo), "python")

    def test_python_poetry(self):
        with tempfile.TemporaryDirectory() as td:
            repo = _make_repo(Path(td), {"pyproject.toml": "[tool.poetry]\n"})
            self.assertEqual(detect_language(repo), "python")

    def test_node_npm(self):
        with tempfile.TemporaryDirectory() as td:
            repo = _make_repo(Path(td), {"package.json": "{}\n"})
            self.assertEqual(detect_language(repo), "node")

    def test_go(self):
        with tempfile.TemporaryDirectory() as td:
            repo = _make_repo(Path(td), {"go.mod": "module test\n"})
            self.assertEqual(detect_language(repo), "go")

    def test_rust(self):
        with tempfile.TemporaryDirectory() as td:
            repo = _make_repo(Path(td), {"Cargo.toml": "[package]\n"})
            self.assertEqual(detect_language(repo), "rust")

    def test_ruby(self):
        with tempfile.TemporaryDirectory() as td:
            repo = _make_repo(Path(td), {"Gemfile": "source 'rubygems'\n"})
            self.assertEqual(detect_language(repo), "ruby")

    def test_java_maven(self):
        with tempfile.TemporaryDirectory() as td:
            repo = _make_repo(Path(td), {"pom.xml": "<project></project>\n"})
            self.assertEqual(detect_language(repo), "java")

    def test_unknown(self):
        with tempfile.TemporaryDirectory() as td:
            repo = _make_repo(Path(td), {"README.md": "hello\n"})
            self.assertIsNone(detect_language(repo))

    def test_polyglot_scores(self):
        """Polyglot repo returns highest-scoring language."""
        with tempfile.TemporaryDirectory() as td:
            repo = _make_repo(Path(td), {
                "requirements.txt": "flask\n",
                "setup.py": "from setuptools import setup\n",
                "pyproject.toml": "[tool.poetry]\n",
            })
            # Python should win with score 3
            self.assertEqual(detect_language(repo), "python")


class TestDetectFrameworks(unittest.TestCase):
    def test_python_fastapi(self):
        with tempfile.TemporaryDirectory() as td:
            repo = _make_repo(Path(td), {
                "requirements.txt": "fastapi\nuvicorn\n",
            })
            fws = detect_frameworks(repo, "python")
            self.assertIn("fastapi", fws)

    def test_python_django(self):
        with tempfile.TemporaryDirectory() as td:
            repo = _make_repo(Path(td), {
                "requirements.txt": "django\n",
            })
            fws = detect_frameworks(repo, "python")
            self.assertIn("django", fws)

    def test_no_frameworks(self):
        with tempfile.TemporaryDirectory() as td:
            repo = _make_repo(Path(td), {"requirements.txt": "requests\n"})
            fws = detect_frameworks(repo, "python")
            self.assertEqual(fws, [])


class TestDetectTestRunner(unittest.TestCase):
    def test_python_pytest(self):
        with tempfile.TemporaryDirectory() as td:
            repo = _make_repo(Path(td), {
                "requirements.txt": "pytest\n",
                "tests/test_foo.py": "",
            })
            runner = detect_test_runner(repo, "python")
            self.assertIsNotNone(runner)
            self.assertEqual(runner["name"], "pytest")

    def test_go_gotest(self):
        with tempfile.TemporaryDirectory() as td:
            repo = _make_repo(Path(td), {"go.mod": "module test\n"})
            runner = detect_test_runner(repo, "go")
            self.assertIsNotNone(runner)
            self.assertEqual(runner["name"], "go test")

    def test_rust_cargo(self):
        with tempfile.TemporaryDirectory() as td:
            repo = _make_repo(Path(td), {"Cargo.toml": "[package]\n"})
            runner = detect_test_runner(repo, "rust")
            self.assertIsNotNone(runner)
            self.assertEqual(runner["name"], "cargo test")

    def test_unknown_language(self):
        runner = detect_test_runner(Path("."), "brainfuck")
        self.assertIsNone(runner)


class TestDetectLinter(unittest.TestCase):
    def test_python_ruff(self):
        with tempfile.TemporaryDirectory() as td:
            repo = _make_repo(Path(td), {"ruff.toml": "[tool.ruff]\n"})
            linter = detect_linter(repo, "python")
            self.assertIsNotNone(linter)
            self.assertEqual(linter["name"], "ruff")

    def test_python_fallback(self):
        """If no config found, returns first linter for the language."""
        with tempfile.TemporaryDirectory() as td:
            repo = _make_repo(Path(td), {"requirements.txt": "flask\n"})
            linter = detect_linter(repo, "python")
            self.assertIsNotNone(linter)


class TestDetectBuildCommand(unittest.TestCase):
    def test_pip_requirements(self):
        with tempfile.TemporaryDirectory() as td:
            repo = _make_repo(Path(td), {"requirements.txt": "flask\n"})
            build = detect_build_command(repo, "python")
            self.assertIsNotNone(build)
            self.assertEqual(build["name"], "pip install")

    def test_poetry(self):
        with tempfile.TemporaryDirectory() as td:
            repo = _make_repo(Path(td), {"poetry.lock": ""})
            build = detect_build_command(repo, "python")
            self.assertIsNotNone(build)
            self.assertEqual(build["name"], "poetry install")

    def test_cargo(self):
        with tempfile.TemporaryDirectory() as td:
            repo = _make_repo(Path(td), {"Cargo.toml": "[package]\n"})
            build = detect_build_command(repo, "rust")
            self.assertIsNotNone(build)
            self.assertEqual(build["name"], "cargo build")


class TestDetectExistingGuide(unittest.TestCase):
    def test_ai_guide(self):
        with tempfile.TemporaryDirectory() as td:
            repo = _make_repo(Path(td), {"AI_GUIDE.md": "# Guide\n"})
            self.assertTrue(detect_existing_guide(repo))

    def test_agent_md(self):
        with tempfile.TemporaryDirectory() as td:
            repo = _make_repo(Path(td), {"AGENT.md": "# Agent\n"})
            self.assertTrue(detect_existing_guide(repo))

    def test_no_guide(self):
        with tempfile.TemporaryDirectory() as td:
            repo = _make_repo(Path(td))
            self.assertFalse(detect_existing_guide(repo))


class TestDetectProject(unittest.TestCase):
    def test_full_detection(self):
        with tempfile.TemporaryDirectory() as td:
            repo = _make_repo(Path(td), {
                "requirements.txt": "fastapi\npytest\nruff\n",
                "tests/test_app.py": "",
            })
            result = detect_project(repo)
            self.assertEqual(result["language"], "python")
            self.assertIn("fastapi", result["frameworks"])
            self.assertIsNotNone(result["test_runner"])
            self.assertEqual(result["test_runner"]["name"], "pytest")
            self.assertFalse(result["has_guide"])

    def test_not_a_directory(self):
        with tempfile.TemporaryDirectory() as td:
            not_dir = Path(td) / "file.txt"
            not_dir.write_text("nope")
            with self.assertRaises(FileNotFoundError):
                detect_project(not_dir)


class TestGenerateGuide(unittest.TestCase):
    """D2.T1 validation — generates valid AI_GUIDE.md with tech stack, commands, boundaries."""

    def test_guide_has_required_sections(self):
        result = {
            "language": "python",
            "version": "Python 3.11.0",
            "frameworks": ["fastapi"],
            "test_runner": {"name": "pytest", "command": "python3 -m pytest"},
            "linter": {"name": "ruff", "command": "ruff check ."},
            "build_command": {"name": "pip install", "command": "pip install -r requirements.txt"},
            "has_guide": False,
        }
        guide = generate_guide(result)
        self.assertIn("# AI Guide", guide)
        self.assertIn("Python 3.11.0", guide)
        self.assertIn("fastapi", guide)
        self.assertIn("python3 -m pytest", guide)
        self.assertIn("ruff check .", guide)

    def test_guide_has_boundaries(self):
        result = {
            "language": "python",
            "version": "Python 3.11.0",
            "frameworks": [],
            "test_runner": {"name": "pytest", "command": "python3 -m pytest"},
            "linter": {"name": "ruff", "command": "ruff check ."},
            "build_command": {"name": "pip install", "command": "pip install -r requirements.txt"},
            "has_guide": False,
        }
        guide = generate_guide(result)
        self.assertIn("Auto-approve", guide)
        self.assertIn("Decide and act", guide)
        self.assertIn("Ask first", guide)

    def test_guide_unknown_language(self):
        result = {
            "language": None,
            "version": "unknown",
            "frameworks": [],
            "test_runner": None,
            "linter": None,
            "build_command": None,
            "has_guide": False,
        }
        guide = generate_guide(result)
        self.assertIn("# AI Guide", guide)
        self.assertIn("unknown", guide)
        self.assertIn("Auto-approve", guide)


class TestGenerateOrchestratorConfig(unittest.TestCase):
    def test_config_fields(self):
        result = {
            "language": "python",
            "test_runner": {"name": "pytest", "command": "python3 -m pytest"},
            "linter": {"name": "ruff", "command": "ruff check ."},
        }
        config = generate_orchestrator_config("owner/repo", result)
        self.assertEqual(config["repo"], "owner/repo")
        self.assertEqual(config["label"], "agent-ready")
        self.assertEqual(config["language"], "python")
        self.assertEqual(config["test_command"], "python3 -m pytest")
        self.assertEqual(config["lint_command"], "ruff check .")
        self.assertEqual(config["pipeline"], "standard-pipeline")


class TestOnboardFull(unittest.TestCase):
    """D3.T1 validation — single command sets up everything."""

    def test_dry_run_local_path(self):
        with tempfile.TemporaryDirectory() as td:
            repo = _make_repo(Path(td), {
                "requirements.txt": "fastapi\npytest\n",
                "tests/test_app.py": "",
            })
            result = onboard_full(str(repo), dry_run=True)
            self.assertEqual(result["status"], "dry_run")
            actions = {a["type"]: a for a in result["actions"]}
            self.assertIn("detect", actions)
            self.assertIn("guide", actions)
            self.assertEqual(actions["guide"]["status"], "would_write")
            self.assertIn("config", actions)
            self.assertEqual(actions["config"]["status"], "would_generate")

    def test_dry_run_skips_existing_guide(self):
        with tempfile.TemporaryDirectory() as td:
            repo = _make_repo(Path(td), {
                "requirements.txt": "pytest\n",
                "AI_GUIDE.md": "# Existing Guide\n",
            })
            result = onboard_full(str(repo), dry_run=True)
            actions = {a["type"]: a for a in result["actions"]}
            self.assertEqual(actions["guide"]["status"], "skipped")

    def test_full_writes_guide(self):
        with tempfile.TemporaryDirectory() as td:
            repo = _make_repo(Path(td), {
                "requirements.txt": "pytest\n",
            })
            result = onboard_full(str(repo), dry_run=False)
            self.assertEqual(result["status"], "success")
            guide_path = repo / "AI_GUIDE.md"
            self.assertTrue(guide_path.exists())
            content = guide_path.read_text()
            self.assertIn("# AI Guide", content)

    def test_dry_run_no_side_effects(self):
        """Dry run must not create any files."""
        with tempfile.TemporaryDirectory() as td:
            repo = _make_repo(Path(td), {
                "requirements.txt": "pytest\n",
            })
            files_before = set(repo.rglob("*"))
            onboard_full(str(repo), dry_run=True)
            files_after = set(repo.rglob("*"))
            # Only original files should exist (AI_GUIDE.md should NOT be created)
            self.assertEqual(files_before, files_after)

    def test_unsupported_type_still_works(self):
        """Unknown language repo should still produce valid detection."""
        with tempfile.TemporaryDirectory() as td:
            repo = _make_repo(Path(td), {"README.md": "A project\n"})
            result = onboard_full(str(repo), dry_run=True)
            self.assertEqual(result["status"], "dry_run")


if __name__ == "__main__":
    unittest.main()
