"""Tests for llm module -- parse_json_response and internal helpers."""

import json
import pytest

from possibilities.llm import (
    ParseError,
    _extract_markdown_blocks,
    _find_json_bounds,
    _normalize_result,
    _parse_markdown_fenced_json,
    _parse_raw_json,
    _parse_whole_text,
    parse_json_response,
)


# ---------------------------------------------------------------------------
# _normalize_result
# ---------------------------------------------------------------------------

class TestNormalizeResult:
    def test_list_passthrough(self):
        data = [{"a": 1}, {"b": 2}]
        assert _normalize_result(data) == data

    def test_empty_list(self):
        assert _normalize_result([]) == []

    def test_dict_wrapped_in_list(self):
        assert _normalize_result({"a": 1}) == [{"a": 1}]

    def test_non_dict_scalar_returns_empty(self):
        assert _normalize_result(42) == []

    def test_string_returns_empty(self):
        assert _normalize_result("hello") == []

    def test_none_returns_empty(self):
        assert _normalize_result(None) == []

    def test_bool_returns_empty(self):
        assert _normalize_result(True) == []

    def test_nested_list_returns_filtered(self):
        """A list of non-dicts gets filtered to only dicts (empty in this case)."""
        assert _normalize_result([1, 2, 3]) == []

    def test_mixed_list_keeps_only_dicts(self):
        """Non-dict items are filtered out, dicts are kept."""
        data = [1, {"a": 1}, "str", {"b": 2}, None, True]
        assert _normalize_result(data) == [{"a": 1}, {"b": 2}]

    def test_list_of_empty_dicts(self):
        """Empty dicts are still dicts — they pass through."""
        assert _normalize_result([{}, {}]) == [{}, {}]

    def test_list_of_lists_filtered_out(self):
        """Nested lists are not dicts — filtered out."""
        assert _normalize_result([[1, 2], [3, 4]]) == []


# ---------------------------------------------------------------------------
# _extract_markdown_blocks
# ---------------------------------------------------------------------------

class TestExtractMarkdownBlocks:
    def test_no_fences(self):
        assert _extract_markdown_blocks("plain text") == []

    def test_single_json_block(self):
        text = "```json\n{\"a\": 1}\n```"
        assert _extract_markdown_blocks(text) == ['{"a": 1}\n']

    def test_single_unlabeled_block(self):
        text = "```\n[1, 2, 3]\n```"
        assert _extract_markdown_blocks(text) == ["[1, 2, 3]\n"]

    def test_multiple_blocks(self):
        text = "```json\n{\"a\": 1}\n```\nSome text\n```\n{\"b\": 2}\n```"
        blocks = _extract_markdown_blocks(text)
        assert len(blocks) == 2
        assert '{"a": 1}\n' in blocks
        assert '{"b": 2}\n' in blocks

    def test_unclosed_fence_not_extracted(self):
        text = "```json\n{\"a\": 1}"
        assert _extract_markdown_blocks(text) == []


# ---------------------------------------------------------------------------
# _parse_markdown_fenced_json
# ---------------------------------------------------------------------------

class TestParseMarkdownFencedJson:
    def test_valid_json_array(self):
        text = "```json\n[{\"a\": 1}]\n```"
        assert _parse_markdown_fenced_json(text) == [{"a": 1}]

    def test_valid_json_object(self):
        text = "```json\n{\"a\": 1}\n```"
        assert _parse_markdown_fenced_json(text) == [{"a": 1}]

    def test_invalid_block_returns_none(self):
        text = "```json\nnot json\n```"
        assert _parse_markdown_fenced_json(text) is None

    def test_first_valid_block_wins(self):
        text = "```json\nbad\n```\n```json\n[{\"ok\": true}]\n```"
        assert _parse_markdown_fenced_json(text) == [{"ok": True}]

    def test_no_fences_returns_none(self):
        assert _parse_markdown_fenced_json("no fences") is None


# ---------------------------------------------------------------------------
# _find_json_bounds
# ---------------------------------------------------------------------------

