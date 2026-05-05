#!/usr/bin/env python3
"""
Geometry OS Autodev Watchdog

Runs every 15 minutes. Reads event log, git log, and cron job statuses
to determine overall loop health. Writes verdict to ~/.cache/geo-status.txt
and outputs structured data for the cron agent to act on.

Health levels:
  HEALTHY    - Workers firing, commits landing, no stalls
  DEGRADED   - One worker slow/missed, but loop still moving
  STALLED    - No commits or no worker activity for >2x interval

Checks:
  1. Git commit freshness (no commits = dead drafter or dead reviewer)
  2. Event log freshness (no events = preflight scripts not running)
  3. Test gate health (ratio of halts to passes in last 4 hours)
  4. Worker-specific: drafter (10m), reviewer (15m), auditor (60m)
"""

import os, sys, json, re, time, subprocess
from datetime import datetime, timezone, timedelta

PROJECT = os.path.expanduser("~/zion/projects/geometry_os/geometry_os")
STATUS_FILE = os.path.expanduser("~/.cache/geo-status.txt")
EVENT_LOG = os.path.expanduser("~/.cache/geo-events/events.jsonl")
BLOCKED_FILE = os.path.join(PROJECT, "BLOCKED.md")

# Worker intervals (minutes) -- 2x these are the stall thresholds
WORKERS = {
    "drafter": {"interval_m": 10, "cron_name": "autodev-coreutils-roadmap"},
    "reviewer": {"interval_m": 15, "cron_name": "geo-reviewer-shipper"},
    "auditor": {"interval_m": 60, "cron_name": "Geometry OS Roadmap Audit"},
}

# How stale before we alert (multiples of interval)
STALL_MULTIPLIER = 2.5


def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] WATCHDOG: {msg}", file=sys.stderr)


def now_utc():
    return datetime.now(timezone.utc)


def parse_iso(s):
    """Parse ISO timestamp, forgiving."""
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except:
        return None


def minutes_ago(dt):
    """Minutes between a datetime and now."""
    if dt is None:
        return 9999
    return (now_utc() - dt).total_seconds() / 60


def load_events(limit=200):
    """Load last N events from the JSONL log."""
    if not os.path.exists(EVENT_LOG):
        return []
    events = []
    try:
        with open(EVENT_LOG) as f:
            lines = f.readlines()
        for line in lines[-limit:]:
            try:
                events.append(json.loads(line.strip()))
            except:
                continue
    except:
        pass
    return events


def check_git_commits():
    """Check how recently the last commit was made."""
    try:
        r = subprocess.run(
            ["git", "log", "-1", "--format=%ct"],
            capture_output=True, text=True, timeout=10,
            cwd=PROJECT,
        )
        if r.returncode == 0 and r.stdout.strip():
            ts = int(r.stdout.strip())
            dt = datetime.fromtimestamp(ts, tz=timezone.utc)
            return dt, minutes_ago(dt)
    except:
        pass
    return None, 9999


def count_recent_commits(window_minutes=60):
    """Count commits in the last N minutes."""
    try:
        since = (now_utc() - timedelta(minutes=window_minutes)).strftime("%Y-%m-%dT%H:%M:%S")
        r = subprocess.run(
            ["git", "log", f"--since={since}", "--oneline"],
            capture_output=True, text=True, timeout=10,
            cwd=PROJECT,
        )
        if r.returncode == 0:
            return len([l for l in r.stdout.strip().split("\n") if l.strip()])
    except:
        pass
    return 0


def check_event_log_freshness(events):
    """How long since the last event?"""
    if not events:
        return None, 9999
    last = events[-1]
    dt = parse_iso(last.get("ts", ""))
    return dt, minutes_ago(dt)


def check_test_gate_health(events, window_minutes=240):
    """Check test gate pass/halt ratio in the last N hours."""
    cutoff = now_utc() - timedelta(minutes=window_minutes)
    passes = halts = timeouts = 0
    for e in events:
        dt = parse_iso(e.get("ts", ""))
        if dt is None or dt < cutoff:
            continue
        t = e.get("type", "")
        if t == "test_gate":
            passes += 1
        elif t == "test_gate_halt":
            halts += 1
        elif t == "test_gate_timeout":
            timeouts += 1
    total = passes + halts
    ratio = passes / total if total > 0 else 1.0
    return {"passes": passes, "halts": halts, "timeouts": timeouts,
            "total": total, "pass_ratio": round(ratio, 3)}


