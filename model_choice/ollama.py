"""Ollama lifecycle management -- auto-start, model loading, health recovery.

Full lifecycle:
  init -> start -> (running) -> stop -> cleanup
                -> recover (on error) -> running

Five responsibilities:
1. If ollama is not running, start it (via systemd or direct)
2. If the configured model isn't loaded, pull it
3. If ollama is unhealthy, restart it
4. Stop ollama cleanly (systemd stop or SIGTERM)
5. Cleanup orphaned resources (leaked processes, stale temp files)
"""

import json
import os
import shutil
import signal
import subprocess
import tempfile
import time
import urllib.request
import urllib.error
import logging
from typing import Optional
from enum import Enum

logger = logging.getLogger("model_choice.ollama")

DEFAULT_API_BASE = "http://localhost:11434"
STARTUP_TIMEOUT = 30  # seconds to wait for ollama to come up
HEALTH_TIMEOUT = 5    # seconds for health check ping
PULL_TIMEOUT = 300    # seconds for model pull
SHUTDOWN_TIMEOUT = 10 # seconds to wait for graceful shutdown


class LifecycleState(Enum):
    """Ollama lifecycle states."""
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    ERROR = "error"


def _api_base(config_api_base: Optional[str] = None) -> str:
    return config_api_base or DEFAULT_API_BASE


def health_check(api_base: Optional[str] = None) -> bool:
    """Ping ollama /api/tags. Returns True if responding."""
    base = _api_base(api_base)
    try:
        urllib.request.urlopen(f"{base}/api/tags", timeout=HEALTH_TIMEOUT)
        return True
    except Exception:
        return False


def list_models(api_base: Optional[str] = None) -> list[str]:
    """List locally available ollama model names."""
    base = _api_base(api_base)
    try:
        resp = urllib.request.urlopen(f"{base}/api/tags", timeout=HEALTH_TIMEOUT)
        data = json.loads(resp.read())
        return [m["name"] for m in data.get("models", [])]
    except Exception:
        return []


def model_loaded(model: str, api_base: Optional[str] = None) -> bool:
    """Check if a specific model is available locally.

    Handles both 'ollama/qwen2.5-coder:14b' (litellm format) and
    plain 'qwen2.5-coder:14b'.
    """
    # Strip ollama/ prefix if present
    name = model.split("/", 1)[-1] if "/" in model else model

    available = list_models(api_base)

    # Exact match
    if name in available:
        return True

    # Match without tag (e.g. 'qwen2.5-coder' matches 'qwen2.5-coder:14b')
    base_name = name.split(":")[0]
    for m in available:
        if m.split(":")[0] == base_name:
            return True

    # Match with tag against base names (e.g. 'qwen2.5-coder:latest' check)
    if ":latest" in name:
        plain = name.replace(":latest", "")
        if plain in available:
            return True

    return False


