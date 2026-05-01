#!/usr/bin/env python3
"""
Safety Policies and Approval Gates for the Hermes Agent Orchestrator.

Enforces safety rules on pipeline execution:
- File path restrictions (no writes outside workspace)
- Command blacklisting (dangerous bash commands)
- Resource limits (max runtime, max output size)
- Approval gates (require human approval for sensitive operations)
- Audit logging of all policy decisions

Usage:
    python3 safety.py --check PATH        # Check if path is allowed
    python3 safety.py --check-cmd "rm -rf"  # Check if command is allowed
    python3 safety.py --audit             # Show recent audit log
    python3 safety.py --policy            # Show current policy
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional

PROJECT_DIR = Path(os.environ.get(
    "ORCH_PROJECT_DIR",
    os.path.expanduser("~/zion/projects/agent-orchestration"),
))
ORCH_DIR = Path(os.path.expanduser("~/.orchestrator"))
AUDIT_DIR = ORCH_DIR / "logs" / "audit"


class PolicyAction(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    APPROVE = "approve"  # Requires human approval


class PolicyDecision:
    """Result of a policy check."""

    def __init__(self, action: PolicyAction, reason: str, policy: str = ""):
        self.action = action
        self.reason = reason
        self.policy = policy

    def to_dict(self) -> dict:
        return {
            "action": self.action.value,
            "reason": self.reason,
            "policy": self.policy,
        }

    @property
    def allowed(self) -> bool:
        return self.action == PolicyAction.ALLOW


# --- Default Policy Configuration ---

DEFAULT_POLICY = {
    # Dangerous commands that are always denied
    "command_blacklist": [
        r"rm\s+-rf\s+/",
        r"rm\s+-rf\s+\*",
        r"mkfs",
        r"dd\s+if=",
        r"chmod\s+777\s+/",
        r":\(\)\{\s*:\|",
        r"curl.*\|\s*bash",
        r"wget.*\|\s*sh",
        r"sudo\s+rm",
        r"shutdown",
        r"reboot",
        r"init\s+0",
        r">\s*/dev/sd",
    ],

    # Paths that are always denied
    "path_blacklist": [
        "/etc/passwd",
        "/etc/shadow",
        "/etc/sudoers",
        "/boot/",
        "/usr/bin/",
        "/usr/lib/",
        "/usr/sbin/",
        "/bin/",
        "/sbin/",
        "/root/",
    ],

    # File extensions that require approval
    "sensitive_extensions": [
        ".sh", ".bash", ".zsh",
        ".service",
        ".cron",
        ".conf",
        ".env",
    ],

    # Resource limits
    "max_bash_timeout_seconds": 300,
    "max_ai_turns": 50,
    "max_output_bytes": 1_000_000,  # 1MB

    # Write restrictions
    "workspace_only_writes": True,
}


def _ensure_dirs():
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)


# --- Policy Checks ---

def check_command(command: str, policy: dict | None = None) -> PolicyDecision:
    """
    Check if a bash command is allowed under policy.

    Args:
        command: The command string to check.
        policy: Policy dict (uses DEFAULT_POLICY if None).

    Returns:
        PolicyDecision with allow/deny/approve.
    """
    policy = policy or DEFAULT_POLICY

    for pattern in policy.get("command_blacklist", []):
        if re.search(pattern, command, re.IGNORECASE):
            _audit("command_check", "deny", command, f"Matched blacklist: {pattern}")
            return PolicyDecision(PolicyAction.DENY, f"Command matches blacklist pattern: {pattern}", "command_blacklist")

    _audit("command_check", "allow", command, "No blacklist match")
    return PolicyDecision(PolicyAction.ALLOW, "Command allowed", "command_check")


def check_path(path: str, workspace: str = "", policy: dict | None = None) -> PolicyDecision:
    """
    Check if a file path is allowed under policy.

    Args:
        path: File path to check.
        workspace: Workspace directory (for workspace-only-writes enforcement).
        policy: Policy dict.

    Returns:
        PolicyDecision.
    """
    policy = policy or DEFAULT_POLICY

    resolved = Path(path).resolve()

    # Check blacklist
    for blacklisted in policy.get("path_blacklist", []):
        if str(resolved).startswith(blacklisted):
            _audit("path_check", "deny", path, f"In blacklist: {blacklisted}")
            return PolicyDecision(PolicyAction.DENY, f"Path in blacklist: {blacklisted}", "path_blacklist")

    # Check workspace restriction
    if policy.get("workspace_only_writes") and workspace:
        ws_resolved = Path(workspace).resolve()
        if not str(resolved).startswith(str(ws_resolved)):
            _audit("path_check", "approve", path, f"Outside workspace: {workspace}")
            return PolicyDecision(PolicyAction.APPROVE, f"Path outside workspace, requires approval", "workspace_only_writes")

    _audit("path_check", "allow", path, "All checks passed")
    return PolicyDecision(PolicyAction.ALLOW, "Path allowed", "path_check")


def check_file_extension(filename: str, policy: dict | None = None) -> PolicyDecision:
    """Check if a file extension requires approval."""
    policy = policy or DEFAULT_POLICY

    p = Path(filename)
    ext = p.suffix.lower()
    name = p.name.lower()  # For dotfiles like .env

    # Check both suffix and full name against sensitive list
    sensitive = policy.get("sensitive_extensions", [])
    if ext in sensitive or name in sensitive:
        _audit("extension_check", "approve", filename, f"Sensitive extension: {ext or name}")
        return PolicyDecision(PolicyAction.APPROVE, f"Sensitive file extension: {ext or name}", "sensitive_extensions")

    _audit("extension_check", "allow", filename, "Not sensitive")
    return PolicyDecision(PolicyAction.ALLOW, "Extension allowed", "extension_check")


def check_resource_usage(duration_seconds: float, output_bytes: int, policy: dict | None = None) -> PolicyDecision:
    """Check if resource usage is within limits."""
    policy = policy or DEFAULT_POLICY

    max_timeout = policy.get("max_bash_timeout_seconds", 300)
    if duration_seconds > max_timeout:
        _audit("resource_check", "deny", "", f"Exceeded timeout: {duration_seconds}s > {max_timeout}s")
        return PolicyDecision(PolicyAction.DENY, f"Exceeded max timeout: {duration_seconds}s > {max_timeout}s", "max_timeout")

    max_output = policy.get("max_output_bytes", 1_000_000)
    if output_bytes > max_output:
        _audit("resource_check", "approve", "", f"Large output: {output_bytes} bytes")
        return PolicyDecision(PolicyAction.APPROVE, f"Large output: {output_bytes} bytes", "max_output")

    _audit("resource_check", "allow", "", f"Duration: {duration_seconds}s, Output: {output_bytes} bytes")
    return PolicyDecision(PolicyAction.ALLOW, "Resource usage OK", "resource_check")


# --- Approval Queue ---

def request_approval(operation: str, detail: str, policy: str = "") -> dict:
    """Add an operation to the approval queue."""
    _ensure_dirs()
    queue_dir = ORCH_DIR / "approval_queue"
    queue_dir.mkdir(parents=True, exist_ok=True)

    request = {
        "id": datetime.now().strftime("%Y%m%d-%H%M%S-%f"),
        "operation": operation,
        "detail": detail,
        "policy": policy,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
    }

    path = queue_dir / f"{request['id']}.json"
    path.write_text(json.dumps(request, indent=2))

    _audit("approval_request", "approve", operation, detail)
    return request


def list_pending_approvals() -> list[dict]:
    """List pending approval requests."""
    queue_dir = ORCH_DIR / "approval_queue"
    if not queue_dir.exists():
        return []

    pending = []
    for f in sorted(queue_dir.glob("*.json")):
        try:
            data = json.loads(f.read_text())
            if data.get("status") == "pending":
                pending.append(data)
        except json.JSONDecodeError:
            continue
    return pending


# --- Audit Logging ---

def _audit(check_type: str, action: str, target: str, detail: str):
    """Log a policy decision to the audit log."""
    _ensure_dirs()
    entry = {
        "timestamp": datetime.now().isoformat(),
        "check_type": check_type,
        "action": action,
        "target": target[:200],  # Truncate long targets
        "detail": detail[:500],
    }
    log_path = AUDIT_DIR / f"{datetime.now().strftime('%Y%m%d')}.jsonl"
    with open(log_path, "a") as f:
        f.write(json.dumps(entry) + "\n")


def get_audit_log(days: int = 7) -> list[dict]:
    """Get recent audit log entries."""
    if not AUDIT_DIR.exists():
        return []

    entries = []
    for f in sorted(AUDIT_DIR.glob("*.jsonl")):
        try:
            for line in f.read_text().strip().split("\n"):
                if line.strip():
                    entries.append(json.loads(line))
        except (json.JSONDecodeError, IOError):
            continue
    return entries


# --- Full Policy Check ---

def check_all(
    command: str = "",
    path: str = "",
    workspace: str = "",
    filename: str = "",
    duration: float = 0,
    output_bytes: int = 0,
    policy: dict | None = None,
) -> dict:
    """Run all applicable policy checks and return combined result."""
    results = []

    if command:
        results.append(("command", check_command(command, policy).to_dict()))
    if path:
        results.append(("path", check_path(path, workspace, policy).to_dict()))
    if filename:
        results.append(("extension", check_file_extension(filename, policy).to_dict()))
    if duration > 0 or output_bytes > 0:
        results.append(("resource", check_resource_usage(duration, output_bytes, policy).to_dict()))

    has_deny = any(r[1]["action"] == "deny" for r in results)
    has_approve = any(r[1]["action"] == "approve" for r in results)

    overall = "deny" if has_deny else ("approve" if has_approve else "allow")

    return {
        "overall": overall,
        "checks": {name: result for name, result in results},
    }


def get_policy() -> dict:
    """Get the current policy configuration."""
    import copy
    return copy.deepcopy(DEFAULT_POLICY)


def main():
    parser = argparse.ArgumentParser(description="Safety policy enforcement")
    parser.add_argument("--check", help="Check a file path")
    parser.add_argument("--check-cmd", help="Check a command")
    parser.add_argument("--workspace", help="Workspace directory (for path checks)")
    parser.add_argument("--audit", action="store_true", help="Show audit log")
    parser.add_argument("--policy", action="store_true", help="Show current policy")
    parser.add_argument("--approvals", action="store_true", help="List pending approvals")

    args = parser.parse_args()

    if args.check:
        result = check_path(args.check, workspace=args.workspace or "")
        print(json.dumps(result.to_dict(), indent=2))
    elif args.check_cmd:
        result = check_command(args.check_cmd)
        print(json.dumps(result.to_dict(), indent=2))
    elif args.policy:
        print(json.dumps(get_policy(), indent=2))
    elif args.audit:
        entries = get_audit_log()
        for e in entries:
            print(json.dumps(e))
    elif args.approvals:
        pending = list_pending_approvals()
        print(json.dumps(pending, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
