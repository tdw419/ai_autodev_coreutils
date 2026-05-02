#!/usr/bin/env python3
"""
Tests for the Structural Invariants Engine (invariant_checker.py).

Creates temporary Python files with intentional violations and verifies
the checker detects them correctly.

Usage:
    python3 -m pytest test_invariant_checker.py -v
    python3 test_invariant_checker.py  (standalone)
"""

import os
import sys
import tempfile
import textwrap
from pathlib import Path

# Add the project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from invariant_checker import (
    InvariantConfig,
    Violation,
    scan_project,
    check_circular_dependencies,
    _determine_layer,
    _is_excluded,
)


# ─── Test fixtures ───────────────────────────────────────────────────────────

def create_test_project(base_dir: str, files: dict[str, str]) -> None:
    """Create a test project with the given files. Keys are paths relative to base_dir."""
    for path, content in files.items():
        full_path = os.path.join(base_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(textwrap.dedent(content))


def make_config(layers=None, forbidden=None, dep_rules=None, annotations=None, circular=0):
    """Create an InvariantConfig with specified settings."""
    data = {
        "layers": layers or [],
        "forbidden_imports": forbidden or [],
        "dependency_rules": dep_rules or {},
        "required_annotations": annotations or {},
        "circular_limit": circular,
        "exclude_dirs": [".git", "__pycache__", "node_modules"],
    }
    return InvariantConfig(data)


# ─── Test: Valid project passes ─────────────────────────────────────────────

def test_valid_project_passes():
    """A well-structured project with no violations should pass cleanly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = make_config(
            layers=[
                {"name": "models", "dir": os.path.join(tmpdir, "models")},
                {"name": "api", "dir": os.path.join(tmpdir, "api")},
            ],
            dep_rules={"api": ["models", "api"]},
        )
        create_test_project(tmpdir, {
            "models/user.py": """
                class User:
                    def __init__(self, name: str):
                        self.name = name
                    def get_name(self) -> str:
                        return self.name
            """,
            "api/handler.py": """
                from models.user import User
                def get_user(name: str) -> User:
                    return User(name)
            """,
        })
        report = scan_project(tmpdir, config)
        errors = [v for v in report["violations"] if v["severity"] == "error"]
        assert len(errors) == 0, f"Expected 0 errors, got {len(errors)}: {errors}"
        assert report["files_scanned"] == 2
        print("  ✅ test_valid_project_passes")


# ─── Test: Forbidden import detection ────────────────────────────────────────

def test_forbidden_import_detected():
    """Forbidden imports should be flagged."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = make_config(
            forbidden=[
                {"pattern": "^os$", "severity": "error", "message": "Use pathlib instead"},
            ],
        )
        create_test_project(tmpdir, {
            "bad.py": """
                import os
                print(os.getcwd())
            """,
            "good.py": """
                from pathlib import Path
                print(Path.cwd())
            """,
        })
        report = scan_project(tmpdir, config)
        forbidden_violations = [v for v in report["violations"] if v["rule"] == "forbidden_import"]
        assert len(forbidden_violations) == 1, f"Expected 1 forbidden import, got {len(forbidden_violations)}"
        assert "bad.py" in forbidden_violations[0]["file"]
        print("  ✅ test_forbidden_import_detected")


# ─── Test: Layer violation detection ─────────────────────────────────────────

def test_layer_violation_detected():
    """Importing from a higher layer should be flagged."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = make_config(
            layers=[
                {"name": "models", "dir": os.path.join(tmpdir, "models")},
                {"name": "api", "dir": os.path.join(tmpdir, "api")},
            ],
            dep_rules={"models": ["models"], "api": ["models", "api"]},
        )
        create_test_project(tmpdir, {
            "models/user.py": """
                from api.handler import get_user  # BAD: models importing from api
                class User:
                    pass
            """,
            "api/handler.py": """
                from models.user import User  # OK: api importing from models
                def get_user():
                    return User()
            """,
        })
        report = scan_project(tmpdir, config)
        layer_violations = [v for v in report["violations"] if v["rule"] == "layer_violation"]
        assert len(layer_violations) >= 1, f"Expected >=1 layer violation, got {len(layer_violations)}"
        # The violation should be in models/user.py
        assert any("user.py" in v["file"] for v in layer_violations), \
            f"Expected violation in user.py, got: {[v['file'] for v in layer_violations]}"
        print("  ✅ test_layer_violation_detected")


# ─── Test: Circular dependency detection ─────────────────────────────────────

def test_circular_dependency_detected():
    """Circular imports should be detected."""
    graph = {
        "module_a": ["module_b"],
        "module_b": ["module_a"],
        "module_c": ["module_d"],
        "module_d": ["module_c", "module_a"],
    }
    violations = check_circular_dependencies(graph, limit=0)
    # Should find cycles: a -> b -> a and c -> d -> c
    cycle_messages = set(v.message for v in violations)
    assert len(cycle_messages) >= 2, f"Expected >=2 unique cycles, got {len(cycle_messages)}: {cycle_messages}"
    print("  ✅ test_circular_dependency_detected")


def test_no_circular_with_limit():
    """With circular_limit > cycle length, longer cycles should still be caught."""
    graph = {
        "a": ["b"],
        "b": ["c"],
        "c": ["a"],
    }
    # Limit of 0 means no cycles allowed at all
    violations = check_circular_dependencies(graph, limit=0)
    assert len(violations) > 0, "Should detect cycle of length 3"
    # Limit of 2 means cycles of length > 2 are allowed
    violations_limited = check_circular_dependencies(graph, limit=2)
    assert len(violations_limited) == 0, f"Cycles of length 3 should be allowed with limit 2, got {violations_limited}"
    print("  ✅ test_no_circular_with_limit")


# ─── Test: Empty project ─────────────────────────────────────────────────────

def test_empty_project():
    """An empty directory should produce a clean report."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = make_config()
        report = scan_project(tmpdir, config)
        assert report["files_scanned"] == 0
        assert report["total_violations"] == 0
        assert report["errors"] == 0
        print("  ✅ test_empty_project")


