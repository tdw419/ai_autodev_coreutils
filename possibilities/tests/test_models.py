"""Tests for models module -- PossibilityNode serialization and defaults."""

import time
import uuid

import pytest

from possibilities.models import PossibilityNode, ExplorationConfig


# ---------------------------------------------------------------------------
# PossibilityNode defaults
# ---------------------------------------------------------------------------

class TestPossibilityNodeDefaults:
    def test_auto_generated_id(self):
        node = PossibilityNode()
        assert len(node.id) == 8
        # Verify it's hex
        int(node.id, 16)

    def test_unique_ids(self):
        ids = {PossibilityNode().id for _ in range(100)}
        assert len(ids) == 100

    def test_default_fields(self):
        node = PossibilityNode()
        assert node.title == ""
        assert node.description == ""
        assert node.enables == []
        assert node.risk == ""
        assert node.category == ""
        assert node.depth == 0
        assert node.parent_id is None
        assert node.children == []
        assert node.fertility_score == 0.0
        assert node.direct_fertility == 0
        assert node.total_descendants == 0
        assert node.model_used == ""
        assert node.explored is False
        assert node.pruned is False
        assert node.prune_reason == ""
        assert isinstance(node.created_at, float)

    def test_created_at_is_recent(self):
        before = time.time()
        node = PossibilityNode()
        after = time.time()
        assert before <= node.created_at <= after

    def test_explicit_values(self):
        node = PossibilityNode(
            id="custom",
            title="Test Idea",
            description="A test",
            enables=["a", "b"],
            risk="might break",
            category="wildcard",
            depth=2,
            parent_id="parent",
            model_used="test-model",
            explored=True,
        )
        assert node.id == "custom"
        assert node.title == "Test Idea"
        assert node.category == "wildcard"
        assert node.depth == 2
        assert node.explored is True


# ---------------------------------------------------------------------------
# PossibilityNode.to_dict
# ---------------------------------------------------------------------------

class TestPossibilityNodeToDict:
    def test_flat_node(self):
        node = PossibilityNode(id="abc123", title="Idea", description="Desc")
        d = node.to_dict()
        assert d["id"] == "abc123"
        assert d["title"] == "Idea"
        assert d["description"] == "Desc"
        assert d["children"] == []
        assert d["enables"] == []

    def test_with_children(self):
        child = PossibilityNode(id="c1", title="Child", depth=1)
        parent = PossibilityNode(id="p1", title="Parent", children=[child])
        d = parent.to_dict()
        assert len(d["children"]) == 1
        assert d["children"][0]["id"] == "c1"
        assert d["children"][0]["title"] == "Child"

    def test_nested_children(self):
        grandchild = PossibilityNode(id="gc", title="GC", depth=2)
        child = PossibilityNode(id="c", title="C", depth=1, children=[grandchild])
        root = PossibilityNode(id="r", title="R", children=[child])
        d = root.to_dict()
        assert d["children"][0]["children"][0]["id"] == "gc"

    def test_all_fields_present(self):
        node = PossibilityNode(
            id="x", title="T", description="D",
            enables=["e1"], risk="R", category="obvious",
            depth=1, parent_id="p",
            fertility_score=3.5, direct_fertility=2, total_descendants=5,
            model_used="m", explored=True, pruned=True, prune_reason="dup",
        )
        d = node.to_dict()
        assert set(d.keys()) >= {
            "id", "title", "description", "enables", "risk", "category",
            "depth", "parent_id", "children", "fertility_score",
            "direct_fertility", "total_descendants", "model_used",
            "explored", "pruned", "prune_reason", "created_at",
        }


# ---------------------------------------------------------------------------
# PossibilityNode.from_dict
# ---------------------------------------------------------------------------

class TestPossibilityNodeFromDict:
    def test_roundtrip_flat(self):
        original = PossibilityNode(
            id="rt1", title="Round", description="Trip",
            enables=["a"], risk="low", category="contrarian",
            depth=3, parent_id="p1",
            fertility_score=2.0, direct_fertility=1, total_descendants=4,
            model_used="m1", explored=True, pruned=False, prune_reason="",
        )
        d = original.to_dict()
        restored = PossibilityNode.from_dict(d)
        assert restored.id == original.id
        assert restored.title == original.title
        assert restored.description == original.description
        assert restored.enables == original.enables
        assert restored.risk == original.risk
        assert restored.category == original.category
        assert restored.depth == original.depth
        assert restored.parent_id == original.parent_id
        assert restored.fertility_score == original.fertility_score
        assert restored.direct_fertility == original.direct_fertility
        assert restored.total_descendants == original.total_descendants
        assert restored.model_used == original.model_used
        assert restored.explored == original.explored
        assert restored.pruned == original.pruned
        assert restored.prune_reason == original.prune_reason
        assert restored.children == []

    def test_roundtrip_with_children(self):
        child = PossibilityNode(id="c", title="Child", depth=1)
        parent = PossibilityNode(id="p", title="Parent", children=[child])
        d = parent.to_dict()
        restored = PossibilityNode.from_dict(d)
        assert len(restored.children) == 1
        assert restored.children[0].id == "c"
        assert restored.children[0].title == "Child"

    def test_roundtrip_deeply_nested(self):
        gc = PossibilityNode(id="gc", title="Grandchild", depth=2)
        c = PossibilityNode(id="c", title="Child", depth=1, children=[gc])
        root = PossibilityNode(id="r", title="Root", children=[c])
        restored = PossibilityNode.from_dict(root.to_dict())
        assert restored.children[0].children[0].title == "Grandchild"

    def test_missing_fields_get_defaults(self):
        minimal = {"id": "x"}
        node = PossibilityNode.from_dict(minimal)
        assert node.id == "x"
        assert node.title == ""
        assert node.description == ""
        assert node.children == []
        assert node.depth == 0
        assert node.parent_id is None

    def test_empty_dict(self):
        node = PossibilityNode.from_dict({})
        assert node.title == ""
        assert len(node.id) == 8  # auto-generated

    def test_missing_id_gets_generated(self):
        node = PossibilityNode.from_dict({"title": "T"})
        assert len(node.id) == 8


# ---------------------------------------------------------------------------
# ExplorationConfig
# ---------------------------------------------------------------------------

class TestExplorationConfig:
    def test_defaults(self):
        config = ExplorationConfig()
        assert config.seed_question == "What should we build next?"
        assert config.project_path == "."
        assert config.max_depth == 3
        assert config.branch_min == 3
        assert config.branch_max == 7
        assert config.model == "openai/glm-5.1"
        assert config.complexity == "balanced"
        assert config.decay == 0.7
        assert config.dedup_threshold == 0.85
        assert config.max_nodes == 80
        assert config.explore_strategy == "bfs"
        assert config.context_files == []
        assert config.temperature == 0.9
        assert config.show_paths == 10

    def test_custom_values(self):
        config = ExplorationConfig(
            seed_question="Custom?",
            project_path="/tmp",
            max_depth=5,
            complexity="fast",
        )
        assert config.seed_question == "Custom?"
        assert config.max_depth == 5
        assert config.complexity == "fast"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
