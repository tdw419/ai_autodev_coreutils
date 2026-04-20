"""Tests for explorer module -- PossibilityExplorer internals and explore/resume."""

import pytest

from possibilities.models import ExplorationConfig, PossibilityNode
from possibilities.explorer import PossibilityExplorer


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
        **kw,
    )
    return n


def _make_tree():
    root = _node("Root", depth=0, description="What to build?")
    root.explored = True
    c1 = _node("Idea A", depth=1, explored=True, parent_id=root.id)
    c2 = _node("Idea B", depth=1, explored=True, parent_id=root.id)
    gc1 = _node("Sub A1", depth=2, parent_id=c1.id)
    gc2 = _node("Sub A2", depth=2, parent_id=c1.id)
    gc3 = _node("Sub B1", depth=2, parent_id=c2.id)
    c1.children = [gc1, gc2]
    c2.children = [gc3]
    root.children = [c1, c2]
    return root


# ---------------------------------------------------------------------------
# _count_nodes
# ---------------------------------------------------------------------------

class TestCountNodes:
    def test_empty_tree(self):
        root = _node("Root")
        config = ExplorationConfig(project_path="/nonexistent")
        explorer = PossibilityExplorer(config)
        explorer.root = root
        assert explorer._count_nodes() == 1

    def test_counts_all(self):
        root = _make_tree()
        config = ExplorationConfig(project_path="/nonexistent")
        explorer = PossibilityExplorer(config)
        explorer.root = root
        # Root + 2 children + 3 grandchildren = 6
        assert explorer._count_nodes() == 6


# ---------------------------------------------------------------------------
# _all_ideas
# ---------------------------------------------------------------------------

class TestAllIdeas:
    def test_flat(self):
        root = _node("Root", depth=0, description="Q?")
        root.children = [_node("A", depth=1), _node("B", depth=1)]
        config = ExplorationConfig(project_path="/nonexistent")
        explorer = PossibilityExplorer(config)
        explorer.root = root
        ideas = explorer._all_ideas()
        assert len(ideas) == 3
        titles = {i["title"] for i in ideas}
        assert "Root" in titles
        assert "A" in titles

    def test_includes_descriptions(self):
        root = _node("Root", depth=0, description="The question")
        config = ExplorationConfig(project_path="/nonexistent")
        explorer = PossibilityExplorer(config)
        explorer.root = root
        ideas = explorer._all_ideas()
        assert ideas[0]["description"] == "The question"


# ---------------------------------------------------------------------------
# _resolve_model
# ---------------------------------------------------------------------------

class TestResolveModel:
    def test_fallback_on_missing_model_choice(self, monkeypatch):
        """If model_choice can't be imported, returns config model."""
        import builtins
        real_import = builtins.__import__

        def blocking_import(name, *args, **kwargs):
            if name == "model_choice":
                raise ImportError("no model_choice")
            return real_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", blocking_import)
        config = ExplorationConfig(
            project_path="/nonexistent",
            model="test-model",
        )
        explorer = PossibilityExplorer(config)
        assert explorer._resolved_model == "test-model"


# ---------------------------------------------------------------------------
# explore (mocked LLM)
# ---------------------------------------------------------------------------

class TestExplore:
    def test_explore_builds_tree(self, monkeypatch):
        """Explore should generate branches and build a tree."""
        config = ExplorationConfig(
            project_path="/nonexistent",
            max_depth=1,
            max_nodes=20,
            branch_min=2,
            branch_max=3,
        )
        explorer = PossibilityExplorer(config)

        # Mock LLM to return branches
        fake_branches = [
            {"title": "Idea 1", "description": "D1", "enables": [],
             "risk": "R1", "category": "obvious"},
            {"title": "Idea 2", "description": "D2", "enables": [],
             "risk": "R2", "category": "wildcard"},
        ]
        monkeypatch.setattr(
            explorer.llm, "generate_json",
            lambda prompt: fake_branches,
        )
        # Mock dedup to never flag duplicates
        monkeypatch.setattr(
            explorer.deduper, "check",
            lambda new, existing: __import__("possibilities.dedup", fromlist=["DupResult"]).DupResult(is_duplicate=False),
        )

        tree = explorer.explore()
        assert tree is explorer.root
        # Root should have children (the branches)
        visible = [c for c in tree.children if not c.pruned]
        assert len(visible) >= 2

    def test_explore_respects_max_depth(self, monkeypatch):
        """No branches beyond max_depth."""
        config = ExplorationConfig(
            project_path="/nonexistent",
            max_depth=0,  # No exploration allowed
            max_nodes=50,
        )
        explorer = PossibilityExplorer(config)
        tree = explorer.explore()
        assert len(tree.children) == 0


# ---------------------------------------------------------------------------
# resume
# ---------------------------------------------------------------------------

class TestResume:
    def test_resume_sets_root(self, monkeypatch):
        """Resume replaces the explorer's root with the existing tree."""
        root = _make_tree()
        # Mark one depth-1 node as unexplored (clear its children to be a frontier)
        root.children[0].explored = False
        root.children[0].children = []

        config = ExplorationConfig(
            project_path="/nonexistent",
            max_depth=2,
            max_nodes=50,
        )
        explorer = PossibilityExplorer(config)

        # Just verify resume sets the root correctly and runs explore
        from possibilities.dedup import DupResult
        monkeypatch.setattr(
            explorer.deduper, "check",
            lambda new, existing: DupResult(is_duplicate=False),
        )
        monkeypatch.setattr(
            explorer.llm, "generate_json",
            lambda prompt: [],
        )

        tree = explorer.resume(root)
        assert tree is explorer.root
        # The root's description should be preserved
        assert tree.description == "What to build?"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
