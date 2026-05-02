#!/usr/bin/env python3
"""
Agent-Readable Trace Formatter for the Hermes Agent Orchestrator.

Converts pipeline execution logs into compact, agent-optimized summaries
that can be injected into AI node prompts for self-debugging.

The core idea: instead of "a human reviews the log," the agent reviews its
own trace and self-corrects. This requires traces that are compact enough
to fit in a prompt context window while retaining the key debugging info.

Usage:
    python3 trace_formatter.py --run RUN_ID
    python3 trace_formatter.py --run RUN_ID --format compact
    python3 trace_formatter.py --run RUN_ID --format detailed
    python3 trace_formatter.py --run RUN_ID --format diff
    python3 trace_formatter.py --correlate --last 20
    python3 trace_formatter.py --last 5

Based on Harness Engineering "Application Legibility":
agents should have local access to logs, metrics, and traces.
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent))
from execution_log import RUNS_DIR, get_run, list_runs


# ─── Token estimation (rough: ~4 chars per token) ────────────────────────────

def _estimate_tokens(text: str) -> int:
    """Rough token estimate: ~4 characters per token."""
    return len(text) // 4


# ─── Compact formatter (for prompt injection, target <2000 tokens) ───────────

def format_compact(run_data: dict) -> str:
    """
    Format a pipeline run as a compact summary for prompt injection.

    Targets <2000 tokens. Shows: pipeline name, status, failure chain,
    node summaries (status + duration + error if any).
    """
    lines = []
    lines.append(f"## Pipeline Run: {run_data.get('pipeline_name', 'unknown')}")
    lines.append(f"Status: {run_data.get('status', 'unknown')}")
    lines.append(f"Duration: {run_data.get('duration_seconds', 0)}s")
    lines.append(f"Nodes: {run_data.get('completed_nodes', 0)}/{run_data.get('total_nodes', 0)} completed, {run_data.get('failed_nodes', 0)} failed")

    results = run_data.get("results", [])
    if not results:
        lines.append("(no node results recorded)")
        return "\n".join(lines)

    lines.append("")
    lines.append("### Node Results")

    for r in results:
        status_icon = {"completed": "✅", "failed": "❌", "skipped": "⏭️"}.get(r.get("status", ""), "❓")
        duration = r.get("duration_seconds", 0)
        node_line = f"{status_icon} {r.get('node_id', '?')} ({r.get('node_type', '?')}) [{duration:.1f}s]"

        if r.get("status") == "failed" and r.get("error"):
            # Truncate long errors to keep compact
            error = r["error"]
            if len(error) > 200:
                error = error[:200] + "..."
            node_line += f"\n   Error: {error}"

        lines.append(node_line)

    # Failure chain analysis
    failed = [r for r in results if r.get("status") == "failed"]
    if failed:
        lines.append("")
        lines.append("### Failure Chain")
        for i, r in enumerate(failed):
            lines.append(f"{i + 1}. {r.get('node_id', '?')} failed: {r.get('error', 'unknown error')[:150]}")

        # Identify which node to focus on (the first failure in the chain)
        lines.append("")
        lines.append(f"Root cause likely at: {failed[0].get('node_id', '?')}")

    result = "\n".join(lines)

    # If too long, trim
    tokens = _estimate_tokens(result)
    if tokens > 2000:
        # Remove detailed error messages, keep only failure chain
        lines = lines[:lines.index("### Node Results") + 1]
        lines.append("(summary truncated for context budget)")
        for r in results:
            status_icon = {"completed": "✅", "failed": "❌", "skipped": "⏭️"}.get(r.get("status", ""), "❓")
            lines.append(f"{status_icon} {r.get('node_id', '?')} - {r.get('status', '?')}")
        if failed:
            lines.append(f"Root cause: {failed[0].get('node_id', '?')}: {failed[0].get('error', '?')[:100]}")
        result = "\n".join(lines)

    return result


# ─── Detailed formatter (for human debugging) ───────────────────────────────

def format_detailed(run_data: dict) -> str:
    """
    Format a pipeline run with full details for human debugging.

    Shows all node results with full output and error messages.
    """
    lines = []
    lines.append(f"Pipeline: {run_data.get('pipeline_name', 'unknown')}")
    lines.append(f"Run ID: {run_data.get('_run_id', 'unknown')}")
    lines.append(f"Status: {run_data.get('status', 'unknown')}")
    lines.append(f"Duration: {run_data.get('duration_seconds', 0)}s")
    lines.append(f"Logged: {run_data.get('_logged_at', 'unknown')}")
    lines.append(f"Total nodes: {run_data.get('total_nodes', 0)}")
    lines.append(f"Completed: {run_data.get('completed_nodes', 0)}")
    lines.append(f"Failed: {run_data.get('failed_nodes', 0)}")
    lines.append(f"Skipped: {run_data.get('skipped_nodes', 0)}")
    lines.append("")

    results = run_data.get("results", [])
    for r in results:
        lines.append(f"{'─' * 60}")
        lines.append(f"Node: {r.get('node_id', '?')}")
        lines.append(f"Type: {r.get('node_type', '?')}")
        lines.append(f"Status: {r.get('status', '?')}")
        lines.append(f"Duration: {r.get('duration_seconds', 0):.2f}s")
        lines.append(f"Exit Code: {r.get('exit_code', 0)}")
        lines.append(f"Iterations: {r.get('iterations', 1)}")

        if r.get("output"):
            lines.append(f"Output:\n{r['output']}")

        if r.get("error"):
            lines.append(f"Error:\n{r['error']}")

        lines.append("")

    lines.append(f"{'─' * 60}")
    return "\n".join(lines)


# ─── Diff-focused formatter (shows what changed at each node) ────────────────

def format_diff(run_data: dict) -> str:
    """
    Format a pipeline run focused on file changes at each node.

    Parses node outputs for git diff markers and file references.
    Useful for understanding what the pipeline actually did.
    """
    lines = []
    lines.append(f"## Pipeline Run: {run_data.get('pipeline_name', 'unknown')}")
    lines.append(f"Status: {run_data.get('status', 'unknown')}")
    lines.append("")

    results = run_data.get("results", [])
    for r in results:
        node_id = r.get("node_id", "?")
        output = r.get("output", "")

        # Look for file references in the output
        files_changed = set()
        for word in output.split():
            # Match common file patterns
            if any(word.endswith(ext) for ext in [".py", ".js", ".ts", ".yaml", ".yml", ".json", ".md", ".sh"]):
                files_changed.add(word.strip("`,;'\""))

        # Look for git-like patterns
        if "git add" in output or "git commit" in output:
            lines.append(f"📄 {node_id}: git operation detected")
        elif files_changed:
            lines.append(f"📄 {node_id}: {', '.join(sorted(files_changed))}")
        elif r.get("status") == "failed":
            lines.append(f"❌ {node_id}: failed - {r.get('error', 'unknown')[:100]}")
        else:
            lines.append(f"✅ {node_id}: completed (no file references detected)")

    return "\n".join(lines)


# ─── Cross-run failure correlation ───────────────────────────────────────────

def correlate_failures(runs: list[dict], min_occurrences: int = 2) -> str:
    """
    Analyze multiple runs to find recurring failure patterns.

    Args:
        runs: List of run data dicts (full data, not summaries).
        min_occurrences: Minimum times a failure pattern must appear to be reported.

    Returns:
        Formatted analysis string.
    """
    if not runs:
        return "No runs found to analyze."

    total = len(runs)
    completed = sum(1 for r in runs if r.get("status") == "completed")
    failed = sum(1 for r in runs if r.get("status") == "failed")

    lines = []
    lines.append(f"## Failure Correlation Analysis ({total} runs)")
    lines.append(f"Success rate: {completed}/{total} ({100 * completed // total if total else 0}%)")
    lines.append(f"Failure rate: {failed}/{total} ({100 * failed // total if total else 0}%)")
    lines.append("")

    # Group failures by node_id
    node_failures = defaultdict(list)
    error_patterns = defaultdict(int)

    for run in runs:
        for r in run.get("results", []):
            if r.get("status") == "failed":
                node_id = r.get("node_id", "unknown")
                node_failures[node_id].append({
                    "run_id": run.get("_run_id", "?"),
                    "pipeline": run.get("pipeline_name", "?"),
                    "error": r.get("error", "unknown"),
                })
                # Extract error type (first word or common pattern)
                error = r.get("error", "")
                if ":" in error:
                    error_type = error.split(":")[0].strip()
                elif "Error" in error:
                    error_type = error.split("Error")[0].strip() + "Error"
                else:
                    error_type = error[:50]
                error_patterns[error_type] += 1

    # Report recurring node failures
    if node_failures:
        lines.append("### Recurring Node Failures")
        for node_id, failures in sorted(node_failures.items(), key=lambda x: -len(x[1])):
            count = len(failures)
            pct = 100 * count // total
            if count >= min_occurrences:
                lines.append(f"  ⚠️  Node '{node_id}': failed in {count}/{total} runs ({pct}%)")
                # Show most common error for this node
                errors = [f["error"][:80] for f in failures]
                most_common = max(set(errors), key=errors.count)
                lines.append(f"      Most common error: {most_common}")
        lines.append("")

    # Report recurring error types
    if error_patterns:
        lines.append("### Common Error Types")
        for error_type, count in sorted(error_patterns.items(), key=lambda x: -x[1]):
            if count >= min_occurrences:
                lines.append(f"  • {error_type}: {count} occurrence(s)")
        lines.append("")

    # Pipeline-level analysis
    pipeline_stats = defaultdict(lambda: defaultdict(int))
    for run in runs:
        name = run.get("pipeline_name", "unknown")
        pipeline_stats[name]["total"] += 1
        status = run.get("status", "unknown")
        pipeline_stats[name][status] += 1

    if len(pipeline_stats) > 1:
        lines.append("### Pipeline Success Rates")
        for name, stats in sorted(pipeline_stats.items()):
            success = stats.get("completed", 0)
            tot = stats["total"]
            pct = 100 * success // tot if tot else 0
            lines.append(f"  {name}: {success}/{tot} ({pct}%)")
        lines.append("")

    # Suggested fixes for common patterns
    lines.append("### Suggestions")
    if not node_failures:
        lines.append("  No recurring failures detected. System is healthy.")
    else:
        worst_node = max(node_failures, key=lambda k: len(node_failures[k]))
        worst_count = len(node_failures[worst_node])
        worst_pct = 100 * worst_count // total
        if worst_pct > 50:
            lines.append(f"  🔴 Node '{worst_node}' fails in >50% of runs. Investigate root cause.")
        elif worst_pct > 25:
            lines.append(f"  🟡 Node '{worst_node}' fails in >25% of runs. May need attention.")
        else:
            lines.append(f"  🟢 No node exceeds 25% failure rate. Failures are sporadic.")

    return "\n".join(lines)


# ─── Debug context builder (for executor integration) ────────────────────────

def build_debug_context(run_data: dict) -> str:
    """
    Build a debug context string for injection into an AI node prompt.

    This is the compact format wrapped with clear markers that the agent
    can parse. Designed for the executor's retry/failure loop.
    """
    if run_data is None:
        return ""

    status = run_data.get("status", "unknown")
    if status == "completed":
        return ""

    compact = format_compact(run_data)
    return f"""<previous_attempt_failed>
{compact}

