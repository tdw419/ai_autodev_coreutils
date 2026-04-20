"""LLM wrapper for generating possibilities.

Delegates to model_choice for provider selection, fallback, caching,
and cost tracking. The LLMClient class is kept as a thin adapter so
that explorer.py and dedup.py continue to work unchanged.
"""

import json
import logging
import re
from typing import Any

logger = logging.getLogger(__name__)


class ParseError(Exception):
    """Raised when JSON response parsing fails completely."""


def _normalize_result(data: Any) -> list[dict]:
    """Normalize parsed JSON into list[dict].

    Accepts list or dict.  Lists are filtered to remove non-dict items
    (with a warning).  Anything else returns an empty list.
    """
    if isinstance(data, list):
        # Filter out non-dict items that would break downstream consumers
        # expecting list[dict].
        clean = [item for item in data if isinstance(item, dict)]
        if len(clean) != len(data):
            logger.warning(
                "Filtered %d non-dict item(s) from parsed list (had %d, kept %d)",
                len(data) - len(clean), len(data), len(clean),
            )
        return clean
    if isinstance(data, dict):
        return [data]
    logger.debug("Unexpected JSON type %s, returning []", type(data).__name__)
    return []


def _extract_markdown_blocks(text: str) -> list[str]:
    """Extract code block contents from markdown fences."""
    return re.findall(r'```(?:json)?\s*\n(.*?)```', text, re.DOTALL)


def _parse_markdown_fenced_json(text: str) -> list[dict] | None:
    """Try to parse JSON from markdown code fences.

    Returns parsed list[dict] on first successful parse, or None.
    Catches JSON errors and unexpected parsing failures (e.g. RecursionError
    from pathological nesting).
    """
    blocks = _extract_markdown_blocks(text)
    for i, block in enumerate(blocks):
        try:
            result = json.loads(block.strip())
            return _normalize_result(result)
        except json.JSONDecodeError as exc:
            logger.debug("Markdown block %d failed to parse: %s", i, exc)
            continue
        except (RecursionError, ValueError, TypeError) as exc:
            # Catch pathological inputs: deeply nested JSON, bad value types,
            # or structural issues that bypass JSONDecodeError.
            logger.warning("Unexpected error parsing markdown block %d: %s: %s",
                           i, type(exc).__name__, exc)
            continue
    return None


def _find_json_bounds(text: str) -> tuple[int, int] | None:
    """Find the bounds of the outermost JSON structure in text.

    Looks for the first '[' or '{' and finds its matching close.
    Returns (start, end+1) slice indices, or None.
    """
    # Find the first structural character
    start = -1
    open_char = None
    for i, ch in enumerate(text):
        if ch in ('{', '['):
            start = i
            open_char = ch
            break
    if start == -1:
        return None

    close_char = '}' if open_char == '{' else ']'
    depth = 0
    in_string = False
    escape = False

    for i in range(start, len(text)):
        ch = text[i]
        if escape:
            escape = False
            continue
        if ch == '\\' and in_string:
            escape = True
            continue
        if ch == '"' and not escape:
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == open_char:
            depth += 1
        elif ch == close_char:
            depth -= 1
            if depth == 0:
                return (start, i + 1)

    return None


def _parse_raw_json(text: str) -> list[dict] | None:
    """Try to find and parse raw JSON embedded in text.

    Uses balanced-bracket matching to avoid truncated trailing content.
    Returns parsed list[dict] or None.
    Catches both JSON errors and unexpected failures from malformed content.
    """
    bounds = _find_json_bounds(text)
    if bounds is None:
        return None
    start, end = bounds
    try:
        result = json.loads(text[start:end])
        return _normalize_result(result)
    except json.JSONDecodeError as exc:
        logger.debug("Raw JSON parse failed at %d-%d: %s", start, end, exc)
        return None
    except (RecursionError, ValueError, TypeError) as exc:
        logger.warning("Unexpected error parsing raw JSON at %d-%d: %s: %s",
                       start, end, type(exc).__name__, exc)
        return None


def _parse_whole_text(text: str) -> list[dict] | None:
    """Try to parse the entire text as JSON.

    Returns parsed list[dict] or None.
    Catches both JSON errors and unexpected failures.
    """
    try:
        result = json.loads(text)
        return _normalize_result(result)
    except json.JSONDecodeError as exc:
        logger.debug("Whole-text parse failed: %s", exc)
        return None
    except (RecursionError, ValueError, TypeError) as exc:
        logger.warning("Unexpected error in whole-text parse: %s: %s",
                       type(exc).__name__, exc)
        return None


# Safety limit: reject inputs larger than 10 MB to avoid OOM / CPU spikes.
_MAX_INPUT_CHARS = 10 * 1024 * 1024


