#!/usr/bin/env python3
"""
LLM Oracle Preflight -- replaces the dumb FIFO phase claiming with an
intelligent LLM Oracle that reads the roadmap and map state, then decides
which phase to build next.

Uses model_choice (same stack as opcode 0x9C) to query a local LLM with
full project context. The Oracle sees:
  - All phases and their statuses
  - What buildings/features already exist
  - Dependency relationships between phases
  - Recent build history

And returns a structured decision with implementation guidance.
"""

import os, sys, json, re, time, subprocess, yaml, atexit, signal

sys.path.insert(0, os.path.dirname(__file__))
from geo_event_log import claim, stale_steal, test_gate, test_gate_halt, test_gate_timeout, auto_replenish, roadmap_empty, wip_self_commit

PROJECT = os.path.expanduser("~/zion/projects/geometry_os/geometry_os")


def _kill_stale_test_runners():
    """Kill any lingering geometry_os test runner processes."""
    try:
        subprocess.run(
            ["pkill", "-f", "target/.*geometry_os"],
            capture_output=True, timeout=5
        )
    except Exception:
        pass


atexit.register(_kill_stale_test_runners)
# Also clean up stale runners at startup
_kill_stale_test_runners()
WORKER_ID = os.environ.get("GEO_WORKER_ID", os.environ.get("HOSTNAME", "worker-0"))
IN_PROGRESS_TIMEOUT = 1800  # 30 min -- steal stale claims


def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] ORACLE [{WORKER_ID}]: {msg}", file=sys.stderr)


def load_roadmap():
    path = os.path.join(PROJECT, "roadmap_v2.yaml")
    with open(path) as f:
        return yaml.safe_load(f)


def save_roadmap(data):
    """Save roadmap_v2.yaml with integrity check to prevent truncation."""
    path = os.path.join(PROJECT, "roadmap_v2.yaml")
    
    # Validate before writing: must have phases and top-level fields
    phases = data.get("phases", [])
    if len(phases) < 5:
        raise ValueError(f"Roadmap integrity check FAILED: only {len(phases)} phases. "
                         f"Refusing to save (likely truncation bug). "
                         f"Expected 5+ phases.")
    
    # Backup current file before overwriting
    import shutil
    backup = path + ".bak"
    if os.path.exists(path):
        shutil.copy2(path, backup)
    
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    # Verify written file has same phase count
    with open(path) as f:
        verify = yaml.safe_load(f)
    if len(verify.get("phases", [])) != len(phases):
        # RESTORE from backup
        shutil.copy2(backup, path)
        raise ValueError(f"Roadmap write verification FAILED: wrote {len(phases)} phases "
                         f"but read back {len(verify.get('phases', []))}. Restored from backup.")


def get_phase_summary(roadmap):
    """Build a compact summary of all phases for the Oracle."""
    lines = []
    done_count = 0
    planned_count = 0
    in_progress_count = 0

    for phase in roadmap.get("phases", []):
        status = phase.get("status", "unknown")
        pid = phase.get("id", "?")
        title = phase.get("title", "?")
        goal = phase.get("goal", "")[:100]
        scope = phase.get("scope_lines_total", 0)
        test_target = phase.get("test_target", 0)

        if status == "done" or status == "complete":
            done_count += 1
            lines.append(f"  [DONE] {pid}: {title}")
        elif status == "planned":
            planned_count += 1
            delivs = phase.get("deliverables", [])
            todo_names = [d["name"] for d in delivs if d.get("status") == "todo"]
            planned_names = [d["name"] for d in delivs if d.get("status") == "planned"]
            total_delivs = len(delivs)
            lines.append(f"  [PLANNED] {pid}: {title}")
            lines.append(f"    goal: {goal}")
            lines.append(f"    deliverables: {total_delivs} ({len(planned_names)} planned, {len(todo_names)} todo)")
            lines.append(f"    scope: ~{scope} LOC, ~{test_target} tests")
            # Show dependencies/context from deliverable descriptions
            for d in delivs[:4]:
                desc = d.get("description", "")[:80]
                if desc:
                    lines.append(f"    - {d['name']}: {desc}")
        elif status == "in_progress":
            in_progress_count += 1
            claimed_by = phase.get("_claimed_by", "?")
            claimed_at = phase.get("_claimed_at", 0)
            age = int(time.time()) - claimed_at if claimed_at else 0
            lines.append(f"  [IN_PROGRESS] {pid}: {title} (by {claimed_by}, {age}s ago)")

    return lines, done_count, planned_count, in_progress_count


def get_existing_features():
    """Scan the codebase for what already exists -- buildings, opcodes, programs."""
    features = []

    # Count opcodes
    mod_rs = os.path.join(PROJECT, "src/vm/mod.rs")
    if os.path.exists(mod_rs):
        with open(mod_rs) as f:
            content = f.read()
        opcode_count = content.count("0x")  # rough
        # Count actual opcode handlers
        import re
        opcodes = re.findall(r"0x([0-9A-Fa-f]{2})\s*=>", content)
        features.append(f"  VM: {len(opcodes)} opcodes implemented")

    # List programs
    prog_dir = os.path.join(PROJECT, "programs")
    if os.path.isdir(prog_dir):
        progs = [f for f in os.listdir(prog_dir) if f.endswith(".asm")]
        features.append(f"  Programs: {', '.join(sorted(progs)[:15])}")

    # Count tests
    test_file = os.path.join(PROJECT, "src/vm/tests.rs")
    if os.path.exists(test_file):
        with open(test_file) as f:
            test_count = f.read().count("fn test_")
        features.append(f"  Tests: {test_count} test functions")

    # Check for key subsystems
    subsystems = []
    for name, path in [
        ("IPC", "src/ipc.rs"),
        ("VFS", "src/vfs.rs"),
        ("Process manager", "src/process.rs"),
        ("LLM Oracle (0x9C)", "src/vm/mod.rs"),
        ("Hypervisor", "src/hypervisor.rs"),
        ("RISC-V emulator", "src/riscv"),
        ("Assembler", "src/assembler"),
        ("MCP server", "src/mcp_server.rs"),
        ("Renderer", "src/render.rs"),
    ]:
        full = os.path.join(PROJECT, path)
        if os.path.exists(full):
            subsystems.append(name)
    if subsystems:
        features.append(f"  Subsystems: {', '.join(subsystems)}")

    return features


