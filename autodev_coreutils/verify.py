"""verify -- Verify an agent's claims against actual files and git.

Like `test` but for agent outputs. Takes an agent's "I did X" claim and
checks it against the actual codebase.

Input:  A claim string, or an outcome file from .autodev/
Output: Verification result (pass/fail with evidence)
State:  verify_state.json with results

Usage:
    autodev-verify --claim "Added error handling to parser.py"
    autodev-verify --outcome .autodev/outcome.md
    autodev-verify --last-run
    autodev-verify --diff HEAD~1
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

try:
    from model_choice import generate as llm_generate
except ImportError:
    llm_generate = None

from .contract import (
    make_parser, find_project, ensure_autodev_dir,
    write_state, output, error,
)


def get_git_diff(project: Path, ref: str = "HEAD~1") -> str:
    """Get git diff for a given ref."""
    try:
        result = subprocess.run(
            ["git", "diff", ref],
            capture_output=True, text=True, cwd=project, timeout=30,
        )
        return result.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return ""


def get_git_log(project: Path, n: int = 5) -> str:
    """Get recent git log."""
    try:
        result = subprocess.run(
            ["git", "log", f"-{n}", "--oneline"],
            capture_output=True, text=True, cwd=project, timeout=10,
        )
        return result.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return ""


def check_files_exist(project: Path, files: list[str]) -> dict:
    """Check which files exist."""
    results = {}
    for f in files:
        results[f] = (project / f).exists()
    return results


def check_test_passes(project: Path, test_cmd: str = None) -> dict:
    """Run tests and return result."""
    if test_cmd is None:
        # Auto-detect
        if (project / "Cargo.toml").exists():
            test_cmd = "cargo test 2>&1"
        elif (project / "pyproject.toml").exists():
            test_cmd = "python -m pytest -q 2>&1"
        else:
            return {"status": "skipped", "reason": "No test framework detected"}

    try:
        result = subprocess.run(
            test_cmd, shell=True, capture_output=True, text=True,
            cwd=project, timeout=120,
        )
        return {
            "status": "pass" if result.returncode == 0 else "fail",
            "exit_code": result.returncode,
            "output": (result.stdout + result.stderr)[-1000:],
        }
    except subprocess.TimeoutExpired:
        return {"status": "timeout"}


def verify_claim(project: Path, claim: str, model: str = None) -> dict:
    """Use LLM to verify a claim against the codebase."""
    if llm_generate is None:
        error("model_choice not installed")

    # Gather evidence
    diff = get_git_diff(project)
    log = get_git_log(project)

    prompt = f"""Verify this agent claim against the actual codebase evidence.

CLAIM: {claim}

RECENT GIT LOG:
{log}

LATEST DIFF:
{diff[:4000]}

Analyze whether the claim is supported by the evidence.
Output JSON: {{"verified": true/false, "confidence": 0.0-1.0, "evidence": "what supports it", "gaps": "what's missing or suspicious"}}
Output ONLY valid JSON."""

    if model:
        resp = llm_generate(prompt, model=model)
    else:
        resp = llm_generate(prompt)

    text = resp.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:-1])

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        import re
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return {"verified": False, "confidence": 0, "evidence": "Could not parse verification", "gaps": text[:200]}


def main(argv=None):
    parser = make_parser("verify", "Verify agent claims against actual codebase state")
    parser.add_argument(
        "--claim", default=None,
        help="Claim to verify (e.g. 'Added error handling to parser')",
    )
    parser.add_argument(
        "--outcome", default=None,
        help="Outcome file to verify claims from",
    )
    parser.add_argument(
        "--diff", default="HEAD~1",
        help="Git ref to diff against (default: HEAD~1)",
    )
    parser.add_argument(
        "--test", default=None,
        help="Test command to run (auto-detected if omitted)",
    )
    parser.add_argument(
        "--test-only", action="store_true",
        help="Only run tests, skip LLM verification",
    )
    parser.add_argument(
        "-m", "--model", default=None,
        help="LLM model to use (via model_choice)",
    )

    args = parser.parse_args(argv)
    project = find_project(args.workdir)
    ad = ensure_autodev_dir(project)

    results = {}

    # Get diff
    diff = get_git_diff(project, args.diff)
    results["diff_summary"] = f"{len(diff)} chars of diff" if diff else "No diff"

    # Run tests
    test_result = check_test_passes(project, args.test)
    results["tests"] = test_result

    if not args.test_only:
        # Get claim
        claim = args.claim
        if not claim and args.outcome:
            outcome_path = Path(args.outcome)
            if outcome_path.exists():
                claim = outcome_path.read_text()[:2000]
        if not claim:
            # Try to read from .autodev/outcome.md
            outcome_file = ad / "outcome.md"
            if outcome_file.exists():
                claim = outcome_file.read_text()[:2000]

        if claim:
            verify_result = verify_claim(project, claim, args.model)
            results["verification"] = verify_result
        else:
            results["verification"] = {"skipped": True, "reason": "No claim to verify"}

    # Write state
    write_state(project, "verify", results)

    # Determine overall status
    tests_ok = test_result.get("status") in ("pass", "skipped")
    claim_ok = results.get("verification", {}).get("verified", True)
    overall = tests_ok and claim_ok

    if args.json_output:
        output(results, json_mode=True)
    elif not args.quiet:
        status = "PASS" if overall else "FAIL"
        output(f"[{status}] Verification result:")
        output(f"  Tests: {test_result.get('status', 'unknown')}")
        if "verification" in results and not results["verification"].get("skipped"):
            v = results["verification"]
            output(f"  Claim verified: {v.get('verified', '?')} (confidence: {v.get('confidence', '?')})")
            if v.get("gaps"):
                output(f"  Gaps: {v['gaps']}")

    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main() or 0)
