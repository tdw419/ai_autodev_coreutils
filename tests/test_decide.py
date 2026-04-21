"""Tests for decide coreutil."""

import json
from pathlib import Path
from unittest.mock import patch, MagicMock

from autodev_coreutils.contract import ensure_autodev_dir
from autodev_coreutils.decide import (
    build_prompt, parse_response, format_text, log_decision, main,
)


# --- build_prompt ---

def test_build_prompt_basic():
    """build_prompt includes question, options, and evidence."""
    prompt = build_prompt(
        "Which task first?",
        ["task_a", "task_b"],
        "Tests are passing",
    )
    assert "Which task first?" in prompt
    assert "task_a" in prompt
    assert "task_b" in prompt
    assert "Tests are passing" in prompt


def test_build_prompt_with_criteria():
    """build_prompt includes criteria when provided."""
    prompt = build_prompt(
        "Pick one",
        ["a", "b"],
        "evidence",
        criteria="speed, cost",
    )
    assert "speed, cost" in prompt


def test_build_prompt_no_evidence():
    """build_prompt handles missing evidence gracefully."""
    prompt = build_prompt("Pick", ["a", "b"], "")
    assert "no evidence provided" in prompt


# --- parse_response ---

def test_parse_response_clean_json():
    """parse_response handles clean JSON."""
    raw = '{"choice": "a", "reasoning": "better", "confidence": 0.9}'
    result = parse_response(raw)
    assert result["choice"] == "a"
    assert result["confidence"] == 0.9
    assert result["parse_error"] is False


def test_parse_response_markdown_fenced():
    """parse_response strips markdown fences."""
    raw = '```json\n{"choice": "b", "reasoning": "yes", "confidence": 0.7}\n```'
    result = parse_response(raw)
    assert result["choice"] == "b"
    assert result["parse_error"] is False


def test_parse_response_embedded_json():
    """parse_response extracts JSON from surrounding text."""
    raw = 'Here is my decision:\n{"choice": "a", "reasoning": "looks good", "confidence": 0.8}\nDone.'
    result = parse_response(raw)
    assert result["choice"] == "a"


def test_parse_response_garbage():
    """parse_response returns parse_error on unparseable text."""
    result = parse_response("I choose option a because reasons")
    assert result.get("parse_error") is True
    assert "I choose" in result["choice"]


def test_parse_response_clamps_confidence():
    """parse_response clamps confidence to 0-1."""
    result = parse_response('{"choice": "a", "confidence": 2.5}')
    assert result["confidence"] == 1.0

    result = parse_response('{"choice": "a", "confidence": -0.5}')
    assert result["confidence"] == 0.0


def test_parse_response_defaults():
    """parse_response fills missing fields."""
    result = parse_response('{"choice": "a"}')
    assert result["confidence"] == 0.5
    assert result["reasoning"] == ""


# --- format_text ---

def test_format_text():
    """format_text produces readable output."""
    decision = {
        "choice": "keep",
        "confidence": 0.85,
        "reasoning": "Tests pass, code is clean",
        "matched_option": True,
    }
    text = format_text(decision)
    assert "keep" in text
    assert "85%" in text
    assert "Tests pass" in text


def test_format_text_unmatched():
    """format_text notes when choice didn't match an option."""
    decision = {
        "choice": "maybe keep",
        "confidence": 0.6,
        "reasoning": "unsure",
        "matched_option": False,
    }
    text = format_text(decision)
    assert "did not exactly match" in text


# --- log_decision ---

def test_log_decision(tmp_path):
    """log_decision appends to decisions.jsonl."""
    ensure_autodev_dir(tmp_path)
    decision = {"choice": "a", "confidence": 0.9, "reasoning": "test"}

    log_decision(tmp_path, decision)
    log_decision(tmp_path, {"choice": "b", "confidence": 0.7, "reasoning": "also test"})

    log_file = tmp_path / ".autodev" / "decisions.jsonl"
    assert log_file.exists()

    lines = log_file.read_text().strip().split("\n")
    assert len(lines) == 2

    entry = json.loads(lines[0])
    assert entry["choice"] == "a"
    assert "timestamp" in entry