def get_recent_builds(n=5):
    """Get the last N completed phases for context."""
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "-n", n, "--grep=phase"],
            capture_output=True, text=True, timeout=10,
            cwd=PROJECT,
        )
        if result.returncode == 0 and result.stdout.strip():
            return [f"  {line}" for line in result.stdout.strip().split("\n")]
    except:
        pass
    return []


def build_oracle_prompt(phase_lines, features, recent_builds,
                        done_count, planned_count, in_progress_count):
    """Build the prompt for the LLM Oracle."""

    prompt = f"""You are the Geometry OS Oracle -- the AI architect that decides what gets built next.

## Current State
- {done_count} phases completed
- {planned_count} phases planned
- {in_progress_count} phases in progress

## Existing Codebase
{chr(10).join(features)}

## Recent Builds
{chr(10).join(recent_builds) if recent_builds else "  (no recent phase commits found)"}

## Planned Phases (candidates)
{chr(10).join(phase_lines)}

## Your Task
Decide which ONE planned phase should be built next. Consider:
1. **Dependencies**: Does this phase build on previously completed work?
2. **Foundation value**: Does this phase unlock multiple future phases?
3. **Complexity fit**: Can a single worker session complete it? (prefer <800 LOC phases)
4. **Coherence**: Does this phase connect to recently completed phases thematically?

Respond with JSON:
{{
  "phase_id": "phase-N",
  "reasoning": "2-3 sentences explaining why this phase next",
  "implementation_plan": ["step 1", "step 2", ...],
  "risk_notes": "any concerns or tricky parts",
  "estimated_loc": 500
}}"""

    return prompt


def call_oracle(prompt):
    """Call the LLM Oracle via model_choice."""
    try:
        from model_choice import generate
    except ImportError:
        log("model_choice not available, falling back to FIFO")
        return None

    try:
        log("Querying Oracle for phase selection...")
        response = generate(
            prompt,
            complexity="fast",
            max_tokens=500,
            temperature=0.4,  # low temp for consistent decisions
            template="ai_daemon",
            json_mode=True,
        )
        log(f"Oracle responded ({len(response)} chars)")
        return response
    except Exception as e:
        log(f"Oracle call failed: {e}")
        return None


def parse_oracle_decision(response):
    """Parse the Oracle's JSON response."""
    if not response:
        return None

    # Try to extract JSON from the response
    try:
        # model_choice with json_mode may return wrapped text
        import re
        json_match = re.search(r'\{[^{}]*\}', response, re.DOTALL)
        if json_match:
            decision = json.loads(json_match.group())
            if "phase_id" in decision:
                return decision
    except json.JSONDecodeError:
        pass

    log(f"Could not parse Oracle response as JSON: {response[:200]}")
    return None


def find_phase(roadmap, phase_id):
    """Find a phase by ID in the roadmap."""
    for phase in roadmap.get("phases", []):
        if phase.get("id") == phase_id:
            return phase
    return None


def claim_phase(roadmap, phase):
    """Claim a phase for this worker."""
    now = time.time()
    phase["status"] = "in_progress"
    phase["_claimed_by"] = WORKER_ID
    phase["_claimed_at"] = int(now)
    save_roadmap(roadmap)
    log(f"Claimed phase {phase['id']}: {phase['title']}")
    claim(phase["id"], WORKER_ID, reason=phase.get("goal", "")[:120])


def claim_stale_phase(roadmap):
    """Steal a phase that's been in_progress too long."""
    now = time.time()
    for phase in roadmap.get("phases", []):
        if phase.get("status") != "in_progress":
            continue
        claimed_at = phase.get("_claimed_at", 0)
        if now - claimed_at > IN_PROGRESS_TIMEOUT:
            log(f"Stealing stale phase {phase['id']} (claimed {int(now - claimed_at)}s ago)")
            claim_phase(roadmap, phase)
            stale_steal(phase["id"], WORKER_ID, int(now - claimed_at))
            return phase
    return None


def fifo_fallback(roadmap):
    """Original FIFO claiming as fallback if Oracle is unavailable.
    Skips phases listed in BLOCKED.md."""
    blocked_ids = {b["id"] for b in load_blocked_phases()}
    for phase in roadmap.get("phases", []):
        if phase.get("status") != "planned":
            continue
        if phase.get("id") in blocked_ids:
            log(f"FIFO skipping blocked phase {phase.get('id')}")
            continue
        has_todo = any(
            d.get("status") in ("todo", "planned")
            for d in phase.get("deliverables", [])
        )
        if has_todo:
            claim_phase(roadmap, phase)
            return phase
    return None

BLOCKED_FILE = os.path.join(PROJECT, "BLOCKED.md")
BLOCKED_MAX_AGE = 3600  # 1 hour -- blocked phases auto-expire


def load_blocked_phases():
    """Load phase IDs that the reviewer has blocked (reverted recently).
    
    The reviewer writes BLOCKED.md when it reverts a commit, so the drafter
    doesn't immediately re-claim and re-write the same broken code.
    Entries auto-expire after BLOCKED_MAX_AGE seconds.
    """
    if not os.path.exists(BLOCKED_FILE):
        return []
    
    try:
        now = time.time()
        blocked = []
        with open(BLOCKED_FILE) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                # Format: phase-N | reason | unix_timestamp | block_count
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 3:
                    pid = parts[0]
                    reason = parts[1]
                    try:
                        ts = float(parts[2])
                    except ValueError:
                        ts = 0
                    block_count = int(parts[3]) if len(parts) >= 4 and parts[3].isdigit() else 1
                    age = now - ts
                    if age < BLOCKED_MAX_AGE:
                        blocked.append({"id": pid, "reason": reason, "age_min": int(age / 60), "block_count": block_count})
        return blocked
    except Exception as e:
        log(f"Error reading BLOCKED.md: {e}")
        return []


