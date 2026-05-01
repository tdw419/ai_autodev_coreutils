#!/usr/bin/env python3
"""
Agent-Legible Self-Documentation for the Hermes Agent Orchestrator.

Generates AI_GUIDE.md, CHANGELOG.md, and architecture docs by introspecting
the codebase. These documents are written to be easily parsed by LLM agents,
enabling new agents to quickly understand the codebase.

Usage:
    python3 self_doc.py --guide              # Generate AI_GUIDE.md
    python3 self_doc.py --changelog          # Generate CHANGELOG.md
    python3 self_doc.py --architecture       # Generate architecture overview
    python3 self_doc.py --all                # Generate all documents
    python3 self_doc.py --inventory          # List all modules with stats
"""

from __future__ import annotations

import argparse
import ast
import importlib
import inspect
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

PROJECT_DIR = Path(os.environ.get(
    "ORCH_PROJECT_DIR",
    os.path.expanduser("~/zion/projects/agent-orchestration"),
))
DOCS_DIR = PROJECT_DIR / "docs"


def _get_python_files() -> list[Path]:
    """Get all Python files in the project (excluding tests and __pycache__)."""
    files = []
    for f in PROJECT_DIR.glob("*.py"):
        if f.name.startswith("test_"):
            continue
        files.append(f)
    return sorted(files)


def _parse_module(file_path: Path) -> dict:
    """Parse a Python module and extract public API."""
    try:
        source = file_path.read_text()
    except (UnicodeDecodeError, PermissionError):
        return {"file": str(file_path), "error": "unreadable"}

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return {"file": str(file_path), "error": "syntax error"}

    functions = []
    classes = []
    imports = []

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not node.name.startswith("_"):
                docstring = ast.get_docstring(node) or ""
                args = [a.arg for a in node.args.args if a.arg != "self"]
                functions.append({
                    "name": node.name,
                    "args": args,
                    "docstring": docstring.split("\n")[0] if docstring else "",
                    "line": node.lineno,
                })
        elif isinstance(node, ast.ClassDef):
            if not node.name.startswith("_"):
                methods = []
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        if not item.name.startswith("_"):
                            methods.append(item.name)
                docstring = ast.get_docstring(node) or ""
                classes.append({
                    "name": node.name,
                    "docstring": docstring.split("\n")[0] if docstring else "",
                    "methods": methods,
                    "line": node.lineno,
                })
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                imports.append(f"{module}.{alias.name}")

    loc = len(source.split("\n"))
    return {
        "file": file_path.name,
        "loc": loc,
        "functions": functions,
        "classes": classes,
        "imports": imports,
    }


# --- AI Guide Generator ---

