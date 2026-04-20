"""Tests for scorer module -- _is_question_node, _depth1_branch, lca_depth, classify_convergence."""

import pytest
from possibilities.models import PossibilityNode
from possibilities.scorer import (
    _is_question_node,
    _depth1_branch,
    lca_depth,
    classify_convergence,
    collect_all_paths,
)


# ---------------------------------------------------------------------------
# Helpers for building test trees
# ---------------------------------------------------------------------------

def _node(title, category="", depth=0, children=None, **kw):
    n = PossibilityNode(
        id=kw.get("id", title[:8]),
        title=title,
        category=category,
        depth=depth,
        children=children or [],
    )
    for k, v in kw.items():
        if k == "id":
            continue
        setattr(n, k, v)
    return n


def _flat_tree():
    """Single-question tree: root -> ideas at depth 1."""
    root = _node("Root", depth=0, description="What should we build?")
    root.children = [
        _node("TUI Interface", category="obvious", depth=1, parent_id=root.id),
        _node("API Platform", category="contrarian", depth=1, parent_id=root.id),
        _node("Plugin System", category="wildcard", depth=1, parent_id=root.id),
    ]
    return root


def _merged_tree():
    """Two-question merged tree with synthetic root and intermediates."""
    root = _node("Merged Exploration", depth=0, description="Q1 + Q2")

    # Depth-1: question intermediates (category="merged")
    q1 = _node("What is the highest impact?", category="merged", depth=1, parent_id=root.id)
    q2 = _node("What non-obvious direction?", category="merged", depth=1, parent_id=root.id)

    # Depth-2: real ideas
    tui = _node("Interactive TUI with live branch surgery", category="obvious", depth=2, parent_id=q1.id)
    sliders = _node("Sliders for every parameter", category="contrarian", depth=2, parent_id=q1.id)
    diff = _node("Possibility Diff Engine for Temporal Drift", category="wildcard", depth=2, parent_id=q2.id)
    graph = _node("Cross-Project Possibility Graph", category="foundational", depth=2, parent_id=q2.id)

    # Depth-3: sub-ideas
    undo = _node("Retained command log with undo/redo replay", category="obvious", depth=3, parent_id=tui.id)
    graft = _node("Multi-tree workspace with cross-tree grafting", category="contrarian", depth=3, parent_id=tui.id)
    reviewer = _node("AI reviewer that flags merge/prune candidates", category="wildcard", depth=3, parent_id=sliders.id)
    redteam = _node("Adversarial Red-Team Branch Pruning", category="contrarian", depth=3, parent_id=diff.id)

    tui.children = [undo, graft]
    sliders.children = [reviewer]
    diff.children = [redteam]
    q1.children = [tui, sliders]
    q2.children = [diff, graph]
    root.children = [q1, q2]

    return root


# ---------------------------------------------------------------------------
# _is_question_node
# ---------------------------------------------------------------------------

class TestIsQuestionNode:
    def test_merged_category(self):
        assert _is_question_node(_node("X", category="merged")) is True

    def test_real_categories_are_ideas(self):
        for cat in ("obvious", "contrarian", "wildcard", "foundational"):
            n = _node("What is this?", category=cat)
            assert _is_question_node(n) is False, f"{cat} should be idea"

    def test_empty_category_with_question_mark(self):
        assert _is_question_node(_node("What should we build?", category="")) is True

    def test_empty_category_with_question_word(self):
        for word in ("What", "How", "Why", "Is", "Can"):
            n = _node(f"{word} does this work", category="")
            assert _is_question_node(n) is True, f"'{word}' should trigger question"

    def test_empty_category_normal_title(self):
        assert _is_question_node(_node("TUI Interface", category="")) is False

    def test_question_mark_overrides_empty_category(self):
        assert _is_question_node(_node("Really a question?", category="")) is True

    def test_real_category_with_question_title(self):
        """A real idea might have a question-like title but real category wins."""
        n = _node("What if we made it modular?", category="contrarian")
        assert _is_question_node(n) is False


# ---------------------------------------------------------------------------
# _depth1_branch
# ---------------------------------------------------------------------------