def git_pull():
    try:
        subprocess.run(
            ["git", "pull", "--rebase"],
            capture_output=True, text=True, timeout=30,
            cwd=PROJECT,
        )
    except:
        pass


def check_tests():
    """Run cargo test with a two-tier strategy.

    Tier 1: Targeted tests (3 core tests, 2 threads, 60s timeout).
      Fast smoke test -- if these pass, the codebase is probably healthy.

    Tier 2: Full suite (8 threads, 90s timeout).
      Only runs if Tier 1 passes. Catches regressions in less-critical tests.

    A timeout is an INFRASTRUCTURE problem (tests are slow), NOT a code failure.
    We log it separately and proceed, rather than halting the drafter on a
    phantom failure.
    """
    lock_path = "/tmp/geo_cargo_test.lock"
    try:
        import fcntl
        lock_fd = open(lock_path, "w")
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except (ImportError, IOError):
        log("TEST GATE: another cargo test is already running. Skipping.")
        print("TEST_GATE: SKIP (concurrent test running)")
        return 0, 0, []

    try:
        # ── Tier 1: Targeted smoke test ──
        log("TEST GATE TIER 1: running targeted tests...")
        try:
            r = subprocess.run(
                ["cargo", "test", "--lib", "--",
                 "--test-threads=2",
                 "test_save_load", "test_basic_arithmetic", "test_ffi_syscall_dispatch"],
                capture_output=True, text=True, timeout=60,
                cwd=PROJECT,
            )
            output = r.stdout + r.stderr
            target_passed, target_failed = _parse_test_results(output)
            failures = re.findall(r'test (\S+) \.\.\. FAILED', output)

            if target_failed > 0:
                # Real failures in core tests -- halt
                log(f"TEST GATE: {target_passed} passed, {target_failed} FAILED in targeted. Halting.")
                for f in failures[:10]:
                    log(f"  FAIL: {f}")
                test_gate_halt(target_failed, failures[:10])
                return target_passed, target_failed, failures
        except subprocess.TimeoutExpired:
            # Even targeted tests timed out -- something is very wrong (stuck test)
            log("TEST GATE: targeted tests TIMED OUT (60s). Infrastructure issue.")
            test_gate_timeout(60)
            # Don't halt -- this is not a code failure. Proceed with caution.
            print("TEST_GATE: TIMEOUT (targeted tests exceeded 60s)")
            print("TEST_GATE_TIMEOUT: true")
            return 0, 0, []

        # ── Tier 2: Full suite ──
        log(f"TEST GATE TIER 2: running full suite ({target_passed} targeted passed)...")
        try:
            r = subprocess.run(
                ["cargo", "test", "--lib", "--", "--test-threads=8",
                 "--skip", "test_linux_kernel_early_boot"],
                capture_output=True, text=True, timeout=90,
                cwd=PROJECT,
            )
            output = r.stdout + r.stderr
            total_passed, total_failed = _parse_test_results(output)
            failures = re.findall(r'test (\S+) \.\.\. FAILED', output)

            if total_failed > 0:
                log(f"TEST GATE: {total_passed} passed, {total_failed} FAILED in full suite. Halting.")
                for f in failures[:10]:
                    log(f"  FAIL: {f}")
                test_gate_halt(total_failed, failures[:10])
                return total_passed, total_failed, failures
            else:
                log(f"TEST GATE: {total_passed} passed, 0 failed. Green.")
                test_gate(total_passed, 0)
                return total_passed, 0, []
        except subprocess.TimeoutExpired:
            # Full suite timed out but targeted passed -- infrastructure issue
            log("TEST GATE: full suite TIMED OUT (90s) but targeted passed. Proceeding.")
            test_gate_timeout(90)
            print(f"TEST_GATE: TIMEOUT (full suite exceeded 90s, but {target_passed} targeted passed)")
            print("TEST_GATE_TIMEOUT: true")
            return target_passed, 0, []  # 0 failures -- targeted passed

    except Exception as e:
        log(f"TEST GATE: error running tests: {e}. Proceeding anyway.")
        return 0, 0, []
    finally:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
            lock_fd.close()
        except:
            pass


def _parse_test_results(output):
    """Parse 'N passed; M failed' lines from cargo test output."""
    total_passed = 0
    total_failed = 0
    for match in re.finditer(r'(\d+) passed.*?(\d+) failed', output):
        total_passed += int(match.group(1))
        total_failed += int(match.group(2))
    return total_passed, total_failed


def check_desktop():
    """Run geo_desktop_alive.py to ensure the desktop binary is running."""
    try:
        result = subprocess.run(
            [sys.executable, os.path.expanduser("~/.hermes/scripts/geo_desktop_alive.py")],
            capture_output=True, text=True, timeout=30,
        )
        alive = "DESKTOP_ALIVE: true" in result.stdout
        log(f"Desktop alive: {alive}")
        # Print desktop status for worker to consume
        for line in result.stdout.strip().split("\n"):
            if line.startswith("DESKTOP_"):
                print(line)
        return alive
    except Exception as e:
        log(f"Desktop check failed: {e}")
        print("DESKTOP_ALIVE: false")
        print(f"DESKTOP_REASON: check failed ({e})")
        return False


