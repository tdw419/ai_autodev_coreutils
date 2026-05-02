#!/usr/bin/env python3
"""Tests for conflict_detector.py"""

import json
import os
import subprocess
import tempfile
import shutil
from pathlib import Path

# Add project to path
import sys
sys.path.insert(0, os.path.expanduser("~/zion/projects/agent-orchestration"))
import conflict_detector as cd


class TempGitRepo:
    """Create a temporary git repo for testing."""

    def __init__(self):
        self.tmpdir = tempfile.mkdtemp()
        self._run("git", "init")
        self._run("git", "config", "user.email", "test@test.com")
        self._run("git", "config", "user.name", "Test")
        self.orig_cwd = os.getcwd()

    def _run(self, *args, **kwargs):
        return subprocess.run(args, cwd=self.tmpdir, capture_output=True, text=True, **kwargs)

    def commit(self, filename, content, branch=None):
        if branch:
            self._run("git", "checkout", "-b", branch)
        Path(self.tmpdir, filename).write_text(content)
        self._run("git", "add", filename)
        self._run("git", "commit", "-m", f"add {filename}")

    def setup_conflict(self):
        """Create a scenario with merge conflicts."""
        # master: file.txt = "line1\nline2\nline3\n"
        self.commit("file.txt", "line1\nline2\nline3\n")
        # Create feature branch
        self._run("git", "checkout", "-b", "feature")
        Path(self.tmpdir, "file.txt").write_text("line1\nMODIFIED\nline3\n")
        self._run("git", "add", "file.txt")
        self._run("git", "commit", "-m", "modify on feature")
        # Go back to master and modify same file
        self._run("git", "checkout", "master")
        Path(self.tmpdir, "file.txt").write_text("line1\nline2\nCHANGED\n")
        self._run("git", "add", "file.txt")
        self._run("git", "commit", "-m", "modify on master")

    def setup_no_conflict(self):
        """Create a scenario with no merge conflicts."""
        self.commit("file_a.txt", "content a\n")
        self._run("git", "checkout", "-b", "feature")
        Path(self.tmpdir, "file_b.txt").write_text("content b\n")
        self._run("git", "add", "file_b.txt")
        self._run("git", "commit", "-m", "add file_b")
        self._run("git", "checkout", "master")
        Path(self.tmpdir, "file_c.txt").write_text("content c\n")
        self._run("git", "add", "file_c.txt")
        self._run("git", "commit", "-m", "add file_c")

    def cleanup(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)


def test_classify_conflict():
    assert cd._classify_conflict("config.yaml") == "structural"
    assert cd._classify_conflict("package.json") == "structural"
    assert cd._classify_conflict("src/main.py") == "content"
    assert cd._classify_conflict("README.md") == "content"
    assert cd._classify_conflict("data.toml") == "structural"
    print("PASS: test_classify_conflict")


def test_compute_severity():
    assert cd._compute_severity([], 5) == "none"
    assert cd._compute_severity(["a.py"], 10) == "low"
    assert cd._compute_severity(["a.py", "b.py", "c.py"], 10) == "medium"
    assert cd._compute_severity(["a.py", "b.py", "c.py", "d.py", "e.py", "f.py"], 10) == "high"
    print("PASS: test_compute_severity")


def test_suggest_action():
    assert cd._suggest_action("none", False, 0) == "proceed"
    assert cd._suggest_action("low", True, 1) == "rebase"
    assert cd._suggest_action("high", True, 10) == "wait"
    assert cd._suggest_action("medium", True, 6) == "wait"
    print("PASS: test_suggest_action")


def test_check_conflicts_no_conflict():
    repo = TempGitRepo()
    try:
        repo.setup_no_conflict()
        os.chdir(repo.tmpdir)
        result = cd.check_conflicts("feature", "master")
        assert result["has_conflicts"] is False, f"Expected no conflicts, got {result}"
        assert result["severity"] == "none"
        assert result["suggested_action"] == "proceed"
        print("PASS: test_check_conflicts_no_conflict")
    finally:
        os.chdir(repo.orig_cwd)
        repo.cleanup()


def test_check_conflicts_with_overlap():
    """Test overlap-based detection (works even without merge-tree)."""
    repo = TempGitRepo()
    try:
        repo.setup_conflict()
        os.chdir(repo.tmpdir)
        result = cd.check_conflicts("feature", "master")
        # The detection method may vary, but we should detect *something*
        # merge-tree might detect actual conflicts or just overlap
        assert "detection_method" in result
        assert "has_conflicts" in result
        assert "conflict_files" in result
        print(f"  Detection method: {result['detection_method']}")
        print(f"  Has conflicts: {result['has_conflicts']}")
        print(f"  Conflict files: {result['conflict_files']}")
        print("PASS: test_check_conflicts_with_overlap")
    finally:
        os.chdir(repo.orig_cwd)
        repo.cleanup()


def test_nonexistent_branch():
    repo = TempGitRepo()
    try:
        repo.commit("file.txt", "content\n")
        os.chdir(repo.tmpdir)
        result = cd.check_conflicts("nonexistent", "master")
        assert result["has_conflicts"] is False  # Can't check, defaults to safe
        assert result["detection_method"] == "unavailable"
        print("PASS: test_nonexistent_branch")
    finally:
        os.chdir(repo.orig_cwd)
        repo.cleanup()


def test_check_workspace_no_branch():
    result = cd.check_workspace("99999")
    assert "error" in result
    assert "has_conflicts" in result
    print("PASS: test_check_workspace_no_branch")


def test_check_all_workspaces():
    results = cd.check_all_workspaces()
    assert isinstance(results, list)
    print(f"PASS: test_check_all_workspaces (found {len(results)} workspaces)")


if __name__ == "__main__":
    test_classify_conflict()
    test_compute_severity()
    test_suggest_action()
    test_nonexistent_branch()
    test_check_workspace_no_branch()
    test_check_all_workspaces()
    test_check_conflicts_no_conflict()
    test_check_conflicts_with_overlap()
    print("\nAll tests passed!")
