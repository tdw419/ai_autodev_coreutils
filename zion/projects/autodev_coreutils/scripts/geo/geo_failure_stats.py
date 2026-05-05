#!/usr/bin/env python3
"""
Analyzes events.jsonl to find common failure patterns.
Used by the Oracle to prioritize fixes or infra improvements.
"""
import json, os, sys
from collections import Counter
from datetime import datetime, timedelta

LOG_DIR = os.path.expanduser("~/.cache/geo-events")
LOG_FILE = os.path.join(LOG_DIR, "events.jsonl")

def main():
    if not os.path.exists(LOG_FILE):
        print("No log file found.")
        return

    failures = []
    timeouts = 0
    total_runs = 0
    
    cutoff = datetime.now() - timedelta(days=7)

    with open(LOG_FILE, "r") as f:
        for line in f:
            try:
                e = json.loads(line)
                ts = datetime.fromisoformat(e["ts"].replace("Z", "+00:00")).replace(tzinfo=None)
                if ts < cutoff:
                    continue
                
                etype = e.get("type")
                if etype in ["test_gate", "test_gate_halt"]:
                    total_runs += 1
                
                if etype == "test_gate_halt":
                    for t in e.get("failing_tests", []):
                        failures.append(t)
                elif etype == "test_gate_timeout":
                    timeouts += 1
            except Exception:
                continue

    counts = Counter(failures)
    
    print("### Failure Pattern Report (Last 7 Days) ###")
    print(f"Total Test Runs: {total_runs}")
    print(f"Total Timeouts:  {timeouts}")
    print("\nTop Failing Tests:")
    for test, count in counts.most_common(10):
        print(f"  - {test}: {count} times")
    
    if timeouts > total_runs * 0.1 and total_runs > 10:
        print("\nINFRASTRUCTURE ALERT: High timeout rate (>10%). Check test runner resources.")

if __name__ == "__main__":
    main()