Instructions: The above shows what went wrong in the previous attempt. Analyze the failure chain and adjust your approach. Focus on the root cause node.
</previous_attempt_failed>"""


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Agent-Readable Trace Formatter")
    parser.add_argument("--run", "-r", help="Run ID to format (filename without .json)")
    parser.add_argument("--last", "-n", type=int, default=None, help="Show last N runs")
    parser.add_argument("--format", "-f", choices=["compact", "detailed", "diff"], default="compact",
                        help="Output format (default: compact)")
    parser.add_argument("--correlate", action="store_true", help="Analyze failure patterns across runs")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Output as JSON")
    parser.add_argument("--debug-context", action="store_true", help="Build debug context for prompt injection")

    args = parser.parse_args()

    if args.correlate:
        # Correlate failures across multiple runs
        limit = args.last or 20
        runs_list = list_runs(limit=limit)
        # Load full data for each run
        full_runs = []
        for r in runs_list:
            full = get_run(r["run_id"])
            if full:
                full_runs.append(full)
        result = correlate_failures(full_runs)
        print(result)
        return

    if args.last and not args.run:
        # Show last N runs summary
        runs_list = list_runs(limit=args.last)
        if not runs_list:
            print("No runs found.")
            return

        for r in runs_list:
            icon = "✅" if r["status"] == "completed" else "❌"
            print(f"{icon} {r['run_id']} | {r['pipeline_name']} | {r['status']} | "
                  f"{r['completed_nodes']}/{r['total_nodes']} nodes | {r['duration_seconds']}s")
        return

    if not args.run:
        parser.error("Either --run, --last, or --correlate is required")

    run_data = get_run(args.run)
    if not run_data:
        print(f"Run '{args.run}' not found.", file=sys.stderr)
        sys.exit(1)

    if args.debug_context:
        result = build_debug_context(run_data)
        if result:
            print(result)
        else:
            print("(no failure context — previous run succeeded)", file=sys.stderr)
        return

    formatters = {
        "compact": format_compact,
        "detailed": format_detailed,
        "diff": format_diff,
    }

    formatter = formatters[args.format]
    result = formatter(run_data)

    if args.json_output:
        # Output as JSON with format metadata
        output = {
            "run_id": run_data.get("_run_id", args.run),
            "format": args.format,
            "estimated_tokens": _estimate_tokens(result),
            "content": result,
        }
        print(json.dumps(output, indent=2))
    else:
        print(result)


if __name__ == "__main__":
    main()
