#!/usr/bin/env python3
"""
Per-repo cost tracking for the Hermes Agent Orchestrator.

Estimates token usage per pipeline execution, accumulates daily costs
per repo, and alerts when approaching budget limits.

Cost model:
  - AI nodes: ~10K tokens/turn * $0.003/1K tokens (Claude Sonnet estimate)
  - Bash/Loop/Dependency nodes: free (just compute)
  - Review nodes: ~15K tokens * $0.003/1K tokens
  - Per-repo daily budget enforcement

Usage:
    python3 cost_tracker.py record --repo owner/repo --tokens 10000
    python3 cost_tracker.py report --period week
    python3 cost_tracker.py check --repo owner/repo --budget 10.0
"""

import argparse
import json
import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

COSTS_DIR = Path(os.path.expanduser("~/.orchestrator/costs"))

# Cost per 1K tokens (estimate for Claude Sonnet)
COST_PER_1K_TOKENS = 0.003
# Estimated tokens per AI node turn
TOKENS_PER_AI_TURN = 10000
# Estimated tokens per review node
TOKENS_PER_REVIEW = 15000


def repo_dir(repo: str) -> Path:
    """Get the cost storage directory for a repo."""
    safe_name = repo.replace("/", "__")
    return COSTS_DIR / safe_name


def record_usage(
    repo: str,
    tokens: int,
    node_type: str = "ai",
    run_id: str | None = None,
    issue_number: int | None = None,
) -> dict:
    """
    Record token usage for a repo.

    Returns the updated daily summary.
    """
    today = date.today().isoformat()
    rd = repo_dir(repo)
    rd.mkdir(parents=True, exist_ok=True)

    daily_path = rd / f"{today}.json"
    daily = {"date": today, "repo": repo, "entries": [], "total_tokens": 0, "total_cost": 0.0}

    if daily_path.exists():
        daily = json.loads(daily_path.read_text())

    cost = (tokens / 1000) * COST_PER_1K_TOKENS
    entry = {
        "timestamp": datetime.now().isoformat(),
        "tokens": tokens,
        "cost": round(cost, 4),
        "node_type": node_type,
        "run_id": run_id,
        "issue_number": issue_number,
    }
    daily["entries"].append(entry)
    daily["total_tokens"] += tokens
    daily["total_cost"] = round(sum(e["cost"] for e in daily["entries"]), 4)

    daily_path.write_text(json.dumps(daily, indent=2))
    return daily


def estimate_pipeline_cost(node_types: list[str]) -> dict:
    """
    Estimate cost for a pipeline execution based on node types.

    Returns dict with estimated_tokens and estimated_cost.
    """
    total_tokens = 0
    for nt in node_types:
        nt_lower = nt.lower()
        if nt_lower == "ai":
            total_tokens += TOKENS_PER_AI_TURN
        elif nt_lower == "review":
            total_tokens += TOKENS_PER_REVIEW
        # bash, loop, dependency are free

    cost = (total_tokens / 1000) * COST_PER_1K_TOKENS
    return {
        "estimated_tokens": total_tokens,
        "estimated_cost": round(cost, 4),
    }


def get_daily_cost(repo: str, target_date: date | None = None) -> dict | None:
    """Get cost summary for a repo on a specific date."""
    target_date = target_date or date.today()
    daily_path = repo_dir(repo) / f"{target_date.isoformat()}.json"
    if daily_path.exists():
        return json.loads(daily_path.read_text())
    return None


def get_period_cost(repo: str, days: int = 7) -> dict:
    """
    Get cost summary for a repo over a period of days.

    Returns dict with total_tokens, total_cost, daily breakdown.
    """
    total_tokens = 0
    total_cost = 0.0
    daily_breakdown = []

    for i in range(days):
        d = date.today() - timedelta(days=i)
        daily = get_daily_cost(repo, d)
        if daily:
            total_tokens += daily["total_tokens"]
            total_cost += daily["total_cost"]
            daily_breakdown.append({
                "date": d.isoformat(),
                "tokens": daily["total_tokens"],
                "cost": daily["total_cost"],
                "executions": len(daily["entries"]),
            })

    return {
        "repo": repo,
        "period_days": days,
        "total_tokens": total_tokens,
        "total_cost": round(total_cost, 4),
        "daily": daily_breakdown,
    }


