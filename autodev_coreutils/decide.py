"""decide -- Pick between options using evidence.

Like `test` but for judgment calls. Takes a question, a set of options,
and evidence, then returns a structured decision with confidence.

Input:  Question + options + evidence (files, stdin, or args)
Output: JSON or text with {choice, confidence, reasoning}
State:  decisions.jsonl in .autodev/ (append-only audit trail)

Usage:
    autodev-decide "Which task first?" --options task_0.md task_1.md
    git diff | autodev-decide "Keep these changes?" --options keep revert
    autodev-decide "Ready to ship?" --evidence tests.log --options yes no --confidence
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from model_choice import generate as llm_generate
except ImportError:
    llm_generate = None

from .contract import (
    make_parser, find_project, ensure_autodev_dir,
    write_state, output, error, EXIT_FAILURE,
)


DECISIONS_LOG = "decisions.jsonl"


def build_prompt(question: str, options: list[str], evidence: str,
                 criteria: str = "", confidence: bool = False) -> str:
    """Build the LLM prompt for a decision."""
    opts_text = "\n".join(f"  {i+1}. {opt}" for i, opt in enumerate(options))

    prompt = f"""You are a decision engine. Given a question, discrete options, and evidence, pick the best option.

QUESTION:
{question}

OPTIONS:
{opts_text}
"""

    if criteria:
        prompt += f"""
CRITERIA (evaluate options against these):
{criteria}
"""

    prompt += f"""
EVIDENCE:
{evidence if evidence else "(no evidence provided)"}
"""

    prompt += """
RULES:
- You MUST pick exactly one option from the list above
- Be concise in your reasoning
- Base your decision on the evidence, not assumptions

Respond with ONLY valid JSON:
{"choice": "<exact option text>", "reasoning": "<brief why>", "confidence": <0.0-1.0>}

No markdown fences, no extra text."""

    return prompt


def parse_response(raw: str) -> dict:
    """Parse the LLM response into a structured decision."""
    text = raw.strip()

    # Strip markdown fences if present
    if text.startswith("```"):
        lines = text.split("\n")
        # Remove first and last fence lines
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines)

    # Try direct parse
    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        # Try to extract JSON object from text
        import re
        match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
        if match:
            result = json.loads(match.group())
        else:
            return {
                "choice": text[:200],
                "reasoning": "Could not parse LLM response as JSON",
                "confidence": 0.0,
                "parse_error": True,
                "raw": text[:500],
            }

    # Normalize keys
    result.setdefault("confidence", 0.5)
    result.setdefault("reasoning", "")
    result["parse_error"] = False

    # Clamp confidence
    try:
        result["confidence"] = max(0.0, min(1.0, float(result["confidence"])))
    except (ValueError, TypeError):
        result["confidence"] = 0.5

    return result


def decide(question: str, options: list[str], evidence: str = "",
           criteria: str = "", model: str = None) -> dict:
    """Make a decision. Returns {choice, confidence, reasoning}."""
    if llm_generate is None:
        error("model_choice not installed. Run: pip install model_choice")

    if not options or len(options) < 2:
        error("Need at least 2 options to make a decision")

    prompt = build_prompt(question, options, evidence, criteria)

    if model:
        resp = llm_generate(prompt, model=model)
    else:
        resp = llm_generate(prompt)

    result = parse_response(resp)

    # Validate choice matches an option (fuzzy)
    choice = result.get("choice", "")
    matched = False
    for opt in options:
        if choice.lower() == opt.lower() or choice.lower() in opt.lower():
            result["choice"] = opt  # Normalize to exact option text
            matched = True
            break

    result["matched_option"] = matched
    result["question"] = question
    result["options"] = options

    return result


def log_decision(project: Path, decision: dict) -> Path:
    """Append a decision to the audit trail."""
    ad = ensure_autodev_dir(project)
    log_file = ad / DECISIONS_LOG

    from datetime import datetime, timezone
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **decision,
    }

    with open(log_file, "a") as f:
        f.write(json.dumps(entry, default=str) + "\n")

    return log_file


def format_text(decision: dict) -> str:
    """Format a decision for human-readable text output."""
    lines = [
        f"Decision: {decision['choice']}",
        f"Confidence: {decision['confidence']:.0%}",
        f"Reasoning: {decision['reasoning']}",
    ]
    if not decision.get("matched_option", True):
        lines.append(f"(choice did not exactly match any option)")
    return "\n".join(lines)


def read_evidence_from_args(args) -> str:
    """Collect evidence from --evidence flags and stdin."""
    parts = []

    # Read evidence files
    for ef in getattr(args, "evidence", []) or []:
        p = Path(ef)
        if p.exists():
            content = p.read_text()
            # Truncate large files
            if len(content) > 8000:
                content = content[:8000] + f"\n... (truncated, {len(content)} bytes total)"
            parts.append(f"--- {ef} ---\n{content}")
        else:
            print(f"WARNING: evidence file not found: {ef}", file=sys.stderr)

    # Read stdin if piped
    if hasattr(sys.stdin, "isatty") and not sys.stdin.isatty():
        try:
            stdin_text = sys.stdin.read()
            if stdin_text.strip():
                parts.append(f"--- stdin ---\n{stdin_text}")
        except OSError:
            pass  # stdin not available (e.g. under pytest)

    return "\n\n".join(parts)


def main(argv=None):
    parser = make_parser("decide", "Pick between options using evidence")
    parser.add_argument(
        "question",
        help="The decision question",
    )
    parser.add_argument(
        "--options", "-o", nargs="+", required=True,
        help="Discrete options to choose from (at least 2)",
    )
    parser.add_argument(
        "--evidence", "-e", nargs="*", default=[],
        help="Files to use as evidence (also reads stdin if piped)",
    )
    parser.add_argument(
        "--criteria", "-c", default="",
        help="Criteria to evaluate options against",
    )
    parser.add_argument(
        "--model", "-m", default=None,
        help="LLM model to use (via model_choice)",
    )
    parser.add_argument(
        "--confidence", action="store_true",
        help="Always show confidence score in text output",
    )
    parser.add_argument(
        "--no-log", action="store_true",
        help="Don't log this decision to .autodev/decisions.jsonl",
    )

    args = parser.parse_args(argv)

    # Validate options
    if len(args.options) < 2:
        error("Need at least 2 options to decide between")

    # Collect evidence
    evidence = read_evidence_from_args(args)

    # Find project (best effort -- decide can work without .autodev/)
    project = find_project(args.workdir)

    # Make the decision
    result = decide(
        question=args.question,
        options=args.options,
        evidence=evidence,
        criteria=args.criteria,
        model=args.model,
    )

    # Log it
    if not args.no_log:
        log_decision(project, result)

    # Write state
    write_state(project, "decide", result)

    # Output
    if args.json_output:
        output(result, json_mode=True)
    elif not args.quiet:
        output(format_text(result))

    # Exit code: 0 if high confidence, 1 if low
    if result.get("confidence", 0) < 0.3:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
