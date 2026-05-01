#!/usr/bin/env python3
"""Tests for Phase 9: Inferential Sensor (LLM-as-Judge Post-Review)."""

import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from review_sensor import (
    evaluate_run,
    evaluate_latest,
    get_review,
    get_review_stats,
    _build_review_prompt,
    _parse_response,
    _compute_weighted_score,
    DEFAULT_CRITERIA,
)
from execution_log import log_pipeline_run, get_run, RUNS_DIR


@pytest.fixture(autouse=True)
def setup_dirs(tmp_path, monkeypatch):
    """Redirect log directories to tmp_path."""
    monkeypatch.setattr("review_sensor.REVIEWS_DIR", tmp_path / "reviews")
    monkeypatch.setattr("execution_log.RUNS_DIR", tmp_path / "runs")
    monkeypatch.setattr("execution_log.LOOPS_DIR", tmp_path / "loops")


def _make_run(status="completed", pipeline_name="test-pipeline"):
    """Create a test pipeline run dict."""
    return {
        "pipeline_name": pipeline_name,
        "status": status,
        "total_nodes": 2,
        "completed_nodes": 2,
        "failed_nodes": 0,
        "skipped_nodes": 0,
        "duration_seconds": 5.0,
        "results": [
            {
                "node_id": "implement",
                "node_type": "ai",
                "status": "completed",
                "output": "Implemented feature X with tests",
                "duration_seconds": 3.0,
            },
            {
                "node_id": "test",
                "node_type": "bash",
                "status": "completed",
                "output": "5 tests passed",
                "exit_code": 0,
                "duration_seconds": 2.0,
            },
        ],
    }


def test_build_review_prompt():
    """Review prompt includes run data and criteria."""
    run_data = _make_run()
    prompt = _build_review_prompt(run_data, DEFAULT_CRITERIA)

    assert "test-pipeline" in prompt
    assert "implement" in prompt
    assert "code_quality" in prompt
    assert "task_adherence" in prompt
    assert "JSON" in prompt


def test_parse_response_valid_json():
    """Valid JSON response is parsed correctly."""
    response = json.dumps({
        "scores": {"code_quality": 8, "task_adherence": 9, "test_coverage": 7, "no_regressions": 8, "overall": 8},
        "verdict": "pass",
        "summary": "Good implementation",
        "concerns": []
    })
    result = _parse_response(response)

    assert result["verdict"] == "pass"
    assert result["scores"]["code_quality"] == 8
    assert result["summary"] == "Good implementation"


def test_parse_response_markdown_fenced():
    """JSON wrapped in code fences is extracted."""
    response = '```json\n{"scores": {"code_quality": 5}, "verdict": "fail", "summary": "bad", "concerns": ["x"]}\n```'
    result = _parse_response(response)

    assert result["verdict"] == "fail"
    assert result["scores"]["code_quality"] == 5


def test_parse_response_invalid():
    """Invalid response returns needs_review."""
    result = _parse_response("not json at all")

    assert result["verdict"] == "needs_review"
    assert "Failed to parse" in result["summary"]


def test_compute_weighted_score():
    """Weighted average is computed correctly."""
    scores = {"code_quality": 8, "task_adherence": 6, "test_coverage": 10, "no_regressions": 4}
    # weights: 1.0, 1.5, 1.0, 1.5 = total 5.0
    # weighted: 8*1.0 + 6*1.5 + 10*1.0 + 4*1.5 = 8 + 9 + 10 + 6 = 33
    # avg: 33/5.0 = 6.6
    score = _compute_weighted_score(scores, DEFAULT_CRITERIA)
    assert score == 6.6


def test_compute_weighted_score_empty():
    """Empty scores return 0."""
    score = _compute_weighted_score({}, DEFAULT_CRITERIA)
    assert score == 0.0


