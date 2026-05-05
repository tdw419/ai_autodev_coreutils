#!/usr/bin/env python3
"""
Geometry OS Reviewer/Shipper Preflight

Runs before the reviewer cron job. Checks:
1. Whether the drafter worker left any uncommitted work
2. Current test status (with cargo test lock, retry on contention)
3. Roadmap phases with all deliverables done but phase status still planned
4. Whether breakage is committed or uncommitted (scopes the revert)

Outputs structured data for the reviewer agent to consume.
"""

import os, sys, subprocess, re, time, json

sys.path.insert(0, os.path.dirname(__file__))
from geo_event_log import block, escalate, revert, test_gate

PROJECT = os.path.expanduser("~/zion/projects/geometry_os/geometry_os")
LOCK_PATH = "/tmp/geo_cargo_test.lock"
LOCK_RETRY_DELAY = 30  # seconds to wait if another cargo test is running


def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] REVIEWER: {msg}", file=sys.stderr)


def git_status():
    """Check for uncommitted changes."""
    r = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True, text=True, timeout=10,
        cwd=PROJECT,
    )
    lines = [l for l in r.stdout.strip().split("\n") if l.strip()]
    # staged: index changes (first column is M/A/D/R/C, second is space or ?)
    staged = [l for l in lines if len(l) >= 2 and l[0] in "MADRC" and l[1] == " "]
    # unstaged: working tree changes (second column is M/A/D/R/C)
    unstaged = [l for l in lines if len(l) >= 2 and l[1] in "MADRC"]
    untracked = [l for l in lines if l.startswith("??")]
    return staged, unstaged, untracked


def git_diff_stat():
    """Get diff stats for unstaged changes."""
    r = subprocess.run(
        ["git", "diff", "--stat"],
        capture_output=True, text=True, timeout=10,
        cwd=PROJECT,
    )
    return r.stdout.strip()


def git_diff_cached_stat():
    """Get diff stats for staged changes."""
    r = subprocess.run(
        ["git", "diff", "--cached", "--stat"],
        capture_output=True, text=True, timeout=10,
        cwd=PROJECT,
    )
    return r.stdout.strip()


def git_last_commit():
    """Get the last commit hash and message."""
    r = subprocess.run(
        ["git", "log", "-1", "--format=%H %s"],
        capture_output=True, text=True, timeout=10,
        cwd=PROJECT,
    )
    return r.stdout.strip()


def git_log_recent(n=10):
    """Get recent commits."""
    r = subprocess.run(
        ["git", "log", "--oneline", f"-{n}"],
        capture_output=True, text=True, timeout=10,
        cwd=PROJECT,
    )
    return r.stdout.strip().split("\n") if r.stdout.strip() else []


def acquire_lock_with_retry():
    """Try to acquire cargo test lock, retry once after delay."""
    import fcntl
    try:
        lock_fd = open(LOCK_PATH, "w")
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return lock_fd
    except (ImportError, IOError):
        pass

    # Retry once after delay
    log(f"Lock contention -- retrying in {LOCK_RETRY_DELAY}s")
    time.sleep(LOCK_RETRY_DELAY)
    try:
        lock_fd = open(LOCK_PATH, "w")
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        log("Lock acquired on retry")
        return lock_fd
    except (ImportError, IOError):
        log("Lock still held after retry. Skipping test gate.")
        return None


def run_tests(targeted=True):
    """Run cargo test with lock. Returns (passed, failed, failures, output_snippet)."""
    lock_fd = acquire_lock_with_retry()
    if lock_fd is None:
        print("TEST_GATE: SKIP (lock contention after retry)")
        return None, None, [], ""

    try:
        if targeted:
            cmd = [
                "cargo", "test", "--lib", "--",
                "--test-threads=2",
                "test_save_load", "test_basic_arithmetic", "test_ffi_syscall_dispatch"
            ]
            timeout = 120
        else:
            cmd = [
                "cargo", "test", "--lib", "--",
                "--test-threads=2",
                "--skip", "test_linux_kernel_early_boot",
                "--skip", "test_full_linux"
            ]
            timeout = 480

        r = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout,
            cwd=PROJECT,
        )
        output = r.stdout + r.stderr

        total_passed = 0
        total_failed = 0
        for m in re.finditer(r'(\d+) passed.*?(\d+) failed', output):
            total_passed += int(m.group(1))
            total_failed += int(m.group(2))

        failures = re.findall(r'test (\S+) \.\.\. FAILED', output)

        # Get last 20 lines for context
        snippet = "\n".join(output.strip().split("\n")[-20:])

        return total_passed, total_failed, failures, snippet
    except subprocess.TimeoutExpired:
        log(f"cargo test timed out ({timeout}s)")
        return None, None, ["timeout"], "cargo test timed out"
    except Exception as e:
        log(f"cargo test error: {e}")
        return None, None, [], str(e)
    finally:
        try:
            import fcntl
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
            lock_fd.close()
        except:
            pass


