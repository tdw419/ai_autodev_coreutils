#!/usr/bin/env python3
"""
Project onboarding bootstrap for the Hermes Agent Orchestrator.

Analyzes a repository to detect its language, framework, build system,
and test runner, then generates an appropriate AI_GUIDE.md and
orchestrator configuration.

Usage:
    python3 onboard.py --detect ~/path/to/repo
    python3 onboard.py --guide ~/path/to/repo
    python3 onboard.py --guide ~/path/to/repo --write
    python3 onboard.py owner/repo --full [--dry-run] [--pipeline standard-pipeline]
    python3 onboard.py owner/repo --full --dry-run

Inspired by OpenAI Symphony's WORKFLOW.md auto-detection pattern:
making projects agent-legible with minimal human effort.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


# ─── Project Type Detection ─────────────────────────────────────

LANGUAGE_MARKERS: dict[str, list[str]] = {
    "python": ["setup.py", "setup.cfg", "pyproject.toml", "requirements.txt",
               "Pipfile", "poetry.lock", ".python-version", "manage.py"],
    "node": ["package.json", "tsconfig.json", ".nvmrc", "node_modules",
             "next.config.js", "vite.config.ts", "webpack.config.js"],
    "go": ["go.mod", "go.sum", "main.go", "Makefile"],
    "rust": ["Cargo.toml", "Cargo.lock"],
    "ruby": ["Gemfile", "Rakefile", "Gemfile.lock", ".ruby-version"],
    "java": ["pom.xml", "build.gradle", "build.gradle.kts", "settings.gradle"],
}

FRAMEWORK_PATTERNS: dict[str, dict[str, list[str]]] = {
    "python": {
        "django": ["django", "DJANGO_SETTINGS_MODULE"],
        "fastapi": ["fastapi", "uvicorn"],
        "flask": ["flask", "Flask"],
        "pydantic": ["pydantic"],
        "click": ["click"],
        "pytest": ["pytest"],
    },
    "node": {
        "express": ["express"],
        "nextjs": ["next", "next.config"],
        "react": ["react", "React"],
        "vue": ["vue"],
        "nest": ["@nestjs/core"],
    },
    "go": {
        "gin": ["gin-gonic/gin"],
        "echo": ["labstack/echo"],
        "chi": ["go-chi/chi"],
    },
}

TEST_RUNNERS: dict[str, list[dict[str, str]]] = {
    "python": [
        {"name": "pytest", "marker": "pytest", "command": "python3 -m pytest"},
        {"name": "unittest", "marker": "unittest", "command": "python3 -m unittest discover"},
    ],
    "node": [
        {"name": "jest", "marker": '"jest"', "command": "npx jest"},
        {"name": "vitest", "marker": '"vitest"', "command": "npx vitest"},
        {"name": "mocha", "marker": '"mocha"', "command": "npx mocha"},
    ],
    "go": [
        {"name": "go test", "marker": "go_test", "command": "go test ./..."},
    ],
    "rust": [
        {"name": "cargo test", "marker": "Cargo.toml", "command": "cargo test"},
    ],
    "ruby": [
        {"name": "rspec", "marker": "rspec", "command": "bundle exec rspec"},
    ],
    "java": [
        {"name": "maven", "marker": "pom.xml", "command": "mvn test"},
        {"name": "gradle", "marker": "build.gradle", "command": "gradle test"},
    ],
}

LINTERS: dict[str, list[dict[str, str]]] = {
    "python": [
        {"name": "ruff", "marker": "ruff", "command": "ruff check ."},
        {"name": "flake8", "marker": "flake8", "command": "flake8 ."},
        {"name": "pylint", "marker": "pylint", "command": "pylint ."},
        {"name": "mypy", "marker": "mypy", "command": "mypy ."},
    ],
    "node": [
        {"name": "eslint", "marker": "eslint", "command": "npx eslint ."},
        {"name": "prettier", "marker": "prettier", "command": "npx prettier --check ."},
    ],
    "go": [
        {"name": "golangci-lint", "marker": "golangci", "command": "golangci-lint run"},
    ],
    "rust": [
        {"name": "cargo clippy", "marker": "Cargo.toml", "command": "cargo clippy"},
    ],
}

BUILD_COMMANDS: dict[str, list[dict[str, str]]] = {
    "python": [
        {"name": "pip install", "marker": "requirements.txt", "command": "pip install -r requirements.txt"},
        {"name": "pip install -e", "marker": "setup.py", "command": "pip install -e ."},
        {"name": "poetry install", "marker": "poetry.lock", "command": "poetry install"},
    ],
    "node": [
        {"name": "npm install", "marker": "package.json", "command": "npm install"},
        {"name": "npm build", "marker": "package.json", "command": "npm run build"},
    ],
    "go": [
        {"name": "go build", "marker": "go.mod", "command": "go build ./..."},
    ],
    "rust": [
        {"name": "cargo build", "marker": "Cargo.toml", "command": "cargo build"},
    ],
}


def detect_language(repo_path: Path) -> str | None:
    """Detect the primary programming language from file markers."""
    scores: dict[str, int] = {}
    for lang, markers in LANGUAGE_MARKERS.items():
        for marker in markers:
            if (repo_path / marker).exists():
                scores[lang] = scores.get(lang, 0) + 1

    if not scores:
        return None
    return max(scores, key=scores.get)


def detect_frameworks(repo_path: Path, language: str) -> list[str]:
    """Detect frameworks from dependency files."""
    found = []
    patterns = FRAMEWORK_PATTERNS.get(language, {})

    # Check dependency files
    dep_files = []
    if language == "python":
        for f in ["requirements.txt", "pyproject.toml", "setup.py"]:
            if (repo_path / f).exists():
                dep_files.append(repo_path / f)
    elif language == "node":
        if (repo_path / "package.json").exists():
            dep_files.append(repo_path / "package.json")
    elif language == "go":
        if (repo_path / "go.mod").exists():
            dep_files.append(repo_path / "go.mod")

    for dep_file in dep_files:
        try:
            content = dep_file.read_text()
            for framework, markers in patterns.items():
                for marker in markers:
                    if marker.lower() in content.lower():
                        if framework not in found:
                            found.append(framework)
        except (OSError, UnicodeDecodeError):
            continue

    return found


def detect_test_runner(repo_path: Path, language: str) -> dict[str, str] | None:
    """Detect the test runner by checking for test files and configs."""
    runners = TEST_RUNNERS.get(language, [])
    if not runners:
        return None

    # Check for test config files
    for runner in runners:
        marker = runner["marker"]
        # Check for config files
        config_files = {
            "pytest": ["pytest.ini", "pyproject.toml", "setup.cfg"],
            "jest": ["jest.config.js", "jest.config.ts", "package.json"],
            "vitest": ["vitest.config.ts", "vite.config.ts"],
            "mocha": [".mocharc.js", ".mocharc.json"],
        }
        if runner["name"] in config_files:
            for cfg in config_files[runner["name"]]:
                if (repo_path / cfg).exists():
                    content = (repo_path / cfg).read_text()
                    if marker.lower() in content.lower():
                        return runner

    # Check for test directories
    test_dirs = {
        "python": ["tests", "test"],
        "node": ["__tests__", "test", "tests"],
        "go": ["", ],  # Go uses _test.go files
        "rust": ["tests"],
    }
    lang_test_dirs = test_dirs.get(language, [])
    for d in lang_test_dirs:
        if d and (repo_path / d).is_dir():
            # If there are test files, use the first matching runner
            for runner in runners:
                return runner

    # Fallback: return the first runner for the language
    return runners[0] if runners else None


def detect_linter(repo_path: Path, language: str) -> dict[str, str] | None:
    """Detect the linter from config files."""
    linters = LINTERS.get(language, [])
    if not linters:
        return None

    config_patterns = {
        "ruff": ["ruff.toml", "pyproject.toml"],
        "flake8": [".flake8", "setup.cfg", "tox.ini"],
        "pylint": [".pylintrc", "pyproject.toml"],
        "mypy": ["mypy.ini", "pyproject.toml"],
        "eslint": [".eslintrc.js", ".eslintrc.json", "eslint.config.js"],
        "prettier": [".prettierrc", ".prettierrc.json", "prettier.config.js"],
        "golangci-lint": [".golangci.yml", ".golangci.yaml"],
    }

    for linter in linters:
        name = linter["name"]
        if name in config_patterns:
            for cfg in config_patterns[name]:
                if (repo_path / cfg).exists():
                    content = (repo_path / cfg).read_text()
                    if linter["marker"].lower() in content.lower():
                        return linter

    # Fallback: return the first linter
    return linters[0] if linters else None


def detect_build_command(repo_path: Path, language: str) -> dict[str, str] | None:
    """Detect the build/install command."""
    builds = BUILD_COMMANDS.get(language, [])
    if not builds:
        return None

    for build in builds:
        marker = build["marker"]
        if (repo_path / marker).exists():
            return build

    return builds[0] if builds else None


def detect_existing_guide(repo_path: Path) -> bool:
    """Check if an AI_GUIDE.md or AGENT.md already exists."""
    return (
        (repo_path / "AI_GUIDE.md").exists()
        or (repo_path / "AGENT.md").exists()
        or (repo_path / ".ai-guide.md").exists()
    )


def get_version_command(language: str) -> str:
    """Get the version command for a language."""
    return {
        "python": "python3 --version",
        "node": "node --version",
        "go": "go version",
        "rust": "rustc --version",
        "ruby": "ruby --version",
        "java": "java --version",
    }.get(language, "echo 'unknown'")


def get_version(repo_path: Path, language: str) -> str:
    """Run the version command and return the output."""
    cmd = get_version_command(language)
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=10,
            cwd=str(repo_path)
        )
        return result.stdout.strip().split("\n")[0]
    except (subprocess.TimeoutExpired, Exception):
        return "unknown"


def detect_project(repo_path: str | Path) -> dict[str, Any]:
    """
    Analyze a repository and return a structured detection result.

    Returns:
        dict with keys: path, language, frameworks, test_runner,
        linter, build_command, has_guide, version
    """
    repo = Path(repo_path).resolve()
    if not repo.is_dir():
        raise FileNotFoundError(f"Not a directory: {repo}")

    language = detect_language(repo)
    frameworks = detect_frameworks(repo, language) if language else []
    test_runner = detect_test_runner(repo, language) if language else None
    linter = detect_linter(repo, language) if language else None
    build_cmd = detect_build_command(repo, language) if language else None
    has_guide = detect_existing_guide(repo)
    version = get_version(repo, language) if language else "unknown"

    return {
        "path": str(repo),
        "language": language,
        "frameworks": frameworks,
        "test_runner": test_runner,
        "linter": linter,
        "build_command": build_cmd,
        "has_guide": has_guide,
        "version": version,
    }


def format_detection(result: dict[str, Any]) -> str:
    """Format detection result as human-readable output."""
    lines = [
        f"Project: {result['path']}",
        f"Language: {result['language'] or 'unknown'}",
        f"Version: {result['version']}",
    ]

    if result["frameworks"]:
        lines.append(f"Frameworks: {', '.join(result['frameworks'])}")

    if result["test_runner"]:
        lines.append(f"Test runner: {result['test_runner']['name']} "
                      f"({result['test_runner']['command']})")

    if result["linter"]:
        lines.append(f"Linter: {result['linter']['name']} "
                      f"({result['linter']['command']})")

    if result["build_command"]:
        lines.append(f"Build: {result['build_command']['name']} "
                      f"({result['build_command']['command']})")

    if result["has_guide"]:
        lines.append("AI guide: exists ✓")
    else:
        lines.append("AI guide: none (use --guide to generate)")

    return "\n".join(lines)


# ─── AI_GUIDE.md Generation ─────────────────────────────────────

def generate_guide(result: dict[str, Any]) -> str:
    """
    Generate an AI_GUIDE.md based on the project detection result.

    Produces a guide with:
    - Tech stack section
    - Executable commands (build, test, lint)
    - Three-tier boundaries (auto-approve, decide, ask)
    - Project-specific conventions
    """
    lang = result.get("language") or "unknown"
    version = result.get("version", "unknown")
    frameworks = result.get("frameworks", [])
    test = result.get("test_runner", {})
    linter = result.get("linter", {})
    build = result.get("build_command", {})

    fw_str = ", ".join(frameworks) if frameworks else "none detected"

    sections = [
        "# AI Guide",
        "",
        f"**Project language:** {lang} ({version})",
        f"**Frameworks:** {fw_str}",
        "",
        "## Commands",
        "",
    ]

    # Build command
    if build:
        sections.append(f"- **Install/Build:** `{build['command']}`")
    else:
        sections.append(f"- **Install/Build:** (auto-detect failed — add manually)")

    # Test command
    if test:
        sections.append(f"- **Test:** `{test['command']}`")
    else:
        sections.append(f"- **Test:** (auto-detect failed — add manually)")

    # Lint command
    if linter:
        sections.append(f"- **Lint:** `{linter['command']}`")

    sections.extend([
        "",
        "## Conventions",
        "",
        "These were auto-detected. Review and correct as needed:",
        "",
        f"- Language: **{lang}**",
    ])

    if frameworks:
        for fw in frameworks:
            sections.append(f"- Framework: **{fw}**")

    sections.extend([
        "",
        "## Boundaries",
        "",
        "### ✅ Auto-approve (no permission needed)",
        "",
        "- Running tests",
        "- Running linter",
        "- Fixing lint errors",
        "- Adding missing imports",
        "- Updating type annotations",
        "",
        "### ⚡ Decide and act (commit first, explain later)",
        "",
        "- Fixing failing tests",
        "- Refactoring within a module",
        "- Adding new files following existing patterns",
        "- Updating dependencies",
        "- Changing configuration",
        "",
        "### 🛑 Ask first",
        "",
        "- Changing the public API",
        "- Modifying database schemas",
        "- Changing authentication/authorization",
        "- Removing features or deprecating APIs",
        "- Changing deployment configuration",
        "",
        "---",
        "",
        "_This guide was auto-generated by the Hermes Orchestrator onboarding tool._",
        "_Review and customize it for your project._",
        "",
    ])

    return "\n".join(sections)


# ─── Orchestrator Config Generation ─────────────────────────────

def generate_orchestrator_config(repo_name: str, result: dict[str, Any],
                                  pipeline: str = "standard-pipeline") -> dict[str, Any]:
    """Generate a minimal orchestrator.yaml entry for a repo."""
    lang = result.get("language") or "unknown"
    test_cmd = (result.get("test_runner") or {}).get("command", "")
    lint_cmd = (result.get("linter") or {}).get("command", "")

    return {
        "repo": repo_name,
        "label": "agent-ready",
        "pipeline": pipeline,
        "language": lang,
        "test_command": test_cmd,
        "lint_command": lint_cmd,
        "max_concurrent": 1,
    }


# ─── Full Onboarding Flow ───────────────────────────────────────

def onboard_full(repo_spec: str, *, dry_run: bool = False,
                 pipeline: str = "standard-pipeline") -> dict[str, Any]:
    """
    Full onboarding flow for a GitHub repo.

    Args:
        repo_spec: GitHub owner/repo or local path
        dry_run: Preview changes without applying
        pipeline: Pipeline template to use

    Returns:
        dict with all actions taken (or would take)
    """
    actions = []

    # Resolve repo path
    if "/" in repo_spec and not os.path.exists(repo_spec):
        # GitHub repo spec — try to clone or find locally
        repo_path = Path(repo_spec.replace("/", "_"))
        if not repo_path.exists():
            if dry_run:
                actions.append({"type": "clone", "repo": repo_spec,
                                "target": str(repo_path), "status": "would_clone"})
                repo_path = None
            else:
                try:
                    subprocess.run(
                        ["gh", "repo", "clone", repo_spec, str(repo_path)],
                        check=True, capture_output=True, timeout=120
                    )
                    actions.append({"type": "clone", "repo": repo_spec,
                                    "target": str(repo_path), "status": "cloned"})
                except (subprocess.CalledProcessError, FileNotFoundError) as e:
                    actions.append({"type": "clone", "repo": repo_spec,
                                    "status": "failed", "error": str(e)})
                    return {"actions": actions, "status": "failed"}
    else:
        repo_path = Path(repo_spec).resolve()

    # Detect project
    if repo_path and repo_path.exists():
        detection = detect_project(repo_path)
        actions.append({"type": "detect", "result": detection})

        # Generate AI_GUIDE.md
        guide_content = generate_guide(detection)
        guide_path = repo_path / "AI_GUIDE.md"

        if detection["has_guide"]:
            actions.append({"type": "guide", "status": "skipped",
                            "reason": "AI_GUIDE.md already exists"})
        elif dry_run:
            actions.append({"type": "guide", "path": str(guide_path),
                            "status": "would_write", "preview_length": len(guide_content)})
        else:
            guide_path.write_text(guide_content)
            actions.append({"type": "guide", "path": str(guide_path),
                            "status": "written"})

        # Generate orchestrator config
        config = generate_orchestrator_config(repo_spec, detection, pipeline)

        if dry_run:
            actions.append({"type": "config", "status": "would_generate",
                            "config": config})
        else:
            actions.append({"type": "config", "status": "generated",
                            "config": config})

        # Add GitHub label
        if dry_run:
            actions.append({"type": "label", "repo": repo_spec,
                            "label": "agent-ready", "status": "would_create"})
        else:
            try:
                subprocess.run(
                    ["gh", "label", "create", "agent-ready",
                     "--description", "Ready for agent orchestration",
                     "--color", "0E8A16", "--force", "-R", repo_spec],
                    check=True, capture_output=True, timeout=30
                )
                actions.append({"type": "label", "repo": repo_spec,
                                "label": "agent-ready", "status": "created"})
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                actions.append({"type": "label", "repo": repo_spec,
                                "status": "failed", "error": str(e)})

        # Generate cron command
        cron_cmd = f"*/5 * * * * cd ~/zion/projects/agent-orchestration && python3 orchestrator.py 2>&1"
        actions.append({"type": "cron", "command": cron_cmd, "status": "suggested"})
    else:
        actions.append({"type": "detect", "status": "skipped",
                        "reason": "repo path not available"})

    return {
        "actions": actions,
        "status": "success" if not dry_run else "dry_run",
        "repo": repo_spec,
    }


def format_onboarding_result(result: dict[str, Any]) -> str:
    """Format the onboarding result as human-readable output."""
    lines = [
        f"{'='*60}",
        f"  Onboarding: {result['repo']}",
        f"  Status: {result['status']}",
        f"{'='*60}",
        "",
    ]

    for action in result["actions"]:
        atype = action["type"]

        if atype == "detect":
            if "result" in action:
                lines.append("📋 Detection:")
                lines.append(format_detection(action["result"]))
            else:
                lines.append(f"📋 Detection: {action.get('reason', 'skipped')}")
            lines.append("")

        elif atype == "guide":
            if action["status"] == "written":
                lines.append(f"📝 AI_GUIDE.md written to {action['path']}")
            elif action["status"] == "would_write":
                lines.append(f"📝 AI_GUIDE.md would be written ({action['preview_length']} chars)")
            elif action["status"] == "skipped":
                lines.append(f"📝 AI_GUIDE.md skipped ({action['reason']})")
            lines.append("")

        elif atype == "config":
            lines.append("⚙️  Orchestrator config:")
            config = action["config"]
            lines.append(f"   repo: {config['repo']}")
            lines.append(f"   label: {config['label']}")
            lines.append(f"   pipeline: {config['pipeline']}")
            lines.append(f"   language: {config['language']}")
            if config.get("test_command"):
                lines.append(f"   test: {config['test_command']}")
            if config.get("lint_command"):
                lines.append(f"   lint: {config['lint_command']}")
            lines.append("")

        elif atype == "label":
            if action["status"] == "created":
                lines.append(f"🏷️  GitHub label 'agent-ready' created on {action['repo']}")
            elif action["status"] == "would_create":
                lines.append(f"🏷️  Would create label 'agent-ready' on {action['repo']}")
            else:
                lines.append(f"🏷️  Label creation failed: {action.get('error', 'unknown')}")
            lines.append("")

        elif atype == "cron":
            lines.append("⏰ Suggested cron job:")
            lines.append(f"   {action['command']}")
            lines.append("")

        elif atype == "clone":
            if action["status"] == "cloned":
                lines.append(f"📦 Cloned {action['repo']} to {action['target']}")
            elif action["status"] == "would_clone":
                lines.append(f"📦 Would clone {action['repo']} to {action['target']}")
            lines.append("")

    return "\n".join(lines)


# ─── CLI ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Onboard a project to the Hermes Agent Orchestrator"
    )
    parser.add_argument("repo", help="GitHub owner/repo or local path")
    parser.add_argument("--detect", action="store_true",
                        help="Detect project type only")
    parser.add_argument("--guide", action="store_true",
                        help="Generate AI_GUIDE.md")
    parser.add_argument("--write", action="store_true",
                        help="Write AI_GUIDE.md to repo root (use with --guide)")
    parser.add_argument("--full", action="store_true",
                        help="Full onboarding (detect + guide + config + label)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview changes without applying")
    parser.add_argument("--pipeline", default="standard-pipeline",
                        help="Pipeline template to use (default: standard-pipeline)")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")

    args = parser.parse_args()

    if args.detect:
        result = detect_project(args.repo)
        if args.json:
            print(json.dumps(result, indent=2, default=str))
        else:
            print(format_detection(result))

    elif args.guide:
        result = detect_project(args.repo)
        guide = generate_guide(result)
        if args.write:
            guide_path = Path(args.repo) / "AI_GUIDE.md"
            guide_path.write_text(guide)
            print(f"AI_GUIDE.md written to {guide_path}")
        else:
            print(guide)

    elif args.full:
        result = onboard_full(
            args.repo, dry_run=args.dry_run, pipeline=args.pipeline
        )
        if args.json:
            print(json.dumps(result, indent=2, default=str))
        else:
            print(format_onboarding_result(result))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