def classify_phase_type(phase):
    """Classify a phase as 'rust', 'asm', or 'mixed' based on deliverables.

    ASM-only phases can use the canvas-as-IDE loop:
      load_source -> assemble -> run -> vmscreen -> save_asm -> git commit

    Rust phases need host filesystem + cargo build.
    Mixed phases need both.
    """
    delivs = phase.get("deliverables", [])
    if not delivs:
        # No explicit deliverables -- check the title and goal for hints
        title = phase.get("title", "").lower()
        goal = phase.get("goal", "").lower()
        asm_keywords = ["program", "demo", "app", "game", "tetris", "snake",
                        "paint", "terminal", "self-modif", "canvas"]
        rust_keywords = ["opcode", "vm ", "render", "assembler", "compiler",
                         "kernel", "hypervisor", "vfs", "ipc", "socket",
                         "build", "test", "benchmark", "refactor", "perf"]
        asm_score = sum(1 for k in asm_keywords if k in title or k in goal)
        rust_score = sum(1 for k in rust_keywords if k in title or k in goal)
        if asm_score > 0 and rust_score == 0:
            return "asm"
        if rust_score > 0 and asm_score == 0:
            return "rust"
        return "mixed"

    asm_exts = {".asm", ".glyph"}
    rust_exts = {".rs", ".toml", ".md", ".yaml", ".json"}
    has_asm = False
    has_rust = False

    for d in delivs:
        name = d.get("name", "")
        if "." in name:
            ext = "." + name.rsplit(".", 1)[-1]
            if ext in asm_exts:
                has_asm = True
            elif ext in rust_exts:
                has_rust = True
        else:
            # No extension -- check acceptance criteria for hints
            for ac in d.get("acceptance_criteria", []):
                desc = ac.get("description", "").lower()
                if any(k in desc for k in ["cargo", "opcode", "rust", "build"]):
                    has_rust = True
                if any(k in desc for k in ["program", "canvas", "assemble", "vm screen"]):
                    has_asm = True

    if has_asm and not has_rust:
        return "asm"
    if has_rust and not has_asm:
        return "rust"
    return "mixed"


def get_next_phase_num(roadmap):
    """Find the highest phase number and return next."""
    import re
    nums = []
    for p in roadmap.get("phases", []):
        pid = p.get("id", "")
        m = re.search(r"phase-(\d+)", pid)
        if m:
            nums.append(int(m.group(1)))
    return max(nums) + 1 if nums else 141


def scan_codebase_gaps():
    """Scan the codebase for missing features and return gap descriptions."""
    gaps = []
    
    # Check what opcodes exist
    try:
        result = subprocess.run(
            ["grep", "-c", "\"fn op_", "src/vm/mod.rs"],
            capture_output=True, text=True, timeout=10, cwd=PROJECT
        )
        if result.returncode == 0:
            count = int(result.stdout.strip()) if result.stdout.strip().isdigit() else 0
    except:
        pass
    
    # Check what programs exist
    try:
        programs = [f for f in os.listdir(os.path.join(PROJECT, "programs")) 
                    if f.endswith(".asm")]
        program_names = [p.replace(".asm", "") for p in programs]
    except:
        program_names = []
    
    # Check what apps have buildings on the map
    try:
        result = subprocess.run(
            ["grep", "-r", "BUILDING", "programs/"],
            capture_output=True, text=True, timeout=10, cwd=PROJECT
        )
        building_programs = set()
        for line in result.stdout.split("\n"):
            m = re.search(r'programs/(\w+)', line)
            if m:
                building_programs.add(m.group(1))
    except:
        building_programs = set()
    
    # Check what host FS opcodes exist (for daily driver gaps)
    host_fs_opcodes = []
    try:
        result = subprocess.run(
            ["grep", "-E", "FSOPEN|FSREAD|FSWRITE|FSLS|FSCLOSE", "src/vm/mod.rs"],
            capture_output=True, text=True, timeout=10, cwd=PROJECT
        )
        host_fs_opcodes = re.findall(r'FSOPEN|FSREAD|FSWRITE|FSLS|FSCLOSE', result.stdout)
    except:
        pass
    
    # Check terminal features
    has_terminal = "host_term" in program_names
    has_text_editor = any("editor" in p for p in program_names)
    has_process_monitor = any("proc" in p or "htop" in p or "monitor" in p for p in program_names)
    has_file_manager = any("file_browser" in p or "filemgr" in p for p in program_names)
    has_settings = any("settings" in p for p in program_names)
    
    # Gap analysis based on daily driver needs
    if has_terminal and not has_text_editor:
        gaps.append({
            "id_prefix": "text_editor",
            "title": "Text Editor App (nano-like)",
            "goal": "Edit real host files inside GeOS using the FS bridge",
            "description": "A nano-like editor that uses FSOPEN/FSREAD/FSWRITE to edit host files. "
                          "Essential for GeOS to be a daily driver -- you need to be able to edit configs and code.",
            "deliverables": [
                {"name": "Core editor: open, scroll, edit, save", 
                 "description": "nano_editor.asm: FSREAD file into line buffer, render visible window with SMALLTEXT, "
                               "arrow keys scroll, typing inserts, Ctrl+S saves via FSWRITE, Ctrl+Q exits",
                 "tasks": [
                     {"title": "File loading via FSREAD into line buffer"},
                     {"title": "Rendering: visible lines window with SMALLTEXT"},
                     {"title": "Editing: insert/delete chars, line breaks"},
                     {"title": "Save: FSWRITE modified buffer back to file"},
                 ]},
                {"name": "Search and navigation",
                 "description": "Ctrl+F search forward with highlight, Ctrl+G goto line number",
                 "tasks": [
                     {"title": "Search: Ctrl+F forward search with highlight"},
                     {"title": "Goto: Ctrl+G jump to line number"},
                 ]},
            ],
        })
    
    if not has_process_monitor:
        gaps.append({
            "id_prefix": "process_monitor",
            "title": "Process Monitor (htop for GeOS)",
            "goal": "See what's running -- both GeOS processes and host stats from /proc",
            "description": "Read process table from RAM, show PID/state/PC/cycles. Read /proc/meminfo "
                          "via FSREAD for host stats. Interactive: arrow keys, k to kill.",
            "deliverables": [
                {"name": "GeOS process list with color coding",
                 "description": "Read process table from VM RAM (0xF00 region). Show PID, state, PC, cycles. "
                               "Color: green=running, yellow=waiting, red=crashed.",
                 "tasks": [
                     {"title": "Read process table from VM RAM"},
                     {"title": "Render process list with color coding"},
                     {"title": "Interactive: kill process, sort by column"},
                 ]},
                {"name": "Host system stats via /proc",
                 "description": "FSREAD /proc/meminfo for RAM, /proc/stat for CPU. Render top bar.",
                 "tasks": [
                     {"title": "Parse /proc/meminfo for RAM stats"},
                     {"title": "Render system stats panel"},
                 ]},
            ],
        })
    
    if not has_file_manager:
        gaps.append({
            "id_prefix": "file_manager",
            "title": "File Manager App (midnight-commander style)",
            "goal": "Browse and manage host files from inside GeOS",
            "description": "Two-pane file manager using FSLS for directory listing, FSREAD for preview, "
                          "FSWRITE for copy. Navigate with arrow keys, enter to open dirs.",
            "deliverables": [
                {"name": "Directory browser with FSLS",
                 "description": "Left pane: current directory listing from FSLS. Navigate dirs, show file sizes.",
                 "tasks": [
                     {"title": "FSLS directory listing and rendering"},
                     {"title": "Navigate into/out of directories"},
                     {"title": "File preview pane (FSREAD first 256 bytes)"},
                 ]},
            ],
        })
    
    # Always check for polish/improvement gaps
    gaps.append({
        "id_prefix": "desktop_polish",
        "title": "Terminal Polish -- Scrollback and Visual Refinements",
        "goal": "Make the terminal feel like a real terminal emulator, not a demo",
        "description": "Scrollback buffer (PageUp/PageDown), better color rendering, "
                      "cursor improvements (blinking, block/underline toggle), and smooth scrolling.",
        "deliverables": [
            {"name": "Scrollback buffer with PageUp/PageDown",
             "description": "Ring buffer of 1000+ past lines. PageUp enters scrollback, PageDown toward live, any key exits.",
             "tasks": [
                 {"title": "Ring buffer for terminal history (1000 lines)"},
                 {"title": "PageUp/PageDown scroll navigation"},
                 {"title": "Visual indicator when in scrollback mode"},
             ]},
            {"name": "Cursor improvements",
             "description": "Blinking cursor, block/underline/bar toggle via Ctrl+click, cursor color matches terminal theme.",
             "tasks": [
                 {"title": "Blinking cursor (toggle every 500ms)"},
                 {"title": "Block vs underline cursor style toggle"},
             ]},
        ],
    })
    
    return gaps