def check_roadmap_drift():
    """Find phases where all deliverables are done but phase is still planned."""
    import yaml
    path = os.path.join(PROJECT, "roadmap_v2.yaml")
    if not os.path.exists(path):
        return []

    with open(path) as f:
        data = yaml.safe_load(f)

    drifted = []
    for phase in data.get("phases", []):
        if not isinstance(phase, dict):
            continue
        if phase.get("status") != "planned":
            continue
        delivs = phase.get("deliverables", [])
        if not delivs:
            continue
        if all(d.get("status") == "done" for d in delivs if isinstance(d, dict)):
            drifted.append(phase.get("id", "?"))

    return drifted


def check_in_progress_stale():
    """Find in_progress phases claimed >30 min ago."""
    import yaml
    path = os.path.join(PROJECT, "roadmap_v2.yaml")
    if not os.path.exists(path):
        return []

    with open(path) as f:
        data = yaml.safe_load(f)

    now = time.time()
    stale = []
    for phase in data.get("phases", []):
        if not isinstance(phase, dict):
            continue
        if phase.get("status") != "in_progress":
            continue
        claimed_at = phase.get("_claimed_at", 0)
        if now - claimed_at > 1800:
            stale.append({
                "id": phase.get("id", "?"),
                "title": phase.get("title", "?"),
                "age_minutes": int((now - claimed_at) / 60),
            })

    return stale


BLOCKED_FILE = os.path.join(PROJECT, "BLOCKED.md")


def identify_phase_from_commit():
    """Try to figure out which phase a commit relates to, by checking the commit
    message and the roadmap's in_progress phases."""
    import yaml
    
    # Check commit message for phase-N pattern
    last = git_last_commit()
    if not last:
        return None
    
    msg = last.split(" ", 1)[-1] if " " in last else ""
    m = re.search(r'phase[- ](\d+)', msg, re.IGNORECASE)
    if m:
        return f"phase-{m.group(1)}"
    
    # Check roadmap for any in_progress phase
    roadmap_path = os.path.join(PROJECT, "roadmap_v2.yaml")
    if not os.path.exists(roadmap_path):
        return None
    try:
        with open(roadmap_path) as f:
            data = yaml.safe_load(f)
        for phase in data.get("phases", []):
            if phase.get("status") == "in_progress":
                return phase.get("id")
    except:
        pass
    
    return None


BLOCK_MAX_BLOCKS = 3  # After this many blocks, escalate phase to deferred


def get_block_count(phase_id):
    """Count how many times a phase has been blocked (non-expired entries)."""
    if not os.path.exists(BLOCKED_FILE):
        return 0
    try:
        now = time.time()
        count = 0
        with open(BLOCKED_FILE) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 4 and parts[0] == phase_id:
                    try:
                        ts = float(parts[2])
                        if now - ts < 3600:  # within TTL window
                            count += 1
                    except ValueError:
                        pass
        return count
    except:
        return 0


def write_blocked_phase(phase_id, reason):
    """Append a blocked phase entry to BLOCKED.md.
    Format: phase-N | reason | unix_timestamp | block_count
    Returns the new block count for this phase."""
    ts = str(int(time.time()))
    count = get_block_count(phase_id) + 1
    line = f"{phase_id} | {reason} | {ts} | {count}\n"

    # Ensure header exists
    if not os.path.exists(BLOCKED_FILE):
        with open(BLOCKED_FILE, "w") as f:
            f.write("# Blocked Phases -- reverted by reviewer, skip in drafter\n")
            f.write("# Format: phase-N | reason | unix_timestamp | block_count\n")
            f.write("# Entries auto-expire after 1 hour\n")
            f.write(f"# Phases blocked {BLOCK_MAX_BLOCKS}+ times are escalated to deferred\n\n")

    with open(BLOCKED_FILE, "a") as f:
        f.write(line)

    log(f"Blocked {phase_id}: {reason} (block #{count})")

    # Escalate if threshold reached
    if count >= BLOCK_MAX_BLOCKS:
        escalate_phase_to_deferred(phase_id, reason, count)

    block(phase_id, reason, count)
    return count


