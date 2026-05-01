#!/usr/bin/env python3
"""
Role profile loader for the Hermes Agent Orchestrator.

Loads YAML role profiles from the roles/ directory and provides
utilities for matching issues to appropriate roles based on labels
or heuristics.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

PROJECT_DIR = Path(os.environ.get("ORCH_PROJECT_DIR", os.path.expanduser("~/zion/projects/agent-orchestration")))
ROLES_DIR = PROJECT_DIR / "roles"

# Label-to-role mapping heuristic
LABEL_ROLE_MAP: dict[str, str] = {
    "bug": "tester",
    "test": "tester",
    "testing": "tester",
    "feature": "implementer",
    "enhancement": "implementer",
    "refactor": "implementer",
    "review": "reviewer",
    "code-review": "reviewer",
    "triage": "coordinator",
    "coordination": "coordinator",
    "planning": "coordinator",
}

# Title keyword heuristics (used when no matching labels)
TITLE_ROLE_MAP: dict[str, str] = {
    "fix": "tester",
    "bug": "tester",
    "test": "tester",
    "implement": "implementer",
    "add": "implementer",
    "create": "implementer",
    "build": "implementer",
    "refactor": "implementer",
    "review": "reviewer",
    "audit": "reviewer",
    "plan": "coordinator",
    "triage": "coordinator",
    "organize": "coordinator",
}


@dataclass
class Role:
    """A role profile loaded from YAML."""
    name: str
    description: str
    system_prompt: str
    allowed_toolsets: list[str]
    max_turns: int
    acp_command: str = "claude"
    # Source file path
    source_file: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "system_prompt": self.system_prompt,
            "allowed_toolsets": self.allowed_toolsets,
            "max_turns": self.max_turns,
            "acp_command": self.acp_command,
        }


def load_role(path: str | Path) -> Role:
    """Load a single role profile from a YAML file."""
    path = Path(path)
    with open(path) as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict) or "name" not in data:
        raise ValueError(f"Invalid role profile: {path}")

    return Role(
        name=data["name"],
        description=data.get("description", ""),
        system_prompt=data.get("system_prompt", ""),
        allowed_toolsets=data.get("allowed_toolsets", []),
        max_turns=data.get("max_turns", 20),
        acp_command=data.get("acp_command", "claude"),
        source_file=str(path),
    )


def load_all_roles(roles_dir: str | Path | None = None) -> dict[str, Role]:
    """Load all role profiles from the roles directory."""
    roles_dir = Path(roles_dir) if roles_dir else ROLES_DIR
    roles: dict[str, Role] = {}

    if not roles_dir.exists():
        return roles

    for f in sorted(roles_dir.glob("*.yaml")):
        try:
            role = load_role(f)
            roles[role.name] = role
        except ValueError as e:
            print(f"Warning: {e}", file=__import__("sys").stderr)

    return roles


def match_role(issue: dict, roles: dict[str, Role] | None = None) -> Role | None:
    """
    Match an issue to the best role based on labels and title heuristics.

    Priority:
    1. Explicit label match (e.g. 'agent-role:reviewer')
    2. Known label heuristic (e.g. 'bug' -> tester)
    3. Title keyword heuristic
    4. Default: implementer (if available)
    """
    if roles is None:
        roles = load_all_roles()

    if not roles:
        return None

    labels = [l.lower() for l in issue.get("labels", [])]
    title = issue.get("title", "").lower()

    # 1. Check for explicit agent-role label
    for label in labels:
        if label.startswith("agent-role:"):
            role_name = label.split(":", 1)[1].strip()
            if role_name in roles:
                return roles[role_name]

    # 2. Check known label mappings
    for label in labels:
        if label in LABEL_ROLE_MAP:
            role_name = LABEL_ROLE_MAP[label]
            if role_name in roles:
                return roles[role_name]

    # 3. Check title keywords
    for keyword, role_name in TITLE_ROLE_MAP.items():
        if keyword in title and role_name in roles:
            return roles[role_name]

    # 4. Default to implementer
    return roles.get("implementer")


def build_role_prompt(base_prompt: str, role: Role) -> str:
    """Prepend role system prompt to the task prompt."""
    if not role.system_prompt:
        return base_prompt
    return f"{role.system_prompt}\n\n---\n\n{base_prompt}"
