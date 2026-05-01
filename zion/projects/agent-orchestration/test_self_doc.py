#!/usr/bin/env python3
"""Tests for Phase 12: Agent-Legible Self-Documentation."""

import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

from self_doc import (
    _get_python_files,
    _parse_module,
    generate_ai_guide,
    generate_changelog,
    generate_architecture,
    get_inventory,
    _save_doc,
    PROJECT_DIR,
)


@pytest.fixture(autouse=True)
def setup_dirs(tmp_path, monkeypatch):
    """Redirect directories to tmp_path."""
    monkeypatch.setattr("self_doc.PROJECT_DIR", tmp_path)
    monkeypatch.setattr("self_doc.DOCS_DIR", tmp_path / "docs")


# --- Module Parsing ---

def test_parse_module_simple(tmp_path):
    """Simple module is parsed correctly."""
    f = tmp_path / "simple.py"
    f.write_text('''
def greet(name):
    """Greet someone."""
    return f"Hello, {name}"

class Calculator:
    """A simple calculator."""

    def add(self, a, b):
        """Add two numbers."""
        return a + b
''')

    result = _parse_module(f)

    assert result["file"] == "simple.py"
    assert result["loc"] > 0
    assert len(result["functions"]) == 1
    assert result["functions"][0]["name"] == "greet"
    assert result["functions"][0]["args"] == ["name"]
    assert len(result["classes"]) == 1
    assert result["classes"][0]["name"] == "Calculator"
    assert "add" in result["classes"][0]["methods"]


def test_parse_module_private_ignored(tmp_path):
    """Private functions/classes are excluded."""
    f = tmp_path / "private.py"
    f.write_text('''
def _internal():
    pass

class _Secret:
    pass

def public():
    pass
''')

    result = _parse_module(f)
    func_names = [fn["name"] for fn in result["functions"]]
    assert "public" in func_names
    assert "_internal" not in func_names
    assert len(result["classes"]) == 0


def test_parse_module_syntax_error(tmp_path):
    """Module with syntax error returns error dict."""
    f = tmp_path / "broken.py"
    f.write_text("def broken(:\n  pass")

    result = _parse_module(f)
    assert "error" in result


def test_parse_module_imports(tmp_path):
    """Import statements are captured."""
    f = tmp_path / "imports.py"
    f.write_text('''
import os
import json
from pathlib import Path
from collections import defaultdict
''')

    result = _parse_module(f)
    assert "os" in result["imports"]
    assert "json" in result["imports"]
    assert "pathlib.Path" in result["imports"]
    assert "collections.defaultdict" in result["imports"]


# --- Python File Discovery ---

def test_get_python_files(tmp_path):
    """Finds .py files but not test files."""
    (tmp_path / "main.py").write_text("pass")
    (tmp_path / "utils.py").write_text("pass")
    (tmp_path / "test_main.py").write_text("pass")

    result = _get_python_files()

    assert len(result) == 2
    names = [f.name for f in result]
    assert "main.py" in names
    assert "utils.py" in names
    assert "test_main.py" not in names


def test_get_python_files_empty(tmp_path):
    """Empty directory returns empty list."""
    result = _get_python_files()
    assert result == []


# --- AI Guide Generation ---

def test_generate_ai_guide(tmp_path):
    """AI guide contains expected sections."""
    (tmp_path / "example.py").write_text('''
def hello():
    """Say hello."""
    pass
''')

    guide = generate_ai_guide()

    assert "# AI Guide" in guide
    assert "Architecture Overview" in guide
    assert "Module API Reference" in guide
    assert "Conventions" in guide
    assert "Pipeline Node Types" in guide
    assert "example.py" in guide
    assert "hello" in guide


# --- Changelog Generation ---

def test_generate_changelog(tmp_path):
    """Changelog is generated (even without git history)."""
    changelog = generate_changelog()

    assert "# Changelog" in changelog
    # May have real git history or fallback message
    assert "Generated:" in changelog or "Unable" in changelog


# --- Architecture Overview ---

def test_generate_architecture(tmp_path):
    """Architecture doc contains expected sections."""
    (tmp_path / "mod1.py").write_text("def f(): pass")
    (tmp_path / "mod2.py").write_text("class C: pass")

    arch = generate_architecture()

    assert "# Architecture Overview" in arch
    assert "Module Dependency Graph" in arch
    assert "Data Flow" in arch
    assert "Module Sizes" in arch
    assert "Test Coverage" in arch
    assert "mod1.py" in arch
    assert "mod2.py" in arch


# --- Inventory ---

def test_get_inventory(tmp_path):
    """Inventory aggregates module stats."""
    (tmp_path / "a.py").write_text('''
def f1(): pass
def f2(): pass
class C1: pass
''')
    (tmp_path / "b.py").write_text('''
def g1(): pass
class C2: pass
class C3: pass
''')

    inv = get_inventory()

    assert inv["total_modules"] == 2
    assert inv["total_functions"] == 3
    assert inv["total_classes"] == 3
    assert inv["total_loc"] > 0
    assert len(inv["modules"]) == 2


# --- Save Document ---

def test_save_doc(tmp_path):
    """Document is saved to docs directory."""
    content = "# Test Document\n\nHello."
    path = _save_doc(content, "TEST.md")

    assert path.endswith("TEST.md")
    assert Path(path).exists()
    assert Path(path).read_text() == content


# --- Integration: Run on actual project ---

def test_generate_on_real_project():
    """Can generate docs for the actual project."""
    import self_doc as sd
    original = sd.PROJECT_DIR
    sd.PROJECT_DIR = Path(__file__).parent

    try:
        guide = sd.generate_ai_guide()
        assert "# AI Guide" in guide
        assert "dag.py" in guide
        assert "executor.py" in guide

        arch = sd.generate_architecture()
        assert "# Architecture Overview" in arch

        inv = sd.get_inventory()
        assert inv["total_modules"] > 5
    finally:
        sd.PROJECT_DIR = original