def escalate_phase_to_deferred(phase_id, reason, block_count):
    """Move a repeatedly-blocked phase to deferred status so it stops cycling."""
    import yaml
    roadmap_path = os.path.join(PROJECT, "roadmap_v2.yaml")
    if not os.path.exists(roadmap_path):
        return

    try:
        with open(roadmap_path) as f:
            data = yaml.safe_load(f)

        for phase in data.get("phases", []):
            if phase.get("id") == phase_id:
                phase["status"] = "deferred"
                phase["_deferred_reason"] = f"Blocked {block_count} times by reviewer: {reason}"
                break

        import shutil
        backup = roadmap_path + ".bak"
        shutil.copy2(roadmap_path, backup)

        with open(roadmap_path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        # Verify
        with open(roadmap_path) as f:
            verify = yaml.safe_load(f)
        if len(verify.get("phases", [])) != len(data.get("phases", [])):
            shutil.copy2(backup, roadmap_path)
            log(f"ESCALATION FAILED: roadmap write verification failed for {phase_id}")
            return

        log(f"ESCALATED {phase_id} to deferred after {block_count} blocks")
        print(f"ESCALATED: {phase_id} to deferred (blocked {block_count} times)")
        escalate(phase_id, reason, block_count)
    except Exception as e:
        log(f"Escalation failed for {phase_id}: {e}")


def check_compile():
    """Quick cargo check to see if it compiles."""
    try:
        r = subprocess.run(
            ["cargo", "check", "--lib"],
            capture_output=True, text=True, timeout=120,
            cwd=PROJECT,
        )
        if r.returncode == 0:
            return True, ""
        else:
            # Extract errors
            errors = [l for l in (r.stderr + r.stdout).split("\n") if "error" in l.lower()][:5]
            return False, "\n".join(errors)
    except subprocess.TimeoutExpired:
        return None, "cargo check timed out"


def identify_breakage_scope(has_changes, compiles):
    """
    Determine whether breakage is in committed code or uncommitted working tree.
    
    This is critical: if the drafter committed good code then made uncommitted
    changes that broke the build, we should only revert the working tree.
    If the breakage is in committed code, we need git reset/revert.
    
    Returns: "working_tree", "committed", or "none"
    """
    if compiles is None or compiles:
        return "none"
    
    if has_changes:
        # Working tree has changes AND it doesn't compile.
        # Check: does the last commit compile? (stash working tree, check, pop)
        try:
            subprocess.run(
                ["git", "stash", "-q"],
                capture_output=True, text=True, timeout=15,
                cwd=PROJECT,
            )
            r = subprocess.run(
                ["cargo", "check", "--lib"],
                capture_output=True, text=True, timeout=120,
                cwd=PROJECT,
            )
            last_commit_clean = (r.returncode == 0)
            subprocess.run(
                ["git", "stash", "pop", "-q"],
                capture_output=True, text=True, timeout=15,
                cwd=PROJECT,
            )
            if last_commit_clean:
                return "working_tree"
            else:
                return "committed"
        except Exception as e:
            log(f"Breakage scope check failed: {e}. Assuming working_tree.")
            return "working_tree"
    else:
        # Clean tree but doesn't compile -- breakage is committed
        return "committed"


def main():
    log("Starting reviewer preflight...")

    # 1. Git status
    staged, unstaged, untracked = git_status()
    has_changes = bool(staged or unstaged)

    print(f"UNCOMMITTED: {has_changes}")
    if staged:
        print(f"STAGED_FILES: {len(staged)}")
    if unstaged:
        print(f"UNSTAGED_FILES: {len(unstaged)}")
    if untracked:
        print(f"UNTRACKED_FILES: {len(untracked)}")

    if has_changes:
        stat = git_diff_stat()
        if stat:
            print(f"DIFF_STAT:\n{stat}")
        cached_stat = git_diff_cached_stat()
        if cached_stat:
            print(f"STAGED_STAT:\n{cached_stat}")

    # 2. Compile check
    compiles, compile_errors = check_compile()
    print(f"COMPILES: {compiles}")
    if not compiles and compile_errors:
        print(f"COMPILE_ERRORS:\n{compile_errors}")

    # 2b. Identify breakage scope (if broken)
    breakage_scope = identify_breakage_scope(has_changes, compiles)
    if breakage_scope != "none":
        print(f"BREAKAGE_SCOPE: {breakage_scope}")
        if breakage_scope == "committed":
            last = git_last_commit()
            print(f"LAST_COMMIT: {last}")

    # 3. Test gate (only if it compiles)
    if compiles:
        passed, failed, failures, snippet = run_tests(targeted=True)
        if passed is not None:
            print(f"TEST_PASSED: {passed}")
            print(f"TEST_FAILED: {failed}")
            if failures:
                print(f"FAILING_TESTS: {', '.join(failures[:10])}")
            if failed and failed > 0:
                print(f"TEST_OUTPUT:\n{snippet}")
        else:
            print("TEST_RESULT: unavailable (locked or error)")
    else:
        print("TEST_RESULT: skipped (compile failed)")

    # 4. Roadmap drift check
    drifted = check_roadmap_drift()
    if drifted:
        print(f"DRIFTED_PHASES: {', '.join(drifted)}")
    else:
        print("DRIFTED_PHASES: none")

    # 5. Stale in_progress
    stale = check_in_progress_stale()
    if stale:
        for s in stale:
            print(f"STALE_PHASE: {s['id']} ({s['title']}) -- claimed {s['age_minutes']}m ago")
    else:
        print("STALE_PHASES: none")

    # 6. Recent commits for context
    recent = git_log_recent(5)
    print(f"RECENT_COMMITS:")
    for c in recent:
        print(f"  {c}")

    # 7. Decision recommendation
    if not compiles:
        if breakage_scope == "working_tree":
            print("ACTION: REVERT_WORKING_TREE (uncommitted changes broke the build)")
        else:
            print("ACTION: REVERT_COMMIT (committed code broke the build)")
            # Identify the phase to block
            phase_id = identify_phase_from_commit()
            if phase_id:
                write_blocked_phase(phase_id, "compile broken after commit")
                print(f"BLOCKED_PHASE: {phase_id}")
                revert(phase_id, "compile broken after commit", scope="committed")
    elif has_changes and failed and failed > 0:
        # Tests fail with uncommitted changes -- check if tests were already failing
        print("ACTION: EVALUATE (uncommitted changes + test failures -- inspect scope)")
    elif has_changes and (failed == 0 or passed is not None):
        print("ACTION: COMMIT (changes look good)")
    elif not has_changes and drifted:
        print("ACTION: TICK_ROADMAP (drifted phases to complete)")
    elif not has_changes and stale:
        print("ACTION: RELEASE_STALE (reset stale in_progress claims)")
    else:
        # Check if there are todo phases but no planned ones (pipeline stall)
        import yaml as _yaml
        _rpath = os.path.join(PROJECT, "roadmap_v2.yaml")
        if os.path.exists(_rpath):
            with open(_rpath) as _rf:
                _rdata = _yaml.safe_load(_rf)
            _all_phases = _rdata.get("phases", [])
            _todo_count = sum(1 for p in _all_phases if isinstance(p, dict) and p.get("status") == "todo")
            _planned_count = sum(1 for p in _all_phases if isinstance(p, dict) and p.get("status") == "planned")
            if _todo_count > 0 and _planned_count == 0:
                print(f"ACTION: PROMOTE_TODO ({_todo_count} todo phases, 0 planned -- promote some to unblock drafter)")
                print(f"TODO_PHASES: {_todo_count}")
            else:
                print("ACTION: NOTHING (clean tree, no drift)")
        else:
            print("ACTION: NOTHING (clean tree, no drift)")

    # Emit heartbeat so watchdog knows reviewer is alive (even when nothing to review)
    try:
        from geo_event_log import heartbeat
        heartbeat("reviewer")
    except ImportError:
        pass  # older geo_event_log without heartbeat

    log("Preflight complete.")


if __name__ == "__main__":
    main()