def generate_ai_guide() -> str:
    """
    Generate an AI_GUIDE.md document by introspecting the codebase.

    This guide is structured for LLM consumption: concise, with clear
    module descriptions, API surfaces, and conventions.
    """
    files = _get_python_files()
    modules = [_parse_module(f) for f in files]

    lines = []
    lines.append("# AI Guide - Agent Orchestrator")
    lines.append("")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"Modules: {len(modules)}")
    total_loc = sum(m.get("loc", 0) for m in modules)
    lines.append(f"Total LOC: {total_loc}")
    lines.append("")
    lines.append("## Architecture Overview")
    lines.append("")
    lines.append("The orchestrator executes DAG-based pipelines where each node is")
    lines.append("an AI agent, bash command, loop, dependency, or review gate.")
    lines.append("")
    lines.append("Core components:")
    lines.append("")
    lines.append("1. **dag.py** - DAG/Pipeline data structures and YAML loader")
    lines.append("2. **executor.py** - Pipeline execution engine (DAGExecutor)")
    lines.append("3. **spawner.py** - Claude Code subprocess spawner")
    lines.append("4. **orchestrator.py** - GitHub issue polling and orchestration loop")
    lines.append("5. **poller.py** - GitHub issue tracker polling")
    lines.append("6. **execution_log.py** - Structured execution logging")
    lines.append("7. **review_sensor.py** - LLM-as-Judge post-review evaluation")
    lines.append("8. **garbage_collector.py** - Workspace GC and convention scanning")
    lines.append("9. **workspace_manager.py** - Workspace lifecycle state machine")
    lines.append("10. **roles.py** - Agent role definitions")
    lines.append("11. **orch_history.py** - Orchestration history tracking")
    lines.append("12. **self_doc.py** - This module (self-documentation)")
    lines.append("")
    lines.append("## Conventions")
    lines.append("")
    lines.append("- Use `python3` (not `python`)")
    lines.append("- Tests: `python3 -m pytest test_*.py -v`")
    lines.append("- Config: `orchestrator.yaml` in project root")
    lines.append("- Pipelines: YAML files in `pipelines/` directory")
    lines.append("- Logs: `~/.orchestrator/logs/`")
    lines.append("- Workspaces: `workspaces/{issue_number}/` with `meta.json`")
    lines.append("")
    lines.append("## Module API Reference")
    lines.append("")

    for mod in modules:
        if "error" in mod:
            continue

        lines.append(f"### {mod['file']}")
        lines.append("")
        lines.append(f"**Lines of code:** {mod['loc']}")
        lines.append("")

        if mod["functions"]:
            lines.append("**Functions:**")
            lines.append("")
            for func in mod["functions"]:
                args_str = ", ".join(func["args"]) if func["args"] else ""
                lines.append(f"- `{func['name']}({args_str})` - {func['docstring']}")
            lines.append("")

        if mod["classes"]:
            lines.append("**Classes:**")
            lines.append("")
            for cls in mod["classes"]:
                lines.append(f"- `{cls['name']}` - {cls['docstring']}")
                if cls["methods"]:
                    for m in cls["methods"]:
                        lines.append(f"  - `{m}()`")
            lines.append("")

    lines.append("## Pipeline Node Types")
    lines.append("")
    lines.append("| Type | Description |")
    lines.append("|------|-------------|")
    lines.append("| `ai` | Run an AI agent (Claude Code) |")
    lines.append("| `bash` | Execute a shell command |")
    lines.append("| `loop` | Repeat child nodes N times |")
    lines.append("| `dependency` | Wait for external condition |")
    lines.append("| `review` | LLM-as-Judge quality gate |")
    lines.append("")
    lines.append("## Pipeline YAML Format")
    lines.append("")
    lines.append("```yaml")
    lines.append("name: my-pipeline")
    lines.append("version: '1.0'")
    lines.append("nodes:")
    lines.append("  step1:")
    lines.append("    type: ai")
    lines.append("    prompt: 'Do X'")
    lines.append("    depends_on: []")
    lines.append("  step2:")
    lines.append("    type: bash")
    lines.append("    command: 'python3 test.py'")
    lines.append("    depends_on: [step1]")
    lines.append("```")
    lines.append("")
    lines.append("## Available Pipelines")
    lines.append("")

    pipelines_dir = PROJECT_DIR / "pipelines"
    if pipelines_dir.exists():
        for pf in sorted(pipelines_dir.glob("*.yaml")):
            try:
                from dag import load_pipeline
                pipeline = load_pipeline(str(pf))
                node_count = len(pipeline.nodes)
                lines.append(f"- **{pf.name}** ({pipeline.name}) - {node_count} nodes")
                if pipeline.description:
                    lines.append(f"  - {pipeline.description}")
            except Exception:
                lines.append(f"- **{pf.name}** - (parse error)")
            lines.append("")

    return "\n".join(lines)


# --- Changelog Generator ---