class TestFindJsonBounds:
    def test_array_in_text(self):
        text = "Here is the result: [1, 2, 3] and more"
        bounds = _find_json_bounds(text)
        assert bounds is not None
        start, end = bounds
        assert json.loads(text[start:end]) == [1, 2, 3]

    def test_object_in_text(self):
        text = 'prefix {"key": "value"} suffix'
        bounds = _find_json_bounds(text)
        assert bounds is not None
        start, end = bounds
        assert json.loads(text[start:end]) == {"key": "value"}

    def test_nested_brackets(self):
        text = "outer [[1, 2], 3] trailing"
        bounds = _find_json_bounds(text)
        assert bounds is not None
        start, end = bounds
        assert json.loads(text[start:end]) == [[1, 2], 3]

    def test_no_brackets(self):
        assert _find_json_bounds("no json here") is None

    def test_unclosed_bracket(self):
        assert _find_json_bounds("[1, 2") is None

    def test_string_with_brackets(self):
        """Brackets inside strings should be ignored."""
        text = '{"text": "array [1, 2] inside"}'
        bounds = _find_json_bounds(text)
        assert bounds is not None
        start, end = bounds
        parsed = json.loads(text[start:end])
        assert parsed["text"] == "array [1, 2] inside"

    def test_escaped_quotes_in_string(self):
        text = '{"msg": "He said \\"hello\\""}'
        bounds = _find_json_bounds(text)
        assert bounds is not None
        start, end = bounds
        parsed = json.loads(text[start:end])
        assert parsed["msg"] == 'He said "hello"'

    def test_escaped_backslash(self):
        text = '{"path": "C:\\\\Users\\\\test"}'
        bounds = _find_json_bounds(text)
        assert bounds is not None
        start, end = bounds
        parsed = json.loads(text[start:end])
        assert parsed["path"] == "C:\\Users\\test"


# ---------------------------------------------------------------------------
# _parse_raw_json
# ---------------------------------------------------------------------------

class TestParseRawJson:
    def test_array_with_trailing_text(self):
        text = 'Here is data: [{"a": 1}] and some trailing text here'
        assert _parse_raw_json(text) == [{"a": 1}]

    def test_object_with_surrounding_text(self):
        text = 'prefix {"b": 2} suffix'
        assert _parse_raw_json(text) == [{"b": 2}]

    def test_no_json_returns_none(self):
        assert _parse_raw_json("just text") is None

    def test_bare_array(self):
        """Non-dict items are filtered, so a bare number array returns []."""
        assert _parse_raw_json("[1, 2, 3]") == []


# ---------------------------------------------------------------------------
# _parse_whole_text
# ---------------------------------------------------------------------------

class TestParseWholeText:
    def test_valid_array(self):
        assert _parse_whole_text('[{"x": 1}]') == [{"x": 1}]

    def test_valid_object(self):
        assert _parse_whole_text('{"x": 1}') == [{"x": 1}]

    def test_invalid_returns_none(self):
        assert _parse_whole_text("not json") is None


# ---------------------------------------------------------------------------
# parse_json_response (integration of all strategies)
# ---------------------------------------------------------------------------

