#!/usr/bin/env python3
"""
Geometry OS Terminal QA Tester.

Runs headless terminal tests via geos-term, analyzes results,
and generates roadmap phases for any failures found.

Usage:
    python3 terminal_qa.py              # run all tests, print report
    python3 terminal_qa.py --fix        # also patch roadmap.yaml with fix phases
    python3 terminal_qa.py --script     # run a custom test script

Output: JSON test results + optional roadmap phase generation.
"""

import subprocess, sys, os, json, re, time
from datetime import datetime

GEOS_DIR = os.path.expanduser("~/zion/projects/geometry_os/geometry_os")
GEOS_TERM = os.path.join(GEOS_DIR, "target/release/geos-term")
ROADMAP = os.path.join(GEOS_DIR, "roadmap.yaml")

# Next available phase number (auto-detected from roadmap.yaml)
def get_next_phase_num():
    try:
        import yaml
        with open(ROADMAP) as f:
            data = yaml.safe_load(f)
        nums = []
        for p in data.get("phases", []):
            pid = p.get("id", "")
            m = re.search(r"phase-(\d+)", pid)
            if m:
                nums.append(int(m.group(1)))
        return max(nums) + 1 if nums else 141
    except:
        return 141


def run_geos_test(test_name):
    """Run a single geos-term --test and capture output."""
    cmd = [GEOS_TERM, "--test", test_name]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, cwd=GEOS_DIR)
        return {
            "name": test_name,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "passed": result.returncode == 0,
        }
    except subprocess.TimeoutExpired as e:
        return {
            "name": test_name,
            "exit_code": -1,
            "stdout": (e.stdout or "")[:500],
            "stderr": (e.stderr or "")[:500],
            "passed": False,
            "timeout": True,
        }


def run_geos_script(script, label="custom"):
    """Run a geos-term --script and capture output."""
    cmd = [GEOS_TERM, "--script", script]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, cwd=GEOS_DIR)
        return {
            "name": label,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "passed": result.returncode == 0,
        }
    except subprocess.TimeoutExpired as e:
        return {
            "name": label,
            "exit_code": -1,
            "stdout": (e.stdout or "")[:500],
            "stderr": (e.stderr or "")[:500],
            "passed": False,
            "timeout": True,
        }


# ============================================================
# Test definitions
# ============================================================

BUILTIN_TESTS = [
    ("echo_round_trip", "Bash echo round-trip: type 'echo hello', verify output"),
    ("line_wrap", "Line wrapping: type 86+ chars, verify wrap at 80 cols"),
    ("ctrl_c", "Ctrl-C: interrupt sleep process, verify prompt returns"),
]

SCRIPT_TESTS = [
    # Test: pwd command
    ("pwd_command", "frame:120,type:pwd,key:13,frame:80,dump", 
     "pwd output should contain /"),
    # Test: tab completion
    ("tab_completion", "frame:120,type:ls /tm,key:9,frame:40,dump",
     "tab completion should expand /tm to /tmp"),
    # Test: backspace
    ("backspace", "frame:120,type:echo hellx,key:8,key:111,key:13,frame:80,dump",
     "backspace should correct 'hellx' to 'hello'"),
    # Test: multiple commands
    ("two_commands", "frame:120,type:echo first,key:13,frame:60,type:echo second,key:13,frame:80,dump",
     "two echo commands should both appear"),
    # Test: clear screen
    ("clear_screen", "frame:120,type:clear,key:13,frame:40,dump",
     "clear command should empty the screen"),
]


def run_builtin_tests():
    """Run the built-in geos-term --test suite."""
    results = []
    for test_name, description in BUILTIN_TESTS:
        r = run_geos_test(test_name)
        r["description"] = description
        results.append(r)
    return results


def run_script_tests():
    """Run custom script-based tests."""
    results = []
    for name, script, assertion in SCRIPT_TESTS:
        r = run_geos_script(script, label=name)
        r["description"] = assertion
        results.append(r)
    return results


def analyze_failures(results):
    """Analyze test failures and generate fix suggestions."""
    fixes = []
    for r in results:
        if r["passed"]:
            continue
        
        name = r["name"]
        stdout = r.get("stdout", "")
        stderr = r.get("stderr", "")
        
        # Classify failure type
        if "unknown opcode" in stderr:
            fixes.append({
                "test": name,
                "category": "build",
                "severity": "blocker",
                "issue": f"Assembly error: {stderr.strip()[:200]}",
                "fix": "Rebuild geos-term binary after assembler changes",
            })
        elif "no shell prompt" in stdout:
            fixes.append({
                "test": name,
                "category": "pty",
                "severity": "blocker",
                "issue": "Bash prompt not appearing in terminal output",
                "fix": "Check PTY spawn settings (TERM, PS1), verify reader thread is receiving bytes",
            })
        elif "timeout" in (r.get("stderr", "") or ""):
            fixes.append({
                "test": name,
                "category": "hang",
                "severity": "critical",
                "issue": f"Test timed out: {name}",
                "fix": "Program may be stuck in infinite loop or blocking on PTY read",
            })
        else:
            fixes.append({
                "test": name,
                "category": "logic",
                "severity": "major",
                "issue": f"Test failed: {name}",
                "detail": (stdout + stderr)[:300],
                "fix": "Investigate test output for specific failure",
            })
    
    return fixes


