"""Shared contract for all autodev coreutils.

Every tool:
1. Reads a project directory (default: .)
2. Reads/writes markdown specs as universal interchange
3. Writes state to .autodev/ in the project dir
4. Exits 0 on success, non-zero on failure
5. Accepts --json for machine-readable output
6. Accepts --quiet for piped composition (errors only)
"""

import json
import os
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


# Exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EXIT_BAD_ARGS = 2
EXIT_TIMEOUT = 3
EXIT_NO_PROJECT = 4


# The state directory -- every project gets one
AUTODEV_DIR = ".autodev"


class Exit(Exception):
    """Clean exit with code and optional message."""
    def __init__(self, code: int, message: str = ""):
        self.code = code
        self.message = message
        super().__init__(message)


def find_project(path: str = ".") -> Path:
    """Find the project root by walking up looking for common markers."""
    p = Path(path).resolve()
    markers = [
        ".git",
        "pyproject.toml",
        "Cargo.toml",
        "package.json",
        "go.mod",
        "AUTODEV_ROOT",  # explicit marker
    ]
    for parent in [p] + list(p.parents):
        for marker in markers:
            if (parent / marker).exists():
                return parent
    # Fall back to cwd
    return p


def ensure_autodev_dir(project: Path) -> Path:
    """Create .autodev/ directory if it doesn't exist."""
    ad = project / AUTODEV_DIR
    ad.mkdir(exist_ok=True)
    return ad


def write_state(project: Path, tool_name: str, data: dict) -> Path:
    """Write a state document for a tool."""
    ad = ensure_autodev_dir(project)
    state_file = ad / f"{tool_name}_state.json"
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    data["tool"] = tool_name
    state_file.write_text(json.dumps(data, indent=2, default=str))
    return state_file


def read_state(project: Path, tool_name: str) -> Optional[dict]:
    """Read a tool's state document."""
    state_file = project / AUTODEV_DIR / f"{tool_name}_state.json"
    if state_file.exists():
        return json.loads(state_file.read_text())
    return None


def write_spec(project: Path, name: str, content: str) -> Path:
    """Write a markdown spec to the project."""
    ad = ensure_autodev_dir(project)
    spec_file = ad / f"{name}.md"
    spec_file.write_text(content)
    return spec_file


def read_spec(project: Path, name: str) -> Optional[str]:
    """Read a markdown spec from the project."""
    spec_file = project / AUTODEV_DIR / f"{name}.md"
    if spec_file.exists():
        return spec_file.read_text()
    return None


def output(result: Any, json_mode: bool = False, quiet: bool = False):
    """Print result respecting --json and --quiet flags."""
    if quiet:
        return
    if json_mode:
        print(json.dumps(result, indent=2, default=str))
    elif isinstance(result, str):
        print(result)
    elif isinstance(result, dict):
        # Pretty-print dict as key-value
        for k, v in result.items():
            print(f"{k}: {v}")
    else:
        print(result)


def error(msg: str, code: int = EXIT_FAILURE):
    """Print error to stderr and exit."""
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def add_common_args(parser: argparse.ArgumentParser):
    """Add the standard flags every coreutil accepts."""
    parser.add_argument(
        "-w", "--workdir",
        default=".",
        help="Project directory (default: current directory)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output in JSON format",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress output (errors only)",
    )


def make_parser(name: str, description: str) -> argparse.ArgumentParser:
    """Create a standard parser with common args."""
    parser = argparse.ArgumentParser(
        prog=f"autodev-{name}",
        description=description,
    )
    add_common_args(parser)
    return parser
