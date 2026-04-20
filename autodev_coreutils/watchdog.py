"""watchdog -- Monitor a running agent/process and intervene on stall.

Like `watch` but for agents: polls a running process, checks for stalls,
timeouts, infinite loops, and can auto-restart or kill.

Input:  PID or process to monitor, or .autodev/watchdog_state.json config
Output: Intervention log + status updates
State:  watchdog_state.json

Usage:
    autodev-watchdog --pid 12345 --timeout 300
    autodev-watchdog --command "rfl run --from-file seed.txt"
    autodev-watchdog --autodev  # monitor the current .autodev/ workflow
"""

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

from .contract import (
    make_parser, find_project, ensure_autodev_dir,
    write_state, output, error,
)


def get_process_info(pid: int) -> dict:
    """Get info about a process by PID."""
    try:
        with open(f"/proc/{pid}/status") as f:
            status = {}
            for line in f:
                if ":" in line:
                    k, v = line.split(":", 1)
                    status[k.strip()] = v.strip()
            return {
                "pid": pid,
                "state": status.get("State", "unknown"),
                "vm_size": status.get("VmSize", "unknown"),
                "threads": status.get("Threads", "unknown"),
            }
    except (FileNotFoundError, PermissionError):
        return {"pid": pid, "state": "not_found"}


def check_output_stall(output_file: Path, min_size: int = 100, check_interval: int = 30) -> bool:
    """Check if an output file is still growing."""
    if not output_file.exists():
        return False
    size1 = output_file.stat().st_size
    time.sleep(check_interval)
    size2 = output_file.stat().st_size
    return size2 <= size1 + min_size  # Not growing = stalled


def run_with_watchdog(
    command: str,
    project: Path,
    timeout: int = 300,
    stall_timeout: int = 60,
    max_restarts: int = 2,
    restart_command: str = None,
    output_file: Path = None,
) -> dict:
    """Run a command with watchdog monitoring."""
    results = {
        "command": command,
        "start_time": time.time(),
        "restarts": 0,
        "events": [],
    }

    for attempt in range(max_restarts + 1):
        results["events"].append({
            "time": time.time(),
            "event": "start" if attempt == 0 else "restart",
            "attempt": attempt,
        })

        proc = subprocess.Popen(
            command, shell=True, cwd=project,
            stdout=subprocess.PIPE if not output_file else open(output_file, "a"),
            stderr=subprocess.PIPE,
        )

        try:
            stdout, stderr = proc.communicate(timeout=timeout)
            results["exit_code"] = proc.returncode
            results["events"].append({
                "time": time.time(),
                "event": "completed",
                "exit_code": proc.returncode,
            })

            if proc.returncode == 0:
                results["status"] = "success"
                return results

            # Non-zero exit
            if attempt < max_restarts:
                results["events"].append({
                    "time": time.time(),
                    "event": "restart_scheduled",
                    "reason": f"exit code {proc.returncode}",
                })
                results["restarts"] += 1
                continue
            else:
                results["status"] = "failed"
                if stderr:
                    results["stderr"] = stderr.decode()[:1000]
                return results

        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
            results["events"].append({
                "time": time.time(),
                "event": "timeout_killed",
                "timeout": timeout,
            })

            if attempt < max_restarts:
                results["restarts"] += 1
                continue
            else:
                results["status"] = "timeout"
                return results

    results["status"] = "max_restarts_exceeded"
    return results


def monitor_pid(
    pid: int,
    timeout: int = 300,
    stall_check: bool = False,
    output_file: Path = None,
) -> dict:
    """Monitor an existing PID."""
    results = {
        "pid": pid,
        "start_time": time.time(),
        "events": [],
    }

    start = time.time()
    while True:
        info = get_process_info(pid)
        if info.get("state") == "not_found":
            results["status"] = "process_ended"
            results["events"].append({"time": time.time(), "event": "process_ended"})
            break

        elapsed = time.time() - start
        if elapsed > timeout:
            results["status"] = "timeout"
            results["events"].append({"time": time.time(), "event": "timeout"})
            # Kill the process
            try:
                os.kill(pid, signal.SIGTERM)
                time.sleep(2)
                # Force kill if still running
                try:
                    os.kill(pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            except ProcessLookupError:
                pass
            break

        # Check for stall
        if stall_check and output_file and output_file.exists():
            if check_output_stall(output_file):
                results["events"].append({"time": time.time(), "event": "stall_detected"})
                try:
                    os.kill(pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                results["status"] = "stall_killed"
                break

        time.sleep(5)

    results["duration"] = time.time() - results["start_time"]
    return results


def main(argv=None):
    parser = make_parser("watchdog", "Monitor a running agent/process and intervene on stall")
    parser.add_argument(
        "--pid", type=int, default=None,
        help="PID to monitor",
    )
    parser.add_argument(
        "--command", default=None,
        help="Command to run under watchdog",
    )
    parser.add_argument(
        "--timeout", type=int, default=300,
        help="Max seconds before killing (default: 300)",
    )
    parser.add_argument(
        "--max-restarts", type=int, default=2,
        help="Max restarts on failure (default: 2)",
    )
    parser.add_argument(
        "--stall-check", action="store_true",
        help="Check if output is growing (detect infinite loops)",
    )
    parser.add_argument(
        "--output-file", default=None,
        help="Output file to monitor for stall detection",
    )

    args = parser.parse_args(argv)
    project = find_project(args.workdir)
    ad = ensure_autodev_dir(project)

    output_file = Path(args.output_file) if args.output_file else None

    if args.pid:
        result = monitor_pid(args.pid, args.timeout, args.stall_check, output_file)
    elif args.command:
        result = run_with_watchdog(
            args.command, project, args.timeout,
            max_restarts=args.max_restarts,
            output_file=output_file,
        )
    else:
        error("Specify --pid <PID> or --command <cmd>")

    write_state(project, "watchdog", result)

    if args.json_output:
        output(result, json_mode=True)
    elif not args.quiet:
        status = result.get("status", "unknown")
        output(f"Watchdog: {status}")
        for evt in result.get("events", []):
            output(f"  [{evt.get('event')}] {evt.get('time', '')}")

    return 0 if result.get("status") == "success" else 1


if __name__ == "__main__":
    sys.exit(main() or 0)