@patch("review_sensor._call_llm")
def test_evaluate_run(mock_llm, tmp_path):
    """evaluate_run calls LLM and stores result."""
    mock_llm.return_value = json.dumps({
        "scores": {"code_quality": 8, "task_adherence": 9, "test_coverage": 7, "no_regressions": 8, "overall": 8},
        "verdict": "pass",
        "summary": "Clean implementation with good tests",
        "concerns": []
    })

    # Create a test run
    run_data = _make_run()
    run_id = log_pipeline_run(run_data)

    result = evaluate_run(run_id)

    assert result["verdict"] == "pass"
    assert result["weighted_score"] == 8.1  # weighted: 8*1.0 + 9*1.5 + 7*1.0 + 8*1.5 = 40.5/5.0
    assert result["run_id"] == run_id
    assert "summary" in result
    mock_llm.assert_called_once()


@patch("review_sensor._call_llm")
def test_evaluate_run_not_found(mock_llm):
    """evaluate_run returns error for missing run."""
    result = evaluate_run("nonexistent-run-id")
    assert "error" in result
    assert "not found" in result["error"]
    mock_llm.assert_not_called()


@patch("review_sensor._call_llm")
def test_evaluate_latest(mock_llm, tmp_path):
    """evaluate_latest evaluates multiple runs."""
    mock_llm.return_value = json.dumps({
        "scores": {"code_quality": 7, "task_adherence": 7, "test_coverage": 7, "no_regressions": 7, "overall": 7},
        "verdict": "pass",
        "summary": "OK",
        "concerns": []
    })

    # Create 3 test runs
    for i in range(3):
        log_pipeline_run(_make_run(pipeline_name=f"test-{i}"))

    results = evaluate_latest(n=3)

    assert len(results) == 3
    assert all(r["verdict"] == "pass" for r in results)


def test_get_review(tmp_path):
    """get_review loads a previously saved review."""
    review_data = {
        "run_id": "test-123",
        "verdict": "pass",
        "weighted_score": 8.0,
        "scores": {},
        "summary": "test",
        "concerns": [],
    }
    review_dir = tmp_path / "reviews"
    review_dir.mkdir(parents=True, exist_ok=True)
    (review_dir / "test-123.json").write_text(json.dumps(review_data))

    result = get_review("test-123")
    assert result is not None
    assert result["verdict"] == "pass"


def test_get_review_not_found(tmp_path):
    """get_review returns None for missing review."""
    result = get_review("nonexistent")
    assert result is None


def test_get_review_stats(tmp_path):
    """get_review_stats aggregates across all reviews."""
    review_dir = tmp_path / "reviews"
    review_dir.mkdir(parents=True, exist_ok=True)

    for i, verdict in enumerate(["pass", "pass", "fail", "needs_review"]):
        data = {
            "run_id": f"run-{i}",
            "verdict": verdict,
            "weighted_score": 7.0 + i,
            "scores": {"code_quality": 7 + i},
            "summary": "",
            "concerns": [],
        }
        (review_dir / f"run-{i}.json").write_text(json.dumps(data))

    stats = get_review_stats()

    assert stats["total_reviews"] == 4
    assert stats["verdicts"]["pass"] == 2
    assert stats["verdicts"]["fail"] == 1
    assert stats["verdicts"]["needs_review"] == 1


# --- Integration: REVIEW node type in dag.py and executor.py ---

def test_review_node_type_in_dag():
    """REVIEW is a valid NodeType."""
    from dag import NodeType
    assert NodeType.REVIEW == "review"
    assert NodeType.REVIEW in list(NodeType)


def test_review_node_parses_from_yaml(tmp_path):
    """Review node with criteria and threshold parses correctly."""
    yaml_content = """
name: test-review-pipeline
version: "1.0"
nodes:
  implement:
    type: ai
    prompt: "do stuff"
  quality_check:
    type: review
    depends_on: [implement]
    criteria: [code_quality, task_adherence]
    review_threshold: 8.0
    on_review_fail: continue
"""
    pipeline_file = tmp_path / "review-pipe.yaml"
    pipeline_file.write_text(yaml_content)

    from dag import load_pipeline
    pipeline = load_pipeline(str(pipeline_file))

    assert "quality_check" in pipeline.nodes
    node = pipeline.nodes["quality_check"]
    assert node.type.value == "review"
    assert node.criteria == ["code_quality", "task_adherence"]
    assert node.review_threshold == 8.0
    assert node.on_review_fail == "continue"
    assert node.depends_on == ["implement"]


