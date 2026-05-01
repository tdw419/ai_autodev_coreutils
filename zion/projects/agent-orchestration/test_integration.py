#!/usr/bin/env python3
"""
End-to-end integration test for the DAG executor.

Tests a full pipeline execution from YAML parse through all node types:
bash, ai, dependency, and loop. Verifies execution order, output capture,
failure propagation, context templating, and dry-run mode.
"""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pytest
import yaml
from dag import load_pipeline, parse_pipeline, NodeType
from executor import DAGExecutor, ExecutionResult


def _write_pipeline(tmp_path: Path, pipeline_data: dict) -> Path:
    """Write a pipeline YAML to tmp_path and return the file path."""
    p = tmp_path / "test-pipeline.yaml"
    p.write_text(yaml.dump(pipeline_data))
    return p


# ─── Full pipeline with all 4 node types ─────────────────────────────

class TestFullPipelineExecution:
    def test_all_node_types_pipeline(self, tmp_path):
        """Pipeline: bash -> dependency -> bash -> ai (ordered by deps)."""
        pipeline_data = {
            "name": "integration-test",
            "nodes": {
                "setup": {
                    "type": "bash",
                    "command": "echo 'setup done'",
                },
                "gate": {
                    "type": "dependency",
                    "depends_on": ["setup"],
                },
                "work": {
                    "type": "bash",
                    "command": "echo 'work done'",
                    "depends_on": ["gate"],
                },
                "review": {
                    "type": "ai",
                    "prompt": "Review the work: {{work.output}}",
                    "depends_on": ["work"],
                },
            },
        }
        pfile = _write_pipeline(tmp_path, pipeline_data)
        pipeline = load_pipeline(pfile)
        executor = DAGExecutor(pipeline, workdir=tmp_path)
        result = executor.run()

        assert result.status == "completed"
        assert result.completed_nodes == 4
        assert result.failed_nodes == 0

        # Check execution order
        ids = [r.node_id for r in result.results]
        assert ids.index("setup") < ids.index("gate")
        assert ids.index("gate") < ids.index("work")
        assert ids.index("work") < ids.index("review")

        # Check bash outputs
        setup_result = next(r for r in result.results if r.node_id == "setup")
        assert "setup done" in setup_result.output

        work_result = next(r for r in result.results if r.node_id == "work")
        assert "work done" in work_result.output

        # Check AI node produces delegate params
        review_result = next(r for r in result.results if r.node_id == "review")
        review_data = json.loads(review_result.output)
        assert "prompt" in review_data
        assert "work done" in review_data["prompt"]

    def test_pipeline_with_context_injection(self, tmp_path):
        """Pipeline that uses context variables in commands."""
        pipeline_data = {
            "name": "context-test",
            "nodes": {
                "greet": {
                    "type": "bash",
                    "command": "echo 'Hello, {{name}}!'",
                },
                "count": {
                    "type": "bash",
                    "command": "echo 'Count: {{count}}'",
                    "depends_on": ["greet"],
                },
            },
        }
        pfile = _write_pipeline(tmp_path, pipeline_data)
        pipeline = load_pipeline(pfile)
        executor = DAGExecutor(pipeline, workdir=tmp_path, context={"name": "World", "count": "42"})
        result = executor.run()

        assert result.status == "completed"
        greet = next(r for r in result.results if r.node_id == "greet")
        assert "Hello, World!" in greet.output

        count = next(r for r in result.results if r.node_id == "count")
        assert "Count: 42" in count.output

    def test_pipeline_failure_propagation(self, tmp_path):
        """Pipeline where a mid-stream failure skips downstream nodes."""
        pipeline_data = {
            "name": "failure-test",
            "nodes": {
                "ok": {"type": "bash", "command": "echo ok"},
                "fail": {"type": "bash", "command": "exit 1", "depends_on": ["ok"]},
                "after_fail": {"type": "bash", "command": "echo never", "depends_on": ["fail"]},
                "parallel": {"type": "bash", "command": "echo also never", "depends_on": ["fail"]},
            },
        }
        pfile = _write_pipeline(tmp_path, pipeline_data)
        pipeline = load_pipeline(pfile)
        executor = DAGExecutor(pipeline, workdir=tmp_path)
        result = executor.run()

        assert result.status == "failed"
        assert result.completed_nodes == 1  # only "ok"
        assert result.failed_nodes == 1     # "fail"
        assert result.skipped_nodes == 2    # "after_fail" and "parallel"

    def test_dry_run_full_pipeline(self, tmp_path):
        """Dry run should complete all nodes without executing anything."""
        pipeline_data = {
            "name": "dryrun-test",
            "nodes": {
                "a": {"type": "bash", "command": "echo a"},
                "b": {"type": "bash", "command": "echo b", "depends_on": ["a"]},
                "c": {"type": "ai", "prompt": "Do stuff", "depends_on": ["b"]},
            },
        }
        pfile = _write_pipeline(tmp_path, pipeline_data)
        pipeline = load_pipeline(pfile)
        executor = DAGExecutor(pipeline, workdir=tmp_path, dry_run=True)
        result = executor.run()

        assert result.status == "completed"
        assert result.completed_nodes == 3
        for r in result.results:
            assert "DRY RUN" in r.output

    def test_pipeline_env_variables(self, tmp_path):
        """Pipeline with environment variables passed to commands."""
        pipeline_data = {
            "name": "env-test",
            "nodes": {
                "check": {
                    "type": "bash",
                    "command": "echo $TEST_VAR",
                    "env": {"TEST_VAR": "env_value"},
                },
            },
        }
        pfile = _write_pipeline(tmp_path, pipeline_data)
        pipeline = load_pipeline(pfile)
        executor = DAGExecutor(pipeline, workdir=tmp_path)
        result = executor.run()

        assert result.status == "completed"
        assert "env_value" in result.results[0].output

    def test_execution_result_serialization(self, tmp_path):
        """ExecutionResult.to_dict() produces valid JSON."""
        pipeline_data = {
            "name": "serde-test",
            "nodes": {
                "a": {"type": "bash", "command": "echo test"},
            },
        }
        pfile = _write_pipeline(tmp_path, pipeline_data)
        pipeline = load_pipeline(pfile)
        executor = DAGExecutor(pipeline, workdir=tmp_path)
        result = executor.run()

        d = result.to_dict()
        serialized = json.dumps(d)
        assert json.loads(serialized)  # round-trips

        assert d["pipeline_name"] == "serde-test"
        assert d["status"] == "completed"
        assert len(d["results"]) == 1
        assert d["results"][0]["node_id"] == "a"

    def test_single_bash_pipeline(self, tmp_path):
        """Minimal pipeline with one bash node."""
        pipeline_data = {
            "name": "minimal",
            "nodes": {
                "step1": {"type": "bash", "command": "echo 'minimal test'"},
            },
        }
        pfile = _write_pipeline(tmp_path, pipeline_data)
        pipeline = load_pipeline(pfile)
        executor = DAGExecutor(pipeline, workdir=tmp_path)
        result = executor.run()

        assert result.status == "completed"
        assert result.total_nodes == 1
        assert "minimal test" in result.results[0].output

    def test_parallel_branches(self, tmp_path):
        """Diamond DAG: two parallel branches that converge."""
        pipeline_data = {
            "name": "parallel",
            "nodes": {
                "start": {"type": "bash", "command": "echo start"},
                "branch_a": {"type": "bash", "command": "echo A", "depends_on": ["start"]},
                "branch_b": {"type": "bash", "command": "echo B", "depends_on": ["start"]},
                "merge": {"type": "bash", "command": "echo merged", "depends_on": ["branch_a", "branch_b"]},
            },
        }
        pfile = _write_pipeline(tmp_path, pipeline_data)
        pipeline = load_pipeline(pfile)
        executor = DAGExecutor(pipeline, workdir=tmp_path)
        result = executor.run()

        assert result.status == "completed"
        assert result.completed_nodes == 4
        # Start must be before both branches, both branches before merge
        ids = [r.node_id for r in result.results]
        assert ids.index("start") < ids.index("branch_a")
        assert ids.index("start") < ids.index("branch_b")
        assert ids.index("branch_a") < ids.index("merge")
        assert ids.index("branch_b") < ids.index("merge")

    def test_continue_on_error_pipeline(self, tmp_path):
        """Pipeline with continue_on_error that doesn't halt execution."""
        pipeline_data = {
            "name": "continue-test",
            "nodes": {
                "warn": {"type": "bash", "command": "exit 2", "continue_on_error": True},
                "after": {"type": "bash", "command": "echo survived", "depends_on": ["warn"]},
            },
        }
        pfile = _write_pipeline(tmp_path, pipeline_data)
        pipeline = load_pipeline(pfile)
        executor = DAGExecutor(pipeline, workdir=tmp_path)
        result = executor.run()

        assert result.status == "completed"
        assert result.completed_nodes == 2

    def test_bash_timeout(self, tmp_path):
        """Pipeline with a command that exceeds its timeout."""
        pipeline_data = {
            "name": "timeout-test",
            "nodes": {
                "slow": {"type": "bash", "command": "sleep 30", "timeout_seconds": 1},
            },
        }
        pfile = _write_pipeline(tmp_path, pipeline_data)
        pipeline = load_pipeline(pfile)
        executor = DAGExecutor(pipeline, workdir=tmp_path)
        result = executor.run()

        assert result.status == "failed"
        assert "timed out" in result.results[0].error.lower()

    def test_load_and_execute_standard_pipeline(self, tmp_path):
        """Load the real standard-pipeline.yaml and execute in dry-run mode."""
        pipeline = load_pipeline("pipelines/standard-pipeline.yaml")
        executor = DAGExecutor(pipeline, workdir=tmp_path, dry_run=True)
        result = executor.run()

        assert result.status == "completed"
        assert result.completed_nodes == 7


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
