#!/usr/bin/env python3
"""
Continuous Self-Improvement Loop for the Hermes Agent Orchestrator.

Analyzes execution history to identify recurring failure patterns,
auto-tune pipeline parameters, and improve the orchestrator's own harness.

The meta-loop: the system analyzes its own pipeline execution data to
identify which nodes fail most, which pipelines have lowest success rates,
and which parameters need tuning. It generates actionable improvement
suggestions.

Usage:
    python3 self_improve.py --analyze --last 50
    python3 self_improve.py --analyze --period week
    python3 self_improve.py --tune
    python3 self_improve.py --tune --apply
    python3 self_improve.py --report
    python3 self_improve.py --health

Based on the research vision of a "self-correcting codebase" where the
system analyzes its own execution history and improves its harness.
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent))
from execution_log import RUNS_DIR, list_runs, get_run, get_stats


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _load_runs(limit: int = 50, status: str | None = None, period_days: int | None = None) -> list[dict]:
    """Load full run data for analysis."""
    runs = []
    runs_list = list_runs(limit=limit * 2, status=status)  # Over-fetch for filtering

    for r in runs_list:
        full = get_run(r["run_id"])
        if not full:
            continue

        # Filter by period if specified
        if period_days:
            logged_at = full.get("_logged_at", "")
            if logged_at:
                try:
                    run_time = datetime.fromisoformat(logged_at)
                    cutoff = datetime.now() - timedelta(days=period_days)
                    if run_time < cutoff:
                        continue
                except ValueError:
                    pass

        runs.append(full)
        if len(runs) >= limit:
            break

    return runs


def _failure_rate(count: int, total: int) -> float:
    return round(count / total, 3) if total > 0 else 0.0


# ─── Failure Pattern Analyzer ────────────────────────────────────────────────

def analyze_failure_patterns(runs: list[dict]) -> dict:
    """
    Analyze runs to identify recurring failure patterns and bottlenecks.

    Returns a structured report with:
    - Per-node failure rates
    - Failure sequences (which nodes fail after which)
    - Slowest nodes (bottlenecks)
    - Pipeline-level success rates
    - Loop retry patterns
    """
    total = len(runs)
    if total == 0:
        return {"error": "No runs to analyze", "total_runs": 0}

    # Per-node stats
    node_stats = defaultdict(lambda: {
        "runs": 0,
        "completed": 0,
        "failed": 0,
        "skipped": 0,
        "total_duration": 0.0,
        "errors": [],
    })

    # Failure sequences: (node_A -> node_B) where both failed in same run
    failure_sequences = defaultdict(int)

    # Pipeline-level stats
    pipeline_stats = defaultdict(lambda: {"total": 0, "completed": 0, "failed": 0})

    # Loop retry patterns
    loop_patterns = defaultdict(lambda: {"runs": 0, "hit_max": 0, "total_iterations": 0})

    for run in runs:
        pipeline = run.get("pipeline_name", "unknown")
        status = run.get("status", "unknown")
        pipeline_stats[pipeline]["total"] += 1
        pipeline_stats[pipeline][status] += 1

        results = run.get("results", [])
        failed_nodes_in_run = []

        for r in results:
            node_id = r.get("node_id", "unknown")
            node_type = r.get("node_type", "unknown")
            ns = node_stats[node_id]
            ns["runs"] += 1
            ns[r.get("status", "unknown")] += 1
            ns["total_duration"] += r.get("duration_seconds", 0)

            if r.get("status") == "failed":
                failed_nodes_in_run.append(node_id)
                error = r.get("error", "unknown")
                ns["errors"].append(error)

            # Track loop patterns
            if node_type == "loop":
                lp = loop_patterns[node_id]
                lp["runs"] += 1
                lp["total_iterations"] += r.get("iterations", 1)
                # If iterations == max_iterations (typically 3), it hit the limit
                # We can't know max_iterations from results alone, so flag if iterations >= 3
                if r.get("iterations", 1) >= 3:
                    lp["hit_max"] += 1

        # Build failure sequences
        for i in range(len(failed_nodes_in_run) - 1):
            seq = f"{failed_nodes_in_run[i]} -> {failed_nodes_in_run[i + 1]}"
            failure_sequences[seq] += 1

    # Build report
    report = {
        "analysis_time": datetime.now().isoformat(),
        "total_runs": total,
        "period": "all",
        "summary": {
            "completed": sum(1 for r in runs if r.get("status") == "completed"),
            "failed": sum(1 for r in runs if r.get("status") == "failed"),
            "partial": sum(1 for r in runs if r.get("status") == "partial"),
            "success_rate": _failure_rate(sum(1 for r in runs if r.get("status") == "completed"), total),
        },
    }

    # Per-node failure rates (sorted by failure rate desc)
    node_report = []
    for node_id, stats in sorted(node_stats.items(), key=lambda x: -_failure_rate(x[1]["failed"], x[1]["runs"])):
        node_report.append({
            "node_id": node_id,
            "runs": stats["runs"],
            "completed": stats["completed"],
            "failed": stats["failed"],
            "failure_rate": _failure_rate(stats["failed"], stats["runs"]),
            "avg_duration": round(stats["total_duration"] / stats["runs"], 2) if stats["runs"] else 0,
            "common_errors": _most_common(stats["errors"], 3),
        })
    report["nodes"] = node_report

    # Top 5 failing nodes
    report["top_failures"] = [n for n in node_report if n["failed"] > 0][:5]

    # Failure sequences
    report["failure_sequences"] = sorted(failure_sequences.items(), key=lambda x: -x[1])[:10]

    # Pipeline stats
    pipeline_report = []
    for name, stats in pipeline_stats.items():
        pipeline_report.append({
            "pipeline": name,
            "total": stats["total"],
            "completed": stats["completed"],
            "failed": stats["failed"],
            "success_rate": _failure_rate(stats["completed"], stats["total"]),
        })
    report["pipelines"] = sorted(pipeline_report, key=lambda x: x["success_rate"])

    # Loop patterns
    loop_report = []
    for node_id, stats in loop_patterns.items():
        loop_report.append({
            "loop_node": node_id,
            "runs": stats["runs"],
            "hit_max_count": stats["hit_max"],
            "hit_max_rate": _failure_rate(stats["hit_max"], stats["runs"]),
            "avg_iterations": round(stats["total_iterations"] / stats["runs"], 1) if stats["runs"] else 0,
        })
    report["loop_patterns"] = loop_report

    # Bottlenecks (slowest nodes)
    bottlenecks = sorted(node_report, key=lambda x: -x["avg_duration"])[:5]
    report["bottlenecks"] = bottlenecks

    # Suggestions
    report["suggestions"] = _generate_suggestions(report)

    return report


def _most_common(items: list[str], n: int) -> list[str]:
    """Return the n most common items in a list."""
    if not items:
        return []
    counts = defaultdict(int)
    for item in items:
        counts[item[:80]] += 1  # Truncate long errors
    return [item for item, _ in sorted(counts.items(), key=lambda x: -x[1])[:n]]


def _generate_suggestions(report: dict) -> list[dict]:
    """Generate improvement suggestions based on analysis."""
    suggestions = []

    # Check for nodes with high failure rates
    for node in report.get("top_failures", []):
        rate = node["failure_rate"]
        if rate > 0.5:
            suggestions.append({
                "priority": "high",
                "type": "node_failure",
                "node": node["node_id"],
                "message": f"Node '{node['node_id']}' fails in {rate * 100:.0f}% of runs. Root cause: {node['common_errors'][0] if node['common_errors'] else 'unknown'}",
                "action": "Investigate and fix the root cause. Consider adding a pre-check or validation step.",
            })
        elif rate > 0.25:
            suggestions.append({
                "priority": "medium",
                "type": "node_failure",
                "node": node["node_id"],
                "message": f"Node '{node['node_id']}' fails in {rate * 100:.0f}% of runs.",
                "action": "Review error patterns and consider adding retry logic or better error handling.",
            })

    # Check for loops hitting max iterations
    for loop in report.get("loop_patterns", []):
        if loop["hit_max_rate"] > 0.5:
            suggestions.append({
                "priority": "high",
                "type": "loop_exhaustion",
                "node": loop["loop_node"],
                "message": f"Loop '{loop['loop_node']}' hits max iterations in {loop['hit_max_rate'] * 100:.0f}% of runs (avg {loop['avg_iterations']} iterations).",
                "action": f"Consider increasing max_iterations or improving the fix strategy to converge faster.",
            })

    # Check for bottlenecks
    for bn in report.get("bottlenecks", []):
        if bn["avg_duration"] > 30:
            suggestions.append({
                "priority": "medium",
                "type": "bottleneck",
                "node": bn["node_id"],
                "message": f"Node '{bn['node_id']}' is slow (avg {bn['avg_duration']}s).",
                "action": "Consider parallelizing or optimizing this node.",
            })

    # Check overall success rate
    success = report["summary"]["success_rate"]
    if success < 0.5:
        suggestions.append({
            "priority": "high",
            "type": "overall_health",
            "message": f"Overall success rate is {success * 100:.0f}%. The orchestrator is failing more than succeeding.",
            "action": "Review the top failure patterns and address systemic issues before continuing.",
        })
    elif success > 0.9:
        suggestions.append({
            "priority": "info",
            "type": "overall_health",
            "message": f"Overall success rate is {success * 100:.0f}%. System is healthy.",
            "action": "Consider adding more complex tasks or reducing safety margins.",
        })

    return suggestions


# ─── Parameter Auto-Tuner ────────────────────────────────────────────────────

def analyze_parameter_tuning(runs: list[dict]) -> dict:
    """
    Analyze pipeline parameters and suggest tuning adjustments.

    Focuses on:
    - Loop max_iterations (are loops exhausting?)
    - Timeout values (are bash nodes timing out?)
    - AI max_turns (are agents running out of turns?)
    """
    if not runs:
        return {"error": "No runs to analyze"}

    suggestions = []

    # Analyze loop nodes
    loop_stats = defaultdict(lambda: {"runs": 0, "iterations": []})
    for run in runs:
        for r in run.get("results", []):
            if r.get("node_type") == "loop":
                node_id = r.get("node_id", "unknown")
                loop_stats[node_id]["runs"] += 1
                loop_stats[node_id]["iterations"].append(r.get("iterations", 1))

    for node_id, stats in loop_stats.items():
        if not stats["iterations"]:
            continue
        avg = sum(stats["iterations"]) / len(stats["iterations"])
        max_seen = max(stats["iterations"])
        hitting_max = sum(1 for i in stats["iterations"] if i >= 3)

        if hitting_max / len(stats["iterations"]) > 0.5:
            suggestions.append({
                "parameter": "max_iterations",
                "node": node_id,
                "current_estimate": 3,
                "suggested": max_seen + 2,
                "confidence": 0.8,
                "reason": f"{hitting_max}/{len(stats['iterations'])} runs hit max iterations (avg {avg:.1f}). Increase to {max_seen + 2}.",
            })

    # Analyze timeout patterns
    timeout_stats = defaultdict(lambda: {"runs": 0, "durations": []})
    for run in runs:
        for r in run.get("results", []):
            if r.get("node_type") == "bash" and r.get("status") == "failed":
                node_id = r.get("node_id", "unknown")
                timeout_stats[node_id]["runs"] += 1
                timeout_stats[node_id]["durations"].append(r.get("duration_seconds", 0))

    for node_id, stats in timeout_stats.items():
        if not stats["durations"]:
            continue
        avg = sum(stats["durations"]) / len(stats["durations"])
        # If avg duration is close to typical timeout values (60, 120), suggest increase
        for typical_timeout in [60, 120, 300]:
            if avg > typical_timeout * 0.8:
                suggestions.append({
                    "parameter": "timeout_seconds",
                    "node": node_id,
                    "current_estimate": typical_timeout,
                    "suggested": int(typical_timeout * 1.5),
                    "confidence": 0.6,
                    "reason": f"Node '{node_id}' avg duration ({avg:.0f}s) is close to timeout ({typical_timeout}s). Consider increasing.",
                })
                break

    return {
        "analysis_time": datetime.now().isoformat(),
        "runs_analyzed": len(runs),
        "suggestions": suggestions,
    }


# ─── Health Score ────────────────────────────────────────────────────────────

def compute_health_score(runs: list[dict]) -> dict:
    """
    Compute a health score (0-100) for the orchestrator based on recent runs.
    """
    if not runs:
        return {"score": 0, "message": "No runs to evaluate"}

    total = len(runs)
    completed = sum(1 for r in runs if r.get("status") == "completed")
    failed = sum(1 for r in runs if r.get("status") == "failed")

    # Components
    success_component = min(completed / total, 1.0) * 40  # 40 points max

    # Stability: how consistent is the success rate?
    # Group by day and check variance
    daily_rates = defaultdict(lambda: {"total": 0, "completed": 0})
    for run in runs:
        logged_at = run.get("_logged_at", "")
        if logged_at:
            try:
                day = logged_at[:10]
                daily_rates[day]["total"] += 1
                daily_rates[day]["completed"] += int(run.get("status") == "completed")
            except (ValueError, IndexError):
                pass

    if len(daily_rates) >= 2:
        rates = [v["completed"] / v["total"] for v in daily_rates.values() if v["total"] > 0]
        avg_rate = sum(rates) / len(rates)
        variance = sum((r - avg_rate) ** 2 for r in rates) / len(rates)
        stability_component = max(0, 1 - variance * 4) * 20  # 20 points max
    else:
        stability_component = 10  # Neutral if not enough data

    # Speed: average duration
    total_duration = sum(r.get("duration_seconds", 0) for r in runs)
    avg_duration = total_duration / total
    speed_component = max(0, 1 - avg_duration / 300) * 20  # 20 points max, degrades after 300s

    # Efficiency: nodes completed vs total
    total_nodes = sum(r.get("total_nodes", 0) for r in runs)
    completed_nodes = sum(r.get("completed_nodes", 0) for r in runs)
    efficiency_component = (completed_nodes / total_nodes if total_nodes else 0) * 20  # 20 points max

    score = int(success_component + stability_component + speed_component + efficiency_component)

    return {
        "score": min(score, 100),
        "components": {
            "success_rate": round(success_component, 1),
            "stability": round(stability_component, 1),
            "speed": round(speed_component, 1),
            "efficiency": round(efficiency_component, 1),
        },
        "details": {
            "total_runs": total,
            "completed": completed,
            "failed": failed,
            "avg_duration_seconds": round(avg_duration, 1),
            "node_completion_rate": round(completed_nodes / total_nodes, 2) if total_nodes else 0,
        },
        "message": _health_message(score),
    }


def _health_message(score: int) -> str:
    if score >= 80:
        return "🟢 Excellent. The orchestrator is performing well."
    elif score >= 60:
        return "🟡 Good. Some areas need attention."
    elif score >= 40:
        return "🟠 Fair. Multiple issues detected that should be addressed."
    else:
        return "🔴 Poor. The orchestrator needs significant improvement."


# ─── Report Formatters ───────────────────────────────────────────────────────

def format_analysis_report(report: dict) -> str:
    """Format the analysis report as human-readable text."""
    lines = []
    lines.append("=" * 60)
    lines.append("SELF-IMPROVEMENT ANALYSIS REPORT")
    lines.append(f"Generated: {report['analysis_time']}")
    lines.append(f"Runs analyzed: {report['total_runs']}")
    lines.append("=" * 60)

    s = report["summary"]
    lines.append(f"\n## Summary")
    lines.append(f"  Success rate: {s['success_rate'] * 100:.0f}% ({s['completed']}/{report['total_runs']})")
    lines.append(f"  Failed: {s['failed']}, Partial: {s['partial']}")

    # Top failures
    if report.get("top_failures"):
        lines.append(f"\n## Top Failing Nodes")
        for node in report["top_failures"]:
            icon = "🔴" if node["failure_rate"] > 0.5 else "🟡" if node["failure_rate"] > 0.25 else "🟢"
            lines.append(f"  {icon} {node['node_id']}: {node['failure_rate'] * 100:.0f}% failure rate ({node['failed']}/{node['runs']})")
            if node["common_errors"]:
                lines.append(f"     Common: {node['common_errors'][0][:60]}")

    # Loop patterns
    if report.get("loop_patterns"):
        lines.append(f"\n## Loop Retry Patterns")
        for lp in report["loop_patterns"]:
            icon = "⚠️" if lp["hit_max_rate"] > 0.5 else "✅"
            lines.append(f"  {icon} {lp['loop_node']}: avg {lp['avg_iterations']} iterations, hit max {lp['hit_max_rate'] * 100:.0f}%")

    # Bottlenecks
    if report.get("bottlenecks"):
        lines.append(f"\n## Bottlenecks (Slowest Nodes)")
        for bn in report["bottlenecks"]:
            lines.append(f"  ⏱️  {bn['node_id']}: avg {bn['avg_duration']}s ({bn['runs']} runs)")

    # Pipeline success rates
    if report.get("pipelines"):
        lines.append(f"\n## Pipeline Success Rates")
        for p in report["pipelines"]:
            icon = "✅" if p["success_rate"] > 0.8 else "🟡" if p["success_rate"] > 0.5 else "❌"
            lines.append(f"  {icon} {p['pipeline']}: {p['success_rate'] * 100:.0f}% ({p['completed']}/{p['total']})")

    # Suggestions
    if report.get("suggestions"):
        lines.append(f"\n## Suggestions")
        for s in report["suggestions"]:
            priority_icon = {"high": "🔴", "medium": "🟡", "info": "ℹ️"}.get(s["priority"], "•")
            lines.append(f"  {priority_icon} [{s['priority'].upper()}] {s['message']}")
            lines.append(f"     Action: {s['action']}")

    lines.append(f"\n{'=' * 60}")
    return "\n".join(lines)


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Continuous Self-Improvement Loop")
    parser.add_argument("--analyze", action="store_true", help="Analyze failure patterns")
    parser.add_argument("--tune", action="store_true", help="Suggest parameter tuning")
    parser.add_argument("--apply", action="store_true", help="Apply tuning suggestions (with --tune)")
    parser.add_argument("--report", action="store_true", help="Generate full improvement report")
    parser.add_argument("--health", action="store_true", help="Show health score")
    parser.add_argument("--last", "-n", type=int, default=50, help="Number of runs to analyze")
    parser.add_argument("--period", choices=["day", "week", "month"], default=None,
                        help="Time period to analyze")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Output as JSON")

    args = parser.parse_args()

    period_days = {"day": 1, "week": 7, "month": 30}.get(args.period) if args.period else None

    if not any([args.analyze, args.tune, args.report, args.health]):
        parser.error("One of --analyze, --tune, --report, --health is required")

    runs = _load_runs(limit=args.last, period_days=period_days)

    if args.analyze or args.report:
        report = analyze_failure_patterns(runs)
        if args.json_output:
            print(json.dumps(report, indent=2))
        else:
            print(format_analysis_report(report))

    if args.tune:
        tuning = analyze_parameter_tuning(runs)
        if args.json_output:
            print(json.dumps(tuning, indent=2))
        else:
            print("## Parameter Tuning Suggestions")
            print(f"Runs analyzed: {tuning.get('runs_analyzed', 0)}")
            if not tuning.get("suggestions"):
                print("  No tuning suggestions. Current parameters look good.")
            else:
                for s in tuning["suggestions"]:
                    icon = "🔧" if s["confidence"] >= 0.7 else "💡"
                    print(f"\n  {icon} {s['node']} -> {s['parameter']}")
                    print(f"     Current: ~{s['current_estimate']}, Suggested: {s['suggested']}")
                    print(f"     Confidence: {s['confidence']:.0%}")
                    print(f"     Reason: {s['reason']}")

    if args.health:
        health = compute_health_score(runs)
        if args.json_output:
            print(json.dumps(health, indent=2))
        else:
            print(f"\n  Health Score: {health['score']}/100")
            print(f"  {health['message']}")
            print(f"\n  Components:")
            for k, v in health["components"].items():
                bar_len = int(v / 4)
                bar = "█" * bar_len + "░" * (10 - bar_len)
                print(f"    {k:12s} {bar} {v:.1f}/20")


if __name__ == "__main__":
    main()