class TestParseJsonResponse:
    # -- Type validation --

    def test_non_string_raises_type_error(self):
        with pytest.raises(TypeError, match="expects str"):
            parse_json_response(42)

    def test_none_raises_type_error(self):
        with pytest.raises(TypeError, match="expects str"):
            parse_json_response(None)

    def test_bytes_raises_type_error(self):
        with pytest.raises(TypeError, match="expects str"):
            parse_json_response(b'{"a": 1}')

    # -- Empty input --

    def test_empty_string(self):
        assert parse_json_response("") == []

    def test_whitespace_only(self):
        assert parse_json_response("   \n\t  ") == []

    # -- Strategy 1: markdown fences --

    def test_json_array_in_code_fence(self):
        text = '```json\n[{"title": "AI Agents", "score": 0.9}]\n```'
        result = parse_json_response(text)
        assert result == [{"title": "AI Agents", "score": 0.9}]

    def test_json_object_in_code_fence(self):
        text = '```json\n{"title": "AI Agents"}\n```'
        result = parse_json_response(text)
        assert result == [{"title": "AI Agents"}]

    def test_unlabeled_code_fence(self):
        text = '```\n[{"a": 1}]\n```'
        result = parse_json_response(text)
        assert result == [{"a": 1}]

    def test_code_fence_with_surrounding_text(self):
        text = 'Here are the results:\n```json\n[{"x": 1}]\n```\nThat is all.'
        result = parse_json_response(text)
        assert result == [{"x": 1}]

    def test_broken_first_fence_uses_second(self):
        text = '```json\nnot valid json\n```\n```json\n[{"ok": true}]\n```'
        result = parse_json_response(text)
        assert result == [{"ok": True}]

    # -- Strategy 2: raw JSON embedded in text --

    def test_array_with_surrounding_prose(self):
        text = 'The LLM responded with [{"title": "Build X"}] which is great.'
        result = parse_json_response(text)
        assert result == [{"title": "Build X"}]

    def test_object_with_surrounding_prose(self):
        text = 'Result: {"title": "Build X"} end.'
        result = parse_json_response(text)
        assert result == [{"title": "Build X"}]

    def test_trailing_text_after_array(self):
        text = '[{"a": 1}] Here is some explanation of the results.'
        result = parse_json_response(text)
        assert result == [{"a": 1}]

    def test_leading_text_before_object(self):
        text = 'Sure, here it is: {"answer": 42}'
        result = parse_json_response(text)
        assert result == [{"answer": 42}]

    # -- Strategy 3: whole text is JSON --

    def test_bare_json_array(self):
        text = '[{"a": 1}, {"b": 2}]'
        result = parse_json_response(text)
        assert result == [{"a": 1}, {"b": 2}]

    def test_bare_json_object(self):
        text = '{"key": "value"}'
        result = parse_json_response(text)
        assert result == [{"key": "value"}]

    def test_empty_json_array(self):
        assert parse_json_response("[]") == []

    def test_json_with_whitespace(self):
        text = '  \n  [{"a": 1}]  \n  '
        assert parse_json_response(text) == [{"a": 1}]

    # -- Failure cases --

    def test_plain_english_returns_empty(self):
        assert parse_json_response("This is just plain text.") == []

    def test_partial_json_returns_empty(self):
        assert parse_json_response('{"broken": ') == []

    def test_random_symbols_returns_empty(self):
        assert parse_json_response("!@#$%^&*()") == []

    # -- Real-world LLM output patterns --

    def test_llm_with_thinking_prefix(self):
        """Some models add reasoning before the JSON."""
        text = 'Let me think about this...\n\n```json\n[{"idea": "quantum UI"}]\n```'
        result = parse_json_response(text)
        assert result == [{"idea": "quantum UI"}]

    def test_llm_with_conversational_wrapper(self):
        text = (
            "Sure! Here are the possibilities:\n"
            "```json\n"
            '[{"title": "Graph DB", "category": "wildcard"}, '
            '{"title": "TUI", "category": "obvious"}]\n'
            "```\n"
            "Let me know if you need more!"
        )
        result = parse_json_response(text)
        assert len(result) == 2
        assert result[0]["title"] == "Graph DB"
        assert result[1]["category"] == "obvious"

    def test_dedup_response_pattern(self):
        """Matches the pattern dedup.py expects."""
        text = '[{"is_duplicate": false, "similarity": 0.3, "reason": "Different topics"}]'
        result = parse_json_response(text)
        assert len(result) == 1
        assert result[0]["is_duplicate"] is False

    def test_nested_json_structure(self):
        text = '[{"title": "X", "children": [{"title": "Y"}]}]'
        result = parse_json_response(text)
        assert result[0]["children"][0]["title"] == "Y"


# ---------------------------------------------------------------------------
# ParseError exists and is importable
# ---------------------------------------------------------------------------

class TestParseError:
    def test_is_exception(self):
        assert issubclass(ParseError, Exception)

    def test_can_be_raised(self):
        with pytest.raises(ParseError):
            raise ParseError("test")


# ---------------------------------------------------------------------------
# Error handling: null bytes, unexpected exceptions, edge cases
# ---------------------------------------------------------------------------

class TestNullByteHandling:
    """Null bytes are stripped before parsing to avoid json.loads errors."""

    def test_null_bytes_stripped_from_valid_json(self):
        text = '[{"title": "AI\x00Agents"}]'
        result = parse_json_response(text)
        # Null bytes are stripped before parsing, so they won't appear in output.
        assert result == [{"title": "AIAgents"}]

    def test_null_bytes_in_fence(self):
        text = '```json\n[{"title": "X\x00Y"}]\n```'
        result = parse_json_response(text)
        assert result == [{"title": "XY"}]

    def test_only_null_bytes_returns_empty(self):
        assert parse_json_response("\x00\x00\x00") == []

    def test_null_bytes_at_start_and_end(self):
        text = '\x00[{"a": 1}]\x00'
        result = parse_json_response(text)
        assert result == [{"a": 1}]


