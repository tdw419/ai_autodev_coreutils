#!/usr/bin/env python3
"""
Comprehensive tests for dag.py - Pipeline parser, validator, and topological sort.
"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pytest
from dag import (
    Node, NodeType, Pipeline,
    parse_node, parse_pipeline, pipeline_to_dict,
)


# ─── parse_node tests ────────────────────────────────────────────────

class TestParseNode:
    def test_bash_node_defaults(self):
        raw = {"type": "bash", "command": "echo hello"}
        node = parse_node("test", raw)
        assert node.id == "test"
        assert node.type == NodeType.BASH
        assert node.command == "echo hello"
        assert node.name == "test"
        assert node.timeout_seconds == 300
        assert node.continue_on_error is False

    def test_ai_node_with_role(self):
        raw = {"type": "ai", "prompt": "Do something", "role": "implementer", "max_turns": 10}
        node = parse_node("ai1", raw)
        assert node.type == NodeType.AI
        assert node.prompt == "Do something"
        assert node.role == "implementer"
        assert node.max_turns == 10

    def test_loop_node(self):
        raw = {"type": "loop", "children": ["a", "b"], "max_iterations": 5, "until": "exit_code == 0"}
        node = parse_node("loop1", raw)
        assert node.type == NodeType.LOOP
        assert node.children == ["a", "b"]
        assert node.max_iterations == 5
        assert node.until == "exit_code == 0"

    def test_dependency_node(self):
        raw = {"type": "dependency"}
        node = parse_node("dep1", raw)
        assert node.type == NodeType.DEPENDENCY

    def test_node_with_env(self):
        raw = {"type": "bash", "command": "echo $FOO", "env": {"FOO": "bar"}}
        node = parse_node("env_test", raw)
        assert node.env == {"FOO": "bar"}

    def test_node_custom_name(self):
        raw = {"type": "bash", "command": "ls", "name": "List Files"}
        node = parse_node("ls1", raw)
        assert node.name == "List Files"


# ─── parse_pipeline tests ────────────────────────────────────────────

class TestParsePipeline:
    def test_single_node_pipeline(self):
        raw = {
            "name": "single",
            "nodes": {
                "step1": {"type": "bash", "command": "echo hi"},
            },
        }
        p = parse_pipeline(raw)
        assert p.name == "single"
        assert len(p.nodes) == 1
        assert "step1" in p.nodes

    def test_pipeline_with_dependencies(self):
        raw = {
            "name": "deps",
            "nodes": {
                "a": {"type": "bash", "command": "echo a"},
                "b": {"type": "bash", "command": "echo b", "depends_on": ["a"]},
                "c": {"type": "bash", "command": "echo c", "depends_on": ["a", "b"]},
            },
        }
        p = parse_pipeline(raw)
        assert len(p.nodes) == 3
        order = p.topological_order()
        assert order.index("a") < order.index("b")
        assert order.index("b") < order.index("c")

    def test_empty_nodes_raises(self):
        with pytest.raises(ValueError, match="no nodes"):
            parse_pipeline({"name": "empty", "nodes": {}})

    def test_none_nodes_raises(self):
        with pytest.raises(ValueError, match="no nodes"):
            parse_pipeline({"name": "empty"})

    def test_missing_dependency_raises(self):
        with pytest.raises(ValueError, match="depends on.*nonexistent"):
            parse_pipeline({
                "name": "bad",
                "nodes": {"a": {"type": "bash", "command": "ls", "depends_on": ["nonexistent"]}},
            })

    def test_ai_node_without_prompt_raises(self):
        with pytest.raises(ValueError, match="no prompt"):
            parse_pipeline({
                "name": "bad",
                "nodes": {"a": {"type": "ai"}},
            })

    def test_bash_node_without_command_raises(self):
        with pytest.raises(ValueError, match="no command"):
            parse_pipeline({
                "name": "bad",
                "nodes": {"a": {"type": "bash"}},
            })

    def test_loop_node_without_children_raises(self):
        with pytest.raises(ValueError, match="no children"):
            parse_pipeline({
                "name": "bad",
                "nodes": {"a": {"type": "loop"}},
            })

    def test_loop_child_not_found_raises(self):
        with pytest.raises(ValueError, match="references child.*ghost"):
            parse_pipeline({
                "name": "bad",
                "nodes": {
                    "loop1": {"type": "loop", "children": ["ghost"]},
                },
            })

    def test_node_not_dict_raises(self):
        with pytest.raises(ValueError, match="must be a dict"):
            parse_pipeline({
                "name": "bad",
                "nodes": {"a": "not a dict"},
            })

    def test_cycle_detection(self):
        with pytest.raises(ValueError, match="Cycle"):
            parse_pipeline({
                "name": "cycle",
                "nodes": {
                    "a": {"type": "bash", "command": "echo a", "depends_on": ["b"]},
                    "b": {"type": "bash", "command": "echo b", "depends_on": ["a"]},
                },
            })

    def test_three_node_cycle(self):
        with pytest.raises(ValueError, match="Cycle"):
            parse_pipeline({
                "name": "cycle3",
                "nodes": {
                    "a": {"type": "bash", "command": "a", "depends_on": ["c"]},
                    "b": {"type": "bash", "command": "b", "depends_on": ["a"]},
                    "c": {"type": "bash", "command": "c", "depends_on": ["b"]},
                },
            })


# ─── topological_order tests ─────────────────────────────────────────

class TestTopologicalOrder:
    def test_diamond_dag(self):
        """Diamond: a -> b, a -> c, b -> d, c -> d"""
        raw = {
            "name": "diamond",
            "nodes": {
                "a": {"type": "bash", "command": "a"},
                "b": {"type": "bash", "command": "b", "depends_on": ["a"]},
                "c": {"type": "bash", "command": "c", "depends_on": ["a"]},
                "d": {"type": "bash", "command": "d", "depends_on": ["b", "c"]},
            },
        }
        p = parse_pipeline(raw)
        order = p.topological_order()
        assert order.index("a") < order.index("b")
        assert order.index("a") < order.index("c")
        assert order.index("b") < order.index("d")
        assert order.index("c") < order.index("d")

    def test_disconnected_nodes(self):
        """Multiple entry points (no deps between them)."""
        raw = {
            "name": "disconnected",
            "nodes": {
                "x": {"type": "bash", "command": "x"},
                "y": {"type": "bash", "command": "y"},
                "z": {"type": "bash", "command": "z"},
            },
        }
        p = parse_pipeline(raw)
        order = p.topological_order()
        assert set(order) == {"x", "y", "z"}


# ─── entry_nodes tests ───────────────────────────────────────────────

class TestEntryNodes:
    def test_single_entry(self):
        raw = {
            "name": "single_entry",
            "nodes": {
                "a": {"type": "bash", "command": "a"},
                "b": {"type": "bash", "command": "b", "depends_on": ["a"]},
            },
        }
        p = parse_pipeline(raw)
        assert p.entry_nodes == ["a"]

    def test_multiple_entries(self):
        raw = {
            "name": "multi",
            "nodes": {
                "a": {"type": "bash", "command": "a"},
                "b": {"type": "bash", "command": "b"},
                "c": {"type": "bash", "command": "c", "depends_on": ["a", "b"]},
            },
        }
        p = parse_pipeline(raw)
        assert set(p.entry_nodes) == {"a", "b"}


# ─── pipeline_to_dict tests ──────────────────────────────────────────

class TestPipelineToDict:
    def test_basic_serialization(self):
        raw = {
            "name": "ser",
            "nodes": {
                "a": {"type": "bash", "command": "echo hi"},
            },
        }
        p = parse_pipeline(raw)
        d = pipeline_to_dict(p)
        assert d["name"] == "ser"
        assert "a" in d["nodes"]
        assert d["nodes"]["a"]["type"] == "bash"
        assert "execution_order" in d
        assert "entry_nodes" in d

    def test_ai_node_in_dict(self):
        raw = {
            "name": "ai_ser",
            "nodes": {
                "a": {"type": "ai", "prompt": "Do it", "role": "coder"},
            },
        }
        p = parse_pipeline(raw)
        d = pipeline_to_dict(p)
        assert d["nodes"]["a"]["prompt"] == "Do it"
        assert d["nodes"]["a"]["role"] == "coder"
        assert d["nodes"]["a"]["max_turns"] == 20

    def test_loop_node_in_dict(self):
        raw = {
            "name": "loop_ser",
            "nodes": {
                "loop1": {"type": "loop", "children": ["inner"]},
                "inner": {"type": "bash", "command": "echo inner"},
            },
        }
        p = parse_pipeline(raw)
        d = pipeline_to_dict(p)
        assert d["nodes"]["loop1"]["children"] == ["inner"]
        assert d["nodes"]["loop1"]["max_iterations"] == 3


# ─── load_pipeline tests (file-based) ────────────────────────────────

class TestLoadPipeline:
    def test_load_standard_pipeline(self):
        p = parse_pipeline.__module__  # just to ensure import works
        from dag import load_pipeline
        p = load_pipeline("pipelines/standard-pipeline.yaml")
        assert p.name == "standard-dev-pipeline"
        assert len(p.nodes) == 7

    def test_load_test_pipeline(self):
        from dag import load_pipeline
        p = load_pipeline("pipelines/test-pipeline.yaml")
        assert len(p.nodes) >= 1

    def test_file_not_found(self):
        from dag import load_pipeline
        with pytest.raises(FileNotFoundError):
            load_pipeline("nonexistent.yaml")

    def test_load_invalid_yaml(self, tmp_path):
        bad = tmp_path / "bad.yaml"
        bad.write_text("not: valid: yaml: [unbalanced")
        from dag import load_pipeline
        # yaml.safe_load will still parse some things; this tests the flow
        # If the file contains invalid YAML, we get a yaml error
        import yaml
        bad.write_text("- just\n  a list\n")
        with pytest.raises(ValueError, match="YAML dict"):
            load_pipeline(str(bad))


# ─── Pipeline defaults ───────────────────────────────────────────────

class TestPipelineDefaults:
    def test_default_version(self):
        raw = {"nodes": {"a": {"type": "bash", "command": "ls"}}}
        p = parse_pipeline(raw)
        assert p.version == "1.0"

    def test_custom_version(self):
        raw = {"version": "2.1", "nodes": {"a": {"type": "bash", "command": "ls"}}}
        p = parse_pipeline(raw)
        assert p.version == "2.1"

    def test_pipeline_env(self):
        raw = {
            "env": {"PROJECT": "test"},
            "nodes": {"a": {"type": "bash", "command": "echo $PROJECT"}},
        }
        p = parse_pipeline(raw)
        assert p.env == {"PROJECT": "test"}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