# --- main (CLI) ---

def test_main_basic(tmp_path, capsys):
    """main runs a basic decision."""
    ensure_autodev_dir(tmp_path)

    mock_decision = {
        "choice": "task_b",
        "confidence": 0.82,
        "reasoning": "Higher impact",
        "matched_option": True,
        "question": "Which first?",
        "options": ["task_a", "task_b"],
    }

    with patch("autodev_coreutils.decide.decide", return_value=mock_decision):
        result = main(["-w", str(tmp_path), "Which first?", "--options", "task_a", "task_b", "--no-log"])

    assert result == 0

    captured = capsys.readouterr()
    assert "task_b" in captured.out


def test_main_json_mode(tmp_path, capsys):
    """main outputs JSON with --json flag."""
    ensure_autodev_dir(tmp_path)

    mock_decision = {
        "choice": "revert",
        "confidence": 0.6,
        "reasoning": "Tests failing",
        "matched_option": True,
        "question": "Keep or revert?",
        "options": ["keep", "revert"],
    }

    with patch("autodev_coreutils.decide.decide", return_value=mock_decision):
        result = main(["-w", str(tmp_path), "Keep or revert?",
                       "--options", "keep", "revert", "--json", "--no-log"])

    assert result == 0

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["choice"] == "revert"


def test_main_low_confidence_exit_code(tmp_path):
    """main returns exit code 1 for low confidence decisions."""
    ensure_autodev_dir(tmp_path)

    mock_decision = {
        "choice": "maybe",
        "confidence": 0.15,
        "reasoning": "Not enough evidence",
        "matched_option": False,
        "question": "Yes or no?",
        "options": ["yes", "no"],
    }

    with patch("autodev_coreutils.decide.decide", return_value=mock_decision):
        result = main(["-w", str(tmp_path), "Yes or no?",
                       "--options", "yes", "no", "--no-log", "-q"])

    assert result == 1


def test_main_with_evidence_file(tmp_path, capsys):
    """main reads evidence from files."""
    ensure_autodev_dir(tmp_path)

    # Create evidence file
    evidence_file = tmp_path / "test_results.txt"
    evidence_file.write_text("10 passed, 0 failed")

    mock_decision = {
        "choice": "yes",
        "confidence": 0.95,
        "reasoning": "All tests pass",
        "matched_option": True,
        "question": "Ship it?",
        "options": ["yes", "no"],
    }

    with patch("autodev_coreutils.decide.decide", return_value=mock_decision) as mock_decide:
        result = main(["-w", str(tmp_path), "Ship it?",
                       "--options", "yes", "no",
                       "--evidence", str(evidence_file), "--no-log", "-q"])

    assert result == 0

    # Verify evidence was collected and passed
    call_args = mock_decide.call_args
    assert "10 passed" in call_args.kwargs.get("evidence", "") or "10 passed" in call_args[1].get("evidence", "")


def test_main_too_few_options(tmp_path):
    """main errors with fewer than 2 options."""
    try:
        main(["-w", str(tmp_path), "Pick one", "--options", "only_one"])
        assert False, "Should have exited"
    except SystemExit as e:
        assert e.code == 1


def test_main_logs_to_decisions_jsonl(tmp_path):
    """main writes to decisions.jsonl when not --no-log."""
    ensure_autodev_dir(tmp_path)

    mock_decision = {
        "choice": "a",
        "confidence": 0.9,
        "reasoning": "test",
        "matched_option": True,
        "question": "Pick one",
        "options": ["a", "b"],
    }

    with patch("autodev_coreutils.decide.decide", return_value=mock_decision):
        main(["-w", str(tmp_path), "Pick one", "--options", "a", "b", "-q"])

    log_file = tmp_path / ".autodev" / "decisions.jsonl"
    assert log_file.exists()
    entry = json.loads(log_file.read_text().strip())
    assert entry["choice"] == "a"
    assert "timestamp" in entry
