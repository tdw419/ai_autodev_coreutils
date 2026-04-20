"""Tests for context module -- project context gathering."""

import os
import tempfile

import pytest

from possibilities.context import (
    CONTEXT_FILENAMES,
    SKIP_DIRS,
    build_dir_tree,
    count_extensions,
    gather_project_context,
)


# ---------------------------------------------------------------------------
# gather_project_context
# ---------------------------------------------------------------------------

class TestGatherProjectContext:
    def test_nonexistent_path(self):
        result = gather_project_context("/nonexistent/path/xyz")
        assert "No project directory" in result

    def test_empty_dir(self):
        with tempfile.TemporaryDirectory() as td:
            result = gather_project_context(td)
            assert "Empty or unrecognized" in result

    def test_finds_readme(self):
        with tempfile.TemporaryDirectory() as td:
            readme = os.path.join(td, "README.md")
            with open(readme, "w") as f:
                f.write("# Test Project\nThis is a test.")
            result = gather_project_context(td)
            assert "README.md" in result
            assert "Test Project" in result

    def test_finds_pyproject(self):
        with tempfile.TemporaryDirectory() as td:
            with open(os.path.join(td, "pyproject.toml"), "w") as f:
                f.write('[project]\nname = "test"\n')
            result = gather_project_context(td)
            assert "pyproject.toml" in result

    def test_extra_files(self):
        with tempfile.TemporaryDirectory() as td:
            notes = os.path.join(td, "NOTES.txt")
            with open(notes, "w") as f:
                f.write("My notes")
            result = gather_project_context(td, extra_files=["NOTES.txt"])
            assert "NOTES.txt" in result
            assert "My notes" in result

    def test_ignores_large_files(self):
        """Large files should not be included as content sections."""
        with tempfile.TemporaryDirectory() as td:
            with open(os.path.join(td, "README.md"), "w") as f:
                f.write("x" * 25000)  # > 20000 byte limit
            result = gather_project_context(td)
            # The file should not be included as a content section
            assert "=== README.md ===" not in result

    def test_truncates_long_files(self):
        with tempfile.TemporaryDirectory() as td:
            with open(os.path.join(td, "README.md"), "w") as f:
                f.write("HEADER\n" + "line\n" * 1000)
            result = gather_project_context(td)
            assert "HEADER" in result

    def test_directory_structure_section(self):
        with tempfile.TemporaryDirectory() as td:
            os.makedirs(os.path.join(td, "src"))
            with open(os.path.join(td, "src", "main.py"), "w") as f:
                f.write("print('hi')")
            result = gather_project_context(td)
            assert "Directory Structure" in result
            assert "src" in result

    def test_file_types_section(self):
        with tempfile.TemporaryDirectory() as td:
            with open(os.path.join(td, "a.py"), "w") as f:
                f.write("")
            with open(os.path.join(td, "b.py"), "w") as f:
                f.write("")
            with open(os.path.join(td, "c.js"), "w") as f:
                f.write("")
            result = gather_project_context(td)
            assert "File Types" in result
            assert "py:" in result or ".py" in result


# ---------------------------------------------------------------------------
# build_dir_tree
# ---------------------------------------------------------------------------

class TestBuildDirTree:
    def test_empty_dir(self):
        from pathlib import Path
        with tempfile.TemporaryDirectory() as td:
            result = build_dir_tree(Path(td))
            assert result == ""

    def test_single_file(self):
        from pathlib import Path
        with tempfile.TemporaryDirectory() as td:
            with open(os.path.join(td, "file.txt"), "w") as f:
                f.write("hi")
            result = build_dir_tree(Path(td))
            assert "file.txt" in result

    def test_respects_max_depth(self):
        from pathlib import Path
        with tempfile.TemporaryDirectory() as td:
            deep = os.path.join(td, "a", "b", "c", "d")
            os.makedirs(deep)
            with open(os.path.join(deep, "f.txt"), "w") as f:
                f.write("")
            result = build_dir_tree(Path(td), max_depth=2)
            assert "f.txt" not in result

    def test_skips_hidden_dirs(self):
        from pathlib import Path
        with tempfile.TemporaryDirectory() as td:
            os.makedirs(os.path.join(td, ".hidden"))
            with open(os.path.join(td, ".hidden", "secret.txt"), "w") as f:
                f.write("")
            with open(os.path.join(td, "visible.txt"), "w") as f:
                f.write("")
            result = build_dir_tree(Path(td))
            assert "visible.txt" in result
            assert "secret.txt" not in result
            assert ".hidden" not in result

    def test_skips_noise_dirs(self):
        from pathlib import Path
        for skip_dir in ["__pycache__", "node_modules", ".git"]:
            with tempfile.TemporaryDirectory() as td:
                os.makedirs(os.path.join(td, skip_dir))
                with open(os.path.join(td, skip_dir, "x.pyc"), "w") as f:
                    f.write("")
                result = build_dir_tree(Path(td))
                assert skip_dir not in result


# ---------------------------------------------------------------------------
# count_extensions
# ---------------------------------------------------------------------------

class TestCountExtensions:
    def test_empty_dir(self):
        with tempfile.TemporaryDirectory() as td:
            exts = count_extensions(td)
            assert len(exts) == 0

    def test_counts_extensions(self):
        with tempfile.TemporaryDirectory() as td:
            for name in ["a.py", "b.py", "c.js", "d.txt"]:
                with open(os.path.join(td, name), "w") as f:
                    f.write("")
            exts = count_extensions(td)
            assert exts["py"] == 2
            assert exts["js"] == 1
            assert exts["txt"] == 1

    def test_no_extension_ignored(self):
        with tempfile.TemporaryDirectory() as td:
            with open(os.path.join(td, "Makefile"), "w") as f:
                f.write("")
            with open(os.path.join(td, "a.py"), "w") as f:
                f.write("")
            exts = count_extensions(td)
            assert "Makefile" not in exts
            assert exts["py"] == 1

    def test_skips_hidden_dirs(self):
        with tempfile.TemporaryDirectory() as td:
            os.makedirs(os.path.join(td, ".git"))
            with open(os.path.join(td, ".git", "x.py"), "w") as f:
                f.write("")
            with open(os.path.join(td, "a.py"), "w") as f:
                f.write("")
            exts = count_extensions(td)
            # Only the top-level .py should be counted
            assert exts["py"] == 1


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

class TestConstants:
    def test_context_filenames_is_list(self):
        assert isinstance(CONTEXT_FILENAMES, list)
        assert "README.md" in CONTEXT_FILENAMES

    def test_skip_dirs_is_set(self):
        assert isinstance(SKIP_DIRS, set)
        assert ".git" in SKIP_DIRS
        assert "node_modules" in SKIP_DIRS


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
