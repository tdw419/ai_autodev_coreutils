"""Tests for render module -- tree, summary, ranked paths, convergence rendering."""

import pytest

from possibilities.models import PossibilityNode
from possibilities.render import (
    render_convergence,
    render_ranked_paths,
    render_summary,
    render_tree,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _node(title, depth=0, children=None, **kw):
    n = PossibilityNode(
        id=kw.pop("id", title[:8]),
        title=title,
        depth=depth,
        children=children or [],
        **kw,
    )
    return n


def _simple_tree():
    root = _node("Root", depth=0, description="What to build?",
                 fertility_score=5.0, total_descendants=5)
    root.explored = True
    a = _node("Idea A", depth=1, category="obvious",
              fertility_score=2.0, enables=["X", "Y"])
    b = _node("Idea B", depth=1, category="contrarian",
              fertility_score=1.5)
    root.children = [a, b]
    return root


# ---------------------------------------------------------------------------
# render_tree
# ---------------------------------------------------------------------------

class TestRenderTree:
    def test_root_node(self):
        root = _simple_tree()
        output = render_tree(root)
        assert "[Root]" in output
        assert "What to build?" in output
        assert "fertility:" in output

    def test_children_shown(self):
        root = _simple_tree()
        output = render_tree(root)
        assert "Idea A" in output
        assert "Idea B" in output

    def test_category_shown(self):
        root = _simple_tree()
        output = render_tree(root)
        assert "(obvious)" in output
        assert "(contrarian)" in output

    def test_enables_count(self):
        root = _simple_tree()
        output = render_tree(root)
        assert "[enables: 2]" in output

    def test_pruned_hidden_by_default(self):
        root = _node("Root", depth=0, fertility_score=1.0)
        pruned = _node("Pruned", depth=1, pruned=True,
                       prune_reason="Duplicate")
        root.children = [pruned]
        output = render_tree(root, show_pruned=False)
        assert "Pruned" not in output

    def test_pruned_shown_when_requested(self):
        root = _node("Root", depth=0, fertility_score=1.0)
        pruned = _node("Pruned", depth=1, pruned=True,
                       prune_reason="Duplicate")
        root.children = [pruned]
        output = render_tree(root, show_pruned=True)
        assert "Pruned" in output
        assert "[PRUNED]" in output

    def test_empty_tree(self):
        root = _node("Root", depth=0, description="Q?")
        output = render_tree(root)
        assert "[Root]" in output


# ---------------------------------------------------------------------------
# render_summary
# ---------------------------------------------------------------------------

class TestRenderSummary:
    def test_basic_summary(self):
        root = _simple_tree()
        output = render_summary(root)
        assert "EXPLORATION SUMMARY" in output
        assert "Total nodes:" in output
        assert "Explored:" in output
        assert "Root fertility:" in output
        assert "Descendants:" in output

    def test_counts_pruned(self):
        root = _node("Root", depth=0)
        pruned = _node("P", depth=1, pruned=True)
        root.children = [pruned, _node("V", depth=1)]
        output = render_summary(root)
        assert "Total nodes:    3" in output
        assert "Pruned (dupes): 1" in output


# ---------------------------------------------------------------------------
# render_ranked_paths
# ---------------------------------------------------------------------------

class TestRenderRankedPaths:
    def test_basic_paths(self):
        paths = [
            (5.0, [_node("Root", depth=0), _node("A", depth=1)]),
            (3.0, [_node("Root", depth=0), _node("B", depth=1)]),
        ]
        output = render_ranked_paths(paths)
        assert "RANKED PATHS" in output
        assert "#1" in output
        assert "#2" in output
        assert "score:" in output

    def test_empty_paths(self):
        output = render_ranked_paths([])
        assert "RANKED PATHS" in output


# ---------------------------------------------------------------------------
# render_convergence
# ---------------------------------------------------------------------------

class TestRenderConvergence:
    def test_basic_convergence(self):
        convergences = [{
            "title": "Shared Theme",
            "strength": "strong",
            "evidence": ["Path 1 says X", "Path 2 says Y"],
            "implication": "This is important",
            "surprise": "genuine",
        }]
        output = render_convergence(convergences)
        assert "CONVERGENCE ANALYSIS" in output
        assert "Shared Theme" in output
        assert "[strong]" in output
        assert "[GENUINE]" in output
        assert "This is important" in output

    def test_genuine_count(self):
        convergences = [
            {"title": "A", "strength": "strong", "evidence": [],
             "implication": "", "surprise": "genuine"},
            {"title": "B", "strength": "weak", "evidence": [],
             "implication": "", "surprise": "expected"},
        ]
        output = render_convergence(convergences)
        assert "1 genuine" in output
        assert "1 expected" in output

    def test_empty_convergence(self):
        output = render_convergence([])
        assert "CONVERGENCE ANALYSIS" in output
        assert "0 convergence point" in output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
