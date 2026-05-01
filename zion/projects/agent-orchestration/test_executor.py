#!/usr/bin/env python3
"""
Comprehensive tests for executor.py - DAG executor for all node types.
"""
import json
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent))

import pytest
from dag import Pipeline, Node, NodeType, parse_pipeline
from executor import DAGExecutor, NodeResult, ExecutionResult


def _make_pipeline(nodes_raw: dict) -> Pipeline:
    """Helper to create a pipeline from raw node dicts."""
    return parse_pipeline({"name": "test", "nodes": nodes_raw})


def _make_bash_node(id="bash1", command="echo hi", **kwargs) -> dict:
    return {"type": "bash", "command": command, **kwargs}


def _make_ai_node(id="ai1", prompt="Do something", **kwargs) -> dict:
    return {"type": "ai", "prompt": prompt, **kwargs}


def _make_loop_node(id="loop1", children=None, **kwargs) -> dict:
    children = children or ["inner"]
    return {"type": "loop", "children": children, **kwargs}


# ─── DAGExecutor init ────────────────────────────────────────────────

class TestExecutorInit:
    def test_default_init(self):
        p = _make_pipeline({"a": _make_bash_node()})
        ex = DAGExecutor(p)
        assert ex.workdir == Path.cwd()
        assert ex.context == {}
        assert ex.dry_run is False

    def test_custom_init(self, tmp_path):
        p = _make_pipeline({"a": _make_bash_node()})
        ex = DAGExecutor(p, workdir=tmp_path, context={"key": "val"}, dry_run=True)
        assert ex.workdir == tmp_path
        assert ex.context == {"key": "val"}
        assert ex.dry_run is True


# ─── Template rendering ──────────────────────────────────────────────

class TestTemplateRendering:
    def test_context_substitution(self):
        p = _make_pipeline({"a": _make_bash_node(command="echo {{greeting}}")})
        ex = DAGExecutor(p, context={"greeting": "hello"})
        assert ex._render_template("echo {{greeting}}") == "echo hello"

    def test_node_output_substitution(self):
        p = _make_pipeline({"a": _make_bash_node()})
        ex = DAGExecutor(p)
        ex.node_outputs["prev"] = "world"
        assert ex._render_template("echo {{prev.output}}") == "echo world"

    def test_no_placeholders(self):
        p = _make_pipeline({"a": _make_bash_node()})
        ex = DAGExecutor(p)
        assert ex._render_template("echo hello") == "echo hello"

    def test_mixed_placeholders(self):
        p = _make_pipeline({"a": _make_bash_node()})
        ex = DAGExecutor(p, context={"name": "test"})
        ex.node_outputs["step1"] = "result1"
        result = ex._render_template("{{name}}: {{step1.output}}")
        assert result == "test: result1"


# ─── Bash node execution ─────────────────────────────────────────────

class TestBashExecution:
    def test_successful_command(self, tmp_path):
        p = _make_pipeline({"a": _make_bash_node(command="echo hello")})
        ex = DAGExecutor(p, workdir=tmp_path)
        result = ex._execute_bash(p.nodes["a"])
        assert result.status == "completed"
        assert "hello" in result.output
        assert result.exit_code == 0

    def test_failing_command(self, tmp_path):
        p = _make_pipeline({"a": _make_bash_node(command="exit 1")})
        ex = DAGExecutor(p, workdir=tmp_path)
        result = ex._execute_bash(p.nodes["a"])
        assert result.status == "failed"
        assert result.exit_code == 1

    def test_continue_on_error(self, tmp_path):
        p = _make_pipeline({"a": _make_bash_node(command="exit 42", continue_on_error=True)})
        ex = DAGExecutor(p, workdir=tmp_path)
        result = ex._execute_bash(p.nodes["a"])
        assert result.status == "completed"
        assert result.exit_code == 42

    def test_command_with_env(self, tmp_path):
        p = _make_pipeline({"a": _make_bash_node(command="echo $MY_VAR", env={"MY_VAR": "secret"})})
        ex = DAGExecutor(p, workdir=tmp_path)
        result = ex._execute_bash(p.nodes["a"])
        assert result.status == "completed"
        assert "secret" in result.output

    def test_command_timeout(self, tmp_path):
        raw = {"type": "bash", "command": "sleep 10", "timeout_seconds": 1}
        p = _make_pipeline({"a": raw})
        ex = DAGExecutor(p, workdir=tmp_path)
        result = ex._execute_bash(p.nodes["a"])
        assert result.status == "failed"
        assert "timed out" in result.error.lower()


# ─── AI node execution ───────────────────────────────────────────────

class TestAIExecution:
    def test_ai_node_preparation(self):
        p = _make_pipeline({"a": _make_ai_node(prompt="Implement feature X")})
        ex = DAGExecutor(p)
        result = ex._execute_ai(p.nodes["a"])
        assert result.status == "completed"
        # Should output delegate_task params as JSON
        data = json.loads(result.output)
        assert "prompt" in data
        assert "Implement feature X" in data["prompt"]
        assert data["workdir"] == str(Path.cwd())

    def test_ai_node_with_role(self):
        p = _make_pipeline({"a": _make_ai_node(prompt="Review code", role="reviewer")})
        ex = DAGExecutor(p)
        result = ex._execute_ai(p.nodes["a"])
        data = json.loads(result.output)
        assert data["role"] == "reviewer"

    def test_ai_node_context_from_prev(self):
        p = parse_pipeline({
            "name": "test",
            "nodes": {
                "b": _make_bash_node(command="echo 'step result'"),
                "a": _make_ai_node(prompt="Summarize", depends_on=["b"]),
            },
        })
        ex = DAGExecutor(p)
        # Simulate a completed bash result
        ex.results.append(NodeResult(
            node_id="b", node_type="bash", status="completed", output="step result"
        ))
        result = ex._execute_ai(p.nodes["a"])
        data = json.loads(result.output)
        # Single prev result includes the node output section header
        assert "### b output:" in data["prompt"]
        assert "step result" in data["prompt"]