def parse_json_response(text: str) -> list[dict]:
    """Extract JSON from an LLM response string.

    Tries multiple strategies in order:
      1. Markdown code fences (```json ... ```)
      2. Raw JSON embedded in surrounding text
      3. The entire text as-is

    Returns a list[dict]. Single dict results are wrapped in a list.
    Non-dict list items are filtered out.  Returns [] if no valid JSON
    can be extracted.

    Raises:
        TypeError: if `text` is not a string.
        ValueError: if `text` exceeds ``_MAX_INPUT_CHARS`` characters.

    Error handling notes:
        - Null bytes are silently stripped before parsing.
        - UnicodeEncodeError / UnicodeDecodeError during preprocessing
          are caught and result in [].
        - MemoryError from pathological inputs is caught and logged.
        - A top-level ``except Exception`` safety net ensures no
          unexpected error ever propagates to the caller.
    """
    if not isinstance(text, str):
        raise TypeError(
            f"parse_json_response expects str, got {type(text).__name__}"
        )

    if len(text) > _MAX_INPUT_CHARS:
        raise ValueError(
            f"Input text too large ({len(text)} chars, max {_MAX_INPUT_CHARS})"
        )

    try:
        text = text.strip()
    except (UnicodeDecodeError, UnicodeEncodeError) as exc:
        logger.error("Unicode error while stripping input: %s: %s",
                     type(exc).__name__, exc)
        return []

    # Null bytes cause json.loads to raise unexpected errors; strip them.
    if "\x00" in text:
        logger.warning("Stripping null bytes from input (%d chars)", len(text))
        try:
            text = text.replace("\x00", "")
        except (UnicodeDecodeError, UnicodeEncodeError) as exc:
            logger.error("Unicode error while stripping nulls: %s: %s",
                         type(exc).__name__, exc)
            return []

    if not text:
        logger.debug("Empty input text, returning []")
        return []

    try:
        # Strategy 1: markdown code fences
        if "```" in text:
            result = _parse_markdown_fenced_json(text)
            if result is not None:
                return result

        # Strategy 2: raw JSON embedded in text
        result = _parse_raw_json(text)
        if result is not None:
            return result

        # Strategy 3: entire text as JSON
        result = _parse_whole_text(text)
        if result is not None:
            return result
    except MemoryError:
        # Pathological input could exhaust memory during parsing.
        logger.error("MemoryError in parse_json_response (input %d chars)",
                     len(text))
        return []
    except Exception as exc:
        # Top-level safety net: unexpected errors should never propagate
        # from a parsing function — log and return empty rather than crash.
        logger.error("Unexpected error in parse_json_response: %s: %s",
                     type(exc).__name__, exc)
        return []

    logger.warning("All JSON parsing strategies failed for text (%d chars)", len(text))
    return []


class LLMClient:
    """Thin adapter over model_choice.generate / generate_json.

    If `model` is set, model_choice uses that exact model (ignoring
    complexity-based auto-selection).  If `model` is None or empty,
    model_choice picks the best available provider for the given
    complexity tier.
    """

    def __init__(self, model: str | None = None, temperature: float = 0.9,
                 complexity: str = "balanced"):
        self.model = model
        self.temperature = temperature
        self.complexity = complexity

    def generate(self, prompt: str) -> str:
        """Generate a raw text response via model_choice.

        Returns the model's text output, or an empty string on any error
        (network failures, provider timeouts, configuration issues).
        """
        from model_choice import generate as mc_generate
        kwargs = dict(
            prompt=prompt,
            temperature=self.temperature,
            max_tokens=3000,
            complexity=self.complexity,
        )
        if self.model:
            kwargs["model"] = self.model
        try:
            return mc_generate(**kwargs)
        except (ValueError, RuntimeError, ConnectionError, TimeoutError, OSError) as exc:
            logger.error("model_choice.generate failed: %s: %s",
                         type(exc).__name__, exc)
            return ""
        except Exception as exc:
            # Catch-all for unexpected provider errors so callers never crash.
            logger.error("Unexpected error in LLMClient.generate: %s: %s",
                         type(exc).__name__, exc)
            return ""

    def generate_json(self, prompt: str) -> list[dict]:
        """Generate a response and parse JSON from it.

        Always returns a list[dict].  If the model returns a single
        dict it gets wrapped in a list.  On parse failure returns [].

        Error handling:
            - Catches network/timeout/OS errors from model_choice.
            - Catches MemoryError for large responses.
            - Normalises unexpected return types (str, int, None) to [].
            - Filters non-dict items from list results to guarantee
              list[dict] output.
        """
        from model_choice import generate_json as mc_generate_json
        kwargs = dict(
            prompt=prompt,
            temperature=self.temperature,
            max_tokens=3000,
            complexity=self.complexity,
        )
        if self.model:
            kwargs["model"] = self.model
        try:
            result = mc_generate_json(**kwargs)
        except MemoryError:
            logger.error("MemoryError in LLMClient.generate_json")
            return []
        except (ValueError, RuntimeError, ConnectionError,
                TimeoutError, OSError) as exc:
            logger.error("model_choice.generate_json failed: %s: %s",
                         type(exc).__name__, exc)
            return []
        except Exception as exc:
            # Catch-all for unexpected provider errors.
            logger.error("Unexpected error in LLMClient.generate_json: %s: %s",
                         type(exc).__name__, exc)
            return []

        if isinstance(result, list):
            # Guarantee every element is a dict.
            clean = [item for item in result if isinstance(item, dict)]
            if len(clean) != len(result):
                logger.warning(
                    "generate_json: filtered %d non-dict item(s) from result",
                    len(result) - len(clean),
                )
            return clean
        if isinstance(result, dict):
            return [result]
        # Unexpected type (str, int, None, etc.) — normalise to [].
        if result is not None:
            logger.warning(
                "generate_json: unexpected return type %s, returning []",
                type(result).__name__,
            )
        return []
