#!/usr/bin/env python3
"""
DAG Executor for the Hermes Agent Orchestrator.

Walks a parsed DAG topologically and executes each node:
- AI nodes: build prompt from config + context, output delegate_task params
- Bash nodes: run shell commands, check exit codes (deterministic gates)
- Loop nodes: repeat children until condition met or max iterations
- Dependency nodes: enforce execution order (no-op)

Designed to be called by the Hermes orchestrator agent, which actually
invokes delegate_task for AI nodes. The executor tracks state and outputs
results per node.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent))
from dag import Pipeline, Node, NodeType, load_pipeline
from execution_log import log_pipeline_run


@dataclass
class NodeResult:
    """Result of executing a single node."""
    node_id: str
    node_type: str
    status: str  # completed, failed, skipped
    output: str = ""
    error: str = ""
    exit_code: int = 0
    duration_seconds: float = 0.0
    iterations: int = 1


@dataclass
class ExecutionResult:
    """Result of executing a full pipeline."""
    pipeline_name: str
    status: str  # completed, failed, partial
    total_nodes: int = 0
    completed_nodes: int = 0
    failed_nodes: int = 0
    skipped_nodes: int = 0
    duration_seconds: float = 0.0
    results: list[NodeResult] = field(default_factory=list)
    context: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "pipeline_name": self.pipeline_name,
            "status": self.status,
            "total_nodes": self.total_nodes,
            "completed_nodes": self.completed_nodes,
            "failed_nodes": self.failed_nodes,
            "skipped_nodes": self.skipped_nodes,
            "duration_seconds": round(self.duration_seconds, 2),
            "results": [asdict(r) for r in self.results],
        }


class DAGExecutor:
    """Execute a Pipeline DAG node by node."""

    def __init__(
        self,
        pipeline: Pipeline,
        workdir: str | Path | None = None,
        context: dict[str, str] | None = None,
        dry_run: bool = False,
    ):
        self.pipeline = pipeline
        self.workdir = Path(workdir) if workdir else Path.cwd()
        self.context = context or {}
        self.dry_run = dry_run
        self.results: list[NodeResult] = []
        self.node_outputs: dict[str, str] = {}  # Store outputs for context chaining
        self.stop_on_failure = True

    def _render_template(self, text: str) -> str:
        """Replace {{key}} placeholders with context values and node outputs."""
        result = text
        for key, value in self.context.items():
            result = result.replace(f"{{{{{key}}}}}", str(value))

        # Also replace {{node_id.output}} with previous node outputs
        for node_id, output in self.node_outputs.items():
            result = result.replace(f"{{{{{node_id}.output}}}}", output)

        return result

    def _execute_bash(self, node: Node) -> NodeResult:
        """Execute a Bash node by running its command."""
        command = self._render_template(node.command)
        start = time.time()

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=str(self.workdir),
                timeout=node.timeout_seconds,
                env={**os.environ, **node.env},
            )
            duration = time.time() - start
            output = result.stdout + result.stderr

            if result.returncode != 0 and not node.continue_on_error:
                return NodeResult(
                    node_id=node.id,
                    node_type=node.type.value,
                    status="failed",
                    output=output[-2000:],  # Truncate large outputs
                    error=f"Command exited with code {result.returncode}",
                    exit_code=result.returncode,
                    duration_seconds=round(duration, 2),
                )

            self.node_outputs[node.id] = output
            return NodeResult(
                node_id=node.id,
                node_type=node.type.value,
                status="completed",
                output=output[-2000:],
                exit_code=result.returncode,
                duration_seconds=round(duration, 2),
            )

        except subprocess.TimeoutExpired:
            duration = time.time() - start
            return NodeResult(
                node_id=node.id,
                node_type=node.type.value,
                status="failed",
                error=f"Command timed out after {node.timeout_seconds}s",
                exit_code=-1,
                duration_seconds=round(duration, 2),
            )

    def _execute_ai(self, node: Node) -> NodeResult:
        """
        Prepare AI node execution.

        Since the executor runs outside the Hermes agent session, AI nodes
        output their prompt as a delegate_task instruction. The orchestrator
        agent reads this and actually calls delegate_task.
        """
        start = time.time()
        prompt = self._render_template(node.prompt)

        # Build the full prompt with context from previous nodes
        context_parts = []
        for prev_result in self.results:
            if prev_result.status == "completed" and prev_result.output:
                context_parts.append(
                    f"### {prev_result.node_id} output:\n{prev_result.output[:1000]}"
                )

        full_prompt = prompt
        if context_parts:
            full_prompt = "\n\n## Previous Step Outputs\n\n".join(context_parts) + "\n\n" + prompt

        duration = time.time() - start

        delegate_params = {
            "prompt": full_prompt,
            "workdir": str(self.workdir),
            "acp_command": "claude",
            "max_turns": node.max_turns,
        }
        if node.role:
            delegate_params["role"] = node.role

        self.node_outputs[node.id] = f"[AI node '{node.id}' - delegate_task needed]"
        return NodeResult(
            node_id=node.id,
            node_type=node.type.value,
            status="completed",
            output=json.dumps(delegate_params, indent=2),
            duration_seconds=round(duration, 2),
        )

    def _execute_loop(self, node: Node) -> NodeResult:
        """Execute a Loop node by iterating over its children."""
        start = time.time()
        last_child_result = None

        for iteration in range(1, node.max_iterations + 1):
            print(f"  [LOOP {node.id}] iteration {iteration}/{node.max_iterations}", file=sys.stderr)

            # Execute children in order
            for child_id in node.children:
                if child_id not in self.pipeline.nodes:
                    continue
                child = self.pipeline.nodes[child_id]
                child_result = self._execute_node(child)
                self.results.append(child_result)
                last_child_result = child_result

                if child_result.status == "failed" and not child.continue_on_error:
                    # Child failed, loop will retry
                    break

            # Check if loop should stop
            if last_child_result and last_child_result.status == "completed":
                # Last child succeeded, loop condition met
                break

        duration = time.time() - start
        iterations_used = iteration if 'iteration' in dir() else node.max_iterations

        if last_child_result and last_child_result.status == "completed":
            status = "completed"
        else:
            status = "failed"

        return NodeResult(
            node_id=node.id,
            node_type=node.type.value,
            status=status,
            output=f"Loop completed after {iterations_used} iterations",
            duration_seconds=round(duration, 2),
            iterations=iterations_used,
        )

    def _execute_review(self, node: Node) -> NodeResult:
        """
        Execute a Review node by evaluating the current pipeline state.

        Uses the review_sensor module to assess output quality.
        """
        start = time.time()

        try:
            from review_sensor import evaluate_run, DEFAULT_CRITERIA
        except ImportError:
            # If review_sensor not available, pass with warning
            return NodeResult(
                node_id=node.id,
                node_type=node.type.value,
                status="completed",
                output="[REVIEW] review_sensor not available, skipping review gate",
                duration_seconds=round(time.time() - start, 2),
            )

        # Build a synthetic run from current results for evaluation
        synthetic_run = {
            "pipeline_name": self.pipeline.name,
            "status": "completed",
            "total_nodes": len(self.results) + 1,
            "completed_nodes": len(self.results),
            "duration_seconds": round(time.time() - start, 2),
            "results": [asdict(r) for r in self.results],
        }

        # Build criteria from node config or use defaults
        criteria = DEFAULT_CRITERIA
        if node.criteria:
            # Map criteria names to default criteria objects
            criteria = [c for c in DEFAULT_CRITERIA if c["name"] in node.criteria]

        # Evaluate using a temporary run ID
        import hashlib
        run_hash = hashlib.md5(json.dumps(synthetic_run, sort_keys=True).encode()).hexdigest()[:16]
        temp_run_id = f"review-{run_hash}"

        # Save temp run for review_sensor to read
        from execution_log import RUNS_DIR
        RUNS_DIR.mkdir(parents=True, exist_ok=True)
        temp_run_path = RUNS_DIR / f"{temp_run_id}.json"
        temp_run_path.write_text(json.dumps(synthetic_run, indent=2))

        try:
            result = evaluate_run(temp_run_id, criteria)
        finally:
            # Clean up temp run
            if temp_run_path.exists():
                temp_run_path.unlink()

        score = result.get("weighted_score", 0)
        verdict = result.get("verdict", "needs_review")
        threshold = node.review_threshold

        if score < threshold:
            if node.on_review_fail == "continue":
                status = "completed"
            elif node.on_review_fail == "warn":
                status = "completed"
                print(f"  [REVIEW WARNING] Score {score} below threshold {threshold}", file=sys.stderr)
            else:  # stop
                status = "failed"
        else:
            status = "completed"

        output = json.dumps({
            "score": score,
            "threshold": threshold,
            "verdict": verdict,
            "summary": result.get("summary", ""),
            "concerns": result.get("concerns", []),
        }, indent=2)

        self.node_outputs[node.id] = f"[REVIEW] score={score}, verdict={verdict}"
        return NodeResult(
            node_id=node.id,
            node_type=node.type.value,
            status=status,
            output=output,
            duration_seconds=round(time.time() - start, 2),
        )

    def _execute_dependency(self, node: Node) -> NodeResult:
        """Dependency nodes are no-ops that just enforce ordering."""
        return NodeResult(
            node_id=node.id,
            node_type=node.type.value,
            status="completed",
            output="Dependency satisfied",
        )

    def _execute_node(self, node: Node) -> NodeResult:
        """Route to the appropriate executor based on node type."""
        if self.dry_run:
            return NodeResult(
                node_id=node.id,
                node_type=node.type.value,
                status="completed",
                output=f"[DRY RUN] Would execute {node.type.value} node",
            )

        executors = {
            NodeType.AI: self._execute_ai,
            NodeType.BASH: self._execute_bash,
            NodeType.LOOP: self._execute_loop,
            NodeType.DEPENDENCY: self._execute_dependency,
            NodeType.REVIEW: self._execute_review,
        }

        executor = executors.get(node.type)
        if not executor:
            return NodeResult(
                node_id=node.id,
                node_type="unknown",
                status="failed",
                error=f"Unknown node type: {node.type}",
            )

        print(f"  [{node.type.value.upper():>11}] {node.id}...", file=sys.stderr, end="")
        result = executor(node)
        print(f" {result.status}", file=sys.stderr)

        return result

    def run(self) -> ExecutionResult:
        """Execute the full pipeline in topological order."""
        start = time.time()
        order = self.pipeline.topological_order()

        exec_result = ExecutionResult(
            pipeline_name=self.pipeline.name,
            status="completed",
            total_nodes=len(order),
        )

        for node_id in order:
            node = self.pipeline.nodes[node_id]

            # Check if dependencies succeeded
            deps_ok = all(
                self.pipeline.nodes[dep].status == "completed"
                for dep in node.depends_on
                if dep in self.pipeline.nodes
            )
            if not deps_ok:
                result = NodeResult(
                    node_id=node_id,
                    node_type=node.type.value,
                    status="skipped",
                    error="Dependency failed",
                )
                self.results.append(result)
                node.status = "skipped"
                exec_result.skipped_nodes += 1
                continue

            result = self._execute_node(node)
            self.results.append(result)
            node.status = result.status

            if result.status == "completed":
                exec_result.completed_nodes += 1
            elif result.status == "failed":
                exec_result.failed_nodes += 1
                if self.stop_on_failure:
                    exec_result.status = "failed"
                    # Mark remaining nodes as skipped
                    remaining = order[order.index(node_id) + 1:]
                    for remaining_id in remaining:
                        skip_result = NodeResult(
                            node_id=remaining_id,
                            node_type=self.pipeline.nodes[remaining_id].type.value,
                            status="skipped",
                            error=f"Pipeline stopped: {node_id} failed",
                        )
                        self.results.append(skip_result)
                        exec_result.skipped_nodes += 1
                    break

        exec_result.results = self.results
        exec_result.duration_seconds = round(time.time() - start, 2)
        if exec_result.failed_nodes > 0 and exec_result.status != "failed":
            exec_result.status = "partial"

        # Log the run to persistent storage
        try:
            log_pipeline_run(exec_result.to_dict())
        except Exception:
            pass  # Don't let logging failures break the pipeline

        return exec_result


def main():
    parser = argparse.ArgumentParser(
        description="Execute a DAG pipeline",
    )
    parser.add_argument("pipeline", help="Path to pipeline YAML file")
    parser.add_argument("--workdir", "-w", default=".", help="Working directory for execution")
    parser.add_argument("--context", "-c", default=None, help="Context JSON (key=value pairs or @file)")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Show execution plan without running")
    parser.add_argument("--continue-on-error", action="store_true", help="Continue pipeline on node failure")

    args = parser.parse_args()

    # Parse context
    context = {}
    if args.context:
        if args.context.startswith("@"):
            with open(args.context[1:]) as f:
                context = json.load(f)
        elif "=" in args.context:
            for pair in args.context.split(","):
                k, v = pair.split("=", 1)
                context[k.strip()] = v.strip()

    # Load and execute
    try:
        pipeline = load_pipeline(args.pipeline)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error loading pipeline: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Executing pipeline: {pipeline.name}", file=sys.stderr)
    print(f"Nodes: {len(pipeline.nodes)}, order: {' -> '.join(pipeline.topological_order())}", file=sys.stderr)
    print(file=sys.stderr)

    executor = DAGExecutor(
        pipeline=pipeline,
        workdir=args.workdir,
        context=context,
        dry_run=args.dry_run,
    )
    executor.stop_on_failure = not args.continue_on_error

    result = executor.run()

    # Output result as JSON
    json.dump(result.to_dict(), sys.stdout, indent=2)
    print()

    # Exit with error if pipeline failed
    if result.status == "failed":
        sys.exit(1)


if __name__ == "__main__":
    main()
