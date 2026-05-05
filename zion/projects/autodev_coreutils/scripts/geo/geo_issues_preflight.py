#!/usr/bin/env python3
"""
Geometry OS GitHub Issues Worker Preflight

Replaces the roadmap-based oracle with GitHub Issues as the task source.
The roadmap is 100% complete (113/113 phases). The real backlog is the
42+ open GitHub issues in tdw419/geometry-os.

Priority order:
1. CRITICAL issues (build breakage)
2. HIGH priority issues
3. MEDIUM priority issues (sorted by issue number = age, oldest first)
4. LOW priority issues

Uses simple file-based locking: /tmp/geo-issues-worker.lock
Claimed issues tracked in /tmp/geo-issues-claimed.json
"""

import os, sys, json, time, subprocess, hashlib

PROJECT = os.path.expanduser("~/zion/projects/geometry_os/geometry_os")
REPO = "tdw419/geometry-os"
LOCK_FILE = "/tmp/geo-issues-worker.lock"
CLAIMED_FILE = "/tmp/geo-issues-claimed.json"
CLAIM_TIMEOUT = 3600  # 1 hour -- release stale claims
WORKER_ID = os.environ.get("GEO_WORKER_ID", os.environ.get("HOSTNAME", f"worker-{os.getpid()}"))

def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] GITHUB-PREFLIGHT [{WORKER_ID}]: {msg}", file=sys.stderr)

def check_lock():
    if os.path.exists(LOCK_FILE):
        try:
            pid = int(open(LOCK_FILE).read().strip())
            os.kill(pid, 0)
            age = time.time() - os.path.getmtime(LOCK_FILE)
            if age < 600:  # 10 min active lock
                return False
        except (ProcessLookupError, ValueError, FileNotFoundError):
            pass
        try: os.unlink(LOCK_FILE)
        except: pass
    return True

def create_lock():
    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))

def release_lock():
    try: os.unlink(LOCK_FILE)
    except: pass

def load_claims():
    if os.path.exists(CLAIMED_FILE):
        try:
            return json.load(open(CLAIMED_FILE))
        except: pass
    return {}

def save_claims(claims):
    with open(CLAIMED_FILE, "w") as f:
        json.dump(claims, f, indent=2)

def get_open_issues():
    """Fetch open issues from GitHub, sorted by priority then age."""
    try:
        result = subprocess.run(
            ["gh", "issue", "list", "--repo", REPO, "--state", "open",
             "--limit", "60", "--json", "number,title,labels"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            log(f"gh issue list failed: {result.stderr[:200]}")
            return []
        issues = json.loads(result.stdout)
    except Exception as e:
        log(f"Failed to fetch issues: {e}")
        return []

    # Parse priority from labels
    priority_map = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    for issue in issues:
        issue["priority"] = 2  # default medium
        for label in issue.get("labels", []):
            name = label.get("name", "")
            if "priority:" in name:
                p = name.split(":")[-1].strip()
                issue["priority"] = priority_map.get(p, 2)

    # Sort: priority ASC, then issue number ASC (oldest first)
    issues.sort(key=lambda i: (i["priority"], i["number"]))
    return issues

def claim_issue(issues, claims):
    """Find and claim the highest-priority unclaimed issue."""
    now = time.time()

    # Clean stale claims
    stale = [k for k, v in claims.items() if now - v.get("claimed_at", 0) > CLAIM_TIMEOUT]
    for k in stale:
        log(f"Releasing stale claim on #{k}")
        del claims[k]

    # Find first unclaimed issue
    for issue in issues:
        num = str(issue["number"])
        if num not in claims:
            claims[num] = {
                "worker": WORKER_ID,
                "claimed_at": now,
                "title": issue["title"]
            }
            save_claims(claims)
            return issue

    return None

def get_issue_body(number):
    """Fetch the full issue body for implementation context."""
    try:
        result = subprocess.run(
            ["gh", "issue", "view", str(number), "--repo", REPO, "--json", "body"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get("body", "")
    except:
        pass
    return ""

def run_carry_forward():
    """Run carry-forward gate check."""
    carry = os.path.expanduser("~/zion/projects/carry_forward/carry_forward/carry_forward.py")
    if not os.path.exists(carry):
        return 0, ""
    try:
        result = subprocess.run(
            ["python3", carry, "run", "--json"],
            capture_output=True, text=True, timeout=30,
            cwd=PROJECT
        )
        return result.returncode, result.stdout
    except Exception as e:
        log(f"Carry forward error: {e}")
        return 1, str(e)

def main():
    log("Starting preflight check")

    # Check lock
    if not check_lock():
        print("STATUS: LOCKED")
        log("Another worker is running")
        return

    # Run carry-forward gate
    cf_rc, cf_out = run_carry_forward()
    if cf_rc != 0 and "Session dead" not in cf_out:
        print(f"STATUS: HALT\nREASON: carry_forward gate blocked: {cf_out[:200]}")
        log(f"Halted by carry_forward: {cf_out[:100]}")
        return

    # Fetch GitHub issues
    issues = get_open_issues()
    if not issues:
        print("STATUS: ROADMAP_EMPTY\nROADMAP_EMPTY: true\nTASK: No open GitHub issues. All done!")
        log("No open issues found")
        return

    # Load claims
    claims = load_claims()

    # Try to claim an issue
    issue = claim_issue(issues, claims)
    if not issue:
        print("STATUS: LOCKED\nREASON: All issues claimed by other workers")
        log("All issues already claimed")
        return

    # Got an issue -- create lock and output task
    create_lock()
    num = issue["number"]
    title = issue["title"]
    priority = issue["priority"]
    pri_names = {0: "CRITICAL", 1: "HIGH", 2: "MEDIUM", 3: "LOW"}

    log(f"Claimed #{num}: {title}")

    # Fetch issue body for context
    body = get_issue_body(num)
    body_preview = body[:500] if body else "(no description)"

    print(f"STATUS: CONTINUE")
    print(f"ISSUE: #{num}")
    print(f"PRIORITY: {pri_names.get(priority, 'MEDIUM')}")
    print(f"TITLE: {title}")
    print(f"REPO: {REPO}")
    print(f"PROJECT_DIR: {PROJECT}")
    print(f"LOCK_FILE: {LOCK_FILE}")
    print(f"CLAIMED_FILE: {CLAIMED_FILE}")
    print(f"---ISSUE BODY---")
    print(body_preview)
    print(f"---END BODY---")

    # Carry-forward context
    if cf_rc == 0 and cf_out.strip():
        print("---CARRY_FORWARD_CONTEXT---")
        print(cf_out.strip()[:2000])
        print("---END_CONTEXT---")

if __name__ == "__main__":
    main()
