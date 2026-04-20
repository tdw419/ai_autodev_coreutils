"""Tests for CLI argument parsing -- all 7 commands."""

import pytest

from possibilities.cli import parse_args


# ---------------------------------------------------------------------------
# No command
# ---------------------------------------------------------------------------

class TestNoCommand:
    def test_no_command_returns_none(self):
        args = parse_args([])
        assert args.command is None


# ---------------------------------------------------------------------------
# explore
# ---------------------------------------------------------------------------

class TestExploreArgs:
    def test_minimal(self):
        args = parse_args(["explore", "What to build?"])
        assert args.command == "explore"
        assert args.question == "What to build?"
        assert args.workdir == "."
        assert args.depth == 3
        assert args.complexity == "balanced"
        assert args.model == "openai/glm-5.1"

    def test_all_options(self):
        args = parse_args([
            "explore", "Question?",
            "-w", "/tmp",
            "-d", "5",
            "--branch-min", "4",
            "--branch-max", "8",
            "-m", "custom-model",
            "-c", "fast",
            "--decay", "0.5",
            "--max-nodes", "100",
            "-s", "fertility_guided",
            "--context-files", "a.txt", "b.txt",
            "--temperature", "0.7",
            "--show-paths", "5",
            "-o", "out.json",
            "--show-pruned",
            "--stats",
        ])
        assert args.question == "Question?"
        assert args.workdir == "/tmp"
        assert args.depth == 5
        assert args.branch_min == 4
        assert args.branch_max == 8
        assert args.model == "custom-model"
        assert args.complexity == "fast"
        assert args.decay == 0.5
        assert args.max_nodes == 100
        assert args.strategy == "fertility_guided"
        assert args.context_files == ["a.txt", "b.txt"]
        assert args.temperature == 0.7
        assert args.show_paths == 5
        assert args.export == "out.json"
        assert args.show_pruned is True
        assert args.stats is True


# ---------------------------------------------------------------------------
# show
# ---------------------------------------------------------------------------

class TestShowArgs:
    def test_minimal(self):
        args = parse_args(["show", "tree.json"])
        assert args.command == "show"
        assert args.file == "tree.json"
        assert args.top == 10
        assert args.show_pruned is False

    def test_with_options(self):
        args = parse_args(["show", "tree.json", "--top", "5", "--show-pruned"])
        assert args.top == 5
        assert args.show_pruned is True


# ---------------------------------------------------------------------------
# resume
# ---------------------------------------------------------------------------

class TestResumeArgs:
    def test_minimal(self):
        args = parse_args(["resume", "tree.json"])
        assert args.command == "resume"
        assert args.file == "tree.json"
        assert args.depth is None
        assert args.model is None
        assert args.max_nodes is None
        assert args.complexity == "balanced"

    def test_with_options(self):
        args = parse_args([
            "resume", "tree.json",
            "-d", "5", "--max-nodes", "200",
            "-m", "strong-model", "-c", "thorough",
            "-o", "updated.json",
        ])
        assert args.depth == 5
        assert args.max_nodes == 200
        assert args.model == "strong-model"
        assert args.complexity == "thorough"
        assert args.export == "updated.json"


# ---------------------------------------------------------------------------
# merge
# ---------------------------------------------------------------------------

class TestMergeArgs:
    def test_minimal(self):
        args = parse_args(["merge", "a.json", "b.json"])
        assert args.command == "merge"
        assert args.files == ["a.json", "b.json"]
        assert args.output is None
        assert args.dedup is False

    def test_with_options(self):
        args = parse_args([
            "merge", "a.json", "b.json", "c.json",
            "-o", "merged.json",
            "--dedup", "-m", "strong", "-c", "thorough",
            "--decay", "0.8", "--top", "5",
        ])
        assert len(args.files) == 3
        assert args.output == "merged.json"
        assert args.dedup is True
        assert args.decay == 0.8


# ---------------------------------------------------------------------------
# escalate
# ---------------------------------------------------------------------------

class TestEscalateArgs:
    def test_minimal(self):
        args = parse_args(["escalate", "tree.json"])
        assert args.command == "escalate"
        assert args.file == "tree.json"
        assert args.starting_complexity == "balanced"
        assert args.max_tiers == 2

    def test_with_options(self):
        args = parse_args([
            "escalate", "tree.json",
            "-w", "/tmp",
            "--starting-complexity", "thorough",
            "--max-tiers", "3",
            "--min-children", "3",
            "-o", "esc.json",
        ])
        assert args.starting_complexity == "thorough"
        assert args.max_tiers == 3
        assert args.min_children == 3


# ---------------------------------------------------------------------------
# converge
# ---------------------------------------------------------------------------

class TestConvergeArgs:
    def test_minimal(self):
        args = parse_args(["converge", "tree.json"])
        assert args.command == "converge"
        assert args.file == "tree.json"
        assert args.model is None
        assert args.complexity == "balanced"
        assert args.show_tree is False

    def test_with_options(self):
        args = parse_args([
            "converge", "tree.json",
            "-m", "strong", "-c", "thorough",
            "--show-tree", "--show-pruned", "--stats",
        ])
        assert args.model == "strong"
        assert args.complexity == "thorough"
        assert args.show_tree is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