def generate_next_phases(roadmap):
    """Generate new roadmap phases when the roadmap runs dry.
    
    Two-pass approach:
    1. Rule-based scanner: checks for known daily driver gaps (fast, free)
    2. Oracle LLM: proposes genuinely new phases based on codebase analysis (burns tokens but discovers novel work)
    
    Only calls the Oracle if the rule-based scanner comes up empty or returns
    fewer than 3 phases.
    """
    next_num = get_next_phase_num(roadmap)
    
    # Pass 1: Rule-based gap scanning
    gaps = scan_codebase_gaps()
    
    # Check which gaps already have corresponding phases
    existing_titles = set()
    for p in roadmap.get("phases", []):
        existing_titles.add(p.get("title", "").lower())
    
    new_phases = []
    last_scope = roadmap["phases"][-1].get("scope_lines_total", 75000) if roadmap["phases"] else 75000
    
    for gap in gaps:
        # Skip if similar phase already exists
        title_lower = gap["title"].lower()
        if any(title_lower[:20] in existing for existing in existing_titles):
            log(f"Skipping {gap['title']} -- similar phase already exists")
            continue
        
        # Build phase YAML structure
        deliverables = []
        for d in gap.get("deliverables", []):
            tasks = []
            for i, t in enumerate(d.get("tasks", []), 1):
                tasks.append({
                    "id": f"p{next_num}.d{len(deliverables)+1}.t{i}",
                    "title": t["title"],
                    "status": "todo",
                    "description": t.get("description", t["title"]),
                })
            scope = 100 * len(tasks)
            deliverables.append({
                "name": d["name"],
                "description": d["description"],
                "status": "todo",
                "tasks": tasks,
                "scope_lines": scope,
            })
            last_scope += scope
        
        phase = {
            "id": f"phase-{next_num}",
            "title": gap["title"],
            "status": "planned",
            "goal": gap["goal"],
            "description": gap["description"],
            "deliverables": deliverables,
            "scope_lines_total": last_scope,
            "test_target": len(deliverables) * 5,
        }
        
        new_phases.append(phase)
        next_num += 1
    
    # Pass 2: Oracle LLM if we found fewer than 3 gaps
    if len(new_phases) < 3:
        log(f"Rule-based scanner found {len(new_phases)} gaps. Querying Oracle for more...")
        oracle_phases = oracle_propose_phases(roadmap, next_num, existing_titles, last_scope)
        if oracle_phases:
            log(f"Oracle proposed {len(oracle_phases)} additional phases")
            new_phases.extend(oracle_phases)
    
    return new_phases


