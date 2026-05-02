#!/usr/bin/env python3
"""Tests for config_watcher.py"""

import json
import os
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, os.path.expanduser("~/zion/projects/agent-orchestration"))
import config_watcher as cw


class TempConfig:
    """Create temporary config files for testing."""

    def __init__(self):
        self.tmpdir = tempfile.mkdtemp()
        self.config_dir = Path(self.tmpdir)
        self.config_file = self.config_dir / "orchestrator.yaml"
        self.roles_dir = self.config_dir / "roles"
        self.pipelines_dir = self.config_dir / "pipelines"
        self.roles_dir.mkdir()
        self.pipelines_dir.mkdir()

        # Write initial config
        self.config_file.write_text("max_concurrent: 2\nlabel: agent-ready\n")
        (self.roles_dir / "implementer.yaml").write_text("name: implementer\n")
        (self.pipelines_dir / "test.yaml").write_text("name: test\n")

    def cleanup(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)


def test_file_hash():
    """Test file hashing."""
    tmp = TempConfig()
    try:
        h1 = cw._file_hash(tmp.config_file)
        h2 = cw._file_hash(tmp.config_file)
        assert h1 == h2, "Same file should have same hash"
        assert len(h1) == 64, "SHA256 should be 64 chars"
        # Modify file
        tmp.config_file.write_text("max_concurrent: 3\n")
        h3 = cw._file_hash(tmp.config_file)
        assert h1 != h3, "Modified file should have different hash"
        print("PASS: test_file_hash")
    finally:
        tmp.cleanup()


def test_load_yaml():
    """Test YAML loading."""
    tmp = TempConfig()
    try:
        data = cw._load_yaml(tmp.config_file)
        assert data is not None
        assert data["max_concurrent"] == 2
        assert data["label"] == "agent-ready"
        # Non-existent file
        assert cw._load_yaml(Path("/nonexistent/foo.yaml")) is None
        print("PASS: test_load_yaml")
    finally:
        tmp.cleanup()


def test_simple_diff():
    """Test diff generation."""
    old = {"max_concurrent": 2, "label": "agent-ready", "repos": []}
    new = {"max_concurrent": 5, "label": "agent-ready", "repos": ["test/repo"]}
    diffs = cw._simple_diff(old, new)
    assert any("max_concurrent" in d for d in diffs), "Should detect max_concurrent change"
    assert any("repos" in d for d in diffs), "Should detect repos change"
    # No changes
    no_diffs = cw._simple_diff(old, old)
    assert len(no_diffs) == 0, "Identical dicts should have no diffs"
    print("PASS: test_simple_diff")


def test_watcher_init():
    """Test watcher initialization."""
    tmp = TempConfig()
    try:
        watcher = cw.ConfigWatcher(
            config_path=str(tmp.config_file),
            roles_dir=str(tmp.roles_dir),
            pipelines_dir=str(tmp.pipelines_dir),
        )
        state = watcher.get_state()
        assert str(tmp.config_file) in state
        assert any(str(tmp.roles_dir) in k for k in state)
        assert any(str(tmp.pipelines_dir) in k for k in state)
        print("PASS: test_watcher_init")
    finally:
        tmp.cleanup()


def test_watcher_detect_change():
    """Test that watcher detects config file changes."""
    tmp = TempConfig()
    try:
        watcher = cw.ConfigWatcher(
            config_path=str(tmp.config_file),
            roles_dir=str(tmp.roles_dir),
            pipelines_dir=str(tmp.pipelines_dir),
        )
        # No changes initially
        events = watcher.check()
        assert len(events) == 0, f"Should have no changes initially, got {events}"

        # Modify config
        time.sleep(0.1)
        tmp.config_file.write_text("max_concurrent: 5\nlabel: agent-ready\n")
        events = watcher.check()
        assert len(events) == 1, f"Should detect one change, got {len(events)}"
        assert events[0]["change"] == "modified"
        assert events[0]["config_type"] == "orchestrator"
        print("PASS: test_watcher_detect_change")
    finally:
        tmp.cleanup()


def test_watcher_detect_new_role():
    """Test that watcher detects new role file."""
    tmp = TempConfig()
    try:
        watcher = cw.ConfigWatcher(
            config_path=str(tmp.config_file),
            roles_dir=str(tmp.roles_dir),
            pipelines_dir=str(tmp.pipelines_dir),
        )
        # Initial scan
        watcher.check()
        # Add new role
        (tmp.roles_dir / "reviewer.yaml").write_text("name: reviewer\n")
        events = watcher.check()
        assert any(e["change"] == "added" and e["config_type"] == "role" for e in events), \
            "Should detect new role file"
        print("PASS: test_watcher_detect_new_role")
    finally:
        tmp.cleanup()


def test_get_set_value():
    """Test get_value and set_value."""
    tmp = TempConfig()
    try:
        watcher = cw.ConfigWatcher(
            config_path=str(tmp.config_file),
            roles_dir=str(tmp.roles_dir),
            pipelines_dir=str(tmp.pipelines_dir),
        )
        assert watcher.get_value("max_concurrent") == 2
        assert watcher.get_value("label") == "agent-ready"
        assert watcher.get_value("nonexistent") is None

        # Set value (dry run)
        result = watcher.set_value("max_concurrent", 5, dry_run=True)
        assert result["success"] is True
        assert result["dry_run"] is True
        assert result["old_value"] == 2
        assert result["new_value"] == 5
        # Value shouldn't change
        assert watcher.get_value("max_concurrent") == 2

        # Set value for real
        result = watcher.set_value("max_concurrent", 5, dry_run=False)
        assert result["success"] is True
        assert watcher.get_value("max_concurrent") == 5
        print("PASS: test_get_set_value")
    finally:
        tmp.cleanup()


def test_validate():
    """Test config validation."""
    tmp = TempConfig()
    try:
        watcher = cw.ConfigWatcher(
            config_path=str(tmp.config_file),
            roles_dir=str(tmp.roles_dir),
            pipelines_dir=str(tmp.pipelines_dir),
        )
        errors = watcher.validate()
        # Should have errors because no repos configured
        assert len(errors) > 0, "Should detect missing repos"
        assert any("repo" in e.lower() for e in errors), "Should mention repos"
        print("PASS: test_validate")
    finally:
        tmp.cleanup()


if __name__ == "__main__":
    test_file_hash()
    test_load_yaml()
    test_simple_diff()
    test_watcher_init()
    test_watcher_detect_change()
    test_watcher_detect_new_role()
    test_get_set_value()
    test_validate()
    print("\nAll config_watcher tests passed!")
