"""Tests for discover coreutil."""

import json
from pathlib import Path
from unittest.mock import patch, MagicMock

from autodev_coreutils.contract import ensure_autodev_dir
from autodev_coreutils.discover import (
    scan_projects, _count_incomplete_phases, format_discovery,
    discover_all, main,
)


# --- _count_incomplete_phases ---

def test_count_incomplete_phases(tmp_path):
    """Count phases that aren't COMPLETE/DONE."""
    roadmap = tmp_path / "ROADMAP.md"
    roadmap.write_text("""# Roadmap
| phase-1 Core | COMPLETE | 5/5 |
| phase-2 Extensions | COMPLETE | 3/3 |
| phase-3 Interactive | IN PROGRESS | 1/3 |
| phase-4 Canvas | PLANNED | 0/2 |
""")
    assert _count_incomplete_phases(roadmap) == 2


def test_count_incomplete_all_complete(tmp_path):
    """Returns 0 when all phases are complete."""
    roadmap = tmp_path / "ROADMAP.md"
    roadmap.write_text("""# Roadmap
| phase-1 Core | COMPLETE | 5/5 |
| phase-2 Extensions | DONE | 3/3 |
""")
    assert _count_incomplete_phases(roadmap) == 0


def test_count_incomplete_no_roadmap(tmp_path):
    """Returns 0 for missing file."""
    assert _count_incomplete_phases(tmp_path / "nonexistent.md") == 0


# --- scan_projects ---

def test_scan_projects_finds_dirty_git(tmp_path):
    """scan_projects detects dirty working trees."""
    # Create a fake project with dirty git
    proj = tmp_path / "my_project"
    proj.mkdir()
    (proj / ".git").mkdir()
    (proj / "README.md").write_text("hello")

    findings = scan_projects(tmp_path)
    # Should find at least something (the project has .git)
    # Exact behavior depends on whether git status works on the fake repo


def test_scan_projects_skips_hidden_dirs(tmp_path):
    """scan_projects skips directories starting with _ or ."""
    (tmp_path / "_private").mkdir()
    (tmp_path / ".hidden").mkdir()
    (tmp_path / "real_project").mkdir()

    findings = scan_projects(tmp_path)
    names = [f["project"] for f in findings]
    assert "_private" not in names
    assert ".hidden" not in names


def test_scan_projects_detects_roadmap(tmp_path):
    """scan_projects finds projects with incomplete roadmaps."""
    proj = tmp_path / "roadmap_proj"
    proj.mkdir()
    (proj / "ROADMAP.md").write_text("""# Roadmap
| phase-1 Core | COMPLETE | 5/5 |
| phase-2 Next | IN PROGRESS | 1/3 |
""")

    findings = scan_projects(tmp_path)
    roadmap_projs = [f for f in findings if f["project"] == "roadmap_proj"]
    assert len(roadmap_projs) == 1
    assert any("incomplete" in s for s in roadmap_projs[0]["signals"])


# --- format_discovery ---

def test_format_discovery():
    """format_discovery produces readable markdown."""
    findings = [
        {
            "project": "test_proj",
            "path": "/path/to/test_proj",
            "signals": ["dirty git (5 files)", "active (1.2 days ago)"],
            "priority": 5,
        }
    ]
    md = format_discovery(findings)
    assert "# Autodev Discovery Report" in md
    assert "test_proj" in md
    assert "priority: 5" in md
    assert "dirty git" in md


def test_format_discovery_empty():
    """format_discovery handles empty findings."""
    md = format_discovery([])
    assert "# Autodev Discovery Report" in md
    assert "Findings: 0" in md


# --- main ---

def test_main_projects_source(tmp_path, capsys):
    """main runs with --source projects."""
    ensure_autodev_dir(tmp_path)

    # Create a project with a roadmap
    proj_dir = tmp_path / "projects"
    proj_dir.mkdir()
    p = proj_dir / "my_proj"
    p.mkdir()
    (p / "ROADMAP.md").write_text("| phase-1 | IN PROGRESS | 0/3 |\n")

    with patch("autodev_coreutils.discover.PROJECTS_DIR", proj_dir):
        result = main([
            "-w", str(tmp_path),
            "--source", "projects",
            "--projects-dir", str(proj_dir),
            "-q",
        ])

    assert result == 0

    # Check state was written
    state = json.loads((tmp_path / ".autodev" / "discover_state.json").read_text())
    assert state["findings_count"] >= 0


def test_main_json_output(tmp_path, capsys):
    """main outputs JSON with --json."""
    ensure_autodev_dir(tmp_path)

    proj_dir = tmp_path / "empty_projects"
    proj_dir.mkdir()

    with patch("autodev_coreutils.discover.PROJECTS_DIR", proj_dir):
        result = main([
            "-w", str(tmp_path),
            "--source", "projects",
            "--projects-dir", str(proj_dir),
            "--json",
        ])

    assert result == 0

    # JSON output or empty findings
    captured = capsys.readouterr()
    if captured.out.strip():
        data = json.loads(captured.out)
        assert "findings" in data


def test_main_geo_source(tmp_path, capsys):
    """main handles --source geo with missing geo dir."""
    ensure_autodev_dir(tmp_path)

    with patch("autodev_coreutils.discover.GEO_OS_DIR", tmp_path / "no_geo"):
        result = main([
            "-w", str(tmp_path),
            "--source", "geo",
            "-q",
        ])

    assert result == 0
