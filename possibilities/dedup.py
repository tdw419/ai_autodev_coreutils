"""Deduplication of similar ideas in the possibility tree."""

import logging
from dataclasses import dataclass
from .models import PossibilityNode
from .llm import LLMClient, parse_json_response

logger = logging.getLogger(__name__)


@dataclass
class DupResult:
    """Result of a dedup check."""
    is_duplicate: bool
    duplicate_of: str = ""
    similarity: float = 0.0
    reason: str = ""


class Deduplicator:
    """Check new ideas against existing ones to avoid redundant exploration."""

    def __init__(self, llm: LLMClient, threshold: float = 0.85):
        self.llm = llm
        self.threshold = threshold

    def check(
        self, new: PossibilityNode, existing: list[dict]
    ) -> DupResult:
        """Check if a new idea duplicates any existing idea."""
        if not existing:
            return DupResult(is_duplicate=False)

        # Quick heuristic passes first (cheap, no LLM call)
        exact = self._exact_match(new, existing)
        if exact:
            return exact

        substring = self._substring_match(new, existing)
        if substring:
            return substring

        # Semantic LLM check as fallback
        return self._semantic_check(new, existing)

    # -- Heuristic checks ---------------------------------------------------

    def _exact_match(
        self, new: PossibilityNode, existing: list[dict]
    ) -> DupResult | None:
        """Return a DupResult if any existing idea has the exact same title."""
        new_title = new.title.lower().strip()
        for e in existing:
            if e["title"].lower().strip() == new_title:
                return DupResult(True, e["title"], 1.0, "Exact title match")
        return None

    def _substring_match(
        self, new: PossibilityNode, existing: list[dict]
    ) -> DupResult | None:
        """Return a DupResult if any existing title is a near-identical substring."""
        new_title = new.title.lower().strip()
        if len(new_title) <= 10:
            return None
        for e in existing:
            existing_title = e["title"].lower().strip()
            if (
                len(existing_title) > 10
                and (new_title in existing_title or existing_title in new_title)
            ):
                return DupResult(
                    True, e["title"], 0.9, "Near-identical title"
                )
        return None

    # -- LLM semantic check -------------------------------------------------

    def _semantic_check(
        self, new: PossibilityNode, existing: list[dict]
    ) -> DupResult:
        """Use the LLM to semantically compare against recent existing ideas."""
        recent = existing[-20:]
        existing_text = "\n".join(
            f"  - {e['title']}: {e.get('description', '')[:100]}"
            for e in recent
        )

        from .prompts import DEDUP_PROMPT
        prompt = DEDUP_PROMPT.format(
            new_title=new.title,
            new_desc=new.description,
            existing_ideas=existing_text,
        )

        try:
            raw = self.llm.generate(prompt)
            results = parse_json_response(raw)
            if results:
                return self._parse_llm_result(results[0])
        except Exception as exc:
            logger.warning("Dedup LLM check failed for '%s': %s: %s",
                           new.title, type(exc).__name__, exc)

        return DupResult(is_duplicate=False)

    def _parse_llm_result(self, data: dict) -> DupResult:
        """Convert raw LLM JSON into a DupResult, applying the similarity threshold."""
        is_dup = data.get("is_duplicate", False)
        similarity = data.get("similarity", 0.0)
        return DupResult(
            is_duplicate=is_dup and similarity >= self.threshold,
            duplicate_of=data.get("duplicate_of", ""),
            similarity=similarity,
            reason=data.get("reason", ""),
        )
