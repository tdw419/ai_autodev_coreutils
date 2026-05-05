#!/usr/bin/env python3
"""Append-only event log for the Geometry OS autodev loop.

Every claim, commit, revert, block, escalation, test gate, and auto-replenish
gets a JSONL line. Fed by both oracle_preflight.py and geo_reviewer_preflight.py.

Location: ~/.cache/geo-events/events.jsonl

Query examples:
  grep '"type":"revert"' events.jsonl | python3 -m json.tool
  python3 -c "
    import json, sys
    [print(json.loads(l)['phase_id'], json.loads(l)['ts'][:16])
     for l in sys.stdin if 'revert' in l]
  " < events.jsonl
"""

import json, os, time
from datetime import datetime, timezone

LOG_DIR = os.path.expanduser("~/.cache/geo-events")
LOG_FILE = os.path.join(LOG_DIR, "events.jsonl")


def _ensure_dir():
    os.makedirs(LOG_DIR, exist_ok=True)


def append(event_type, phase_id=None, worker_id=None, **kwargs):
    """Append one event line. All extra kwargs become fields."""
    _ensure_dir()
    event = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "type": event_type,
        "phase_id": phase_id,
        "worker_id": worker_id,
    }
    # Drop None values, merge extras
    event.update({k: v for k, v in kwargs.items() if v is not None})
    event["phase_id"] = phase_id  # keep even if None for consistent fields
    event["worker_id"] = worker_id

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(event, separators=(",", ":")) + "\n")


def query(event_type=None, phase_id=None, since_iso=None, limit=50):
    """Read events back (newest first). Simple filter, no DB needed."""
    if not os.path.exists(LOG_FILE):
        return []
    events = []
    with open(LOG_FILE) as f:
        for line in f:
            try:
                e = json.loads(line.strip())
            except (json.JSONDecodeError, ValueError):
                continue
            if event_type and e.get("type") != event_type:
                continue
            if phase_id and e.get("phase_id") != phase_id:
                continue
            if since_iso and e.get("ts", "") < since_iso:
                continue
            events.append(e)
    return list(reversed(events[-limit:]))


# Convenience helpers
def claim(phase_id, worker_id, reason=""):
    append("claim", phase_id, worker_id, reason=reason)

def stale_steal(phase_id, worker_id, age_seconds):
    append("stale_steal", phase_id, worker_id, age_seconds=age_seconds)

def test_gate(passed, failed, failures=None):
    append("test_gate", worker_id="preflight",
           passed=passed, failed=failed, failures=failures or [])

def test_gate_halt(failed, failing_tests=None):
    append("test_gate_halt", worker_id="preflight",
           failed=failed, failing_tests=failing_tests or [])

def test_gate_timeout(timeout_seconds):
    """Log when cargo test timed out (infrastructure issue, not code failure)."""
    append("test_gate_timeout", worker_id="preflight",
           timeout_seconds=timeout_seconds)

def wip_self_commit(files_changed=0):
    """Log when the drafter commits uncommitted WIP (reviewer AWOL recovery)."""
    append("wip_self_commit", worker_id="drafter",
           files_changed=files_changed)

def block(phase_id, reason, block_count):
    append("block", phase_id, worker_id="reviewer",
           reason=reason, block_count=block_count)

def escalate(phase_id, reason, block_count):
    append("escalate", phase_id, worker_id="reviewer",
           reason=reason, block_count=block_count)

def phase_done(phase_id, title=""):
    append("phase_done", phase_id, title=title)

def auto_replenish(new_phases):
    append("auto_replenish", new_phases=new_phases)

def roadmap_empty():
    append("roadmap_empty")

def commit(phase_id=None, message=""):
    append("commit", phase_id, message=message)

def revert(phase_id, reason, scope):
    append("revert", phase_id, worker_id="reviewer",
           reason=reason, scope=scope)
