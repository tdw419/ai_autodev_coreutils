#!/usr/bin/env python3
"""
Orchestrator History CLI - query past pipeline runs and loop iterations.

Usage:
    python3 orch_history.py list [--last N] [--status STATUS] [--json]
    python3 orch_history.py show RUN_ID [--json]
    python3 orch_history.py failed [--json]
    python3 orch_history.py stats [--json]
    python3 orch_history.py loops [--date YYYY-MM-DD] [--last N] [--json]
    python3 orch_history.py prune [--days N]
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from execution_log import list_runs, get_run, get_stats, get_loop_history, prune_old_runs


def cmd_list(args):
    """List recent pipeline runs."""
    runs = list_runs(limit=args.last, status=args.status)
    if args.json:
        json.dump(runs, sys.stdout, indent=2)
        print()
        return

    if not runs:
        print("No runs found.")
        return

    # Print a formatted table
    print(f"{'RUN ID':<28} {'PIPELINE':<25} {'STATUS':<10} {'NODES':>8} {'DURATION':>10}")
    print("-" * 83)
    for r in runs:
        nodes = f"{r['completed_nodes']}/{r['total_nodes']}"
        if r["failed_nodes"]:
            nodes += f" ({r['failed_nodes']} failed)"
        dur = f"{r['duration_seconds']:.1f}s"
        print(f"{r['run_id']:<28} {r['pipeline_name'][:24]:<25} {r['status']:<10} {nodes:>8} {dur:>10}")


def cmd_show(args):
    """Show details of a specific run."""
    data = get_run(args.run_id)
    if data is None:
        print(f"Run not found: {args.run_id}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        json.dump(data, sys.stdout, indent=2)
        print()
        return

    print(f"Run: {data.get('_run_id', 'unknown')}")
    print(f"Pipeline: {data.get('pipeline_name', 'unknown')}")
    print(f"Status: {data.get('status', 'unknown')}")
    print(f"Duration: {data.get('duration_seconds', 0):.2f}s")
    print(f"Nodes: {data.get('completed_nodes', 0)}/{data.get('total_nodes', 0)} completed, "
          f"{data.get('failed_nodes', 0)} failed, {data.get('skipped_nodes', 0)} skipped")
    print(f"Logged at: {data.get('_logged_at', 'unknown')}")
    print()

    results = data.get("results", [])
    if results:
        print("Node Results:")
        print(f"  {'NODE':<25} {'TYPE':<12} {'STATUS':<10} {'DURATION':>10}")
        print("  " + "-" * 59)
        for r in results:
            dur = f"{r.get('duration_seconds', 0):.2f}s"
            print(f"  {r['node_id']:<25} {r['node_type']:<12} {r['status']:<10} {dur:>10}")
            if r.get("error"):
                print(f"    Error: {r['error'][:100]}")
            if r.get("output") and r["status"] == "failed":
                print(f"    Output: {r['output'][:200]}")


def cmd_failed(args):
    """Show only failed runs."""
    runs = list_runs(limit=args.last or 50, status="failed")
    if args.json:
        json.dump(runs, sys.stdout, indent=2)
        print()
        return

    if not runs:
        print("No failed runs found.")
        return

    print(f"Failed runs ({len(runs)}):")
    print(f"{'RUN ID':<28} {'PIPELINE':<25} {'NODES':>8} {'DURATION':>10}")
    print("-" * 73)
    for r in runs:
        nodes = f"{r['completed_nodes']}/{r['total_nodes']}"
        dur = f"{r['duration_seconds']:.1f}s"
        print(f"{r['run_id']:<28} {r['pipeline_name'][:24]:<25} {nodes:>8} {dur:>10}")


def cmd_stats(args):
    """Show summary statistics."""
    stats = get_stats()
    if args.json:
        json.dump(stats, sys.stdout, indent=2)
        print()
        return

    print(f"Total runs: {stats['total_runs']}")
    by_status = stats.get("by_status", {})
    print(f"  Completed: {by_status.get('completed', 0)}")
    print(f"  Failed:    {by_status.get('failed', 0)}")
    print(f"  Partial:   {by_status.get('partial', 0)}")
    print(f"Total duration: {stats.get('total_duration_seconds', 0):.1f}s")
    print(f"Avg duration:   {stats.get('avg_duration_seconds', 0):.2f}s")
    print(f"Total nodes executed: {stats.get('total_nodes_executed', 0)}")


def cmd_loops(args):
    """Show orchestrator loop iteration history."""
    entries = get_loop_history(date=args.date, limit=args.last or 50)
    if args.json:
        json.dump(entries, sys.stdout, indent=2)
        print()
        return

    if not entries:
        print("No loop entries found.")
        return

    print(f"Loop iterations ({len(entries)}):")
    print(f"{'TIMESTAMP':<24} {'REPO':<20} {'POLLED':>7} {'SPAWNED':>8} {'ACTIVE':>7}")
    print("-" * 68)
    for e in entries:
        ts = e.get("timestamp", "")[:19]
        repo = e.get("repo", "")[:19]
        polled = e.get("polled", 0)
        spawned = len(e.get("spawned", []))
        active = e.get("active_workers", 0)
        print(f"{ts:<24} {repo:<20} {polled:>7} {spawned:>8} {active:>7}")
        if e.get("skipped_full"):
            print(f"  (skipped: all slots occupied)")


def cmd_prune(args):
    """Remove old log files."""
    removed = prune_old_runs(keep_days=args.days)
    print(f"Removed {removed} log files older than {args.days} days.")


def main():
    parser = argparse.ArgumentParser(
        description="Query orchestrator execution history",
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # list
    list_p = subparsers.add_parser("list", help="List recent runs")
    list_p.add_argument("--last", "-n", type=int, default=20, help="Number of runs to show")
    list_p.add_argument("--status", "-s", choices=["completed", "failed", "partial"], help="Filter by status")
    list_p.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    # show
    show_p = subparsers.add_parser("show", help="Show run details")
    show_p.add_argument("run_id", help="Run ID to show")
    show_p.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    # failed
    failed_p = subparsers.add_parser("failed", help="Show failed runs")
    failed_p.add_argument("--last", "-n", type=int, default=50, help="Number of runs to show")
    failed_p.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    # stats
    stats_p = subparsers.add_parser("stats", help="Show summary statistics")
    stats_p.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    # loops
    loops_p = subparsers.add_parser("loops", help="Show loop iteration history")
    loops_p.add_argument("--date", "-d", help="Date (YYYY-MM-DD), default: today")
    loops_p.add_argument("--last", "-n", type=int, default=50, help="Number of entries")
    loops_p.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    # prune
    prune_p = subparsers.add_parser("prune", help="Remove old log files")
    prune_p.add_argument("--days", type=int, default=30, help="Keep files from last N days")

    args = parser.parse_args()

    if args.command == "list":
        cmd_list(args)
    elif args.command == "show":
        cmd_show(args)
    elif args.command == "failed":
        cmd_failed(args)
    elif args.command == "stats":
        cmd_stats(args)
    elif args.command == "loops":
        cmd_loops(args)
    elif args.command == "prune":
        cmd_prune(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
