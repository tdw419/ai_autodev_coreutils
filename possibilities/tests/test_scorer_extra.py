"""Tests for scorer module -- compute_fertility, rank_paths, collect_all_paths, converge, paths_to_text."""

import pytest

from possibilities.models import PossibilityNode
from possibilities.scorer import (
    collect_all_paths,
    compute_fertility,
    converge,
    most_fertile_frontier,
    paths_to_text,
    rank_paths,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _node(title, category="obvious", depth=0, children=None, **kw):
    n = PossibilityNode(
        id=kw.pop("id", title[:8]),
        title=title,
        category=category,
        depth=depth,
        children=children or [],
        **kw,
    )
    return n


def _simple_tree():
    """Root -> 3 children, each with 2 grandchildren."""
    root = _node("Root", depth=0, description="What to build?")
    for i, name in enumerate(["Alpha", "Beta", "Gamma"]):
        child = _node(name, depth=1, parent_id=root.id)
        for j in range(2):
            gc = _node(f"{name}-sub{j}", depth=2, parent_id=child.id)
            child.children.append(gc)
        root.children.append(child)
    return root


# ---------------------------------------------------------------------------
# compute_fertility
# ---------------------------------------------------------------------------

class TestComputeFertility:
    def test_leaf_has_zero_fertility(self):
        leaf = _node("Leaf", depth=2)
        score = compute_fertility(leaf)
        assert score == 0.0
        assert leaf.fertility_score == 0.0
        assert leaf.direct_fertility == 0
        assert leaf.total_descendants == 0

    def test_branch_with_only_pruned_children(self):
        parent = _node("Parent", depth=1)
        child = _node("PrunedChild", depth=2, pruned=True)
        parent.children.append(child)
        score = compute_fertility(parent)
        assert score == 0.0
        assert parent.direct_fertility == 0

    def test_simple_branch(self):
        parent = _node("Parent", depth=0)
        child1 = _node("C1", depth=1)
        child2 = _node("C2", depth=1)
        parent.children = [child1, child2]
        score = compute_fertility(parent)
        assert score > 0
        assert parent.direct_fertility == 2
        assert parent.total_descendants == 2

    def test_nested_tree_scoring(self):
        root = _simple_tree()
        score = compute_fertility(root)
        assert score > 0
        assert root.total_descendants == 9  # 3 children + 6 grandchildren

    def test_pruned_nodes_excluded(self):
        root = _node("Root", depth=0)
        good = _node("Good", depth=1)
        bad = _node("Bad", depth=1, pruned=True, prune_reason="dup")
        root.children = [good, bad]
        score = compute_fertility(root)
        assert root.direct_fertility == 1

    def test_decay_parameter(self):
        """Higher decay means deeper branching scores higher."""
        root = _simple_tree()
        score_low = compute_fertility(root, decay=0.3)
        root2 = _simple_tree()
        # Need a fresh tree since compute_fertility mutates in place
        root2_copy = PossibilityNode.from_dict(root2.to_dict())
        score_high = compute_fertility(root2_copy, decay=0.9)
        # Higher decay -> higher score (deeper generations contribute more)
        assert score_high > score_low


# ---------------------------------------------------------------------------
# rank_paths
# ---------------------------------------------------------------------------

class TestRankPaths:
    def test_single_path(self):
        leaf = _node("Leaf", depth=1)
        root = _node("Root", depth=0, children=[leaf])
        compute_fertility(root)
        paths = rank_paths(root, top_n=10)
        assert len(paths) == 1

    def test_top_n_limits(self):
        root = _node("Root", depth=0)
        for i in range(20):
            child = _node(f"Child{i}", depth=1)
            root.children.append(child)
        compute_fertility(root)
        paths = rank_paths(root, top_n=5)
        assert len(paths) == 5

    def test_paths_sorted_descending(self):
        root = _node("Root", depth=0)
        rich = _node("Rich", depth=1)
        rich.children = [_node("RC1", depth=2), _node("RC2", depth=2)]
        poor = _node("Poor", depth=1)
        root.children = [rich, poor]
        compute_fertility(root)
        paths = rank_paths(root, top_n=10)
        scores = [score for score, _ in paths]
        assert scores == sorted(scores, reverse=True)

    def test_empty_tree(self):
        """A root with no children is itself a leaf, so rank_paths returns one path."""
        root = _node("Root", depth=0)
        compute_fertility(root)
        paths = rank_paths(root, top_n=10)
        assert len(paths) == 1
        assert paths[0][0] == 0.0  # fertility_score of root is 0


# ---------------------------------------------------------------------------
# collect_all_paths
# ---------------------------------------------------------------------------

class TestCollectAllPaths:
    def test_flat_children(self):
        root = _node("Root", depth=0)
        root.children = [_node("A", depth=1), _node("B", depth=1)]
        paths = collect_all_paths(root)
        assert len(paths) == 2

    def test_nested_paths(self):
        root = _simple_tree()
        paths = collect_all_paths(root)
        # 3 branches * 2 grandchildren = 6 leaf paths
        assert len(paths) == 6

    def test_pruned_excluded(self):
        root = _node("Root", depth=0)
        visible = _node("Visible", depth=1)
        pruned = _node("Pruned", depth=1, pruned=True)
        root.children = [visible, pruned]
        paths = collect_all_paths(root)
        # Only the visible path
        assert len(paths) == 1


# ---------------------------------------------------------------------------
# most_fertile_frontier
# ---------------------------------------------------------------------------

class TestMostFertileFrontier:
    def test_none_when_all_explored(self):
        root = _simple_tree()
        compute_fertility(root)

        def mark_explored(n):
            n.explored = True
            for c in n.children:
                mark_explored(c)

        mark_explored(root)
        assert most_fertile_frontier(root) is None

    def test_returns_highest_unexplored(self):
        root = _node("Root", depth=0)
        high = _node("HighFert", depth=1, explored=False, fertility_score=5.0)
        low = _node("LowFert", depth=1, explored=False, fertility_score=1.0)
        root.children = [high, low]
        result = most_fertile_frontier(root)
        assert result.title == "HighFert"

    def test_skips_pruned(self):
        """Pruned nodes are skipped, but the root itself can still be a candidate."""
        root = _node("Root", depth=0, explored=False)
        pruned = _node("Pruned", depth=1, pruned=True, fertility_score=10.0)
        root.children = [pruned]
        result = most_fertile_frontier(root)
        # The pruned child is skipped, but root (unexplored, score=0) is returned
        assert result is root


# ---------------------------------------------------------------------------
# paths_to_text
# ---------------------------------------------------------------------------

class TestPathsToText:
    def test_basic_formatting(self):
        root = _node("Root", depth=0, description="What to build?")
        child = _node("Idea", category="obvious", depth=1,
                       enables=["Thing A", "Thing B"])
        root.children = [child]
        paths = collect_all_paths(root)
        text = paths_to_text(paths)
        assert "Path 1" in text
        assert "[Root]" in text
        assert "Idea" in text

    def test_branch_annotations(self):
        root = _node("Root", depth=0, description="Q?")
        a = _node("BranchA", category="obvious", depth=1)
        b = _node("BranchB", category="contrarian", depth=1)
        root.children = [a, b]
        paths = collect_all_paths(root)
        text = paths_to_text(paths)
        assert "branch:" in text


# ---------------------------------------------------------------------------
# converge
# ---------------------------------------------------------------------------

class TestConverge:
    def test_too_few_paths(self):
        """Single-path tree returns fallback convergence."""
        root = _node("Root", depth=0, description="Q?")
        root.children = [_node("Only", depth=1)]
        result = converge(root, model="test")
        assert len(result) == 1
        assert "Not enough paths" in result[0]["title"]

    def test_llm_failure_returns_fallback(self, monkeypatch):
        """If LLM returns no valid JSON, converge returns fallback."""
        root = _node("Root", depth=0, description="Q?")
        root.children = [_node("A", depth=1), _node("B", depth=1)]

        from possibilities import llm as llm_mod
        monkeypatch.setattr(llm_mod.LLMClient, "generate_json",
                            lambda self, prompt: [])
        result = converge(root, model="test")
        assert len(result) == 1
        assert "failed" in result[0]["title"].lower()

    def test_successful_convergence(self, monkeypatch):
        root = _node("Root", depth=0, description="Q?")
        a = _node("Idea A", category="obvious", depth=1)
        b = _node("Idea B", category="contrarian", depth=1)
        root.children = [a, b]

        fake_result = [{
            "title": "Common Theme",
            "evidence": ["Path 1 says X", "Path 2 says Y"],
            "strength": "strong",
            "implication": "Important",
        }]
        from possibilities import llm as llm_mod
        monkeypatch.setattr(llm_mod.LLMClient, "generate_json",
                            lambda self, prompt: fake_result)
        result = converge(root, model="test")
        assert len(result) == 1
        assert result[0]["title"] == "Common Theme"
        assert "surprise" in result[0]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
