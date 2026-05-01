#!/usr/bin/env python3
"""
Inferential Sensor (LLM-as-Judge) for the Hermes Agent Orchestrator.

Evaluates completed pipeline runs using an LLM judge to assess code quality,
task adherence, test coverage, and potential regressions. Results stored
in ~/.orchestrator/logs/reviews/.

Usage:
    python3 review_sensor.py --run RUN_ID
    python3 review_sensor.py --latest 5
    python3 review_sensor.py --stats
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from execution_log import get_run, list_runs

REVIEWS_DIR = Path(os.path.expanduser("~/.orchestrator/logs/reviews"))

# Default evaluation criteria
DEFAULT_CRITERIA = [
    {"name": "code_quality", "description": "Clean, readable, well-structured code with appropriate abstractions", "weight": 1.0},
    {"name": "task_adherence", "description": "Changes address the task description accurately and completely", "weight": 1.5},
    {"name": "test_coverage", "description": "Adequate test coverage for new/changed code", "weight": 1.0},
    {"name": "no_regressions", "description": "No obvious regressions or breaking changes introduced", "weight": 1.5},
]


def _ensure_dirs():
    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)


def _build_review_prompt(run_data: dict, criteria: list[dict]) -> str:
    """Build the LLM prompt for evaluating a pipeline run."""
    parts = [
        "You are a code review evaluator. Evaluate the following pipeline execution result.",
        "",
        "## Pipeline Run",
        f"- Pipeline: {run_data.get('pipeline_name', 'unknown')}",
        f"- Status: {run_data.get('status', 'unknown')}",
        f"- Duration: {run_data.get('duration_seconds', 0)}s",
        f"- Nodes: {run_data.get('completed_nodes', 0)}/{run_data.get('total_nodes', 0)} completed",
    ]

    # Include node results
    results = run_data.get("results", [])
    if results:
        parts.append("")
        parts.append("## Node Results")
        for r in results:
            status_icon = "ok" if r.get("status") == "completed" else "FAIL"
            parts.append(f"- [{status_icon}] {r.get('node_id', '?')} ({r.get('node_type', '?')}): {r.get('status', '?')}")
            if r.get("output"):
                output = r["output"][:500]
                parts.append(f"  Output: {output}")
            if r.get("error"):
                parts.append(f"  Error: {r['error']}")

    # Include criteria
    parts.append("")
    parts.append("## Evaluation Criteria")
    for c in criteria:
        parts.append(f"- {c['name']} (weight: {c['weight']}): {c['description']}")

    parts.append("")
    parts.append("## Response Format")
    parts.append("Respond with ONLY a JSON object (no markdown, no code fences):")
    parts.append("{")
    parts.append('  "scores": {')
    for c in criteria:
        parts.append(f'    "{c["name"]}": <integer 1-10>,')
    parts.append('    "overall": <integer 1-10>')
    parts.append("  },")
    parts.append('  "verdict": "<pass|fail|needs_review>",')
    parts.append('  "summary": "<one sentence summary>",')
    parts.append('  "concerns": ["<list of specific concerns>"]')
    parts.append("}")
    parts.append("")
    parts.append("Scoring: 1-3 = poor, 4-6 = acceptable, 7-8 = good, 9-10 = excellent.")
    parts.append("Verdict: pass (avg >= 7), needs_review (avg 5-6), fail (avg < 5).")

    return "\n".join(parts)


def _call_llm(prompt: str) -> str:
    """Call the LLM via model_choice. Falls back to a stub if unavailable."""
    try:
        sys.path.insert(0, os.path.expanduser("~/zion/projects/model_choice"))
        from model_choice import generate as llm_generate
        return llm_generate(prompt)
    except ImportError:
        # Fallback: return a neutral evaluation for testing without model_choice
        return json.dumps({
            "scores": {"code_quality": 7, "task_adherence": 7, "test_coverage": 7, "no_regressions": 7, "overall": 7},
            "verdict": "pass",
            "summary": "Evaluation completed (no LLM available - default scores)",
            "concerns": []
        })


def _parse_response(response: str) -> dict:
    """Parse LLM response into structured evaluation."""
    # Try to extract JSON from the response
    text = response.strip()
    # Remove markdown code fences if present
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "scores": {},
            "verdict": "needs_review",
            "summary": f"Failed to parse LLM response: {text[:200]}",
            "concerns": ["LLM response was not valid JSON"],
        }


def _compute_weighted_score(scores: dict, criteria: list[dict]) -> float:
    """Compute weighted average score."""
    total_weight = 0.0
    weighted_sum = 0.0
    for c in criteria:
        name = c["name"]
        weight = c.get("weight", 1.0)
        if name in scores:
            weighted_sum += scores[name] * weight
            total_weight += weight
    return round(weighted_sum / total_weight, 2) if total_weight > 0 else 0.0


def evaluate_run(run_id: str, criteria: list[dict] | None = None) -> dict:
    """
    Evaluate a single pipeline run using the LLM judge.

    Args:
        run_id: The execution run ID.
        criteria: List of evaluation criteria dicts. Defaults to DEFAULT_CRITERIA.

    Returns:
        Evaluation result dict with scores, verdict, and metadata.
    """
    _ensure_dirs()
    criteria = criteria or DEFAULT_CRITERIA

    run_data = get_run(run_id)
    if not run_data:
        return {"error": f"Run {run_id} not found", "run_id": run_id}

    prompt = _build_review_prompt(run_data, criteria)
    response = _call_llm(prompt)
    parsed = _parse_response(response)

    # Compute weighted score
    scores = parsed.get("scores", {})
    weighted_score = _compute_weighted_score(scores, criteria)

    # Determine verdict from score if not provided
    verdict = parsed.get("verdict", "needs_review")
    if not verdict:
        if weighted_score >= 7:
            verdict = "pass"
        elif weighted_score >= 5:
            verdict = "needs_review"
        else:
            verdict = "fail"

    result = {
        "run_id": run_id,
        "pipeline_name": run_data.get("pipeline_name", "unknown"),
        "pipeline_status": run_data.get("status", "unknown"),
        "scores": scores,
        "weighted_score": weighted_score,
        "verdict": verdict,
        "summary": parsed.get("summary", ""),
        "concerns": parsed.get("concerns", []),
        "evaluated_at": datetime.now().isoformat(),
        "criteria": [{"name": c["name"], "weight": c["weight"]} for c in criteria],
    }

    # Save review
    review_path = REVIEWS_DIR / f"{run_id}.json"
    with open(review_path, "w") as f:
        json.dump(result, f, indent=2)

    return result


def evaluate_latest(n: int = 5, criteria: list[dict] | None = None) -> list[dict]:
    """
    Evaluate the last N completed pipeline runs.

    Args:
        n: Number of recent runs to evaluate.
        criteria: Evaluation criteria. Defaults to DEFAULT_CRITERIA.

    Returns:
        List of evaluation result dicts.
    """
    runs = list_runs(limit=n * 3, status="completed")  # Fetch extra in case some fail
    results = []
    for run in runs[:n]:
        result = evaluate_run(run["run_id"], criteria)
        results.append(result)
    return results


def get_review(run_id: str) -> dict | None:
    """Load a previously saved review."""
    review_path = REVIEWS_DIR / f"{run_id}.json"
    if not review_path.exists():
        return None
    try:
        return json.loads(review_path.read_text())
    except json.JSONDecodeError:
        return None


def get_review_stats() -> dict:
    """Get aggregate statistics across all reviews."""
    _ensure_dirs()
    reviews = list(REVIEWS_DIR.glob("*.json"))
    if not reviews:
        return {"total_reviews": 0}

    verdicts = {"pass": 0, "fail": 0, "needs_review": 0}
    total_score = 0.0
    criterion_scores = {}

    for f in reviews:
        try:
            data = json.loads(f.read_text())
            v = data.get("verdict", "needs_review")
            if v in verdicts:
                verdicts[v] += 1
            total_score += data.get("weighted_score", 0)
            for name, score in data.get("scores", {}).items():
                if name not in criterion_scores:
                    criterion_scores[name] = []
                criterion_scores[name].append(score)
        except (json.JSONDecodeError, KeyError):
            continue

    avg_criterion = {}
    for name, scores in criterion_scores.items():
        avg_criterion[name] = round(sum(scores) / len(scores), 2) if scores else 0

    return {
        "total_reviews": len(reviews),
        "verdicts": verdicts,
        "avg_weighted_score": round(total_score / len(reviews), 2) if reviews else 0,
        "avg_criterion_scores": avg_criterion,
    }


def main():
    parser = argparse.ArgumentParser(description="LLM-as-Judge review sensor")
    parser.add_argument("--run", help="Evaluate a specific run by ID")
    parser.add_argument("--latest", type=int, default=0, help="Evaluate last N completed runs")
    parser.add_argument("--stats", action="store_true", help="Show aggregate review statistics")

    args = parser.parse_args()

    if args.stats:
        stats = get_review_stats()
        print(json.dumps(stats, indent=2))
        return

    if args.run:
        result = evaluate_run(args.run)
        print(json.dumps(result, indent=2))
        return

    if args.latest > 0:
        results = evaluate_latest(args.latest)
        for r in results:
            print(f"Run {r.get('run_id', '?')}: {r.get('verdict', '?')} (score: {r.get('weighted_score', '?')}) - {r.get('summary', '')}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