def test_review_node_executor_with_mock_llm(tmp_path):
    """REVIEW node executor calls review_sensor and returns appropriate status."""
    with patch("review_sensor._call_llm") as mock_llm:
        mock_llm.return_value = json.dumps({
            "scores": {"code_quality": 9, "task_adherence": 9, "test_coverage": 8, "no_regressions": 9, "overall": 9},
            "verdict": "pass",
            "summary": "Excellent",
            "concerns": []
        })

        # Create a simple pipeline with review node
        yaml_content = """
name: review-test
version: "1.0"
nodes:
  step1:
    type: bash
    command: "echo hello"
  gate:
    type: review
    depends_on: [step1]
    criteria: [code_quality, task_adherence]
    review_threshold: 7.0
"""
        pipeline_file = tmp_path / "pipe.yaml"
        pipeline_file.write_text(yaml_content)

        from dag import load_pipeline
        from executor import DAGExecutor

        pipeline = load_pipeline(str(pipeline_file))
        executor = DAGExecutor(pipeline=pipeline, workdir=tmp_path)
        result = executor.run()

        assert result.status == "completed"
        review_result = [r for r in result.results if r.node_id == "gate"]
        assert len(review_result) == 1
        assert review_result[0].status == "completed"
        mock_llm.assert_called_once()


def test_review_node_executor_fails_below_threshold(tmp_path):
    """REVIEW node fails when score is below threshold."""
    with patch("review_sensor._call_llm") as mock_llm:
        mock_llm.return_value = json.dumps({
            "scores": {"code_quality": 3, "task_adherence": 2, "test_coverage": 1, "no_regressions": 2, "overall": 2},
            "verdict": "fail",
            "summary": "Poor quality",
            "concerns": ["many issues"]
        })

        yaml_content = """
name: review-fail-test
version: "1.0"
nodes:
  step1:
    type: bash
    command: "echo hello"
  gate:
    type: review
    depends_on: [step1]
    review_threshold: 7.0
"""
        pipeline_file = tmp_path / "pipe.yaml"
        pipeline_file.write_text(yaml_content)

        from dag import load_pipeline
        from executor import DAGExecutor

        pipeline = load_pipeline(str(pipeline_file))
        executor = DAGExecutor(pipeline=pipeline, workdir=tmp_path)
        result = executor.run()

        assert result.status == "failed"
        review_result = [r for r in result.results if r.node_id == "gate"]
        assert review_result[0].status == "failed"


def test_review_node_continue_on_fail(tmp_path):
    """REVIEW node with on_review_fail=continue passes even below threshold."""
    with patch("review_sensor._call_llm") as mock_llm:
        mock_llm.return_value = json.dumps({
            "scores": {"code_quality": 3, "task_adherence": 2, "test_coverage": 1, "no_regressions": 2, "overall": 2},
            "verdict": "fail",
            "summary": "Poor",
            "concerns": []
        })

        yaml_content = """
name: review-continue-test
version: "1.0"
nodes:
  step1:
    type: bash
    command: "echo hello"
  gate:
    type: review
    depends_on: [step1]
    review_threshold: 7.0
    on_review_fail: continue
"""
        pipeline_file = tmp_path / "pipe.yaml"
        pipeline_file.write_text(yaml_content)

        from dag import load_pipeline
        from executor import DAGExecutor

        pipeline = load_pipeline(str(pipeline_file))
        executor = DAGExecutor(pipeline=pipeline, workdir=tmp_path)
        result = executor.run()

        assert result.status == "completed"
        review_result = [r for r in result.results if r.node_id == "gate"]
        assert review_result[0].status == "completed"