def oracle_propose_phases(roadmap, start_num, existing_titles, last_scope):
    """Ask the Oracle LLM to propose new phases based on the current codebase state.
    
    This only fires when the roadmap is nearly empty and the rule-based scanner
    found few gaps. Burns tokens but discovers genuinely novel work.
    """
    # Gather context
    features = get_existing_features()
    recent = get_recent_builds()
    
    # Summarize what's been built recently (last 10 done phases)
    recent_done = []
    for p in roadmap.get("phases", []):
        if p.get("status") == "done":
            recent_done.append(f"  {p['id']}: {p['title']}")
    recent_done_summary = "\n".join(recent_done[-10:]) if recent_done else "  (none)"
    
    # List programs that exist
    prog_dir = os.path.join(PROJECT, "programs")
    programs = []
    if os.path.isdir(prog_dir):
        programs = sorted([f.replace(".asm", "") for f in os.listdir(prog_dir) if f.endswith(".asm")])
    programs_summary = ", ".join(programs[:30])
    
    # List opcodes from the assembler
    try:
        result = subprocess.run(
            ["grep", "-E", "\"[A-Z]{2,}\"", "src/vm/mod.rs"],
            capture_output=True, text=True, timeout=10, cwd=PROJECT
        )
        opcode_names = sorted(set(re.findall(r'"([A-Z]{2,})"', result.stdout)))
        opcode_summary = ", ".join(opcode_names[:40])
    except:
        opcode_summary = "(unable to scan)"
    
    prompt = f"""You are the Geometry OS Roadmap Planner. The roadmap is almost empty and needs new phases.

## Project: Geometry OS
Pixel-art virtual machine with assembler, debugger, GUI desktop, infinite map, RISC-V hypervisor.

## CURRENT FOCUS: Layer 2 -- Cooperative Multi-Program Kernel
Every proposed phase MUST move toward Layer 2: cooperative multi-program kernel. This is the
next major milestone for Geometry OS -- enabling multiple programs to run concurrently,
share resources, and communicate with each other.

Acceptable contributions:
- Scheduler primitives (round-robin, priority, timer-based yielding)
- IPC/message-passing (mailboxes, shared memory regions, signal-like notifications)
- Process isolation (separate address spaces, memory protection, fault containment)
- Program lifecycle (load/launch, yield/suspend, exit/cleanup, program loader)
- Shared resource arbitration (screen splitting, input multiplexing, memory allocation)
- Process table and metadata (PID assignment, state tracking, per-program registers)

Validation programs are acceptable ONLY if they demonstrate Layer 2 mechanics:
- "Two programs running concurrently sharing the screen" -- QUALIFIES
- "Ping-pong IPC between two loaded programs" -- QUALIFIES
- "Asteroids game" -- REJECTED
- "L-system fractal renderer" -- REJECTED
- "New opcode for visual effects" -- REJECTED

## What exists:
- {len(programs)} programs: {programs_summary}
- Opcodes: {opcode_summary}
- Host FS bridge (FSOPEN/FSREAD/FSWRITE/FSLS)
- Host terminal (80-column bash via PTY)
- RISC-V hypervisor (guest OS isolation already exists at a higher level)
- Process manager stubs (src/process.rs)
- IPC stubs (src/ipc.rs)
- VFS stubs (src/vfs.rs)

## Recently completed phases:
{recent_done_summary}

## Your task:
Propose 5 new phases that build toward the Layer 2 cooperative multi-program kernel. Each phase should:
- Be completable in a single worker session (~500-800 LOC)
- Be specific (name the source file, the data structures, the opcodes or Rust module)
- Build incrementally (each phase should be testable independently)
- Prefer scheduler/IPC primitives that have a real future use case (e.g. clipboard sharing,
  app switching, notification routing) over abstract demos with no downstream utility

Respond with JSON array:
[
  {{
    "title": "Phase title",
    "goal": "One sentence goal",
    "description": "2-3 sentences of detail",
    "deliverables": [
      {{
        "name": "Deliverable name",
        "description": "Specific implementation",
        "tasks": ["task 1", "task 2", "task 3"]
      }}
    ]
  }}
]"""

    response = call_oracle(prompt)
    if not response:
        log("Oracle did not respond for phase proposal. Using rule-based phases only.")
        return []
    
    # Parse the response
    try:
        # Try to find JSON array in response
        json_match = re.search(r'\[.*\]', response, re.DOTALL)
        if not json_match:
            log(f"Oracle response has no JSON array: {response[:200]}")
            return []
        
        proposals = json.loads(json_match.group())
        if not isinstance(proposals, list):
            return []
    except json.JSONDecodeError as e:
        log(f"Oracle response parse error: {e}")
        return []
    
    # Convert proposals to roadmap phase format
    phases = []
    num = start_num
    scope = last_scope
    
    for prop in proposals[:5]:  # cap at 5
        title = prop.get("title", f"Phase {num}")
        title_lower = title.lower()
        
        # Skip if too similar to existing
        if any(title_lower[:20] in existing for existing in existing_titles):
            log(f"Skipping Oracle proposal '{title}' -- too similar to existing")
            continue
        
        deliverables = []
        for d in prop.get("deliverables", []):
            tasks = []
            for i, t_desc in enumerate(d.get("tasks", []), 1):
                tasks.append({
                    "id": f"p{num}.d{len(deliverables)+1}.t{i}",
                    "title": t_desc if isinstance(t_desc, str) else str(t_desc),
                    "status": "todo",
                    "description": t_desc if isinstance(t_desc, str) else str(t_desc),
                })
            d_scope = 100 * max(len(tasks), 1)
            deliverables.append({
                "name": d.get("name", "Unnamed deliverable"),
                "description": d.get("description", ""),
                "status": "todo",
                "tasks": tasks,
                "scope_lines": d_scope,
            })
            scope += d_scope
        
        phase = {
            "id": f"phase-{num}",
            "title": title,
            "status": "planned",
            "goal": prop.get("goal", ""),
            "description": prop.get("description", ""),
            "deliverables": deliverables,
            "scope_lines_total": scope,
            "test_target": len(deliverables) * 5,
        }
        
        phases.append(phase)
        existing_titles.add(title_lower)
        num += 1
    
    return phases


