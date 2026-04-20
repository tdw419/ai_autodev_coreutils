"""Tests for snapshot coreutil."""

import json
from pathlib import Path

from autodev_coreutils.contract import ensure_autodev_dir, write_state
from autodev_coreutils.snapshot import take_snapshot, list_snapshots, main


def test_take_snapshot(tmp_path):
    """take_snapshot captures .autodev/ state."""
    ad = ensure_autodev_dir(tmp_path)
    write_state(tmp_path, "test_tool", {"status": "ok"})

    result = take_snapshot(tmp_path, tag="test-snap")
    assert result["tag"] == "test-snap"
    assert "test_tool" in result["tool_states"]
    assert result["tool_states"]["test_tool"]["status"] == "ok"
    assert "snap_test-snap.tar.gz" in result["snapshot_file"]


def test_list_snapshots(tmp_path):
    """list_snapshots returns saved snapshots."""
    ad = ensure_autodev_dir(tmp_path)
    take_snapshot(tmp_path, tag="snap1")
    take_snapshot(tmp_path, tag="snap2")

    snaps = list_snapshots(tmp_path)
    assert len(snaps) == 2
    tags = [s["tag"] for s in snaps]
    assert "snap1" in tags
    assert "snap2" in tags


def test_list_snapshots_empty(tmp_path):
    """list_snapshots returns empty when no snapshots."""
    snaps = list_snapshots(tmp_path)
    assert snaps == []


def test_main_list(tmp_path, capsys):
    """autodev-snapshot --list shows snapshots."""
    ad = ensure_autodev_dir(tmp_path)
    take_snapshot(tmp_path, tag="test-list")

    result = main(["-w", str(tmp_path), "--list"])
    assert result == 0