class TestMixedTypeListFiltering:
    """When LLM returns a JSON array with non-dict items, they get filtered."""

    def test_mixed_array_in_fence(self):
        text = '```json\n[1, {"title": "good"}, "bad", {"also": "good"}]\n```'
        result = parse_json_response(text)
        assert result == [{"title": "good"}, {"also": "good"}]

    def test_all_non_dict_array_in_fence(self):
        """An array of only non-dicts should return empty after filtering."""
        text = '```json\n[1, 2, 3]\n```'
        result = parse_json_response(text)
        assert result == []

    def test_mixed_array_raw_json(self):
        text = 'Result: [{"a": 1}, 42, {"b": 2}] done'
        result = parse_json_response(text)
        assert result == [{"a": 1}, {"b": 2}]

    def test_mixed_array_whole_text(self):
        text = '[{"x": 1}, "string", null, {"y": 2}]'
        result = parse_json_response(text)
        assert result == [{"x": 1}, {"y": 2}]


class TestTopLevelSafetyNet:
    """parse_json_response catches truly unexpected errors and returns []."""

    def test_internal_exception_returns_empty(self, monkeypatch):
        """If _parse_raw_json raises an unexpected exception, it's caught."""
        def boom(_text):
            raise RuntimeError("surprise explosion")
        # _parse_markdown_fenced_json won't fire (no ```), so _parse_raw_json
        # is the first strategy hit.  The top-level except catches it.
        monkeypatch.setattr("possibilities.llm._parse_raw_json", boom)
        result = parse_json_response('[{"a": 1}]')
        assert result == []

    def test_fence_strategy_exception_returns_empty(self, monkeypatch):
        """If the markdown strategy explodes, the safety net catches it."""
        def boom(_text):
            raise RuntimeError("fence explosion")
        monkeypatch.setattr("possibilities.llm._parse_markdown_fenced_json", boom)
        text = '```json\n[{"a": 1}]\n```'
        result = parse_json_response(text)
        assert result == []

    def test_whole_text_strategy_exception_returns_empty(self, monkeypatch):
        """If the whole-text strategy explodes, the safety net catches it."""
        def boom(_text):
            raise RuntimeError("whole-text explosion")
        # Make markdown and raw return None so we fall through to whole text.
        monkeypatch.setattr("possibilities.llm._parse_markdown_fenced_json",
                            lambda _: None)
        monkeypatch.setattr("possibilities.llm._parse_raw_json",
                            lambda _: None)
        monkeypatch.setattr("possibilities.llm._parse_whole_text", boom)
        result = parse_json_response('[{"a": 1}]')
        assert result == []


class TestHelperUnexpectedExceptions:
    """Each parsing helper catches RecursionError/ValueError/TypeError."""

    def test_markdown_fenced_catches_value_error(self, monkeypatch):
        """If json.loads raises ValueError (not JSONDecodeError), it's caught."""
        original_loads = json.loads
        call_count = {"n": 0}

        def bad_loads(_s):
            call_count["n"] += 1
            if call_count["n"] == 1:
                raise ValueError("bad value")
            return original_loads(_s)

        monkeypatch.setattr("json.loads", bad_loads)
        from possibilities.llm import _parse_markdown_fenced_json
        text = '```json\n[{"ok": true}]\n```\n```json\n[{"also": true}]\n```'
        # First block raises ValueError (caught), second block succeeds
        result = _parse_markdown_fenced_json(text)
        assert result == [{"also": True}]

    def test_raw_json_catches_type_error(self, monkeypatch):
        """If json.loads raises TypeError, _parse_raw_json returns None."""
        def bad_loads(_s):
            raise TypeError("unexpected type")

        monkeypatch.setattr("json.loads", bad_loads)
        from possibilities.llm import _parse_raw_json
        result = _parse_raw_json('[{"a": 1}]')
        assert result is None

    def test_whole_text_catches_value_error(self, monkeypatch):
        """If json.loads raises ValueError, _parse_whole_text returns None."""
        def bad_loads(_s):
            raise ValueError("bad value")

        monkeypatch.setattr("json.loads", bad_loads)
        from possibilities.llm import _parse_whole_text
        result = _parse_whole_text('[{"a": 1}]')
        assert result is None