# ─── Dependency node execution ───────────────────────────────────────

class TestDependencyExecution:
    def test_dependency_noop(self):
        p = _make_pipeline({"a": {"type": "dependency"}})
        ex = DAGExecutor(p)
        result = ex._execute_dependency(p.nodes["a"])
        assert result.status == "completed"
        assert result.output == "Dependency satisfied"


# ─── Dry run mode ────────────────────────────────────────────────────

class TestDryRun:
    def test_dry_run_bash(self):
        p = _make_pipeline({"a": _make_bash_node()})
        ex = DAGExecutor(p, dry_run=True)
        result = ex._execute_node(p.nodes["a"])
        assert result.status == "completed"
        assert "DRY RUN" in result.output

    def test_dry_run_ai(self):
        p = _make_pipeline({"a": _make_ai_node()})
        ex = DAGExecutor(p, dry_run=True)
        result = ex._execute_node(p.nodes["a"])
        assert result.status == "completed"
        assert "DRY RUN" in result.output

    def test_dry_run_full_pipeline(self):
        p = _make_pipeline({
            "a": _make_bash_node(),
            "b": _make_bash_node(command="echo b", depends_on=["a"]),
        })
        ex = DAGExecutor(p, dry_run=True)
        result = ex.run()
        assert result.status == "completed"
        assert result.completed_nodes == 2
        assert all("DRY RUN" in r.output for r in result.results)


# ─── Full pipeline execution ─────────────────────────────────────────

class TestPipelineRun:
    def test_simple_pipeline(self, tmp_path):
        p = _make_pipeline({
            "a": _make_bash_node(command="echo hello"),
            "b": _make_bash_node(command="echo world", depends_on=["a"]),
        })
        ex = DAGExecutor(p, workdir=tmp_path)
        result = ex.run()
        assert result.status == "completed"
        assert result.completed_nodes == 2
        assert result.failed_nodes == 0

    def test_pipeline_failure_stops(self, tmp_path):
        p = _make_pipeline({
            "a": _make_bash_node(command="echo ok"),
            "b": _make_bash_node(command="exit 1"),
            "c": _make_bash_node(command="echo never", depends_on=["b"]),
        })
        ex = DAGExecutor(p, workdir=tmp_path)
        result = ex.run()
        assert result.status == "failed"
        assert result.completed_nodes == 1
        assert result.failed_nodes == 1
        assert result.skipped_nodes == 1

    def test_pipeline_continue_on_error(self, tmp_path):
        """When stop_on_failure=False, a failed node doesn't halt the pipeline,
        but downstream nodes that depend on the failed one are still skipped."""
        p = _make_pipeline({
            "a": _make_bash_node(command="echo ok"),
            "b": _make_bash_node(command="exit 1"),
            "c": _make_bash_node(command="echo after", depends_on=["b"]),
        })
        ex = DAGExecutor(p, workdir=tmp_path)
        ex.stop_on_failure = False
        result = ex.run()
        assert result.status == "partial"
        assert result.completed_nodes == 1  # only 'a' succeeds
        assert result.failed_nodes == 1    # 'b' fails
        assert result.skipped_nodes == 1   # 'c' skipped due to 'b' failure

    def test_dependency_skip_on_failure(self, tmp_path):
        p = _make_pipeline({
            "a": _make_bash_node(command="exit 1"),
            "b": _make_bash_node(command="echo never", depends_on=["a"]),
            "c": _make_bash_node(command="echo also never", depends_on=["a"]),
        })
        ex = DAGExecutor(p, workdir=tmp_path, dry_run=False)
        result = ex.run()
        assert result.skipped_nodes >= 2

    def test_execution_result_to_dict(self, tmp_path):
        p = _make_pipeline({"a": _make_bash_node(command="echo hi")})
        ex = DAGExecutor(p, workdir=tmp_path)
        result = ex.run()
        d = result.to_dict()
        assert d["pipeline_name"] == "test"
        assert d["total_nodes"] == 1
        assert d["completed_nodes"] == 1
        assert "duration_seconds" in d
        assert isinstance(d["results"], list)

    def test_single_node_pipeline(self, tmp_path):
        p = _make_pipeline({"only": _make_bash_node(command="echo solo")})
        ex = DAGExecutor(p, workdir=tmp_path)
        result = ex.run()
        assert result.status == "completed"
        assert result.completed_nodes == 1


# ─── Context chaining ────────────────────────────────────────────────

class TestContextChaining:
    def test_context_passed_to_commands(self, tmp_path):
        p = _make_pipeline({
            "a": _make_bash_node(command="echo {{msg}}"),
        })
        ex = DAGExecutor(p, workdir=tmp_path, context={"msg": "injected"})
        result = ex.run()
        assert result.status == "completed"
        assert "injected" in result.results[0].output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