def pull_model(model: str, timeout: int = PULL_TIMEOUT) -> bool:
    """Pull a model via `ollama pull`. Returns True on success."""
    name = model.split("/", 1)[-1] if "/" in model else model
    ollama_bin = _find_binary()
    if not ollama_bin:
        logger.error("ollama binary not found, cannot pull model")
        return False

    logger.info(f"Pulling model {name}...")
    try:
        result = subprocess.run(
            [ollama_bin, "pull", name],
            capture_output=True, text=True, timeout=timeout,
        )
        if result.returncode == 0:
            logger.info(f"Model {name} pulled successfully")
            return True
        else:
            logger.error(f"Pull failed: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        logger.error(f"Pull timed out after {timeout}s")
        return False
    except Exception as e:
        logger.error(f"Pull error: {e}")
        return False


def start_ollama(timeout: int = STARTUP_TIMEOUT) -> bool:
    """Start ollama via systemd user service, falling back to direct launch.

    Returns True if ollama is running after the attempt.
    """
    # Try systemd first
    if _has_systemd_service():
        logger.info("Starting ollama via systemd...")
        try:
            subprocess.run(
                ["systemctl", "--user", "start", "ollama"],
                capture_output=True, timeout=10,
            )
            return _wait_for_health(timeout)
        except Exception as e:
            logger.warning(f"systemd start failed: {e}")

    # Fallback: direct launch
    ollama_bin = _find_binary()
    if not ollama_bin:
        logger.error("ollama binary not found")
        return False

    logger.info("Starting ollama directly...")
    try:
        subprocess.Popen(
            [ollama_bin, "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        return _wait_for_health(timeout)
    except Exception as e:
        logger.error(f"Direct start failed: {e}")
        return False


def stop_ollama(timeout: int = SHUTDOWN_TIMEOUT) -> bool:
    """Stop ollama via systemd user service, falling back to SIGTERM.

    Returns True if ollama is confirmed stopped after the attempt.
    """
    # Try systemd first
    if _has_systemd_service():
        logger.info("Stopping ollama via systemd...")
        try:
            subprocess.run(
                ["systemctl", "--user", "stop", "ollama"],
                capture_output=True, timeout=10,
            )
            return _wait_for_stopped(timeout)
        except Exception as e:
            logger.warning(f"systemd stop failed: {e}")

    # Fallback: SIGTERM then SIGKILL
    logger.info("Stopping ollama via signal...")
    _terminate_ollama()
    return _wait_for_stopped(timeout)


def restart_ollama(timeout: int = STARTUP_TIMEOUT) -> bool:
    """Restart ollama (systemd or kill+start)."""
    if _has_systemd_service():
        logger.info("Restarting ollama via systemd...")
        try:
            subprocess.run(
                ["systemctl", "--user", "restart", "ollama"],
                capture_output=True, timeout=10,
            )
            return _wait_for_health(timeout)
        except Exception as e:
            logger.warning(f"systemd restart failed: {e}")

    # Kill and restart
    logger.info("Killing ollama process...")
    _kill_ollama()
    time.sleep(2)
    return start_ollama(timeout)


def ensure_running(
    model: Optional[str] = None,
    api_base: Optional[str] = None,
    auto_start: bool = True,
    auto_pull: bool = True,
) -> bool:
    """Main entry point: ensure ollama is running and model is loaded.

    1. Check health -> if down, start
    2. Check model -> if missing, pull
    3. Final health check

    Returns True if ollama is healthy and model is loaded.
    """
    # Step 1: Health check, start if needed
    if not health_check(api_base):
        if not auto_start:
            return False
        if not start_ollama():
            return False

    # Step 2: Model check, pull if needed
    if model and not model_loaded(model, api_base):
        if not auto_pull:
            return False
        if not pull_model(model):
            return False

    # Step 3: Final check
    return health_check(api_base)


def recover(api_base: Optional[str] = None) -> bool:
    """Attempt full recovery: restart ollama.

    Called when ollama is responding but misbehaving (e.g. model
    load failures, GPU errors, corrupted state).
    """
    logger.info("Attempting ollama recovery...")
    return restart_ollama()


def lifecycle_state(api_base: Optional[str] = None) -> dict:
    """Get detailed lifecycle state of ollama.

    Returns dict with:
        state: LifecycleState value (stopped/starting/running/error)
        healthy: bool
        models: list of loaded model names
        pid: PID of ollama process or None
        managed_by: "systemd", "direct", or None
    """
    healthy = health_check(api_base)
    pid = _find_ollama_pid()
    managed = _detect_management()

    if healthy:
        state = LifecycleState.RUNNING
    elif pid is not None:
        # Process exists but not responding -- error state
        state = LifecycleState.ERROR
    else:
        state = LifecycleState.STOPPED

    return {
        "state": state.value,
        "healthy": healthy,
        "models": list_models(api_base) if healthy else [],
        "pid": pid,
        "managed_by": managed,
    }


def cleanup() -> dict:
    """Clean up orphaned ollama resources.

    Finds and removes:
    - Orphaned ollama processes (not responding to health checks)
    - Stale temp files from interrupted pulls

    Returns dict with counts of cleaned items.
    """
    cleaned = {
        "processes_killed": 0,
        "temp_files_removed": 0,
        "errors": [],
    }

    # Kill orphaned processes (running but not responding)
    pid = _find_ollama_pid()
    if pid is not None and not health_check():
        logger.info(f"Found orphaned ollama process (PID {pid}), killing...")
        try:
            os.kill(pid, signal.SIGTERM)
            time.sleep(2)
            # Check if it's still alive
            try:
                os.kill(pid, 0)  # Doesn't actually send signal, just checks
                # Still alive -- use SIGKILL
                logger.warning(f"Process {pid} didn't stop, sending SIGKILL")
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass  # Good, it's gone
            cleaned["processes_killed"] += 1
        except ProcessLookupError:
            pass  # Already gone
        except PermissionError as e:
            cleaned["errors"].append(f"Cannot kill PID {pid}: {e}")
        except Exception as e:
            cleaned["errors"].append(f"Error killing PID {pid}: {e}")

    # Clean stale temp files from interrupted pulls
    # Ollama stores partial downloads in its data dir
    ollama_data = os.path.expanduser("~/.ollama")
    if os.path.isdir(ollama_data):
        for root, dirs, files in os.walk(ollama_data):
            for fname in files:
                # Partial downloads have .part or .tmp extension
                if fname.endswith((".part", ".tmp", ".partial")):
                    fpath = os.path.join(root, fname)
                    try:
                        os.remove(fpath)
                        cleaned["temp_files_removed"] += 1
                        logger.info(f"Removed stale temp file: {fpath}")
                    except Exception as e:
                        cleaned["errors"].append(f"Cannot remove {fpath}: {e}")

    return cleaned


def shutdown(api_base: Optional[str] = None) -> dict:
    """Full shutdown: stop ollama, cleanup resources.

    Combines stop_ollama() and cleanup() into one call.
    Returns dict with stop result and cleanup stats.
    """
    stopped = stop_ollama()
    cleaned = cleanup()

    return {
        "stopped": stopped,
        "cleanup": cleaned,
    }


def init(
    model: Optional[str] = None,
    api_base: Optional[str] = None,
    timeout: int = STARTUP_TIMEOUT,
) -> dict:
    """Initialize ollama: cleanup stale state, start, load model.

    Returns dict with:
        started: bool (healthy after init)
        models: list of loaded models
        state: lifecycle state string
        cleanup: results of pre-start cleanup
    """
    # Pre-cleanup any orphaned resources
    cleaned = cleanup()

    # Start ollama
    if not health_check(api_base):
        started = start_ollama(timeout)
    else:
        started = True

    # Pull model if needed
    if started and model:
        model_name = model.split("/", 1)[-1] if "/" in model else model
        if not model_loaded(model_name, api_base):
            pull_model(model_name)

    state = lifecycle_state(api_base)

    return {
        "started": started,
        "models": state["models"],
        "state": state["state"],
        "cleanup": cleaned,
    }


# ---- internal helpers ----

def _find_binary() -> Optional[str]:
    """Find ollama binary."""
    # Check PATH
    path = shutil.which("ollama")
    if path:
        return path
    # Check common locations
    for loc in [
        os.path.expanduser("~/.local/bin/ollama"),
        "/usr/local/bin/ollama",
        "/usr/bin/ollama",
    ]:
        if os.path.isfile(loc) and os.access(loc, os.X_OK):
            return loc
    return None


def _has_systemd_service() -> bool:
    """Check if ollama is managed by systemd user service."""
    try:
        result = subprocess.run(
            ["systemctl", "--user", "status", "ollama"],
            capture_output=True, timeout=5,
        )
        # returncode 0 = active, 3 = inactive (but service exists), others = no service
        return result.returncode in (0, 3)
    except Exception:
        return False


def _wait_for_health(timeout: int) -> bool:
    """Poll health check until ollama responds or timeout."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if health_check():
            return True
        time.sleep(1)
    return False


def _wait_for_stopped(timeout: int) -> bool:
    """Poll until ollama stops responding or timeout."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if not health_check():
            return True
        time.sleep(0.5)
    return False


def _kill_ollama():
    """Kill ollama processes (SIGKILL)."""
    try:
        subprocess.run(
            ["pkill", "-f", "ollama serve"],
            capture_output=True, timeout=5,
        )
    except Exception:
        pass


def _terminate_ollama():
    """Terminate ollama processes gracefully (SIGTERM then SIGKILL)."""
    pid = _find_ollama_pid()
    if pid is None:
        # No PID found, try pkill as fallback
        try:
            subprocess.run(
                ["pkill", "-f", "ollama"],
                capture_output=True, timeout=5,
            )
        except Exception:
            pass
        return

    try:
        os.kill(pid, signal.SIGTERM)
        # Wait up to 5 seconds for graceful shutdown
        for _ in range(10):
            try:
                os.kill(pid, 0)
                time.sleep(0.5)
            except ProcessLookupError:
                return  # Process gone -- good
        # Still alive -- SIGKILL
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    except ProcessLookupError:
        pass
    except PermissionError:
        # Fall back to pkill
        try:
            subprocess.run(
                ["pkill", "-f", "ollama"],
                capture_output=True, timeout=5,
            )
        except Exception:
            pass


def _find_ollama_pid() -> Optional[int]:
    """Find the PID of the running ollama server process."""
    try:
        result = subprocess.run(
            ["pgrep", "-f", "ollama"],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode == 0 and result.stdout.strip():
            # May return multiple PIDs (server + children)
            # The first is typically the main process
            pids = result.stdout.strip().split("\n")
            return int(pids[0])
    except Exception:
        pass
    return None


def _detect_management() -> Optional[str]:
    """Detect how ollama is being managed (systemd vs direct)."""
    if _has_systemd_service():
        try:
            result = subprocess.run(
                ["systemctl", "--user", "is-active", "ollama"],
                capture_output=True, text=True, timeout=5,
            )
            if result.stdout.strip() == "active":
                return "systemd"
        except Exception:
            pass
    return "direct" if _find_ollama_pid() else None
