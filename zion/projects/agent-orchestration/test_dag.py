#!/usr/bin/env python3
"""Quick validation tests for dag.py"""
import sys
sys.path.insert(0, ".")
from dag import parse_pipeline, load_pipeline

# Test 1: Parse standard pipeline
print("Test 1: Parse standard pipeline...")
p = load_pipeline("pipelines/standard-pipeline.yaml")
assert len(p.nodes) == 7, f"Expected 7 nodes, got {len(p.nodes)}"
order = p.topological_order()
assert order[0] == "plan", f"First node should be 'plan', got {order[0]}"
assert order[-1] == "commit", f"Last node should be 'commit', got {order[-1]}"
print(f"  PASS: {len(p.nodes)} nodes, order: {' -> '.join(order)}")

# Test 2: Cycle detection
print("Test 2: Cycle detection...")
try:
    parse_pipeline({
        "name": "cycle-test",
        "nodes": {
            "a": {"type": "bash", "command": "echo a", "depends_on": ["b"]},
            "b": {"type": "bash", "command": "echo b", "depends_on": ["a"]},
        }
    })
    print("  FAIL: Should have detected cycle")
    sys.exit(1)
except ValueError as e:
    print(f"  PASS: {e}")

# Test 3: Missing dependency
print("Test 3: Missing dependency...")
try:
    parse_pipeline({
        "name": "missing-dep",
        "nodes": {
            "a": {"type": "bash", "command": "echo a", "depends_on": ["nonexistent"]},
        }
    })
    print("  FAIL: Should have detected missing dep")
    sys.exit(1)
except ValueError as e:
    print(f"  PASS: {e}")

# Test 4: AI node without prompt
print("Test 4: AI node validation...")
try:
    parse_pipeline({
        "name": "no-prompt",
        "nodes": {
            "a": {"type": "ai"},
        }
    })
    print("  FAIL: Should have detected missing prompt")
    sys.exit(1)
except ValueError as e:
    print(f"  PASS: {e}")

# Test 5: Entry nodes
print("Test 5: Entry nodes...")
assert p.entry_nodes == ["plan"], f"Expected ['plan'], got {p.entry_nodes}"
print("  PASS")

print("\nAll tests passed!")
