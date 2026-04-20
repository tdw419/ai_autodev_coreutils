"""Tests for dedup module -- duplicate idea detection."""

import pytest

from possibilities.dedup import DupResult, Deduplicator
from possibilities.models import PossibilityNode


# ---------------------------------------------------------------------------
# DupResult
# ---------------------------------------------------------------------------

class TestDupResult:
    def test_defaults(self):
        r = DupResult(is_duplicate=False)
        assert r.is_duplicate is False
        assert r.duplicate_of == ""
        assert r.similarity == 0.0
        assert r.reason == ""

    def test_full(self):
        r = DupResult(True, "Some Idea", 0.95, "Near identical")
        assert r.is_duplicate is True
        assert r.duplicate_of == "Some Idea"


# ---------------------------------------------------------------------------
# Deduplicator.check -- exact match
# ---------------------------------------------------------------------------

class TestDeduplicatorExactMatch:
    def test_exact_title_match(self):
        dedup = Deduplicator(llm=None, threshold=0.85)
        new = PossibilityNode(title="Plugin System")
        existing = [{"title": "Plugin System", "description": "Add plugins"}]
        result = dedup.check(new, existing)
        assert result.is_duplicate is True
        assert result.similarity == 1.0
        assert "Exact title match" in result.reason

    def test_case_insensitive_match(self):
        dedup = Deduplicator(llm=None, threshold=0.85)
        new = PossibilityNode(title="plugin system")
        existing = [{"title": "Plugin System", "description": ""}]
        result = dedup.check(new, existing)
        assert result.is_duplicate is True

    def test_whitespace_stripped(self):
        dedup = Deduplicator(llm=None, threshold=0.85)
        new = PossibilityNode(title="  Plugin System  ")
        existing = [{"title": "Plugin System", "description": ""}]
        result = dedup.check(new, existing)
        assert result.is_duplicate is True


# ---------------------------------------------------------------------------
# Deduplicator.check -- substring match
# ---------------------------------------------------------------------------

class TestDeduplicatorSubstringMatch:
    def test_substring_match(self):
        dedup = Deduplicator(llm=None, threshold=0.85)
        new = PossibilityNode(title="Build a plugin system for extensions")
        existing = [{"title": "Build a plugin system for extensions and more", "description": ""}]
        result = dedup.check(new, existing)
        assert result.is_duplicate is True
        assert result.similarity == 0.9

    def test_short_titles_skip_substring(self):
        """Titles under 10 chars skip substring check."""
        dedup = Deduplicator(llm=None, threshold=0.85)
        new = PossibilityNode(title="short")
        existing = [{"title": "short", "description": ""}]
        result = dedup.check(new, existing)
        # Still matches via exact match
        assert result.is_duplicate is True


# ---------------------------------------------------------------------------
# Deduplicator.check -- empty existing
# ---------------------------------------------------------------------------

class TestDeduplicatorEmpty:
    def test_no_existing_ideas(self):
        dedup = Deduplicator(llm=None, threshold=0.85)
        new = PossibilityNode(title="New Idea")
        result = dedup.check(new, [])
        assert result.is_duplicate is False


# ---------------------------------------------------------------------------
# Deduplicator.check -- LLM-based (mocked)
# ---------------------------------------------------------------------------

class TestDeduplicatorLLM:
    def test_llm_duplicate_above_threshold(self, monkeypatch):
        dedup = Deduplicator(llm=None, threshold=0.85)

        class FakeLLM:
            def generate(self, prompt):
                return '{"is_duplicate": true, "similarity": 0.9, "duplicate_of": "X", "reason": "Same"}'

        dedup.llm = FakeLLM()
        new = PossibilityNode(title="Different Title", description="Something")
        existing = [{"title": "X", "description": "Else"}]
        result = dedup.check(new, existing)
        assert result.is_duplicate is True
        assert result.similarity == 0.9

    def test_llm_duplicate_below_threshold(self, monkeypatch):
        dedup = Deduplicator(llm=None, threshold=0.85)

        class FakeLLM:
            def generate(self, prompt):
                return '{"is_duplicate": true, "similarity": 0.5, "duplicate_of": "", "reason": "Kinda"}'

        dedup.llm = FakeLLM()
        new = PossibilityNode(title="Different Title", description="Something")
        existing = [{"title": "X", "description": "Else"}]
        result = dedup.check(new, existing)
        # is_duplicate=True but similarity < threshold -> not a dup
        assert result.is_duplicate is False

    def test_llm_not_duplicate(self, monkeypatch):
        dedup = Deduplicator(llm=None, threshold=0.85)

        class FakeLLM:
            def generate(self, prompt):
                return '{"is_duplicate": false, "similarity": 0.2, "reason": "Different"}'

        dedup.llm = FakeLLM()
        new = PossibilityNode(title="Different Title", description="Something")
        existing = [{"title": "X", "description": "Else"}]
        result = dedup.check(new, existing)
        assert result.is_duplicate is False

    def test_llm_failure_keeps_idea(self, monkeypatch):
        """If the LLM call fails, the idea is kept (not marked as dup)."""
        dedup = Deduplicator(llm=None, threshold=0.85)

        class BrokenLLM:
            def generate(self, prompt):
                raise RuntimeError("LLM down")

        dedup.llm = BrokenLLM()
        new = PossibilityNode(title="Different Title", description="Something")
        existing = [{"title": "X", "description": "Else"}]
        result = dedup.check(new, existing)
        assert result.is_duplicate is False

    def test_llm_invalid_json_keeps_idea(self, monkeypatch):
        dedup = Deduplicator(llm=None, threshold=0.85)

        class GarbageLLM:
            def generate(self, prompt):
                return "not json at all"

        dedup.llm = GarbageLLM()
        new = PossibilityNode(title="Different Title", description="Something")
        existing = [{"title": "X", "description": "Else"}]
        result = dedup.check(new, existing)
        assert result.is_duplicate is False


# ---------------------------------------------------------------------------
# Deduplicator -- only checks last 20 for LLM
# ---------------------------------------------------------------------------

class TestDeduplicatorCapping:
    def test_only_last_20_sent_to_llm(self, monkeypatch):
        """When there are >20 existing ideas, only last 20 go to LLM."""
        dedup = Deduplicator(llm=None, threshold=0.85)
        captured_prompts = []

        class SpyLLM:
            def generate(self, prompt):
                captured_prompts.append(prompt)
                return '{"is_duplicate": false, "similarity": 0.1, "reason": "No"}'

        dedup.llm = SpyLLM()
        existing = [{"title": f"Idea {i}", "description": f"Desc {i}"} for i in range(30)]
        new = PossibilityNode(title="Totally New", description="Brand new")
        dedup.check(new, existing)
        # The prompt should only contain the last 20 ideas
        assert len(captured_prompts) == 1
        assert "Idea 10" in captured_prompts[0]
        assert "Idea 0" not in captured_prompts[0]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