def check_budget(repo: str, budget_daily: float) -> dict:
    """
    Check if a repo is within its daily budget.

    Returns dict with status (ok/warning/exceeded), current_cost,
    remaining, and budget.
    """
    daily = get_daily_cost(repo)
    current_cost = daily["total_cost"] if daily else 0.0
    remaining = budget_daily - current_cost
    ratio = current_cost / budget_daily if budget_daily > 0 else 1.0

    if ratio >= 1.0:
        status = "exceeded"
    elif ratio >= 0.8:
        status = "warning"
    else:
        status = "ok"

    return {
        "repo": repo,
        "budget_daily": budget_daily,
        "current_cost": round(current_cost, 4),
        "remaining": round(remaining, 4),
        "usage_ratio": round(ratio, 3),
        "status": status,
    }


def get_all_repos() -> list[str]:
    """List all repos that have cost records."""
    if not COSTS_DIR.exists():
        return []
    repos = []
    for d in COSTS_DIR.iterdir():
        if d.is_dir():
            # Convert safe_name back: owner__repo -> owner/repo
            name = d.name
            if "__" in name:
                repos.append(name.replace("__", "/", 1))
            else:
                repos.append(name)
    return sorted(repos)


def main():
    parser = argparse.ArgumentParser(description="Per-repo cost tracking")
    sub = parser.add_subparsers(dest="command")

    # record
    rec = sub.add_parser("record", help="Record token usage")
    rec.add_argument("--repo", "-r", required=True)
    rec.add_argument("--tokens", "-t", type=int, required=True)
    rec.add_argument("--node-type", "-n", default="ai")
    rec.add_argument("--run-id", default=None)
    rec.add_argument("--issue", type=int, default=None)

    # report
    rep = sub.add_parser("report", help="Show cost report")
    rep.add_argument("--repo", "-r", default=None)
    rep.add_argument("--period", "-p", type=int, default=7)
    rep.add_argument("--json", action="store_true", dest="json_output")

    # check
    chk = sub.add_parser("check", help="Check budget status")
    chk.add_argument("--repo", "-r", required=True)
    chk.add_argument("--budget", "-b", type=float, required=True)

    # estimate
    est = sub.add_parser("estimate", help="Estimate pipeline cost")
    est.add_argument("--nodes", "-n", nargs="+", required=True)

    args = parser.parse_args()

    if args.command == "record":
        daily = record_usage(
            repo=args.repo,
            tokens=args.tokens,
            node_type=args.node_type,
            run_id=args.run_id,
            issue_number=args.issue,
        )
        print(f"Recorded {args.tokens} tokens for {args.repo}")
        print(f"  Daily total: {daily['total_tokens']} tokens (${daily['total_cost']:.4f})")

    elif args.command == "report":
        repos = [args.repo] if args.repo else get_all_repos()
        if not repos:
            print("No cost records found.")
            return

        for repo in repos:
            data = get_period_cost(repo, args.period)
            if args.json_output:
                print(json.dumps(data, indent=2))
            else:
                print(f"\n{'='*50}")
                print(f"  {repo} (last {args.period} days)")
                print(f"{'='*50}")
                print(f"  Total tokens:  {data['total_tokens']:,}")
                print(f"  Total cost:    ${data['total_cost']:.4f}")
                if data["daily"]:
                    print(f"\n  {'Date':<12} {'Tokens':>8} {'Cost':>10} {'Runs':>6}")
                    print(f"  {'-'*12} {'-'*8} {'-'*10} {'-'*6}")
                    for d in data["daily"]:
                        print(f"  {d['date']:<12} {d['tokens']:>8,} ${d['cost']:>9.4f} {d['executions']:>6}")

    elif args.command == "check":
        result = check_budget(args.repo, args.budget)
        status_icon = {"ok": "✅", "warning": "⚠️", "exceeded": "🚫"}.get(result["status"], "?")
        print(f"{status_icon} {args.repo}: ${result['current_cost']:.4f} / ${result['budget_daily']:.2f} ({result['usage_ratio']*100:.1f}%)")
        if result["status"] == "warning":
            print(f"  ⚠️  Approaching budget limit. ${result['remaining']:.4f} remaining.")
        elif result["status"] == "exceeded":
            print(f"  🚫 Budget exceeded by ${abs(result['remaining']):.4f}.")
        sys.exit(1 if result["status"] == "exceeded" else 0)

    elif args.command == "estimate":
        result = estimate_pipeline_cost(args.nodes)
        print(f"Estimated tokens: {result['estimated_tokens']:,}")
        print(f"Estimated cost:   ${result['estimated_cost']:.4f}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