def generate_roadmap_phases(fixes, do_write=False):
    """Generate roadmap phases from failure analysis."""
    if not fixes:
        print("All tests passed -- no new phases needed.")
        return
    
    # Group fixes by category
    categories = {}
    for f in fixes:
        cat = f["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(f)
    
    phases = []
    phase_num = get_next_phase_num()
    
    # Build blocker phase if needed
    blockers = [f for f in fixes if f.get("severity") == "blocker"]
    if blockers:
        tasks = []
        task_num = 1
        for b in blockers:
            tasks.append({
                "id": f"p{phase_num}.d1.t{task_num}",
                "title": f"Fix: {b['test']} -- {b['issue'][:80]}",
                "status": "todo",
                "description": b["fix"],
            })
            task_num += 1
        
        phases.append({
            "id": f"phase-{phase_num}",
            "title": f"Host Terminal -- Test Regression Fixes ({len(blockers)} blockers)",
            "status": "planned",
            "goal": f"Fix {len(blockers)} blocking test failures discovered by terminal QA",
            "description": "Automated terminal QA found blocking failures. These must be fixed before other tests can run.",
            "deliverables": [{
                "name": f"Fix {len(blockers)} blocking test failures",
                "description": "; ".join(b["issue"] for b in blockers),
                "status": "todo",
                "tasks": tasks,
                "scope_lines": 50 * len(blockers),
            }],
            "scope_lines_total": 0,  # will be calculated
            "test_target": 0,
        })
        phase_num += 1
    
    # Other failures as separate phase
    others = [f for f in fixes if f.get("severity") != "blocker"]
    if others:
        tasks = []
        task_num = 1
        for o in others:
            tasks.append({
                "id": f"p{phase_num}.d1.t{task_num}",
                "title": f"Fix: {o['test']} ({o['category']}) -- {o['issue'][:60]}",
                "status": "todo",
                "description": o.get("fix", "Investigate and fix"),
            })
            task_num += 1
        
        phases.append({
            "id": f"phase-{phase_num}",
            "title": f"Host Terminal -- Test Failure Fixes ({len(others)} issues)",
            "status": "planned",
            "goal": f"Fix {len(others)} non-blocking test failures from terminal QA",
            "description": "Automated terminal QA found functional issues.",
            "deliverables": [{
                "name": f"Fix {len(others)} test failures",
                "description": "; ".join(o["issue"] for o in others),
                "status": "todo",
                "tasks": tasks,
                "scope_lines": 30 * len(others),
            }],
            "scope_lines_total": 0,
            "test_target": 0,
        })
    
    if do_write and phases:
        import yaml
        with open(ROADMAP) as f:
            data = yaml.safe_load(f)
        
        # Calculate scope_lines_total
        last_scope = data["phases"][-1].get("scope_lines_total", 74000)
        for p in phases:
            total = sum(d.get("scope_lines", 0) for d in p["deliverables"])
            last_scope += total
            p["scope_lines_total"] = last_scope
            p["test_target"] = 0
        
        data["phases"].extend(phases)
        with open(ROADMAP, "w") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        print(f"Appended {len(phases)} phases to roadmap.yaml")
    
    return phases


def print_report(results, fixes=None):
    """Print a summary report."""
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    
    print(f"\n{'='*60}")
    print(f"TERMINAL QA REPORT -- {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    print(f"Results: {passed}/{total} passed")
    print()
    
    for r in results:
        icon = "PASS" if r["passed"] else "FAIL"
        print(f"  [{icon}] {r['name']}: {r.get('description', '')}")
    
    if fixes:
        print(f"\n--- Failure Analysis ({len(fixes)} issues) ---")
        for f in fixes:
            print(f"  [{f['severity']:8s}] {f['test']}: {f['issue'][:80]}")
    
    print()


def main():
    do_fix = "--fix" in sys.argv
    
    print("Building geos-term (if stale)...")
    build = subprocess.run(
        ["cargo", "build", "--release", "--bin", "geos-term"],
        cwd=GEOS_DIR, capture_output=True, text=True, timeout=120
    )
    if build.returncode != 0:
        print(f"BUILD FAILED: {build.stderr[:500]}")
        sys.exit(1)
    
    print("Running built-in tests...")
    results = run_builtin_tests()
    
    print("Running script tests...")
    results.extend(run_script_tests())
    
    fixes = analyze_failures(results)
    print_report(results, fixes)
    
    if fixes:
        phases = generate_roadmap_phases(fixes, do_write=do_fix)
        if phases:
            print(f"Generated {len(phases)} roadmap phases:")
            for p in phases:
                print(f"  {p['id']}: {p['title']}")
    
    # JSON output for cron consumption
    output = {
        "timestamp": datetime.now().isoformat(),
        "passed": sum(1 for r in results if r["passed"]),
        "total": len(results),
        "failures": len(fixes),
        "results": [{"name": r["name"], "passed": r["passed"], "exit_code": r["exit_code"]} for r in results],
        "fixes": fixes,
        "phases_generated": len(fixes) > 0,
    }
    
    # Write JSON for preflight script
    json_path = "/tmp/geo_terminal_qa.json"
    with open(json_path, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"Results saved to {json_path}")
    
    # Exit code reflects test results
    sys.exit(0 if all(r["passed"] for r in results) else 1)


if __name__ == "__main__":
    main()
