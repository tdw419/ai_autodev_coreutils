"""Tests for autodev_coreutils shared contract."""

import json
import tempfile
from pathlib import Path

from autodev_coreutils.contract import (
    find_project, ensure_autodev_dir, write_state, read_state,
    write_spec, read_spec, make_parser,
)


def test_find_project_with_git(tmp_path):
    """find_project finds a directory with .git."""
    (tmp_path / ".git").mkdir()
    assert find_project(str(tmp_path)) == tmp_path


def test_find_project_with_pyproject(tmp_path):
    """find_project finds a directory with pyproject.toml."""
    (tmp_path / "pyproject.toml").write_text("[project]")
    assert find_project(str(tmp_path)) == tmp_path


def test_find_project_walks_up(tmp_path):
    """find_project walks up to find project root."""
    (tmp_path / ".git").mkdir()
    sub = tmp_path / "src" / "pkg"
    sub.mkdir(parents=True)
    assert find_project(str(sub)) == tmp_path


def test_ensure_autodev_dir(tmp_path):
    """ensure_autodev_dir creates .autodev/."""
    ad = ensure_autodev_dir(tmp_path)
    assert ad == tmp_path / ".autodev"
    assert ad.exists()


def test_write_read_state(tmp_path):
    """write_state and read_state round-trip."""
    data = {"status": "ok", "count": 5}
    write_state(tmp_path, "test_tool", data)
    result = read_state(tmp_path, "test_tool")
    assert result["status"] == "ok"
    assert result["count"] == 5
    assert "updated_at" in result
    assert result["tool"] == "test_tool"


def test_read_state_missing(tmp_path):
    """read_state returns None for missing state."""
    assert read_state(tmp_path, "nonexistent") is None


def test_write_read_spec(tmp_path):
    """write_spec and read_spec round-trip."""
    ensure_autodev_dir(tmp_path)
    md = "# Test Spec\n\nSome content here."
    write_spec(tmp_path, "plan", md)
    result = read_spec(tmp_path, "plan")
    assert result == md


def test_read_spec_missing(tmp_path):
    """read_spec returns None for missing spec."""
    assert read_spec(tmp_path, "nonexistent") is None


def test_make_parser():
    """make_parser creates a parser with standard flags."""
    parser = make_parser("test", "Test tool")
    args = parser.parse_args(["-w", "/tmp", "--json", "-q"])
    assert args.workdir == "/tmp"
    assert args.json_output is True
    assert args.quiet is True
