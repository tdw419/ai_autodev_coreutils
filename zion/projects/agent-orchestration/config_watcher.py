#!/usr/bin/env python3
"""
Config Watcher and Live Tuning for the Hermes Agent Orchestrator.

Watches orchestrator config files for changes and triggers reloads.
Supports hot-reload of orchestrator.yaml, role profiles, and pipeline YAMLs.
Includes audit logging and a live tuning CLI.

Usage:
    python3 config_watcher.py watch                    # watch and report changes
    python3 config_watcher.py status                   # show watched files state
    python3 config_watcher.py get max_concurrent       # get config value
    python3 config_watcher.py set max_concurrent 5     # set config value
    python3 config_watcher.py validate                 # validate config files
    python3 config_watcher.py audit                    # show recent config changes
    python3 config_watcher.py diff                     # show current vs disk config
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional

PROJECT_DIR = Path(os.environ.get(
    "ORCH_PROJECT_DIR",
    os.path.expanduser("~/zion/projects/agent-orchestration"),
))
ORCH_DIR = Path(os.path.expanduser("~/.orchestrator"))
AUDIT_LOG = ORCH_DIR / "logs" / "config-changes.jsonl"
CONFIG_BACKUP_DIR = ORCH_DIR / "backups"

# Default config file locations
DEFAULT_CONFIG = PROJECT_DIR / "orchestrator.yaml"
DEFAULT_ROLES_DIR = PROJECT_DIR / "roles"
DEFAULT_PIPELINES_DIR = PROJECT_DIR / "pipelines"


def _file_hash(path: Path, sample_size: int = 4096) -> str:
    """Compute SHA256 hash of file contents (first sample_size bytes)."""
    try:
        content = path.read_bytes()[:sample_size]
        return hashlib.sha256(content).hexdigest()
    except (OSError, IOError):
        return ""


def _file_mtime(path: Path) -> float:
    """Get file modification time."""
    try:
        return path.stat().st_mtime
    except OSError:
        return 0.0


def _load_yaml(path: Path) -> Any:
    """Load a YAML file safely."""
    try:
        import yaml
        with open(path) as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return None


def _save_yaml(path: Path, data: Any) -> bool:
    """Save data to a YAML file atomically."""
    try:
        import yaml
        tmp_path = path.with_suffix(".yaml.tmp")
        with open(tmp_path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        os.replace(tmp_path, path)
        return True
    except Exception:
        return False


def _simple_diff(old: Any, new: Any, prefix: str = "") -> list[str]:
    """Generate a simple human-readable diff between two values."""
    diffs = []
    if type(old) != type(new):
        diffs.append(f"{prefix}: {old!r} -> {new!r} (type change)")
        return diffs

    if isinstance(old, dict):
        all_keys = set(list(old.keys()) + list(new.keys()))
        for k in sorted(all_keys):
            p = f"{prefix}.{k}" if prefix else k
            if k not in old:
                diffs.append(f"{p}: +{new[k]!r} (added)")
            elif k not in new:
                diffs.append(f"{p}: -{old[k]!r} (removed)")
            elif old[k] != new[k]:
                diffs.extend(_simple_diff(old[k], new[k], p))
    elif isinstance(old, list):
        if old != new:
            diffs.append(f"{prefix}: list changed (len {len(old)} -> {len(new)})")
    else:
        if old != new:
            diffs.append(f"{prefix}: {old!r} -> {new!r}")

    return diffs


class ConfigWatcher:
    """
    Watches config files for changes and triggers callbacks.

    Config types:
        - orchestrator: orchestrator.yaml (main config)
        - role: role profile YAMLs in roles/ directory
        - pipeline: pipeline YAMLs in pipelines/ directory
    """

    def __init__(
        self,
        config_path: Optional[str] = None,
        roles_dir: Optional[str] = None,
        pipelines_dir: Optional[str] = None,
    ):
        self.config_path = Path(config_path) if config_path else DEFAULT_CONFIG
        self.roles_dir = Path(roles_dir) if roles_dir else DEFAULT_ROLES_DIR
        self.pipelines_dir = Path(pipelines_dir) if pipelines_dir else DEFAULT_PIPELINES_DIR

        # File state: path -> {"hash": str, "mtime": float}
        self._state: dict[str, dict] = {}
        self._callbacks: dict[str, list[Callable]] = {
            "orchestrator": [],
            "role": [],
            "pipeline": [],
        }
        self._loaded_configs: dict[str, Any] = {}

        # Initialize state
        self._scan_all()

    def _scan_all(self):
        """Scan all watched files and record their current state."""
        self._scan_file(self.config_path, "orchestrator")

        if self.roles_dir.exists():
            for f in self.roles_dir.glob("*.yaml"):
                self._scan_file(f, "role")

        if self.pipelines_dir.exists():
            for f in self.pipelines_dir.glob("*.yaml"):
                self._scan_file(f, "pipeline")

    def _scan_file(self, path: Path, config_type: str):
        """Record the current state of a single file."""
        key = str(path)
        if path.exists():
            self._state[key] = {
                "hash": _file_hash(path),
                "mtime": _file_mtime(path),
            }
            self._loaded_configs[key] = _load_yaml(path)
        else:
            self._state.pop(key, None)

    def on_change(self, config_type: str, callback: Callable):
        """Register a callback for a config type change."""
        if config_type in self._callbacks:
            self._callbacks[config_type].append(callback)

    def check(self) -> list[dict]:
        """
        Check all watched files for changes since last scan.

        Returns list of change events, each with:
            - config_type: orchestrator/role/pipeline
            - path: file path
            - change: modified/added/deleted
            - diffs: list of change descriptions
        """
        events = []

        # Check orchestrator config
        events.extend(self._check_file(self.config_path, "orchestrator"))

        # Check role profiles
        if self.roles_dir.exists():
            current_roles = {str(f) for f in self.roles_dir.glob("*.yaml")}
            known_roles = {k for k in self._state
                          if k.startswith(str(self.roles_dir))}
            for f in current_roles - known_roles:
                events.extend(self._check_file(Path(f), "role"))
            for f in known_roles - current_roles:
                key = f
                events.append({
                    "config_type": "role",
                    "path": key,
                    "change": "deleted",
                    "diffs": [],
                })
                self._state.pop(key, None)
                self._loaded_configs.pop(key, None)

        # Check pipeline configs
        if self.pipelines_dir.exists():
            current_pipes = {str(f) for f in self.pipelines_dir.glob("*.yaml")}
            known_pipes = {k for k in self._state
                          if k.startswith(str(self.pipelines_dir))}
            for f in current_pipes - known_pipes:
                events.extend(self._check_file(Path(f), "pipeline"))
            for f in known_pipes - current_pipes:
                key = f
                events.append({
                    "config_type": "pipeline",
                    "path": key,
                    "change": "deleted",
                    "diffs": [],
                })
                self._state.pop(key, None)
                self._loaded_configs.pop(key, None)

        # Fire callbacks for detected changes
        for event in events:
            for cb in self._callbacks.get(event["config_type"], []):
                try:
                    cb(event)
                except Exception as e:
                    print(f"Config callback error: {e}", file=sys.stderr)

        # Log changes
        for event in events:
            self._log_change(event)

        return events

    def _check_file(self, path: Path, config_type: str) -> list[dict]:
        """Check a single file for changes."""
        key = str(path)
        events = []

        if not path.exists():
            if key in self._state:
                events.append({
                    "config_type": config_type,
                    "path": key,
                    "change": "deleted",
                    "diffs": [],
                })
                self._state.pop(key, None)
                self._loaded_configs.pop(key, None)
            return events

        current_hash = _file_hash(path)
        current_mtime = _file_mtime(path)

        if key not in self._state:
            # New file
            self._state[key] = {"hash": current_hash, "mtime": current_mtime}
            new_config = _load_yaml(path)
            self._loaded_configs[key] = new_config
            events.append({
                "config_type": config_type,
                "path": key,
                "change": "added",
                "diffs": [f"New file: {path.name}"],
            })
        elif current_hash != self._state[key]["hash"]:
            # Modified file
            old_config = self._loaded_configs.get(key)
            new_config = _load_yaml(path)
            diffs = _simple_diff(old_config, new_config) if old_config and new_config else []

            self._state[key] = {"hash": current_hash, "mtime": current_mtime}
            self._loaded_configs[key] = new_config
            events.append({
                "config_type": config_type,
                "path": key,
                "change": "modified",
                "diffs": diffs,
            })

        return events

    def get_config(self, config_type: str = "orchestrator") -> Any:
        """Get the current loaded config for a type."""
        if config_type == "orchestrator":
            return self._loaded_configs.get(str(self.config_path))
        elif config_type == "role":
            return {k: v for k, v in self._loaded_configs.items()
                    if k.startswith(str(self.roles_dir))}
        elif config_type == "pipeline":
            return {k: v for k, v in self._loaded_configs.items()
                    if k.startswith(str(self.pipelines_dir))}
        return None

    def get_value(self, key: str) -> Any:
        """Get a specific config value by dot-separated key path."""
        config = self._loaded_configs.get(str(self.config_path), {})
        keys = key.split(".")
        current = config
        for k in keys:
            if isinstance(current, dict):
                current = current.get(k)
            else:
                return None
            if current is None:
                return None
        return current

    def set_value(self, key: str, value: Any, dry_run: bool = False) -> dict:
        """
        Set a config value by dot-separated key path.

        Returns result dict with success, old_value, new_value.
        """
        config = self._loaded_configs.get(str(self.config_path), {})
        if config is None:
            return {"success": False, "error": "Config not loaded"}

        keys = key.split(".")
        old_value = config
        for k in keys:
            if isinstance(old_value, dict):
                old_value = old_value.get(k)
            else:
                return {"success": False, "error": f"Path '{key}' not found in config"}

        # Navigate to parent and set
        parent = config
        for k in keys[:-1]:
            if isinstance(parent, dict):
                parent = parent[k]
            else:
                return {"success": False, "error": f"Cannot navigate to '{key}'"}

        if isinstance(parent, dict) and keys[-1] in parent:
            if dry_run:
                return {
                    "success": True,
                    "dry_run": True,
                    "key": key,
                    "old_value": old_value,
                    "new_value": value,
                }
            parent[keys[-1]] = value
            # Backup before writing
            self._backup_config()
            if _save_yaml(self.config_path, config):
                self._scan_file(self.config_path, "orchestrator")
                return {
                    "success": True,
                    "key": key,
                    "old_value": old_value,
                    "new_value": value,
                }
            else:
                return {"success": False, "error": "Failed to write config file"}
        else:
            return {"success": False, "error": f"Key '{keys[-1]}' not found in config"}

    def validate(self) -> list[str]:
        """Validate all watched config files."""
        errors = []

        config = self._loaded_configs.get(str(self.config_path))
        if config is None:
            errors.append(f"orchestrator.yaml: not loaded or invalid YAML")
        elif not isinstance(config, dict):
            errors.append(f"orchestrator.yaml: expected dict, got {type(config).__name__}")
        else:
            if not config.get("repos") and not config.get("repo"):
                errors.append("orchestrator.yaml: no 'repo' or 'repos' configured")
            max_c = config.get("max_concurrent", 0)
            if isinstance(max_c, int) and max_c < 1:
                errors.append(f"orchestrator.yaml: max_concurrent={max_c} must be >= 1")

        if self.roles_dir.exists():
            for f in self.roles_dir.glob("*.yaml"):
                role = self._loaded_configs.get(str(f))
                if role is None:
                    errors.append(f"roles/{f.name}: not loaded or invalid YAML")

        if self.pipelines_dir.exists():
            for f in self.pipelines_dir.glob("*.yaml"):
                pipe = self._loaded_configs.get(str(f))
                if pipe is None:
                    errors.append(f"pipelines/{f.name}: not loaded or invalid YAML")

        return errors

    def get_state(self) -> dict:
        """Get current watcher state for all files."""
        return {
            str(k): {"hash": v["hash"][:12], "mtime": v["mtime"],
                      "iso": datetime.utcfromtimestamp(v["mtime"]).isoformat() + "Z"}
            for k, v in self._state.items()
        }

    def _log_change(self, event: dict):
        """Append a config change event to the audit log."""
        try:
            AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
            entry = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "config_type": event["config_type"],
                "path": event["path"],
                "change": event["change"],
                "diffs": event.get("diffs", []),
                "reloaded_successfully": event["change"] != "deleted",
            }
            with open(AUDIT_LOG, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception:
            pass

    def _backup_config(self):
        """Backup the current orchestrator config before modification."""
        try:
            CONFIG_BACKUP_DIR.mkdir(parents=True, exist_ok=True)
            ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            backup_path = CONFIG_BACKUP_DIR / f"orchestrator_{ts}.yaml"
            if self.config_path.exists():
                import shutil
                shutil.copy2(self.config_path, backup_path)
                # Keep only last 10 backups
                backups = sorted(CONFIG_BACKUP_DIR.glob("orchestrator_*.yaml"))
                for old in backups[:-10]:
                    old.unlink()
        except Exception:
            pass

    def watch_loop(self, interval: float = 5.0, max_iterations: int = 0):
        """
        Watch for config changes in a loop.

        Args:
            interval: seconds between checks (default: 5)
            max_iterations: 0 for infinite, N for N iterations
        """
        print(f"Watching config files (interval: {interval}s)...")
        print(f"  Orchestrator: {self.config_path}")
        print(f"  Roles: {self.roles_dir}/")
        print(f"  Pipelines: {self.pipelines_dir}/")
        print("Press Ctrl+C to stop.\n")

        iteration = 0
        try:
            while max_iterations == 0 or iteration < max_iterations:
                events = self.check()
                if events:
                    for e in events:
                        icon = {"added": "➕", "modified": "✏️", "deleted": "🗑️"}.get(
                            e["change"], "?")
                        print(f"{icon} [{e['config_type']}] {Path(e['path']).name}: {e['change']}")
                        for d in e.get("diffs", []):
                            print(f"   {d}")
                    print()
                time.sleep(interval)
                iteration += 1
        except KeyboardInterrupt:
            print("\nStopped watching.")


def get_audit_log(limit: int = 20) -> list[dict]:
    """Read the most recent entries from the audit log."""
    if not AUDIT_LOG.exists():
        return []
    lines = AUDIT_LOG.read_text().strip().split("\n")
    entries = []
    for line in reversed(lines):
        line = line.strip()
        if line:
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                pass
        if len(entries) >= limit:
            break
    return entries


def main():
    parser = argparse.ArgumentParser(
        description="Config watcher and live tuning for Hermes orchestrator",
    )
    sub = parser.add_subparsers(dest="command")

    # watch
    p_watch = sub.add_parser("watch", help="Watch config files for changes")
    p_watch.add_argument("--interval", type=float, default=5.0)
    p_watch.add_argument("--once", action="store_true", help="Check once and exit")
    p_watch.add_argument("--config", type=str, default=None)
    p_watch.add_argument("--roles-dir", type=str, default=None)
    p_watch.add_argument("--pipelines-dir", type=str, default=None)

    # status
    sub.add_parser("status", help="Show current state of watched files")

    # get
    p_get = sub.add_parser("get", help="Get a config value")
    p_get.add_argument("key", help="Dot-separated key path (e.g. max_concurrent)")

    # set
    p_set = sub.add_parser("set", help="Set a config value")
    p_set.add_argument("key", help="Dot-separated key path")
    p_set.add_argument("value", help="New value (use 'true'/'false' for bools)")
    p_set.add_argument("--dry-run", action="store_true")

    # validate
    sub.add_parser("validate", help="Validate all config files")

    # audit
    p_audit = sub.add_parser("audit", help="Show recent config changes")
    p_audit.add_argument("--limit", type=int, default=20)

    # diff
    sub.add_parser("diff", help="Show diff between current and disk config")

    args = parser.parse_args()

    if args.command == "watch":
        watcher = ConfigWatcher(
            config_path=args.config,
            roles_dir=args.roles_dir,
            pipelines_dir=args.pipelines_dir,
        )
        if args.once:
            events = watcher.check()
            if events:
                for e in events:
                    print(f"[{e['config_type']}] {Path(e['path']).name}: {e['change']}")
                    for d in e.get("diffs", []):
                        print(f"  {d}")
            else:
                print("No changes detected.")
        else:
            watcher.watch_loop(interval=args.interval)

    elif args.command == "status":
        watcher = ConfigWatcher()
        state = watcher.get_state()
        if not state:
            print("No watched files found.")
        for path, info in sorted(state.items()):
            name = Path(path).name
            print(f"  {name:<30} hash:{info['hash']}  mtime:{info['iso']}")

    elif args.command == "get":
        watcher = ConfigWatcher()
        value = watcher.get_value(args.key)
        if value is None:
            print(f"Key '{args.key}' not found in config.")
            sys.exit(1)
        print(json.dumps(value, indent=2))

    elif args.command == "set":
        watcher = ConfigWatcher()
        # Parse value type
        raw_value = args.value
        if raw_value.lower() == "true":
            parsed = True
        elif raw_value.lower() == "false":
            parsed = False
        elif raw_value.isdigit():
            parsed = int(raw_value)
        else:
            try:
                parsed = float(raw_value)
            except ValueError:
                parsed = raw_value

        result = watcher.set_value(args.key, parsed, dry_run=args.dry_run)
        if result.get("success"):
            prefix = "[DRY RUN] " if result.get("dry_run") else ""
            print(f"{prefix}Set {args.key}: {result['old_value']} -> {result['new_value']}")
        else:
            print(f"ERROR: {result.get('error', 'unknown')}")
            sys.exit(1)

    elif args.command == "validate":
        watcher = ConfigWatcher()
        errors = watcher.validate()
        if errors:
            print("Config validation errors:")
            for e in errors:
                print(f"  - {e}")
            sys.exit(1)
        else:
            print("All config files valid.")

    elif args.command == "audit":
        entries = get_audit_log(limit=args.limit)
        if not entries:
            print("No config changes recorded.")
        for e in entries:
            icon = {"added": "➕", "modified": "✏️", "deleted": "🗑️"}.get(
                e.get("change", ""), "?")
            print(f"{icon} {e['timestamp']} [{e['config_type']}] {Path(e['path']).name}: {e['change']}")
            for d in e.get("diffs", [])[:5]:
                print(f"   {d}")
            if len(e.get("diffs", [])) > 5:
                print(f"   ... and {len(e['diffs']) - 5} more")

    elif args.command == "diff":
        watcher = ConfigWatcher()
        events = watcher.check()
        if events:
            for e in events:
                print(f"[{e['config_type']}] {Path(e['path']).name}: {e['change']}")
                for d in e.get("diffs", []):
                    print(f"  {d}")
        else:
            print("Config is up to date (no changes since last check).")

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
