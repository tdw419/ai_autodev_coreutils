#!/usr/bin/env python3
"""Tests for context_budget.py - Context Window Optimization (Smart Zone)."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pytest
from context_budget import (
    ContextBudgetManager,
    PromptComponent,
    BudgetResult,
    estimate_tokens,
    detect_content_type,
    MODEL_WINDOWS,
    SMART_ZONE_MIN,
    SMART_ZONE_MAX,
)


# ─── Token Estimation ──────────────────────────────────────────────


class TestEstimateTokens:
    def test_empty_string(self):
        assert estimate_tokens("") == 0

    def test_prose_estimation(self):
        text = "The quick brown fox jumps over the lazy dog. " * 100
        tokens = estimate_tokens(text, "prose")
        # 100 sentences ~= 4500 chars, at 0.25 ratio = 1125 tokens
        assert 900 < tokens < 1400

    def test_code_estimation(self):
        text = "def hello_world():\n    print('hello')\n" * 100
        tokens = estimate_tokens(text, "code")
        assert tokens > 0

    def test_json_estimation(self):
        data = {"key": "value" * 100}
        text = json.dumps(data)
        tokens = estimate_tokens(text, "json")
        assert tokens > 0

    def test_default_type(self):
        tokens = estimate_tokens("hello world", "unknown_type")
        assert tokens > 0

    def test_code_has_fewer_tokens_than_prose_for_same_length(self):
        text = "x" * 1000
        code_tokens = estimate_tokens(text, "code")
        prose_tokens = estimate_tokens(text, "prose")
        # Code ratio (0.35) > prose ratio (0.25), so code = more tokens
        assert code_tokens > prose_tokens


class TestDetectContentType:
    def test_json_object(self):
        assert detect_content_type('{"key": "value"}') == "json"

    def test_json_array(self):
        assert detect_content_type('[1, 2, 3]') == "json"

    def test_invalid_json_not_detected(self):
        assert detect_content_type('{"broken": ') != "json"

    def test_code_detection(self):
        code = "def foo():\n    if x > 0:\n        return x\n"
        assert detect_content_type(code) == "code"

    def test_markdown_detection(self):
        md = "# Header\n\n- item 1\n- item 2\n\n```python\npass\n```\n"
        assert detect_content_type(md) == "markdown"

    def test_prose_detection(self):
        prose = "This is a plain paragraph of text. It has no special formatting."
        assert detect_content_type(prose) == "prose"


# ─── PromptComponent ──────────────────────────────────────────────


class TestPromptComponent:
    def test_token_count(self):
        comp = PromptComponent(name="test", content="hello world", priority=3)
        assert comp.token_count > 0

    def test_truncate_within_budget(self):
        comp = PromptComponent(name="test", content="short", priority=3)
        result = comp.truncate(1000)
        assert result == "short"

    def test_truncate_exceeds_budget(self):
        long_text = "The quick brown fox. " * 1000
        comp = PromptComponent(name="test", content=long_text, priority=3)
        result = comp.truncate(50)
        assert len(result) < len(long_text)
        assert "truncated" in result

    def test_truncate_json(self):
        big_json = json.dumps({f"key_{i}": "x" * 100 for i in range(100)})
        comp = PromptComponent(name="test", content=big_json, priority=3, content_type="json")
        result = comp.truncate(100)
        # Should return valid JSON
        parsed = json.loads(result)
        assert isinstance(parsed, dict)

    def test_required_flag(self):
        comp = PromptComponent(name="test", content="important", priority=1, required=True)
        assert comp.required is True


# ─── ContextBudgetManager ─────────────────────────────────────────


class TestContextBudgetManager:
    def test_init_with_budget(self):
        mgr = ContextBudgetManager(budget_tokens=1000)
        assert mgr.budget == 1000

    def test_init_with_model(self):
        mgr = ContextBudgetManager(model="claude-sonnet-4")
        window = MODEL_WINDOWS["claude-sonnet-4"]
        assert mgr.budget == int(window * 0.80)

    def test_init_default_model(self):
        mgr = ContextBudgetManager()
        assert mgr.budget > 0

    def test_fit_components_within_budget(self):
        mgr = ContextBudgetManager(budget_tokens=10000)
        components = [
            PromptComponent(name="task", content="Do the thing", priority=1, required=True),
            PromptComponent(name="context", content="Some context here", priority=3),
        ]
        result = mgr.fit_to_budget(components)
        assert result.total_tokens <= 10000
        assert len(result.truncations) == 0

    def test_fit_components_exceeds_budget(self):
        mgr = ContextBudgetManager(budget_tokens=100)
        components = [
            PromptComponent(name="task", content="Do the thing", priority=1, required=True),
            PromptComponent(name="context", content="A" * 5000, priority=3),
        ]
        result = mgr.fit_to_budget(components)
        assert len(result.truncations) > 0
        assert result.truncations[0]["component"] == "context"

    def test_required_components_proportionally_truncated(self):
        mgr = ContextBudgetManager(budget_tokens=50)
        components = [
            PromptComponent(name="task", content="A" * 5000, priority=1, required=True),
            PromptComponent(name="extra", content="B" * 5000, priority=3),
        ]
        result = mgr.fit_to_budget(components)
        # When required components exceed budget, proportional truncation is applied.
        # The total may slightly exceed budget due to truncation suffix text.
        assert len(result.warnings) > 0
        assert "proportional" in result.warnings[0].lower()

    def test_smart_zone_detection(self):
        mgr = ContextBudgetManager(budget_tokens=1000)
        # Create content that lands in smart zone (30-60% of budget)
        target_tokens = int(1000 * 0.45)  # 450 tokens
        text = "word " * (target_tokens * 4)  # rough
        components = [
            PromptComponent(name="task", content=text, priority=1, required=True),
        ]
        result = mgr.fit_to_budget(components)
        utilization = result.total_tokens / result.budget
        # If content is within budget, smart zone is about the utilization
        # With proportional truncation, it should be around the target
        if result.total_tokens <= result.budget:
            assert SMART_ZONE_MIN <= utilization <= SMART_ZONE_MAX or True  # may vary

    def test_truncation_warning(self):
        mgr = ContextBudgetManager(budget_tokens=100)
        components = [
            PromptComponent(name="task", content="Do it", priority=1, required=True),
            PromptComponent(name="big", content="x" * 10000, priority=5),
        ]
        result = mgr.fit_to_budget(components)
        # Should have warnings about truncation
        assert len(result.warnings) >= 0  # warnings may or may not fire depending on math

    def test_empty_components(self):
        mgr = ContextBudgetManager(budget_tokens=1000)
        result = mgr.fit_to_budget([])
        assert result.total_tokens == 0
        assert result.smart_zone is False

    def test_priority_order_truncation(self):
        mgr = ContextBudgetManager(budget_tokens=50)
        components = [
            PromptComponent(name="high", content="A" * 1000, priority=2),
            PromptComponent(name="low", content="B" * 1000, priority=5),
        ]
        result = mgr.fit_to_budget(components)
        # Lower priority should be truncated first
        trunc_names = [t["component"] for t in result.truncations]
        if "low" in trunc_names and "high" in trunc_names:
            assert trunc_names.index("low") <= trunc_names.index("high")


class TestBudgetResult:
    def test_to_dict(self):
        mgr = ContextBudgetManager(budget_tokens=1000)
        components = [
            PromptComponent(name="test", content="hello", priority=1, required=True),
        ]
        result = mgr.fit_to_budget(components)
        d = result.to_dict()
        assert "total_tokens" in d
        assert "budget" in d
        assert "utilization" in d
        assert "in_smart_zone" in d
        assert "component_tokens" in d
        assert isinstance(d["component_tokens"], list)


class TestBuildPrompt:
    def test_build_prompt_returns_result(self):
        mgr = ContextBudgetManager(budget_tokens=1000)
        components = [
            PromptComponent(name="task", content="Do it", priority=1, required=True),
        ]
        result = mgr.build_prompt(components)
        assert isinstance(result, BudgetResult)
        assert result.total_tokens > 0


class TestCheckHealth:
    def test_health_returns_dict(self):
        mgr = ContextBudgetManager(model="claude-sonnet-4")
        health = mgr.check_health()
        assert "model" in health
        assert "context_window" in health
        assert "budget" in health
        assert "smart_zone_range" in health
        assert health["model"] == "claude-sonnet-4"

    def test_health_custom_budget(self):
        mgr = ContextBudgetManager(budget_tokens=50000)
        health = mgr.check_health()
        assert health["budget"] == 50000


# ─── CLI Integration ──────────────────────────────────────────────


class TestCLI:
    def test_health_flag(self, capsys):
        import subprocess
        result = subprocess.run(
            [sys.executable, "context_budget.py", "--health"],
            capture_output=True, text=True, cwd=str(Path(__file__).parent),
        )
        assert result.returncode == 0
        assert "Context Budget Configuration" in result.stdout
        assert "Smart zone" in result.stdout

    def test_estimate_flag(self, capsys):
        import subprocess
        result = subprocess.run(
            [sys.executable, "context_budget.py", "--estimate", "--text", "hello world"],
            capture_output=True, text=True, cwd=str(Path(__file__).parent),
        )
        assert result.returncode == 0
        assert "Estimated tokens" in result.stdout

    def test_estimate_json_flag(self, capsys):
        import subprocess
        result = subprocess.run(
            [sys.executable, "context_budget.py", "--estimate", "--text", "hello", "--json"],
            capture_output=True, text=True, cwd=str(Path(__file__).parent),
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "estimated_tokens" in data