def dump_compiled_prompt(phase):
    """Compile a prompt via prompt-compiler and dump to ~/.cache/geo-prompts/
    for later cross-reference against BLOCKED.md and revert commits.

    Tagged with phase ID and ISO timestamp so you can correlate:
      "phase-267 got reverted -- what did the compiled prompt say vs static?"
    Purely additive -- never blocks the live drafter.
    """
    import hashlib
    from datetime import datetime, timezone

    phase_id = phase.get("id", "unknown")
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M")
    safe_title = re.sub(r'[^a-zA-Z0-9_-]', '_', phase.get("title", ""))[:60]

    cache_dir = os.path.expanduser("~/.cache/geo-prompts")
    os.makedirs(cache_dir, exist_ok=True)
    filename = f"{phase_id}_{ts}_{safe_title}.md"
    filepath = os.path.join(cache_dir, filename)

    try:
        from prompt_compiler.compiler import compile_prompt

        # Build a task description from the phase metadata
        delivs = phase.get("deliverables", [])
        todo_descs = [
            f"- {d['name']}: {d.get('description', '')[:120]}"
            for d in delivs if d.get("status") in ("todo", "planned")
        ]
        task = (
            f"Geometry OS phase {phase_id}: {phase.get('title', '')}\n"
            f"Goal: {phase.get('goal', '')}\n\n"
            f"Deliverables:\n" + "\n".join(todo_descs)
        )

        result = compile_prompt(
            recipe_name="implement-feature",
            task=task,
            base_dir=PROJECT,
            attempt=1,
        )

        content = result.get("content", "")
        tokens = result.get("tokens", 0)
        strategy = result.get("strategy", "?")
        cached = result.get("cached", False)
        prompt_id = result.get("id", "none")

        # Header with metadata for cross-referencing
        header = (
            f"<!-- Compiled Prompt Dump -->\n"
            f"<!-- Phase: {phase_id} -->\n"
            f"<!-- Timestamp: {ts} -->\n"
            f"<!-- Title: {phase.get('title', '')} -->\n"
            f"<!-- Prompt ID: {prompt_id} -->\n"
            f"<!-- Strategy: {strategy} -->\n"
            f"<!-- Tokens: {tokens} -->\n"
            f"<!-- Cached: {cached} -->\n"
            f"<!-- Static prompt hash: {hashlib.md5(open(os.path.expanduser('~/.hermes/cron/jobs.json'), 'rb').read()).hexdigest()[:12] if os.path.exists(os.path.expanduser('~/.hermes/cron/jobs.json')) else 'N/A'} -->\n\n"
        )

        with open(filepath, "w") as f:
            f.write(header + content)

        log(f"Compiled prompt dumped: {filepath} ({tokens} tokens, {strategy}, cached={cached})")

    except ImportError:
        log("prompt-compiler not importable, skipping compiled dump")
    except Exception as e:
        log(f"Compiled prompt dump failed (non-fatal): {e}")


def commit_stale_wip():
    """Commit uncommitted WIP if the reviewer hasn't shown up.

    The reviewer runs every 15m and commits drafter WIP. If WIP sits
    uncommitted for 25+ minutes, the reviewer is probably AWOL. The
    drafter commits it itself so the loop doesn't stall.

    Returns True if WIP was committed.
    """
    WIP_AGE_THRESHOLD = 25 * 60  # 25 minutes

    # Check for uncommitted changes
    r = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True, text=True, timeout=10,
        cwd=PROJECT,
    )
    changed = [l for l in r.stdout.strip().split("\n") if l.strip()]
    if not changed:
        return False

    # Check how long WIP has been sitting (use git status timestamp heuristic)
    # Simple approach: check the mtime of the most recently changed file
    try:
        r2 = subprocess.run(
            ["git", "diff", "--stat"],
            capture_output=True, text=True, timeout=10,
            cwd=PROJECT,
        )
        diff_stat = r2.stdout.strip()
        files_count = len(changed)
    except:
        files_count = len(changed)
        diff_stat = ""

    # Check last commit time vs now
    try:
        r3 = subprocess.run(
            ["git", "log", "-1", "--format=%ct"],
            capture_output=True, text=True, timeout=10,
            cwd=PROJECT,
        )
        last_commit_ts = int(r3.stdout.strip())
        wip_age = time.time() - last_commit_ts
    except:
        wip_age = 0

    if wip_age < WIP_AGE_THRESHOLD:
        log(f"Uncommitted WIP ({files_count} files) is only {int(wip_age/60)}m old. "
            f"Waiting for reviewer (threshold: {WIP_AGE_THRESHOLD//60}m).")
        return False

    # Reviewer is AWOL -- commit the WIP ourselves
    log(f"Reviewer AWOL: committing stale WIP ({files_count} files, {int(wip_age/60)}m old)")
    msg = f"WIP: drafter self-commit (reviewer AWOL, {files_count} files, {int(wip_age/60)}m stale)"
    try:
        subprocess.run(
            ["git", "add", "-A"],
            capture_output=True, text=True, timeout=15,
            cwd=PROJECT,
        )
        subprocess.run(
            ["git", "commit", "-m", msg],
            capture_output=True, text=True, timeout=15,
            cwd=PROJECT,
        )
        subprocess.run(
            ["git", "push"],
            capture_output=True, text=True, timeout=30,
            cwd=PROJECT,
        )
        wip_self_commit(files_count)
        print(f"WIP_SELF_COMMIT: {files_count} files committed (reviewer AWOL)")
        return True
    except Exception as e:
        log(f"WIP self-commit failed: {e}")
        return False