class TestDepth1Branch:
    def test_flat_tree_depth1_ideas(self):
        """Non-merged tree: depth-1 nodes have real categories, use their titles."""
        root = _flat_tree()
        paths = collect_all_paths(root)
        labels = {_depth1_branch(p) for p in paths}
        assert labels == {"TUI Interface", "API Platform", "Plugin System"}

    def test_merged_tree_skips_question_nodes(self):
        """Merged tree: depth-1 nodes are question markers, skip to depth-2."""
        root = _merged_tree()
        paths = collect_all_paths(root)
        labels = [_depth1_branch(p) for p in paths]

        # Should NOT contain the question text at depth-1
        assert "What is the highest impact?" not in labels
        assert "What non-obvious direction?" not in labels

        # Should contain the actual idea titles at depth-2
        assert "Interactive TUI with live branch surgery" in labels
        assert "Sliders for every parameter" in labels
        assert "Possibility Diff Engine for Temporal Drift" in labels
        assert "Cross-Project Possibility Graph" in labels

    def test_merged_tree_branch_count(self):
        """Should have more than 2 unique branch labels (before fix it was 2)."""
        root = _merged_tree()
        paths = collect_all_paths(root)
        labels = {_depth1_branch(p) for p in paths}
        assert len(labels) >= 4, f"Expected >=4 unique labels, got {len(labels)}: {labels}"

    def test_empty_path_returns_root(self):
        assert _depth1_branch([]) == "root"


# ---------------------------------------------------------------------------
# lca_depth with merged trees
# ---------------------------------------------------------------------------

class TestLCADepth:
    def test_same_branch_high_lca(self):
        """Paths from same depth-2 idea should have LCA >= 2."""
        root = _merged_tree()
        paths = collect_all_paths(root)
        # Find two paths under the same depth-2 idea (TUI)
        tui_paths = [p for p in paths if any(n.title == "Interactive TUI with live branch surgery" for n in p)]
        if len(tui_paths) >= 2:
            depth = lca_depth(tui_paths[0], tui_paths[1])
            assert depth >= 2, f"Same-branch paths should share deep LCA, got {depth}"

    def test_cross_subtree_lca_is_root_only(self):
        """Cross-subtree paths only share the synthetic root (depth 0).
        Their depth-1 nodes are different question intermediates with different IDs,
        so lca_depth correctly returns 0 -- maximally independent."""
        root = _merged_tree()
        paths = collect_all_paths(root)
        q1_paths = [p for p in paths if any(n.category == "merged" and "highest" in n.title for n in p)]
        q2_paths = [p for p in paths if any(n.category == "merged" and "non-obvious" in n.title for n in p)]
        if q1_paths and q2_paths:
            depth = lca_depth(q1_paths[0], q2_paths[0])
            assert depth == 0, f"Cross-subtree LCA should be 0 (only root), got {depth}"


# ---------------------------------------------------------------------------
# classify_convergence
# ---------------------------------------------------------------------------

class TestClassifyConvergence:
    def test_genuine_cross_branch(self):
        root = _merged_tree()
        paths = collect_all_paths(root)
        # Simulate LLM finding convergence between path 1 and path 4 (different branches)
        convergences = [{
            "title": "Cross-project knowledge",
            "evidence": ["Path 1 [branch: X] says grafting", "Path 4 [branch: Y] says graph"],
            "strength": "strong",
        }]
        result = classify_convergence(convergences, paths)
        assert result[0]["surprise"] == "genuine"

    def test_expected_same_branch(self):
        root = _merged_tree()
        paths = collect_all_paths(root)
        # Find two paths with the same branch label
        labels = [_depth1_branch(p) for p in paths]
        same_branch_indices = []
        seen = {}
        for i, lbl in enumerate(labels, 1):
            if lbl in seen:
                same_branch_indices = [seen[lbl], i]
                break
            seen[lbl] = i

        if same_branch_indices:
            convs = [{
                "title": "Same idea",
                "evidence": [f"Path {same_branch_indices[0]} says X", f"Path {same_branch_indices[1]} says Y"],
                "strength": "weak",
            }]
            result = classify_convergence(convs, paths)
            assert result[0]["surprise"] == "expected"

    def test_no_surprise_field_added(self):
        """classify_convergence always adds a 'surprise' field."""
        root = _merged_tree()
        paths = collect_all_paths(root)
        convs = [{"title": "T", "evidence": ["Path 1 says X"], "strength": "weak"}]
        result = classify_convergence(convs, paths)
        assert "surprise" in result[0]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
