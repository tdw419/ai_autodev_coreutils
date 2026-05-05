#!/usr/bin/env python3
"""
Geometry OS Dogfood QA -- Exploratory testing of the live GeOS desktop.

This preflight script:
1. Checks if GeOS is running (look for geometry_os process)
2. Runs a representative sample of cargo tests (not full suite -- too slow for cron)
3. Runs the headless terminal QA suite
4. Reports findings as text/JSON for the cron agent to analyze

Usage:
    python3 geo_dogfood_qa.py   # Check GeOS status, report state
"""

import subprocess, sys, os, json, re, signal, atexit
from datetime import datetime

GEOS_DIR = os.path.expanduser("~/zion/projects/geometry_os/geometry_os")
ROADMAP_YAML = os.path.join(GEOS_DIR, "roadmap.yaml")
OUTPUT_JSON = "/tmp/geo_dogfood_qa.json"


def kill_stale_test_processes():
    """Kill any leftover cargo test or geometry_os test runner processes."""
    try:
        result = subprocess.run(
            ["pgrep", "-f", "geometry_os.*--test-threads"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                try:
                    os.kill(int(pid), signal.SIGKILL)
                except (ProcessLookupError, PermissionError):
                    pass
            if pids:
                print("Killed %d stale test processes: %s" % (len(pids), ', '.join(pids[:5])))
    except Exception:
        pass


def get_next_phase_num():
    """Auto-detect next phase number from roadmap.yaml via grep (no YAML parser needed)."""
    try:
        result = subprocess.run(
            ["grep", "-oP", "phase-(\\d+)", ROADMAP_YAML],
            capture_output=True, text=True, timeout=10
        )
        nums = [int(x) for x in re.findall(r"(\d+)", result.stdout)]
        return max(nums) + 1 if nums else 141
    except:
        return 141


def check_geos_running():
    """Check if geometry_os process is alive (excluding test runners)."""
    result = subprocess.run(
        ["pgrep", "-f", "geometry_os"],
        capture_output=True, text=True, timeout=10
    )
    if result.returncode == 0:
        all_pids = result.stdout.strip().split('\n')
        geos_pids = []
        for pid in all_pids:
            try:
                with open("/proc/%s/cmdline" % pid, "rb") as f:
                    cmdline = f.read().decode("utf-8", errors="replace")
                if "--test-threads" not in cmdline:
                    geos_pids.append(pid)
            except (FileNotFoundError, PermissionError):
                geos_pids.append(pid)
        if geos_pids:
            return True, "GeOS running (PIDs: " + ', '.join(geos_pids) + ")"
    return False, "GeOS not running"


def check_build_status():
    """Run cargo test --lib and report pass/fail counts."""
    cmd = [
        "cargo", "test", "--lib", "--",
        "--test-threads=8",
        "--skip", "test_linux_kernel_early_boot",
        "--skip", "test_benchmark",
        "--skip", "test_riscv_full_boot",
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True, text=True, timeout=90, cwd=GEOS_DIR
        )
        output = result.stdout + result.stderr
        timed_out = False
    except subprocess.TimeoutExpired as e:
        output = (e.stdout or b"").decode("utf-8", errors="replace")
        output += (e.stderr or b"").decode("utf-8", errors="replace")
        print("WARNING: cargo test timed out after 90s (partial results)")
        timed_out = True
    
    total_passed = 0
    total_failed = 0
    failures = []
    for match in re.finditer(r'(\d+) passed.*?(\d+) failed', output):
        total_passed += int(match.group(1))
        total_failed += int(match.group(2))
    for match in re.finditer(r'test (\S+) \.\.\. FAILED', output):
        failures.append(match.group(1))
    
    return {
        "passed": total_passed,
        "failed": total_failed,
        "failures": failures[:20],
        "timed_out": timed_out,
        "build_ok": total_failed == 0 and not timed_out,
    }


def check_geos_term():
    """Run the headless terminal QA suite."""
    try:
        result = subprocess.run(
            ["python3", os.path.join(os.path.dirname(__file__), "terminal_qa.py")],
            capture_output=True, text=True, timeout=120, cwd=GEOS_DIR
        )
        return {
            "exit_code": result.returncode,
            "output": result.stdout[:2000],
        }
    except subprocess.TimeoutExpired:
        return {
            "exit_code": -1,
            "output": "Terminal QA timed out after 120s",
        }


def write_fallback_json(running, next_phase, error_msg):
    """Write a minimal JSON even if everything else failed."""
    summary = {
        "timestamp": datetime.now().isoformat(),
        "geos_running": running,
        "build": {"passed": 0, "failed": 0, "failures": [], "timed_out": True, "build_ok": False},
        "term_qa_exit": -1,
        "next_phase_num": next_phase,
        "error": error_msg,
    }
    try:
        with open(OUTPUT_JSON, "w") as f:
            json.dump(summary, f, indent=2)
    except:
        pass


def main():
    print("=== GeOS Dogfood QA === " + datetime.now().strftime('%Y-%m-%d %H:%M') + " ===")
    
    kill_stale_test_processes()
    
    next_phase = get_next_phase_num()
    
    try:
        running, status_msg = check_geos_running()
    except Exception as e:
        running = False
        status_msg = "Error checking GeOS: %s" % e
    print("GeOS Status: " + status_msg)
    
    print("Running cargo test --lib (90s timeout, skipping benchmarks)...")
    try:
        build = check_build_status()
    except Exception as e:
        print("ERROR running tests: %s" % e)
        build = {"passed": 0, "failed": 0, "failures": [], "timed_out": True, "build_ok": False}
    
    print("Tests: %d passed, %d failed" % (build['passed'], build['failed']))
    if build.get('timed_out'):
        print("WARNING: Test run timed out -- results may be incomplete")
    if build['failures']:
        print("Failing tests: " + ', '.join(build['failures'][:10]))
    
    print("Running terminal QA...")
    try:
        term_qa = check_geos_term()
    except Exception as e:
        print("ERROR running terminal QA: %s" % e)
        term_qa = {"exit_code": -1, "output": str(e)}
    
    if build['failed'] > 0:
        print("STATUS: HALT")
        print("REASON: %d tests failing. Workers should fix these first." % build['failed'])
        for f in build['failures'][:10]:
            print("FAILING_TEST: " + f)
    elif build.get('timed_out'):
        print("STATUS: CONTINUE")
        print("REASON: Tests timed out but no failures detected. Agent should do exploratory testing.")
        print("NEXT_PHASE_NUM: %d" % next_phase)
        print("GEOS_RUNNING: " + str(running))
    elif term_qa['exit_code'] != 0:
        print("STATUS: CONTINUE")
        print("REASON: Terminal QA found failures. Agent should investigate.")
        print("NEXT_PHASE_NUM: %d" % next_phase)
    else:
        print("STATUS: CONTINUE")
        print("REASON: All green. Agent should do exploratory testing.")
        print("NEXT_PHASE_NUM: %d" % next_phase)
        print("GEOS_RUNNING: " + str(running))
    print("PROJECT_DIR: " + GEOS_DIR)
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "geos_running": running,
        "build": build,
        "term_qa_exit": term_qa['exit_code'],
        "next_phase_num": next_phase,
    }
    with open(OUTPUT_JSON, "w") as f:
        json.dump(summary, f, indent=2)
    print("Summary saved to " + OUTPUT_JSON)


if __name__ == "__main__":
    atexit.register(kill_stale_test_processes)
    try:
        main()
    except Exception as e:
        print("FATAL: %s" % e)
        write_fallback_json(False, 141, str(e))
        sys.exit(1)
