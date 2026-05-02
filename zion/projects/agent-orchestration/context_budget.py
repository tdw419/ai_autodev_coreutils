#!/usr/bin/env python3
"""
Context Window Optimization (Smart Zone) for the Hermes Agent Orchestrator.

The Ralph Wiggum pattern: AI models exhibit reasoning quality decay after
reaching 30-60% of their context window. This module manages context budgets
so agents always operate in the "smart zone."

Key capabilities:
- Estimate token counts for prompt components
- Prioritize which context to include when budget is tight
- Truncate or summarize context that exceeds budget
- Track actual context usage per AI node run for tuning

Usage:
    python3 context_budget.py --estimate --text "test string"
    python3 context_budget.py --build --components task.txt,guide.md,context.json
    python3 context_budget.py --stats --last 20
    python3 context_budget.py --check --budget 80000 --components task.txt,guide.md

Based on the research insight: "The strategic advantage no longer belongs
to those with the largest models, but to those with the most effective
system around them."
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

sys.path.insert(0, str(Path(__file__).parent))


# ─── Token estimation ────────────────────────────────────────────────────────

# Rough token ratios for different languages
TOKEN_RATIOS = {
    "code": 0.35,       # ~3.5 chars per token for code
    "prose": 0.25,      # ~4 chars per token for prose
    "markdown": 0.30,   # ~3.3 chars per token for markdown (mixed)
    "json": 0.33,       # ~3 chars per token for JSON
    "default": 0.28,    # ~3.5 chars per token default
}

# Model context window sizes (input tokens)
MODEL_WINDOWS = {
    "claude-sonnet-4": 200000,
    "claude-opus-4": 200000,
    "claude-3.5-sonnet": 200000,
    "gpt-4o": 128000,
    "gpt-4-turbo": 128000,
    "gpt-4": 8192,
    "default": 200000,
}

# Default: use 80% of window for input (leave 20% for response)
DEFAULT_BUDGET_RATIO = 0.80

# Smart zone: optimal reasoning at 30-60% of window
SMART_ZONE_MIN = 0.30
SMART_ZONE_MAX = 0.60

# Warning threshold: if truncating more than this, log a warning
TRUNCATION_WARNING_THRESHOLD = 0.30


def estimate_tokens(text: str, content_type: str = "default") -> int:
    """
    Estimate token count for a string.

    Uses character-based heuristics calibrated to typical LLM tokenizers.
    Accuracy is within ~15% for English text and code.
    """
    if not text:
        return 0

    ratio = TOKEN_RATIOS.get(content_type, TOKEN_RATIOS["default"])
    return int(len(text) * ratio)


def detect_content_type(text: str) -> str:
    """Detect the likely content type of a string."""
    # Check for JSON
    text_stripped = text.strip()
    if text_stripped.startswith("{") or text_stripped.startswith("["):
        try:
            json.loads(text)
            return "json"
        except (json.JSONDecodeError, ValueError):
            pass

    # Check for code (high ratio of special characters, indentation)
    code_indicators = sum(1 for c in text if c in "({[]})=;:<>+-*/\\#\"'@\t")
    if code_indicators / max(len(text), 1) > 0.1:
        return "code"

    # Check for markdown
    md_indicators = sum(1 for c in text if c in "#*-|>`~")
    if md_indicators / max(len(text), 1) > 0.02:
        return "markdown"

    return "prose"


# ─── Prompt Component ────────────────────────────────────────────────────────

@dataclass
class PromptComponent:
    """A piece of prompt content with metadata for budget management."""
    name: str
    content: str
    priority: int  # 1 = highest (never truncate), 5 = lowest (truncate first)
    content_type: str = "default"
    required: bool = False  # If True, never truncate

    @property
    def token_count(self) -> int:
        return estimate_tokens(self.content, self.content_type)

    def truncate(self, max_tokens: int) -> str:
        """Truncate content to fit within max_tokens."""
        if self.token_count <= max_tokens:
            return self.content

        ratio = TOKEN_RATIOS.get(self.content_type, TOKEN_RATIOS["default"])
        max_chars = int(max_tokens / ratio)

        if self.content_type == "json":
            # Try to truncate JSON by removing less important fields
            return self._truncate_json(max_chars)

        # For text, truncate at sentence/line boundary
        truncated = self.content[:max_chars]
        # Find last newline
        last_nl = truncated.rfind("\n")
        if last_nl > max_chars * 0.5:
            truncated = truncated[:last_nl]
        # Find last sentence end
        last_dot = truncated.rfind(".")
        if last_dot > max_chars * 0.5:
            truncated = truncated[:last_dot + 1]

        return truncated + f"\n\n[... truncated, original was {self.token_count} tokens ...]"

    def _truncate_json(self, max_chars: int) -> str:
        """Truncate JSON by keeping structure but limiting values."""
        try:
            data = json.loads(self.content)
            truncated = self._truncate_json_obj(data, max_chars * 3)  # 3x for JSON overhead
            return json.dumps(truncated, indent=2)
        except (json.JSONDecodeError, TypeError):
            return self.content[:max_chars]

    def _truncate_json_obj(self, obj: Any, budget: int) -> Any:
        """Recursively truncate a JSON object to fit within a character budget."""
        s = json.dumps(obj)
        if len(s) <= budget:
            return obj

        if isinstance(obj, dict):
            # Keep top-level keys but truncate values
            result = {}
            for k, v in list(obj.items())[:10]:  # Max 10 keys
                result[k] = self._truncate_json_obj(v, budget // 10)
            return result
        elif isinstance(obj, list):
            return [self._truncate_json_obj(item, budget // 5) for item in obj[:5]]
        elif isinstance(obj, str):
            return obj[:budget // 4] + "..." if len(obj) > budget // 4 else obj
        return obj


# ─── Context Budget Manager ─────────────────────────────────────────────────

@dataclass
class BudgetResult:
    """Result of fitting components to a budget."""
    components: list[PromptComponent]
    total_tokens: int
    budget: int
    truncations: list[dict] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    smart_zone: bool = False

    def to_dict(self) -> dict:
        return {
            "total_tokens": self.total_tokens,
            "budget": self.budget,
            "utilization": round(self.total_tokens / self.budget, 3) if self.budget else 0,
            "in_smart_zone": self.smart_zone,
            "truncations": self.truncations,
            "warnings": self.warnings,
            "component_tokens": [
                {"name": c.name, "tokens": c.token_count, "priority": c.priority}
                for c in self.components
            ],
        }


class ContextBudgetManager:
    """
    Manages context budget for AI node prompts.

    Given a list of prompt components with priorities, fits them into
    the available token budget by truncating lowest-priority components first.
    """

    def __init__(
        self,
        budget_tokens: Optional[int] = None,
        model: str = "default",
        budget_ratio: float = DEFAULT_BUDGET_RATIO,
    ):
        if budget_tokens:
            self.budget = budget_tokens
        else:
            window = MODEL_WINDOWS.get(model, MODEL_WINDOWS["default"])
            self.budget = int(window * budget_ratio)
        self.model = model
        self.budget_ratio = budget_ratio

    def fit_to_budget(
        self,
        components: list[PromptComponent],
        respect_required: bool = True,
    ) -> BudgetResult:
        """
        Fit components into the budget, truncating lowest-priority first.

        Required components (priority 1 or required=True) are never truncated.
        """
        # Separate required and optional components
        required = [c for c in components if c.required or c.priority == 1]
        optional = sorted(
            [c for c in components if not c.required and c.priority != 1],
            key=lambda c: -c.priority,  # Truncate lowest priority first
        )

        # Calculate required token cost
        required_tokens = sum(c.token_count for c in required)

        if required_tokens > self.budget:
            # Even required components exceed budget -- truncate proportionally
            warnings = [f"Required components ({required_tokens} tokens) exceed budget ({self.budget}). Proportional truncation applied."]
            scale = self.budget / required_tokens
            for c in required:
                c.content = c.truncate(int(c.token_count * scale))
            return BudgetResult(
                components=required + optional,
                total_tokens=sum(c.token_count for c in required),
                budget=self.budget,
                warnings=warnings,
            )

        # Budget remaining for optional components
        remaining = self.budget - required_tokens
        truncations = []
        warnings = []

        for c in optional:
            if c.token_count <= remaining:
                remaining -= c.token_count
            else:
                # Truncate this component to fit remaining budget
                original_tokens = c.token_count
                c.content = c.truncate(remaining)
                actual_tokens = c.token_count
                saved = original_tokens - actual_tokens
                if saved > 0:
                    truncations.append({
                        "component": c.name,
                        "original_tokens": original_tokens,
                        "truncated_tokens": actual_tokens,
                        "saved": saved,
                    })
                remaining = max(0, remaining - actual_tokens)
                # Continue to next component instead of breaking
                # (there might be more room after truncation)

        # Calculate final totals
        all_components = required + optional
        total_tokens = sum(c.token_count for c in all_components)

        # Hard cap: if still over budget, force-truncate remaining components to empty
        if total_tokens > self.budget:
            warnings.append(f"Post-truncation total ({total_tokens}) still exceeds budget ({self.budget}). Force-truncating lowest-priority remaining components.")
            for c in reversed(optional):
                if total_tokens <= self.budget:
                    break
                total_tokens -= c.token_count
                c.content = f"[{c.name}: truncated due to budget constraints]"
                truncations.append({
                    "component": c.name,
                    "original_tokens": c.token_count,
                    "truncated_tokens": 0,
                    "saved": c.token_count,
                })
            total_tokens = sum(c.token_count for c in required + optional)

        # Check truncation warning
        total_original = sum(estimate_tokens("dummy" + "x" * 100) for _ in truncations)  # rough
        truncation_pct = sum(t["saved"] for t in truncations) / max(self.budget, 1)
        if truncation_pct > TRUNCATION_WARNING_THRESHOLD:
            warnings.append(
                f"Truncated {truncation_pct * 100:.0f}% of context budget. "
                f"Consider increasing budget or reducing input size."
            )

        # Check smart zone
        utilization = total_tokens / self.budget if self.budget else 0
        smart_zone = SMART_ZONE_MIN <= utilization <= SMART_ZONE_MAX

        return BudgetResult(
            components=all_components,
            total_tokens=total_tokens,
            budget=self.budget,
            truncations=truncations,
            warnings=warnings,
            smart_zone=smart_zone,
        )

    def build_prompt(self, components: list[PromptComponent]) -> BudgetResult:
        """Fit components to budget and concatenate into a single prompt string."""
        result = self.fit_to_budget(components)
        return result

    def check_health(self) -> dict:
        """Return budget configuration info."""
        window = MODEL_WINDOWS.get(self.model, MODEL_WINDOWS["default"])
        return {
            "model": self.model,
            "context_window": window,
            "budget": self.budget,
            "budget_ratio": self.budget_ratio,
            "smart_zone_range": f"{SMART_ZONE_MIN * 100:.0f}%-{SMART_ZONE_MAX * 100:.0f}% of budget",
            "recommended_tokens_for_smart_zone": (
                int(window * SMART_ZONE_MIN),
                int(window * SMART_ZONE_MAX),
            ),
        }


# ─── Context Usage Analytics ─────────────────────────────────────────────────

def analyze_context_usage(runs: list[dict]) -> dict:
    """
    Analyze context usage patterns from execution logs.

    Looks for budget fields in node results.
    """
    if not runs:
        return {"error": "No runs to analyze"}

    node_stats = defaultdict(lambda: {"count": 0, "total_tokens": 0, "max_tokens": 0, "budget_exceeded": 0})

    for run in runs:
        for r in run.get("results", []):
            node_id = r.get("node_id", "unknown")
            budget_info = r.get("budget", {})

            if budget_info:
                node_stats[node_id]["count"] += 1
                tokens = budget_info.get("total_tokens", 0)
                node_stats[node_id]["total_tokens"] += tokens
                node_stats[node_id]["max_tokens"] = max(node_stats[node_id]["max_tokens"], tokens)
                if budget_info.get("truncations"):
                    node_stats[node_id]["budget_exceeded"] += 1

    report = {"nodes": {}}
    for node_id, stats in node_stats.items():
        report["nodes"][node_id] = {
            "runs": stats["count"],
            "avg_tokens": round(stats["total_tokens"] / stats["count"]) if stats["count"] else 0,
            "max_tokens": stats["max_tokens"],
            "budget_exceeded_pct": round(
                stats["budget_exceeded"] / stats["count"] * 100, 1
            ) if stats["count"] else 0,
        }

    return report


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Context Window Optimization (Smart Zone)")
    parser.add_argument("--estimate", action="store_true", help="Estimate tokens for a text")
    parser.add_argument("--text", "-t", help="Text to estimate tokens for")
    parser.add_argument("--file", "-f", help="File to estimate tokens for")
    parser.add_argument("--build", action="store_true", help="Build prompt from components")
    parser.add_argument("--components", "-c", help="Comma-separated list of component files (name:priority:file)")
    parser.add_argument("--budget", "-b", type=int, help="Token budget (default: model-dependent)")
    parser.add_argument("--model", "-m", default="claude-sonnet-4", help="Model name for window size")
    parser.add_argument("--check", action="store_true", help="Check if components fit in budget")
    parser.add_argument("--stats", action="store_true", help="Show context usage analytics")
    parser.add_argument("--last", "-n", type=int, default=20, help="Number of runs for stats")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Output as JSON")
    parser.add_argument("--health", action="store_true", help="Show budget configuration")

    args = parser.parse_args()

    if args.health:
        mgr = ContextBudgetManager(budget_tokens=args.budget, model=args.model)
        health = mgr.check_health()
        if args.json_output:
            print(json.dumps(health, indent=2))
        else:
            print("## Context Budget Configuration")
            print(f"  Model: {health['model']}")
            print(f"  Context window: {health['context_window']:,} tokens")
            print(f"  Budget: {health['budget']:,} tokens ({health['budget_ratio'] * 100:.0f}% of window)")
            print(f"  Smart zone: {health['smart_zone_range']}")
            low, high = health["recommended_tokens_for_smart_zone"]
            print(f"  Recommended prompt size: {low:,}-{high:,} tokens")
        return

    if args.estimate:
        text = args.text or ""
        if args.file:
            text = Path(args.file).read_text()

        content_type = detect_content_type(text)
        tokens = estimate_tokens(text, content_type)

        if args.json_output:
            print(json.dumps({
                "text_length": len(text),
                "content_type": content_type,
                "estimated_tokens": tokens,
                "chars_per_token": round(len(text) / tokens, 1) if tokens else 0,
            }, indent=2))
        else:
            print(f"  Text length: {len(text):,} chars")
            print(f"  Content type: {content_type}")
            print(f"  Estimated tokens: {tokens:,}")
            print(f"  Chars per token: {round(len(text) / tokens, 1) if tokens else 0}")
        return

    if args.build or args.check:
        if not args.components:
            parser.error("--components required with --build or --check")

        components = []
        for comp_spec in args.components.split(","):
            parts = comp_spec.strip().split(":")
            if len(parts) == 3:
                name, priority, filepath = parts
                priority = int(priority)
            elif len(parts) == 2:
                name, filepath = parts
                priority = 3
            else:
                filepath = parts[0]
                name = Path(filepath).stem
                priority = 3

            content = Path(filepath).read_text()
            content_type = detect_content_type(content)
            components.append(PromptComponent(
                name=name,
                content=content,
                priority=priority,
                content_type=content_type,
            ))

        mgr = ContextBudgetManager(budget_tokens=args.budget, model=args.model)
        result = mgr.fit_to_budget(components)

        if args.json_output:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print(f"## Budget: {result.budget:,} tokens")
            print(f"## Total: {result.total_tokens:,} tokens ({result.total_tokens / result.budget * 100:.0f}% of budget)")
            print(f"## Smart zone: {'✅ Yes' if result.smart_zone else '❌ No'}")
            print()

            for comp in result.components:
                icon = "🔒" if comp.required or comp.priority == 1 else f"P{comp.priority}"
                print(f"  {icon} {comp.name}: {comp.token_count:,} tokens")

            if result.truncations:
                print("\n## Truncations:")
                for t in result.truncations:
                    print(f"  ✂️  {t['component']}: {t['original_tokens']} -> {t['truncated_tokens']} tokens (saved {t['saved']})")

            if result.warnings:
                print("\n## Warnings:")
                for w in result.warnings:
                    print(f"  ⚠️  {w}")
        return

    if args.stats:
        try:
            from execution_log import list_runs, get_run
        except ImportError:
            print("Cannot import execution_log. Stats require the execution log module.", file=sys.stderr)
            sys.exit(1)

        runs = []
        for r in list_runs(limit=args.last):
            full = get_run(r["run_id"])
            if full:
                runs.append(full)

        report = analyze_context_usage(runs)
        if args.json_output:
            print(json.dumps(report, indent=2))
        else:
            if "error" in report:
                print(report["error"])
            else:
                print("## Context Usage Analytics")
                for node_id, stats in report["nodes"].items():
                    print(f"  {node_id}: avg {stats['avg_tokens']:,} tokens, "
                          f"max {stats['max_tokens']:,}, "
                          f"budget exceeded {stats['budget_exceeded_pct']}%")
        return

    parser.error("One of --estimate, --build, --check, --stats, --health is required")


if __name__ == "__main__":
    main()
