"""Tests for merge module -- tree loading, merging, and helpers."""

import json
import os
import tempfile

import pytest

from possibilities.merge import (
    _collect_all_nodes,
    _normalize_question,
    _reparent_subtree,
    load_tree,
    merge_trees,
)
from possibilities.models import PossibilityNode


# ---------------------------------------------------------------------------
# _normalize_question
# ---------------------------------------------------------------------------

class TestNormalizeQuestion:
    def test_strips_question_mark(self):
        assert _normalize_question("What to build?") == "what to build"

    def test_lowercases(self):
        assert _normalize_question("WHAT TO BUILD") == "what to build"

    def test_strips_whitespace(self):
        assert _normalize_question("  What?  ") == "what"

    def test_no_question_mark(self):
        assert _normalize_question("what to build") == "what to build"


# ---------------------------------------------------------------------------
# _reparent_subtree
# ---------------------------------------------------------------------------

class TestReparentSubtree:
    def test_updates_parent_and_depth(self):
        node = PossibilityNode(id="child", depth=1, parent_id="old_parent")
        child = PossibilityNode(id="grandchild", depth=2, parent_id="child")
        node.children = [child]
        _reparent_subtree(node, "new_parent", 3)
        assert node.parent_id == "new_parent"
        assert node.depth == 3
        assert child.parent_id == "child"
        assert child.depth == 4


# ---------------------------------------------------------------------------
# _collect_all_nodes
# ---------------------------------------------------------------------------

class TestCollectAllNodes:
    def test_single_node(self):
        node = PossibilityNode(title="Root")
        result = _collect_all_nodes(node)
        assert len(result) == 1

    def test_with_children(self):
        root = PossibilityNode(title="Root")
        root.children = [
            PossibilityNode(title="A"),
            PossibilityNode(title="B"),
        ]
        result = _collect_all_nodes(root)
        assert len(result) == 3


# ---------------------------------------------------------------------------
# load_tree
# ---------------------------------------------------------------------------

class TestLoadTree:
    def test_loads_valid_json(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({
                "id": "root",
                "title": "Root",
                "description": "Q?",
                "children": [{"id": "c1", "title": "Child", "depth": 1}],
            }, f)
            f.flush()
            tree = load_tree(f.name)
        assert tree.title == "Root"
        assert len(tree.children) == 1
        os.unlink(f.name)


# ---------------------------------------------------------------------------
# merge_trees
# ---------------------------------------------------------------------------

class TestMergeTrees:
    def _make_tree(self, question="What to build?", ideas=None):
        root = PossibilityNode(title="Root", description=question)
        for idea in (ideas or ["Idea A", "Idea B"]):
            root.children.append(PossibilityNode(title=idea, depth=1))
        return root

    def test_single_tree_passthrough(self):
        tree = self._make_tree()
        merged = merge_trees([tree])
        assert merged is tree

    def test_two_different_questions(self):
        t1 = self._make_tree("Question A?", ["Alpha", "Beta"])
        t2 = self._make_tree("Question B?", ["Gamma"])
        merged = merge_trees([t1, t2])
        # Should have 2 intermediate nodes (one per question)
        assert len(merged.children) == 2
        # Each intermediate should have the original children
        all_grandchildren = []
        for intermediate in merged.children:
            all_grandchildren.extend(intermediate.children)
        assert len(all_grandchildren) == 3

    def test_same_question_merges_children(self):
        t1 = self._make_tree("What to build?", ["Alpha"])
        t2 = self._make_tree("What to build", ["Beta"])
        merged = merge_trees([t1, t2])
        # Same question -> all children under one intermediate
        assert len(merged.children) == 1
        assert len(merged.children[0].children) == 2

    def test_empty_trees_raises(self):
        with pytest.raises(ValueError, match="at least one"):
            merge_trees([])

    def test_dedup_prunes_duplicates(self, monkeypatch):
        t1 = self._make_tree("Q?", ["Plugin System"])
        t2 = self._make_tree("Q?", ["Plugin System"])
        # Mock the deduper to always flag as duplicate
        from possibilities.dedup import DupResult
        monkeypatch.setattr(
            "possibilities.merge.Deduplicator.check",
            lambda self, new, existing: DupResult(True, "Plugin System", 1.0, "Exact match"),
        )
        merged = merge_trees([t1, t2], dedup=True)
        # One of the two "Plugin System" nodes should be pruned
        pruned_count = sum(1 for n in _collect_all_nodes(merged) if n.pruned)
        assert pruned_count >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