# ─── Test: Invalid config handled gracefully ─────────────────────────────────

def test_invalid_config_graceful():
    """Missing or empty config should not crash."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Config with empty/missing sections
        config = make_config()
        create_test_project(tmpdir, {
            "test.py": "print('hello')",
        })
        report = scan_project(tmpdir, config)
        assert report["files_scanned"] == 1
        assert report["total_violations"] == 0  # No violations since no rules configured
        print("  ✅ test_invalid_config_graceful")


# ─── Test: Exclude directories ───────────────────────────────────────────────

def test_exclude_directories():
    """Excluded directories should be skipped during scanning."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = make_config(
            forbidden=[
                {"pattern": "^import os$", "severity": "error", "message": "Use pathlib"},
            ],
        )
        create_test_project(tmpdir, {
            "good.py": "from pathlib import Path\n",
            "__pycache__/bad.py": "import os\n",
            "node_modules/worse.py": "import os\n",
        })
        report = scan_project(tmpdir, config)
        assert report["files_scanned"] == 1, f"Expected 1 file scanned, got {report['files_scanned']}"
        assert report["total_violations"] == 0
        print("  ✅ test_exclude_directories")


# ─── Test: Missing type annotations ──────────────────────────────────────────

def test_missing_annotations():
    """Public functions without return annotations should be flagged when required."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = make_config(
            layers=[{"name": "models", "dir": os.path.join(tmpdir, "models")}],
            annotations={"models": {"require_return_types": True}},
        )
        create_test_project(tmpdir, {
            "models/data.py": """
                def public_func():  # Missing return annotation
                    return 42

                def _private_func():  # Private, should be skipped
                    return 42

                def annotated_func() -> int:  # OK
                    return 42
            """,
        })
        report = scan_project(tmpdir, config)
        annotation_violations = [v for v in report["violations"] if v["rule"] == "missing_annotation"]
        assert len(annotation_violations) == 1, \
            f"Expected 1 annotation violation, got {len(annotation_violations)}: {annotation_violations}"
        assert "public_func" in annotation_violations[0]["message"]
        print("  ✅ test_missing_annotations")


# ─── Test: Violation to_dict serialization ───────────────────────────────────

def test_violation_serialization():
    """Violation objects should serialize to dicts correctly."""
    v = Violation("test.py", 42, "forbidden_import", "error", "Forbidden import: os")
    d = v.to_dict()
    assert d["file"] == "test.py"
    assert d["line"] == 42
    assert d["rule"] == "forbidden_import"
    assert d["severity"] == "error"
    assert d["message"] == "Forbidden import: os"
    print("  ✅ test_violation_serialization")


# ─── Test: Layer determination ───────────────────────────────────────────────

def test_determine_layer():
    """_determine_layer should correctly match files to layers."""
    with tempfile.TemporaryDirectory() as tmpdir:
        layers = [
            {"name": "models", "dir": os.path.join(tmpdir, "src", "models")},
            {"name": "api", "dir": os.path.join(tmpdir, "src", "api")},
        ]
        assert _determine_layer(os.path.join(tmpdir, "src", "models", "user.py"), layers) == "models"
        assert _determine_layer(os.path.join(tmpdir, "src", "api", "handler.py"), layers) == "api"
        assert _determine_layer(os.path.join(tmpdir, "other", "file.py"), layers) is None
        print("  ✅ test_determine_layer")


# ─── Test: Syntax error handling ─────────────────────────────────────────────

def test_syntax_error_handling():
    """Files with syntax errors should be reported but not crash the scanner."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = make_config()
        create_test_project(tmpdir, {
            "bad_syntax.py": "def broken(\n",  # Incomplete syntax
            "good.py": "print('ok')\n",
        })
        report = scan_project(tmpdir, config)
        assert report["files_scanned"] == 2
        assert report["errors"] == 1
        assert "bad_syntax.py" in report["parse_errors"][0]["file"]
        print("  ✅ test_syntax_error_handling")


# ─── Test: Forbidden import with regex ───────────────────────────────────────

def test_forbidden_import_regex():
    """Forbidden import patterns should use regex matching."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = make_config(
            forbidden=[
                {"pattern": "^(pickle|shelve)$", "severity": "error", "message": "Unsafe"},
            ],
        )
        create_test_project(tmpdir, {
            "unsafe.py": "import pickle\n",
            "safe.py": "import json\n",
        })
        report = scan_project(tmpdir, config)
        forbidden = [v for v in report["violations"] if v["rule"] == "forbidden_import"]
        assert len(forbidden) == 1
        assert "unsafe.py" in forbidden[0]["file"]
        print("  ✅ test_forbidden_import_regex")


# ─── Test runner ─────────────────────────────────────────────────────────────

def main():
    """Run all tests."""
    tests = [
        test_valid_project_passes,
        test_forbidden_import_detected,
        test_layer_violation_detected,
        test_circular_dependency_detected,
        test_no_circular_with_limit,
        test_empty_project,
        test_invalid_config_graceful,
        test_exclude_directories,
        test_missing_annotations,
        test_violation_serialization,
        test_determine_layer,
        test_syntax_error_handling,
        test_forbidden_import_regex,
    ]

    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"  ❌ {test.__name__}: {e}")

    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed, {passed + failed} total")
    print(f"{'='*60}")

    if failed > 0:
        sys.exit(1)
    else:
        print("All tests passed! ✅")
        sys.exit(0)


if __name__ == "__main__":
    main()
