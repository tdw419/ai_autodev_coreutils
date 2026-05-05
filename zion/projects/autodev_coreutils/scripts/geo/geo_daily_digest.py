#!/usr/bin/env python3
"""
Geometry OS Autodev Daily Digest

Runs once per day. Reads ~/.cache/geo-status.txt and sends a summary
to the configured messaging platform. Closes the Anticipation Gap —
Jericho doesn't have to check the pipeline, the pipeline reports in.
"""

import os, sys, subprocess

STATUS_FILE = os.path.expanduser("~/.cache/geo-status.txt")
STATS_SCRIPT = os.path.expanduser("~/.hermes/scripts/geo_failure_stats.py")

def main():
    if not os.path.exists(STATUS_FILE):
        print("STATUS_FILE_MISSING: ~/.cache/geo-status.txt not found")
        print("TASK: The watchdog hasn't run yet. Nothing to report.")
        return

    with open(STATUS_FILE) as f:
        status = f.read().strip()

    if not status:
        print("STATUS_FILE_EMPTY: No status to report.")
        return

    # Add failure stats to the digest
    stats_out = ""
    if os.path.exists(STATS_SCRIPT):
        try:
            stats_out = subprocess.check_output([STATS_SCRIPT], text=True)
        except Exception as e:
            stats_out = f"Error running stats: {e}"

    # Output the digest for the Hermes cron agent to deliver
    print(f"TELEGRAM_DIGEST:")
    print(status)
    if stats_out:
        print("\n" + "="*40 + "\n")
        print(stats_out)


if __name__ == "__main__":
    main()