def main():
    git_pull()

    # Self-heal: commit stale WIP if reviewer hasn't shown up
    commit_stale_wip()

    # TEST GATE: If tests are failing, halt and fix instead of taking new phases
    passed, failed, failures = check_tests()
    if failed > 0:
        print(f"STATUS: HALT")
        print(f"HALT_REASON: {failed} tests failing. Must fix before taking new phases.")
        print(f"TESTS_PASSED: {passed}")
        print(f"TESTS_FAILED: {failed}")
        for f in failures[:10]:
            print(f"FAILING_TEST: {f}")
        print("TASK: Fix the failing tests before proceeding with new roadmap phases.")
        print("HINT: Run 'cargo test' to see full failure details. Fix test expectations")
        print("  or fix the code to make all tests pass. Do NOT start new feature work.")
        return

    check_desktop()
    roadmap = load_roadmap()

    # Build context for the Oracle
    phase_lines, done_count, planned_count, in_progress_count = get_phase_summary(roadmap)
    features = get_existing_features()
    recent_builds = get_recent_builds()

    LOW_WATERMARK = 5  # Generate new phases when planned drops below this

    if planned_count == 0:
        # Maybe steal a stale in-progress phase
        phase = claim_stale_phase(roadmap)
        if phase:
            print("STATUS: CONTINUE")
            print(f"WORKER_ID: {WORKER_ID}")
            print(f"PHASE_ID: {phase['id']}")
            print(f"PHASE: {phase['title']}")
            print(f"GOAL: {phase.get('goal', '')}")
            print(f"NOTE: Stolen from stale claim")
            return
        
        # Auto-replenish: generate new phases from codebase analysis
        log(f"Roadmap empty. Auto-generating new phases...")
        new_phases = generate_next_phases(roadmap)
        if new_phases:
            roadmap["phases"].extend(new_phases)
            try:
                save_roadmap(roadmap)
                log(f"Generated and saved {len(new_phases)} new phases")
                # Re-count and fall through to Oracle selection
                phase_lines, done_count, planned_count, in_progress_count = get_phase_summary(roadmap)
                print(f"AUTO_REPLENISHED: {len(new_phases)} new phases added")
                for p in new_phases:
                    print(f"  NEW_PHASE: {p['id']}: {p['title']}")
                auto_replenish([p["id"] for p in new_phases])
            except ValueError as e:
                log(f"Auto-replenish save failed: {e}")
                print("STATUS: ROADMAP_EMPTY")
                print("ROADMAP_EMPTY: true")
                print(f"TASK: Auto-replenish failed: {e}")
                return
        else:
            print("STATUS: ROADMAP_EMPTY")
            print("ROADMAP_EMPTY: true")
            print("TASK: All phases complete or in progress. Nothing to do.")
            roadmap_empty()
            return
    elif planned_count <= LOW_WATERMARK:
        # Low watermark: warn that roadmap needs refilling soon
        print(f"ROADMAP_LOW: true (only {planned_count} planned phases remain)")
        print("ROADMAP_REFILL_INSTRUCTION: After completing this phase, generate 10-15 new phases")
        print("  by analyzing the codebase and appending to roadmap_v2.yaml before regenerating ROADMAP.md.")

    # Call the Oracle
    oracle_prompt = build_oracle_prompt(
        phase_lines, features, recent_builds,
        done_count, planned_count, in_progress_count
    )
    response = call_oracle(oracle_prompt)
    decision = parse_oracle_decision(response)

    # Determine which phase to work on
    phase = None
    oracle_reasoning = ""
    oracle_plan = []
    risk_notes = ""
    est_loc = 0

    if decision:
        phase_id = decision.get("phase_id", "")
        phase = find_phase(roadmap, phase_id)
        # Check if this phase is blocked by the reviewer
        blocked = load_blocked_phases()
        blocked_ids = {b["id"] for b in blocked}
        if phase and phase.get("status") == "planned" and phase_id not in blocked_ids:
            oracle_reasoning = decision.get("reasoning", "")
            oracle_plan = decision.get("implementation_plan", [])
            risk_notes = decision.get("risk_notes", "")
            est_loc = decision.get("estimated_loc", 0)
            claim_phase(roadmap, phase)
            log(f"Oracle chose: {phase_id} -- {oracle_reasoning[:80]}")
        elif phase_id in blocked_ids:
            log(f"Oracle chose {phase_id} but it's BLOCKED by reviewer. Falling back.")
            phase = None
        else:
            log(f"Oracle chose {phase_id} but it's not available (status={phase.get('status') if phase else 'NOT_FOUND'})")
            phase = None

    if not phase:
        # Fallback to FIFO if Oracle failed or chose an unavailable phase
        log("Falling back to FIFO phase selection")
        phase = fifo_fallback(roadmap)
        oracle_reasoning = "Selected by FIFO fallback (Oracle unavailable or chose unavailable phase)"

    if not phase:
        print("STATUS: ROADMAP_EMPTY")
        print("ROADMAP_EMPTY: true")
        print("TASK: No available phases to claim.")
        return

    # Output the decision
    print("STATUS: CONTINUE")
    print(f"WORKER_ID: {WORKER_ID}")
    print(f"PHASE_ID: {phase['id']}")
    print(f"PHASE: {phase['title']}")
    print(f"GOAL: {phase.get('goal', '')}")
    print(f"ORACLE_REASONING: {oracle_reasoning}")

    if oracle_plan:
        print(f"ORACLE_PLAN_STEPS: {len(oracle_plan)}")
        for i, step in enumerate(oracle_plan, 1):
            print(f"ORACLE_STEP_{i}: {step}")

    if risk_notes:
        print(f"ORACLE_RISKS: {risk_notes}")
    if est_loc:
        print(f"ORACLE_EST_LOC: {est_loc}")

    # Classify phase type and output routing info
    phase_type = classify_phase_type(phase)
    print(f"PHASE_TYPE: {phase_type}")

    if phase_type == "asm":
        print("BUILD_PATH: canvas")
        print("CANVAS_DEV_NOTES: Use socket commands for ASM-only development:")
        print("  1. load_source <asm>   -- bulk-load source into canvas")
        print("  2. assemble            -- compile to bytecode")
        print("  3. run                 -- execute in VM")
        print("  4. vmscreen            -- verify output visually")
        print("  5. save_asm <name>     -- persist to programs/<name>.asm")
        print("  6. git add + commit    -- save to repo")
        print("  Do NOT edit .rs files or run cargo build for this phase.")
    elif phase_type == "rust":
        print("BUILD_PATH: host")
        print("HOST_DEV_NOTES: Edit Rust source files on host filesystem.")
        print("  Build with: cargo build --release")
        print("  Test with:  cargo test --release")
        print("  Restart desktop binary after changes.")
    else:
        print("BUILD_PATH: mixed")
        print("MIXED_DEV_NOTES: This phase requires both Rust and ASM work.")
        print("  Do Rust changes first (cargo build, restart), then verify via socket.")
        print("  Use canvas-as-IDE for ASM deliverables (load_source -> assemble -> run -> save_asm).")

    # List todo deliverables
    todos = [d for d in phase.get("deliverables", []) if d.get("status") in ("todo", "planned")]
    if todos:
        print(f"DELIVERABLES_TODO: {len(todos)}")
        for d in todos:
            desc = d.get("description", "")[:120]
            print(f"TODO: {d['name']}: {desc}")

    print(f"PROJECT_DIR: {PROJECT}")

    # Shadow compile: dump a prompt-compiler output for later cross-reference
    # against BLOCKED.md and revert commits. Does NOT affect the live drafter.
    dump_compiled_prompt(phase)

    log(f"Phase {phase['id']} assigned to {WORKER_ID}")


if __name__ == "__main__":
    main()