def generate_changelog(limit: int = 50) -> str:
    """
    Generate a CHANGELOG.md from git commit history.

    Args:
        limit: Maximum number of commits to include.

    Returns:
        Changelog markdown string.
    """
    try:
        result = subprocess.run(
            ["git", "-C", str(PROJECT_DIR), "log", f"--max-count={limit}",
             "--pretty=format:%h|%s|%an|%ad", "--date=short"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode != 0:
            return "# Changelog\n\nUnable to generate from git history.\n"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return "# Changelog\n\nGit not available.\n"

    lines = []
    lines.append("# Changelog")
    lines.append("")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"Showing last {limit} commits")
    lines.append("")

    current_date = None
    for entry in result.stdout.strip().split("\n"):
        if not entry.strip():
            continue
        parts = entry.split("|", 3)
        if len(parts) < 4:
            continue
        sha, subject, author, date = parts

        if date != current_date:
            current_date = date
            lines.append(f"## {date}")
            lines.append("")

        lines.append(f"- {subject} ({sha})")

    lines.append("")
    return "\n".join(lines)


# --- Architecture Overview ---

def generate_architecture() -> str:
    """
    Generate an architecture overview document.

    Returns:
        Architecture markdown string.
    """
    files = _get_python_files()
    modules = {f.name: _parse_module(f) for f in files}

    lines = []
    lines.append("# Architecture Overview")
    lines.append("")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")

    # Module dependency graph (from imports)
    lines.append("## Module Dependency Graph")
    lines.append("")
    lines.append("```")
    lines.append("orchestrator.py")
    lines.append("  -> poller.py")
    lines.append("  -> spawner.py")
    lines.append("  -> executor.py")
    lines.append("  -> execution_log.py")
    lines.append("  -> workspace_manager.py")
    lines.append("  -> roles.py")
    lines.append("")
    lines.append("executor.py")
    lines.append("  -> dag.py")
    lines.append("  -> spawner.py")
    lines.append("  -> execution_log.py")
    lines.append("  -> review_sensor.py")
    lines.append("")
    lines.append("review_sensor.py")
    lines.append("  -> execution_log.py")
    lines.append("")
    lines.append("garbage_collector.py")
    lines.append("  -> workspace_manager.py (indirect via filesystem)")
    lines.append("")
    lines.append("workspace_manager.py")
    lines.append("  (standalone)")
    lines.append("")
    lines.append("self_doc.py")
    lines.append("  -> dag.py (for pipeline listing)")
    lines.append("```")
    lines.append("")

    # Data flow
    lines.append("## Data Flow")
    lines.append("")
    lines.append("1. GitHub Issue created")
    lines.append("2. `poller.py` detects new issue")
    lines.append("3. `orchestrator.py` selects pipeline, creates workspace")
    lines.append("4. `executor.py` runs pipeline DAG")
    lines.append("5. Each node executes (AI/bash/loop/review)")
    lines.append("6. `execution_log.py` records results")
    lines.append("7. `review_sensor.py` evaluates quality (if review node)")
    lines.append("8. `workspace_manager.py` updates lifecycle state")
    lines.append("9. PR created/updated")
    lines.append("")

    # Size table
    lines.append("## Module Sizes")
    lines.append("")
    lines.append("| Module | LOC | Functions | Classes |")
    lines.append("|--------|-----|-----------|---------|")

    total_loc = 0
    total_funcs = 0
    total_classes = 0
    for name, mod in sorted(modules.items()):
        if "error" in mod:
            continue
        loc = mod.get("loc", 0)
        funcs = len(mod.get("functions", []))
        cls = len(mod.get("classes", []))
        total_loc += loc
        total_funcs += funcs
        total_classes += cls
        lines.append(f"| {name} | {loc} | {funcs} | {cls} |")

    lines.append(f"| **Total** | **{total_loc}** | **{total_funcs}** | **{total_classes}** |")
    lines.append("")

    # Test coverage info
    lines.append("## Test Coverage")
    lines.append("")
    test_files = list(PROJECT_DIR.glob("test_*.py"))
    test_loc = sum(
        len(f.read_text().split("\n"))
        for f in test_files
        if f.suffix == ".py"
    )
    lines.append(f"- Test files: {len(test_files)}")
    lines.append(f"- Test LOC: {test_loc}")
    lines.append(f"- Production LOC: {total_loc}")
    lines.append(f"- Test ratio: {test_loc / max(total_loc, 1):.2f}")
    lines.append("")

    return "\n".join(lines)


# --- Module Inventory ---

def get_inventory() -> dict:
    """Get a complete inventory of all modules."""
    files = _get_python_files()
    modules = [_parse_module(f) for f in files]

    return {
        "generated_at": datetime.now().isoformat(),
        "total_modules": len(modules),
        "modules": modules,
        "total_loc": sum(m.get("loc", 0) for m in modules),
        "total_functions": sum(len(m.get("functions", [])) for m in modules),
        "total_classes": sum(len(m.get("classes", [])) for m in modules),
    }


def _save_doc(content: str, filename: str) -> str:
    """Save a document to the docs directory."""
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    path = DOCS_DIR / filename
    path.write_text(content)
    return str(path)


def main():
    parser = argparse.ArgumentParser(description="Self-documentation generator")
    parser.add_argument("--guide", action="store_true", help="Generate AI_GUIDE.md")
    parser.add_argument("--changelog", action="store_true", help="Generate CHANGELOG.md")
    parser.add_argument("--architecture", action="store_true", help="Generate architecture doc")
    parser.add_argument("--all", action="store_true", help="Generate all documents")
    parser.add_argument("--inventory", action="store_true", help="Show module inventory")

    args = parser.parse_args()

    if args.all or args.guide:
        content = generate_ai_guide()
        path = _save_doc(content, "AI_GUIDE.md")
        print(f"Generated: {path}")

    if args.all or args.changelog:
        content = generate_changelog()
        path = _save_doc(content, "CHANGELOG.md")
        print(f"Generated: {path}")

    if args.all or args.architecture:
        content = generate_architecture()
        path = _save_doc(content, "ARCHITECTURE.md")
        print(f"Generated: {path}")

    if args.inventory:
        inv = get_inventory()
        print(json.dumps(inv, indent=2))

    if not any([args.all, args.guide, args.changelog, args.architecture, args.inventory]):
        parser.print_help()


if __name__ == "__main__":
    main()