class TestLLMClientErrorHandling:
    """LLMClient.generate and generate_json handle provider failures."""

    def test_generate_returns_empty_on_connection_error(self, monkeypatch):
        def bad_generate(**kwargs):
            raise ConnectionError("network down")
        monkeypatch.setattr("model_choice.generate", bad_generate, raising=False)
        from possibilities.llm import LLMClient
        client = LLMClient()
        assert client.generate("test prompt") == ""

    def test_generate_returns_empty_on_timeout(self, monkeypatch):
        def bad_generate(**kwargs):
            raise TimeoutError("timed out")
        monkeypatch.setattr("model_choice.generate", bad_generate, raising=False)
        from possibilities.llm import LLMClient
        client = LLMClient()
        assert client.generate("test prompt") == ""

    def test_generate_returns_empty_on_runtime_error(self, monkeypatch):
        def bad_generate(**kwargs):
            raise RuntimeError("provider error")
        monkeypatch.setattr("model_choice.generate", bad_generate, raising=False)
        from possibilities.llm import LLMClient
        client = LLMClient()
        assert client.generate("test prompt") == ""

    def test_generate_returns_empty_on_os_error(self, monkeypatch):
        def bad_generate(**kwargs):
            raise OSError("system error")
        monkeypatch.setattr("model_choice.generate", bad_generate, raising=False)
        from possibilities.llm import LLMClient
        client = LLMClient()
        assert client.generate("test prompt") == ""

    def test_generate_returns_empty_on_unexpected_exception(self, monkeypatch):
        """Catch-all: even KeyError doesn't leak."""
        def bad_generate(**kwargs):
            raise KeyError("missing key")
        monkeypatch.setattr("model_choice.generate", bad_generate, raising=False)
        from possibilities.llm import LLMClient
        client = LLMClient()
        assert client.generate("test prompt") == ""

    def test_generate_json_returns_empty_on_connection_error(self, monkeypatch):
        def bad_generate(**kwargs):
            raise ConnectionError("network down")
        monkeypatch.setattr("model_choice.generate_json", bad_generate, raising=False)
        from possibilities.llm import LLMClient
        client = LLMClient()
        assert client.generate_json("test prompt") == []

    def test_generate_json_returns_empty_on_timeout(self, monkeypatch):
        def bad_generate(**kwargs):
            raise TimeoutError("timed out")
        monkeypatch.setattr("model_choice.generate_json", bad_generate, raising=False)
        from possibilities.llm import LLMClient
        client = LLMClient()
        assert client.generate_json("test prompt") == []

    def test_generate_json_returns_empty_on_unexpected(self, monkeypatch):
        def bad_generate(**kwargs):
            raise AttributeError("surprise")
        monkeypatch.setattr("model_choice.generate_json", bad_generate, raising=False)
        from possibilities.llm import LLMClient
        client = LLMClient()
        assert client.generate_json("test prompt") == []


class TestEdgeCaseInputs:
    """Additional edge cases for robust parsing."""

    def test_very_long_whitespace(self):
        """Input that is all whitespace (many chars) returns []."""
        assert parse_json_response("   " * 1000) == []

    def test_unicode_in_json(self):
        """Unicode characters in values parse correctly."""
        text = '[{"title": "Quantum \u00e9volution", "emoji": "\U0001f680"}]'
        result = parse_json_response(text)
        assert result == [{"title": "Quantum \u00e9volution", "emoji": "\U0001f680"}]

    def test_json_with_trailing_comma_fails_gracefully(self):
        """Trailing commas are invalid JSON — returns []."""
        assert parse_json_response('[{"a": 1},]') == []

    def test_single_number_in_array_filtered(self):
        """A bare JSON number array like [42] has no dicts — returns []."""
        assert parse_json_response("[42]") == []

    def test_empty_object_in_list(self):
        """Empty dicts are valid items — they pass through."""
        assert parse_json_response("[{}]") == [{}]

    def test_deeply_nested_valid_json(self):
        """Reasonably deep nesting should parse fine."""
        # Build a 50-level nested dict
        inner = {"value": 42}
        for _ in range(50):
            inner = {"nested": inner}
        text = json.dumps([inner])
        result = parse_json_response(text)
        assert len(result) == 1
        # Navigate 50 levels down
        node = result[0]
        for _ in range(50):
            node = node["nested"]
        assert node["value"] == 42


class TestInputSizeLimit:
    """parse_json_response rejects inputs exceeding _MAX_INPUT_CHARS."""

    def test_oversized_input_raises_value_error(self):
        from possibilities.llm import _MAX_INPUT_CHARS
        huge = "x" * (_MAX_INPUT_CHARS + 1)
        with pytest.raises(ValueError, match="Input text too large"):
            parse_json_response(huge)

    def test_exactly_at_limit_is_accepted(self):
        """Input at exactly _MAX_INPUT_CHARS should not raise."""
        from possibilities.llm import _MAX_INPUT_CHARS
        # Build valid JSON at exactly the limit size
        padding = _MAX_INPUT_CHARS - len('[{"a":"') - len('"}]')
        text = '[{"a":"' + ("z" * padding) + '"}]'
        # Adjust to hit exactly the limit
        text = "x" * _MAX_INPUT_CHARS  # won't parse, but shouldn't raise ValueError
        result = parse_json_response(text)
        assert result == []  # not valid JSON, but accepted size-wise


