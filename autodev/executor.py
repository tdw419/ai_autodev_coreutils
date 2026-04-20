"""Executor -- builds the creative intent using Hermes subprocess.

The executor takes a CreativeIntent and runs a Hermes subprocess to actually
build it. The key difference from autodev v1: the prompt comes from the AI's
own intent, not from a roadmap task.
"""

import os
import subprocess
import time
from typing import Optional

from .models import CreativeIntent, BuildResult


# The prompt template that turns creative intent into a build instruction
BUILD_PROMPT = """You are building something you chose to create. Nobody assigned this to you.

## What you're building
{summary}

## Why you chose this
{reasoning}

## Specific scope
{scope}

## Rules
1. Build it in: {target_dir}
2. Create the directory if needed
3. Write the code -- make it work, not just look right
4. Test it if possible (run it, check output)
5. Commit to git if the result works
6. Keep it small -- under 200 lines
7. Use absolute paths for all file operations

## What success looks like
The code runs and does something interesting. It doesn't have to be perfect.
It has to be real -- not a stub, not a TODO, not a placeholder.

Build it now."""


def execute_build(intent: CreativeIntent, timeout: int = 900) -> BuildResult:
    """
    Run a Hermes subprocess to build the creative intent.

    Args:
        intent: What the AI chose to build
        timeout: Max seconds for the build (default 15 min)

    Returns:
        BuildResult with success/failure and output
    """
    start = time.time()

    # Ensure target directory exists
    os.makedirs(intent.target_dir, exist_ok=True)

    # Initialize git repo in target
    subprocess.run(
        ["git", "init"],
        cwd=intent.target_dir,
        capture_output=True, timeout=10
    )

    # Build the prompt from the AI's own intent
    prompt = BUILD_PROMPT.format(
        summary=intent.summary,
        reasoning=intent.reasoning,
        scope=intent.scope,
        target_dir=intent.target_dir,
    )

    # Run Hermes subprocess
    try:
        result = subprocess.run(
            ["hermes", "chat", "-q", prompt, "-t", ""],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=intent.target_dir,
        )
        elapsed = time.time() - start

        output = result.stdout or ""
        if result.stderr:
            output += f"\nSTDERR: {result.stderr[-500:]}"

        # Check what was actually created
        artifacts = _list_artifacts(intent.target_dir)
        git_commits = _get_git_commits(intent.target_dir)

        success = len(artifacts) > 0 and result.returncode == 0

        return BuildResult(
            success=success,
            output=output[-3000:],  # Keep last 3000 chars
            artifacts=artifacts,
            error=None if success else f"exit_code={result.returncode}",
            elapsed_seconds=elapsed,
            git_commits=git_commits,
        )

    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        # Check if anything was created before timeout
        artifacts = _list_artifacts(intent.target_dir)
        git_commits = _get_git_commits(intent.target_dir)

        return BuildResult(
            success=len(artifacts) > 0,
            output="(timed out, but files may exist)",
            artifacts=artifacts,
            error="timeout",
            elapsed_seconds=elapsed,
            git_commits=git_commits,
        )

    except Exception as e:
        elapsed = time.time() - start
        return BuildResult(
            success=False,
            output="",
            error=str(e),
            elapsed_seconds=elapsed,
        )


def _list_artifacts(target_dir: str) -> list:
    """List non-git files created in the target directory."""
    artifacts = []
    for root, dirs, files in os.walk(target_dir):
        # Skip .git
        dirs[:] = [d for d in dirs if d != ".git"]
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, target_dir)
            size = os.path.getsize(full)
            if size > 0:
                artifacts.append({"path": rel, "size": size})
    return artifacts


def _get_git_commits(target_dir: str) -> list:
    """Get git commits made in the target directory."""
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "-5"],
            cwd=target_dir,
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
    except Exception:
        pass
    return []
