#!/usr/bin/env python3
"""
DAG YAML schema, parser, and validator for the Hermes Agent Orchestrator.

Defines 4 node types (AI, Bash, Loop, Dependency) and provides:
- Dataclass models for nodes and edges
- YAML parser with DAG validation (acyclic check)
- Topological sort for execution ordering
- CLI for parsing and validating pipeline YAML files

Modeled on Archon's deterministic workflow approach.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class NodeType(str, Enum):
    AI = "ai"
    BASH = "bash"
    LOOP = "loop"
    DEPENDENCY = "dependency"


@dataclass
class Node:
    """A single node in the DAG pipeline."""
    id: str
    type: NodeType
    name: str = ""
    description: str = ""
    # AI node fields
    prompt: str = ""
    role: str = ""
    max_turns: int = 20
    # Bash node fields
    command: str = ""
    continue_on_error: bool = False
    # Loop node fields
    max_iterations: int = 3
    until: str = ""  # condition expression
    children: list[str] = field(default_factory=list)
    # Common fields
    depends_on: list[str] = field(default_factory=list)
    timeout_seconds: int = 300
    env: dict[str, str] = field(default_factory=dict)
    # Runtime state (set during execution)
    status: str = "pending"  # pending, running, completed, failed, skipped
    result: Any = None
    error: str = ""

    def __post_init__(self):
        if not self.name:
            self.name = self.id


@dataclass
class Pipeline:
    """A complete DAG pipeline definition."""
    name: str = ""
    description: str = ""
    version: str = "1.0"
    nodes: dict[str, Node] = field(default_factory=dict)
    env: dict[str, str] = field(default_factory=dict)

    @property
    def entry_nodes(self) -> list[str]:
        """Nodes with no dependencies (pipeline entry points)."""
        return [nid for nid, n in self.nodes.items() if not n.depends_on]

    def topological_order(self) -> list[str]:
        """Return node IDs in topological (execution) order."""
        visited: set[str] = set()
        order: list[str] = []
        temp: set[str] = set()

        def visit(node_id: str):
            if node_id in temp:
                raise ValueError(f"Cycle detected involving node: {node_id}")
            if node_id in visited:
                return
            temp.add(node_id)
            node = self.nodes[node_id]
            for dep in node.depends_on:
                if dep in self.nodes:
                    visit(dep)
            temp.remove(node_id)
            visited.add(node_id)
            order.append(node_id)

        for nid in self.nodes:
            if nid not in visited:
                visit(nid)

        return order


def parse_node(node_id: str, raw: dict) -> Node:
    """Parse a raw dict into a Node dataclass."""
    node_type = NodeType(raw.get("type", "dependency"))
    return Node(
        id=node_id,
        type=node_type,
        name=raw.get("name", node_id),
        description=raw.get("description", ""),
        prompt=raw.get("prompt", ""),
        role=raw.get("role", ""),
        max_turns=raw.get("max_turns", 20),
        command=raw.get("command", ""),
        continue_on_error=raw.get("continue_on_error", False),
        max_iterations=raw.get("max_iterations", 3),
        until=raw.get("until", ""),
        children=raw.get("children", []),
        depends_on=raw.get("depends_on", []),
        timeout_seconds=raw.get("timeout_seconds", 300),
        env=raw.get("env", {}),
    )


def parse_pipeline(raw: dict) -> Pipeline:
    """Parse a raw YAML dict into a Pipeline with validation."""
    pipeline = Pipeline(
        name=raw.get("name", "unnamed"),
        description=raw.get("description", ""),
        version=raw.get("version", "1.0"),
        env=raw.get("env", {}),
    )

    # Parse nodes
    raw_nodes = raw.get("nodes", {})
    if not raw_nodes:
        raise ValueError("Pipeline has no nodes defined")

    for node_id, node_raw in raw_nodes.items():
        if not isinstance(node_raw, dict):
            raise ValueError(f"Node '{node_id}' must be a dict, got {type(node_raw).__name__}")
        pipeline.nodes[node_id] = parse_node(node_id, node_raw)

    # Validate dependencies reference existing nodes
    for node_id, node in pipeline.nodes.items():
        for dep in node.depends_on:
            if dep not in pipeline.nodes:
                raise ValueError(f"Node '{node_id}' depends on '{dep}' which doesn't exist")

    # Validate loop children reference existing nodes
    for node_id, node in pipeline.nodes.items():
        if node.type == NodeType.LOOP:
            for child in node.children:
                if child not in pipeline.nodes:
                    raise ValueError(f"Loop node '{node_id}' references child '{child}' which doesn't exist")

    # Validate node types have required fields
    for node_id, node in pipeline.nodes.items():
        if node.type == NodeType.AI and not node.prompt:
            raise ValueError(f"AI node '{node_id}' has no prompt defined")
        if node.type == NodeType.BASH and not node.command:
            raise ValueError(f"Bash node '{node_id}' has no command defined")
        if node.type == NodeType.LOOP and not node.children:
            raise ValueError(f"Loop node '{node_id}' has no children defined")

    # Check for cycles via topological sort
    pipeline.topological_order()

    return pipeline


def load_pipeline(path: str | Path) -> Pipeline:
    """Load and parse a pipeline from a YAML file."""
    import yaml
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Pipeline file not found: {path}")

    with open(path) as f:
        raw = yaml.safe_load(f)

    if not isinstance(raw, dict):
        raise ValueError(f"Pipeline file must contain a YAML dict, got {type(raw).__name__}")

    return parse_pipeline(raw)


def pipeline_to_dict(pipeline: Pipeline) -> dict:
    """Serialize a Pipeline back to a dict for JSON output."""
    def node_to_dict(node: Node) -> dict:
        d: dict[str, Any] = {
            "type": node.type.value,
            "name": node.name,
            "description": node.description,
            "depends_on": node.depends_on,
            "timeout_seconds": node.timeout_seconds,
        }
        if node.type == NodeType.AI:
            d["prompt"] = node.prompt
            d["role"] = node.role
            d["max_turns"] = node.max_turns
        elif node.type == NodeType.BASH:
            d["command"] = node.command
            d["continue_on_error"] = node.continue_on_error
        elif node.type == NodeType.LOOP:
            d["max_iterations"] = node.max_iterations
            d["until"] = node.until
            d["children"] = node.children
        if node.env:
            d["env"] = node.env
        return d

    return {
        "name": pipeline.name,
        "description": pipeline.description,
        "version": pipeline.version,
        "env": pipeline.env,
        "nodes": {nid: node_to_dict(n) for nid, n in pipeline.nodes.items()},
        "execution_order": pipeline.topological_order(),
        "entry_nodes": pipeline.entry_nodes,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Parse and validate DAG pipeline YAML files",
    )
    parser.add_argument(
        "pipeline",
        help="Path to pipeline YAML file",
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output as JSON",
    )
    parser.add_argument(
        "--order", "-o",
        action="store_true",
        help="Show topological execution order only",
    )

    args = parser.parse_args()

    try:
        pipeline = load_pipeline(args.pipeline)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.order:
        print(" -> ".join(pipeline.topological_order()))
    elif args.json:
        json.dump(pipeline_to_dict(pipeline), sys.stdout, indent=2)
        print()
    else:
        d = pipeline_to_dict(pipeline)
        print(f"Pipeline: {d['name']} (v{d['version']})")
        print(f"Description: {d['description']}")
        print(f"Nodes: {len(d['nodes'])}")
        print(f"Entry points: {d['entry_nodes']}")
        print(f"Execution order: {' -> '.join(d['execution_order'])}")
        print()
        for node_id in d["execution_order"]:
            node = d["nodes"][node_id]
            deps = f" (after: {', '.join(node['depends_on'])})" if node["depends_on"] else ""
            print(f"  [{node['type'].upper():>11}] {node_id}{deps}")
            print(f"              {node['description']}")


if __name__ == "__main__":
    main()
