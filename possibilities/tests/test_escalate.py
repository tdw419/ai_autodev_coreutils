"""Tests for escalate module -- thin node finding and escalation logic."""

import pytest

from possibilities.escalate import (
    ESCALATION_COMPLEXITIES,
    _starting_complexity_index,
    find_thin_nodes,
)
from possibilities.models import PossibilityNode


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _node(title, depth=0, children=None, explored=False, pruned=False, **kw):
    n = PossibilityNode(
        id=kw.pop("id", title[:8]),
        title=title,
        depth=depth,
        explored=explored,
        pruned=pruned,
        children=children or [],
    )
    return n


def _healthy_tree():
    """Every node is explored and has >=2 non-pruned children (not thin)."""
    root = _node("Root", depth=0, explored=True)
    c1 = _node("Branch A", depth=1, explored=True, parent_id=root.id)
    c2 = _node("Branch B", depth=1, explored=True, parent_id=root.id)
    # Grandchildren must themselves have children to not be "thin"
    # (an explored leaf with 0 children is thin by definition)
    gc_a1 = _node("A1", depth=2, explored=True)
    gc_a1.children = [_node("A1a", depth=3, explored=True), _node("A1b", depth=3, explored=True)]
    gc_a2 = _node("A2", depth=2, explored=True)
    gc_a2.children = [_node("A2a", depth=3, explored=True)]
    gc_b1 = _node("B1", depth=2, explored=True)
    gc_b1.children = [_node("B1a", depth=3, explored=True), _node("B1b", depth=3, explored=True)]
    gc_b2 = _node("B2", depth=2, explored=True)
    gc_b2.children = [_node("B2a", depth=3, explored=True)]
    c1.children = [gc_a1, gc_a2]
    c2.children = [gc_b1, gc_b2]
    root.children = [c1, c2]
    return root


def _thin_tree():
    """Some nodes have <2 non-pruned children."""
    root = _node("Root", depth=0, explored=True)
    rich = _node("Rich Branch", depth=1, explored=True, parent_id=root.id)
    thin = _node("Thin Branch", depth=1, explored=True, parent_id=root.id)
    pruned_child = _node("Pruned", depth=2, pruned=True)
    thin.children = [pruned_child]  # 0 non-pruned children
    rich.children = [_node("R1", depth=2), _node("R2", depth=2)]
    root.children = [rich, thin]
    return root


# ---------------------------------------------------------------------------
# find_thin_nodes
# ---------------------------------------------------------------------------

class TestFindThinNodes:
    def test_healthy_tree_no_thin(self):
        """With min_children=1, nodes with >=1 child are not thin.
        But explored leaves (0 children) are still thin."""
        root = _healthy_tree()
        thin = find_thin_nodes(root, min_children=1)
        # The depth-3 leaves are explored with 0 children -> thin
        # But depth-1 and depth-2 nodes have >=1 child -> not thin
        thin_titles = {n.title for n in thin}
        # Depth-3 leaves should be thin (explored, 0 children)
        assert "A1a" in thin_titles
        assert "B1a" in thin_titles
        # Depth-1 branches should NOT be thin (they have children)
        assert "Branch A" not in thin_titles
        assert "Branch B" not in thin_titles

    def test_finds_thin_branches(self):
        root = _thin_tree()
        thin = find_thin_nodes(root, min_children=2)
        titles = {n.title for n in thin}
        assert "Thin Branch" in titles
        assert "Rich Branch" not in titles

    def test_unexplored_leaves_are_thin(self):
        root = _node("Root", depth=0, explored=True)
        leaf = _node("Unexplored Leaf", depth=1, explored=False)
        root.children = [leaf]
        thin = find_thin_nodes(root)
        assert len(thin) == 1
        assert thin[0].title == "Unexplored Leaf"

    def test_pruned_nodes_excluded(self):
        root = _node("Root", depth=0, explored=True)
        pruned = _node("Pruned Node", depth=1, pruned=True)
        root.children = [pruned]
        thin = find_thin_nodes(root)
        assert len(thin) == 0

    def test_root_is_never_thin(self):
        root = _node("Root", depth=0, explored=True)
        root.children = []  # No children
        thin = find_thin_nodes(root)
        assert len(thin) == 0

    def test_min_children_threshold(self):
        root = _node("Root", depth=0, explored=True)
        node1 = _node("One Child", depth=1, explored=True)
        node1.children = [_node("C", depth=2)]
        node2 = _node("Two Children", depth=1, explored=True)
        node2.children = [_node("C1", depth=2), _node("C2", depth=2)]
        root.children = [node1, node2]

        thin_2 = find_thin_nodes(root, min_children=2)
        titles_2 = {n.title for n in thin_2}
        assert "One Child" in titles_2
        assert "Two Children" not in titles_2

        thin_1 = find_thin_nodes(root, min_children=1)
        titles_1 = {n.title for n in thin_1}
        assert "One Child" not in titles_1
        assert "Two Children" not in titles_1


# ---------------------------------------------------------------------------
# _starting_complexity_index
# ---------------------------------------------------------------------------

class TestStartingComplexityIndex:
    def test_known_values(self):
        for i, c in enumerate(ESCALATION_COMPLEXITIES):
            assert _starting_complexity_index(c) == i

    def test_unknown_returns_zero(self):
        assert _starting_complexity_index("nonexistent") == 0


# ---------------------------------------------------------------------------
# ESCALATION_COMPLEXITIES constant
# ---------------------------------------------------------------------------

class TestConstants:
    def test_escalation_chain_order(self):
        assert ESCALATION_COMPLEXITIES == ["balanced", "thorough", "thorough_strong"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