def check_worker_last_run(worker_name, events):
    """Find the last activity timestamp for a worker.

    Drafter: uses event log (claim, test_gate, etc.)
    Reviewer: uses git log (commits mentioning WIP/chore/phase tick)
    Auditor: uses event log + git log fallback

    Returns (datetime, age_minutes).
    """
    # Drafter emits lots of events -- use those
    if worker_name == "drafter":
        patterns = ["claim", "stale_steal", "test_gate", "test_gate_halt",
                    "test_gate_timeout", "auto_replenish", "wip_self_commit"]
        for e in reversed(events):
            if e.get("type") in patterns:
                dt = parse_iso(e.get("ts", ""))
                if dt:
                    return dt, minutes_ago(dt)
        return None, 9999

    # Reviewer doesn't always emit events (only on revert/block).
    # Use git log for reviewer-like commit patterns.
    if worker_name == "reviewer":
        try:
            r = subprocess.run(
                ["git", "log", "-1", "--format=%ct", "--grep=WIP"],
                capture_output=True, text=True, timeout=10,
                cwd=PROJECT,
            )
            if r.returncode == 0 and r.stdout.strip():
                ts = int(r.stdout.strip())
                dt = datetime.fromtimestamp(ts, tz=timezone.utc)
                return dt, minutes_ago(dt)
        except:
            pass
        # Fallback: check event log for reviewer events
        for e in reversed(events):
            if e.get("type") in ("revert", "block", "escalate", "commit"):
                dt = parse_iso(e.get("ts", ""))
                if dt:
                    return dt, minutes_ago(dt)
        return None, 9999

    # Auditor: use event log (if it ever emits), else git log for audit commits
    if worker_name == "auditor":
        # Auditor doesn't reliably emit events -- skip strict check
        return None, None  # None age = "not checked"

    return None, 9999


def check_blocked_phases():
    """Count non-expired blocked phases."""
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
                if len(parts) >= 3:
                    try:
                        ts = float(parts[2])
                        if now - ts < 3600:
                            count += 1
                    except:
                        pass
        return count
    except:
        return 0


def check_roadmap_health():
    """Check roadmap for planned phases and stale in_progress."""
    import yaml
    path = os.path.join(PROJECT, "roadmap_v2.yaml")
    if not os.path.exists(path):
        return {"error": "roadmap missing"}
    try:
        with open(path) as f:
            data = yaml.safe_load(f)
        phases = data.get("phases", [])
        planned = sum(1 for p in phases if p.get("status") == "planned")
        done = sum(1 for p in phases if p.get("status") in ("done", "complete"))
        in_progress = sum(1 for p in phases if p.get("status") == "in_progress")
        total = len(phases)

        # Check for stale in_progress
        now = time.time()
        stale = []
        for p in phases:
            if p.get("status") == "in_progress":
                claimed_at = p.get("_claimed_at", 0)
                if now - claimed_at > 1800:
                    stale.append(p.get("id", "?"))

        return {
            "total": total, "planned": planned, "done": done,
            "in_progress": in_progress, "stale": stale,
            "completion_pct": round(done / total * 100, 1) if total else 0,
        }
    except Exception as e:
        return {"error": str(e)}


def compute_health(checks):
    """Determine overall health level from individual checks."""
    issues = []

    # Check 1: Git commit freshness
    last_commit_age = checks["git"]["last_commit_age_min"]
    commits_per_hour = checks["git"]["commits_last_hour"]
    drafter_interval = WORKERS["drafter"]["interval_m"]

    if last_commit_age > drafter_interval * STALL_MULTIPLIER * 6:
        # No commits in ~2.5 hours -- definitely stalled
        issues.append(f"CRITICAL: No commits in {int(last_commit_age)}m")
    elif last_commit_age > drafter_interval * STALL_MULTIPLIER * 3:
        # No commits in ~75m -- degraded
        issues.append(f"WARN: No commits in {int(last_commit_age)}m")

    # Check 2: Event log freshness
    event_age = checks["events"]["last_event_age_min"]
    if event_age > 60:
        issues.append(f"CRITICAL: Event log stale ({int(event_age)}m old)")
    elif event_age > 30:
        issues.append(f"WARN: Event log quiet ({int(event_age)}m old)")

    # Check 3: Test gate health
    tg = checks["test_gate"]
    if tg["total"] > 0 and tg["pass_ratio"] < 0.3:
        issues.append(f"WARN: Test gate failing {100 - int(tg['pass_ratio']*100)}% of time "
                      f"({tg['halts']} halts, {tg['passes']} passes in last 4h)")
    if tg["timeouts"] > 3:
        issues.append(f"WARN: {tg['timeouts']} test timeouts in last 4h (infrastructure issue)")

    # Check 4: Worker-specific freshness
    for wname, winfo in WORKERS.items():
        age = checks["workers"].get(wname, {}).get("last_activity_age_min", 9999)
        if age is None:
            continue  # Worker not checked (e.g. auditor with no events)
        threshold = winfo["interval_m"] * STALL_MULTIPLIER
        if age > threshold:
            issues.append(f"CRITICAL: {wname} no activity in {int(age)}m "
                          f"(expected every {winfo['interval_m']}m)")
        elif age > threshold * 0.6:
            issues.append(f"WARN: {wname} slow ({int(age)}m since last activity)")

    # Check 5: Roadmap
    rm = checks["roadmap"]
    if "error" not in rm and rm.get("stale"):
        for sid in rm["stale"]:
            issues.append(f"WARN: Stale in_progress phase {sid}")

    # Check 6: Blocked phases
    blocked = checks.get("blocked", 0)
    if blocked > 0:
        issues.append(f"INFO: {blocked} phases currently blocked")

    # Determine health level
    critical = any("CRITICAL" in i for i in issues)
    warn = any("WARN" in i for i in issues)

    if critical:
        level = "STALLED"
    elif warn:
        level = "DEGRADED"
    else:
        level = "HEALTHY"

    return level, issues