class TestMemoryErrorHandling:
    """MemoryError during parsing is caught and returns []."""

    def test_memory_error_in_strategy_returns_empty(self, monkeypatch):
        """If a helper raises MemoryError, parse_json_response returns []."""
        def boom(_text):
            raise MemoryError("out of memory")
        monkeypatch.setattr("possibilities.llm._parse_raw_json", boom)
        result = parse_json_response('[{"a": 1}]')
        assert result == []

    def test_memory_error_in_fence_strategy_returns_empty(self, monkeypatch):
        """MemoryError from markdown-fence strategy is caught."""
        def boom(_text):
            raise MemoryError("fence oom")
        monkeypatch.setattr("possibilities.llm._parse_markdown_fenced_json", boom)
        text = '```json\n[{"a": 1}]\n```'
        result = parse_json_response(text)
        assert result == []


class TestLLMClientGenerateJsonNormalization:
    """generate_json normalises unexpected model_choice return types."""

    def test_returns_none_normalised_to_empty(self, monkeypatch):
        """If model_choice returns None, generate_json returns []."""
        monkeypatch.setattr("model_choice.generate_json",
                            lambda **kw: None, raising=False)
        from possibilities.llm import LLMClient
        assert LLMClient().generate_json("test") == []

    def test_returns_string_normalised_to_empty(self, monkeypatch):
        """If model_choice returns a string, generate_json returns []."""
        monkeypatch.setattr("model_choice.generate_json",
                            lambda **kw: '{"not": "a list"}', raising=False)
        from possibilities.llm import LLMClient
        assert LLMClient().generate_json("test") == []

    def test_returns_int_normalised_to_empty(self, monkeypatch):
        """If model_choice returns an int, generate_json returns []."""
        monkeypatch.setattr("model_choice.generate_json",
                            lambda **kw: 42, raising=False)
        from possibilities.llm import LLMClient
        assert LLMClient().generate_json("test") == []

    def test_mixed_list_filters_non_dicts(self, monkeypatch):
        """Non-dict items in list results are filtered out."""
        monkeypatch.setattr("model_choice.generate_json",
                            lambda **kw: [{"a": 1}, "bad", 42, {"b": 2}],
                            raising=False)
        from possibilities.llm import LLMClient
        result = LLMClient().generate_json("test")
        assert result == [{"a": 1}, {"b": 2}]

    def test_memory_error_returns_empty(self, monkeypatch):
        """MemoryError from model_choice is caught and returns []."""
        def boom(**kwargs):
            raise MemoryError("oom")
        monkeypatch.setattr("model_choice.generate_json", boom, raising=False)
        from possibilities.llm import LLMClient
        assert LLMClient().generate_json("test") == []


class TestUnicodeErrorHandling:
    """Unicode errors during preprocessing are caught gracefully.

    Note: str.strip()/str.replace() cannot actually raise UnicodeDecodeError
    on Python 3 str objects (those are bytes-only errors). The guards in
    parse_json_response are defensive checks for edge-case C extensions or
    future Python changes. We test the behavior indirectly by confirming that
    various unicode-laden inputs still parse correctly.
    """

    def test_surrogate_pair_emoji_parses(self):
        """Emoji and surrogate pairs should parse without error."""
        text = json.dumps([{"emoji": "\U0001f600", "text": "hello \u00e9"}])
        result = parse_json_response(text)
        assert result == [{"emoji": "\U0001f600", "text": "hello \u00e9"}]

    def test_mixed_multibyte_json(self):
        """Mixed CJK, Cyrillic, Arabic content parses correctly."""
        text = json.dumps([{"ja": "\u30c6\u30b9\u30c8", "ru": "\u0442\u0435\u0441\u0442", "ar": "\u0627\u062e\u062a\u0628\u0627\u0631"}])
        result = parse_json_response(text)
        assert len(result) == 1
        assert "ja" in result[0]
        assert "ru" in result[0]
        assert "ar" in result[0]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
