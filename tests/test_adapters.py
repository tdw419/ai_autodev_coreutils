"""Tests for pipe adapters."""

import json
from pathlib import Path

from autodev_coreutils.adapters import (
    possibilities_to_roadmap,
    roadmap_to_task_spec,
    tasks_to_rfl_seeds,
    _extract_paths,
)


def test_extract_paths():
    """_extract_paths walks a tree and returns leaf paths."""
    tree = {
        "description": "root",
        "fertility": 1.0,
        "children": [
            {
                "description": "branch A",
                "fertility": 0.8,
                "children": [
                    {"description": "leaf A1", "fertility": 0.5, "children": []},
                ],
            },
            {
                "description": "branch B",
                "fertility": 0.6,
                "children": [
                    {"description": "leaf B1", "fertility": 0.3, "children": []},
                ],
            },
        ],
    }
    paths = _extract_paths(tree)
    assert len(paths) == 2
    assert "branch A" in paths[0]["name"]
    assert "branch B" in paths[1]["name"]


def test_possibilities_to_roadmap(tmp_path):
    """possibilities_to_roadmap produces valid YAML."""
    tree = {
        "description": "root",
        "fertility": 1.0,
        "children": [
            {
                "description": "idea A",
                "rationale": "because A",
                "fertility": 0.8,
                "children": [
                    {"description": "detail", "fertility": 0.5, "children": []},
                ],
            },
        ],
    }
    tree_file = tmp_path / "tree.json"
    tree_file.write_text(json.dumps(tree))

    result = possibilities_to_roadmap(tree_file)
    assert "phases:" in result
    assert "idea A" in result


def test_possibilities_to_roadmap_output_file(tmp_path):
    """possibilities_to_roadmap writes to output file."""
    tree_file = tmp_path / "tree.json"
    tree_file.write_text(json.dumps({
        "description": "root", "fertility": 1.0, "children": [],
    }))
    output_file = tmp_path / "roadmap.yaml"

    possibilities_to_roadmap(tree_file, output_file)
    assert output_file.exists()
    content = output_file.read_text()
    assert "phases:" in content


def test_roadmap_to_task_spec(tmp_path):
    """roadmap_to_task_spec converts YAML to markdown spec."""
    import yaml
    roadmap = {
        "title": "Test Project",
        "description": "A test",
        "phases": [
            {
                "id": "p1",
                "title": "Foundation",
                "goal": "Get it working",
                "deliverables": [
                    {
                        "name": "Core",
                        "description": "Core module",
                        "tasks": [
                            {"title": "Setup", "status": "done"},
                            {"title": "Implement", "status": "planned", "description": "Do the thing"},
                        ],
                    },
                ],
            },
        ],
    }
    yaml_file = tmp_path / "roadmap.yaml"
    yaml_file.write_text(yaml.dump(roadmap))

    result = roadmap_to_task_spec(yaml_file)
    assert "# Test Project" in result
    assert "Foundation" in result
    assert "[ ] Implement" in result
    # Done tasks should be filtered out
    assert "[ ] Setup" not in result


def test_tasks_to_rfl_seeds(tmp_path):
    """tasks_to_rfl_seeds generates seed files from task markdown."""
    tasks_dir = tmp_path / "tasks"
    tasks_dir.mkdir()

    for i in range(3):
        (tasks_dir / f"task_{i:03d}.md").write_text(f"# Task {i}\nDo thing {i}")

    seeds = tasks_to_rfl_seeds(tasks_dir)
    assert len(seeds) == 3
    for seed in seeds:
        assert seed.exists()
        content = seed.read_text()
        assert "AI_GUIDE.md" in content
        assert "rfl" not in seed.name.lower()  # seeds go in same dir


def test_tasks_to_rfl_seeds_output_dir(tmp_path):
    """tasks_to_rfl_seeds can output to different directory."""
    tasks_dir = tmp_path / "tasks"
    tasks_dir.mkdir()
    (tasks_dir / "task_000.md").write_text("# Task 0")

    out_dir = tmp_path / "seeds"
    out_dir.mkdir()

    seeds = tasks_to_rfl_seeds(tasks_dir, out_dir)
    assert len(seeds) == 1
    assert str(seeds[0]).startswith(str(out_dir))