def write_status_file(level, issues, checks):
    """Write human-readable status to ~/.cache/geo-status.txt."""
    lines = []
    lines.append(f"Geometry OS Autodev Loop Status")
    lines.append(f"{'='*50}")
    lines.append(f"Health:  {level}")
    lines.append(f"Time:    {now_utc().strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"")
    lines.append(f"Git:")
    lines.append(f"  Last commit:    {int(checks['git']['last_commit_age_min'])}m ago")
    lines.append(f"  Commits/hour:   {checks['git']['commits_last_hour']}")
    lines.append(f"")
    lines.append(f"Event Log:")
    lines.append(f"  Last event:     {int(checks['events']['last_event_age_min'])}m ago")
    lines.append(f"  Total events:   {checks['events']['total_count']}")
    lines.append(f"")
    tg = checks["test_gate"]
    lines.append(f"Test Gate (last 4h):")
    lines.append(f"  Pass: {tg['passes']}  Halt: {tg['halts']}  Timeout: {tg['timeouts']}")
    lines.append(f"  Pass rate: {int(tg['pass_ratio']*100)}%")
    lines.append(f"")

    for wname in WORKERS:
        age = checks["workers"].get(wname, {}).get("last_activity_age_min", 9999)
        interval = WORKERS[wname]["interval_m"]
        if age is None:
            lines.append(f"  {wname:10s} (not monitored)")
            continue
        status_icon = "OK" if age < interval * STALL_MULTIPLIER else "STALE"
        lines.append(f"  {wname:10s} last activity {int(age):3d}m ago  [{status_icon}]")

    rm = checks["roadmap"]
    if "error" not in rm:
        lines.append(f"")
        lines.append(f"Roadmap:")
        lines.append(f"  {rm['done']}/{rm['total']} done ({rm['completion_pct']}%)")
        lines.append(f"  {rm['planned']} planned, {rm['in_progress']} in progress")

    if issues:
        lines.append(f"")
        lines.append(f"Issues:")
        for i in issues:
            lines.append(f"  {i}")
    else:
        lines.append(f"")
        lines.append(f"All systems nominal.")

    os.makedirs(os.path.dirname(STATUS_FILE), exist_ok=True)
    with open(STATUS_FILE, "w") as f:
        f.write("\n".join(lines) + "\n")


def main():
    log("Running health checks...")

    events = load_events(300)

    # Gather all checks
    last_commit_dt, last_commit_age = check_git_commits()
    commits_last_hour = count_recent_commits(60)

    last_event_dt, last_event_age = check_event_log_freshness(events)

    test_gate = check_test_gate_health(events, window_minutes=240)

    workers = {}
    for wname in WORKERS:
        last_dt, age = check_worker_last_run(wname, events)
        workers[wname] = {"last_activity": last_dt, "last_activity_age_min": age}

    roadmap = check_roadmap_health()
    blocked = check_blocked_phases()

    checks = {
        "git": {
            "last_commit": last_commit_dt,
            "last_commit_age_min": last_commit_age,
            "commits_last_hour": commits_last_hour,
        },
        "events": {
            "last_event": last_event_dt,
            "last_event_age_min": last_event_age,
            "total_count": len(events),
        },
        "test_gate": test_gate,
        "workers": workers,
        "roadmap": roadmap,
        "blocked": blocked,
    }

    level, issues = compute_health(checks)

    # Write status file
    write_status_file(level, issues, checks)

    # Output structured data for cron agent
    print(f"HEALTH: {level}")
    print(f"LAST_COMMIT_AGE: {int(last_commit_age)} minutes")
    print(f"COMMITS_PER_HOUR: {commits_last_hour}")
    print(f"LAST_EVENT_AGE: {int(last_event_age)} minutes")
    print(f"TEST_GATE_PASS_RATE: {int(test_gate['pass_ratio']*100)}%")
    print(f"TEST_GATE_STATS: {test_gate['passes']} pass, {test_gate['halts']} halt, {test_gate['timeouts']} timeout")

    for wname in WORKERS:
        age = workers[wname]["last_activity_age_min"]
        interval = WORKERS[wname]["interval_m"]
        if age is None:
            print(f"WORKER_{wname.upper()}: NOT_MONITORED")
            continue
        ok = age < interval * STALL_MULTIPLIER
        print(f"WORKER_{wname.upper()}: {'OK' if ok else 'STALE'} ({int(age)}m)")

    if "error" not in roadmap:
        print(f"ROADMAP: {roadmap['done']}/{roadmap['total']} ({roadmap['completion_pct']}%)")

    if issues:
        for i in issues:
            print(f"ISSUE: {i}")

    if level == "STALLED":
        print("ACTION_REQUIRED: Loop is stalled. Investigate immediately.")
    elif level == "DEGRADED":
        print("ACTION_SUGGESTED: Loop is degraded. Monitor closely.")

    log(f"Health: {level} ({len(issues)} issues)")


if __name__ == "__main__":
    main()
