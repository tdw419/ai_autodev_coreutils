#!/usr/bin/env python3
"""
Structural Invariants Engine for the Hermes Agent Orchestrator.

Enforces architectural constraints beyond code style: layer ordering,
dependency direction, forbidden imports, and circular dependencies.

Uses Python AST parsing to check import statements against project-specific
invariants defined in invariants.yaml.

Usage:
    python3 invariant_checker.py --config invariants.yaml --scan ./src
    python3 invariant_checker.py --config invariants.yaml --scan ./src --fix
    python3 invariant_checker.py --config invariants.yaml --scan ./src --json

Based on the Harness Engineering "Rigid Architecture" principle:
enforcing strict layering that limits the agent's search space.
"""

import argparse
import ast
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path


class Violation:
    """A single structural invariant violation."""

    def __init__(self, file: str, line: int, rule: str, severity: str, message: str):
        self.file = file
        self.line = line
        self.rule = rule
        self.severity = severity  # error, warning, info
        self.message = message

    def to_dict(self):
        return {
            "file": self.file,
            "line": self.line,
            "rule": self.rule,
            "severity": self.severity,
            "message": self.message,
        }


class InvariantConfig:
    """Parsed invariants.yaml configuration."""

    def __init__(self, data: dict):
        self.layers = data.get("layers", [])
        self.forbidden_imports = data.get("forbidden_imports", [])
        self.dependency_rules = data.get("dependency_rules", {})
        self.required_annotations = data.get("required_annotations", {})
        self.circular_limit = data.get("circular_limit", 0)
        self.exclude_dirs = data.get("exclude_dirs", [".git", "__pycache__", "node_modules", ".venv", "venv"])
        self.exclude_files = data.get("exclude_files", [])

    @classmethod
    def load(cls, path: str) -> "InvariantConfig":
        import yaml
        with open(path) as f:
            return cls(yaml.safe_load(f) or {})


class ImportVisitor(ast.NodeVisitor):
    """AST visitor that collects all imports from a Python file."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.imports = []  # list of (module, alias, line, is_from)

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append((alias.name, alias.asname, node.lineno, False))
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            for alias in node.names:
                full_import = f"{node.module}.{alias.name}"
                self.imports.append((full_import, alias.asname, node.lineno, True))
        self.generic_visit(node)


class FunctionAnnotationVisitor(ast.NodeVisitor):
    """AST visitor that checks for type annotations on public functions."""

    def __init__(self):
        self.violations = []

    def visit_FunctionDef(self, node):
        self._check_annotations(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self._check_annotations(node)
        self.generic_visit(node)

    def _check_annotations(self, node):
        # Skip private/dunder methods
        if node.name.startswith("_"):
            return
        # Check return annotation
        if node.returns is None:
            self.violations.append((node.lineno, node.name, "return"))


def _determine_layer(file_path: str, layers: list[dict]) -> str | None:
    """Determine which layer a file belongs to based on its path."""
    abs_path = os.path.abspath(file_path)
    for layer in layers:
        layer_dir = os.path.abspath(layer["dir"])
        if abs_path.startswith(layer_dir + os.sep) or abs_path.startswith(layer_dir + "/"):
            return layer["name"]
    return None


def _is_excluded(file_path: str, config: InvariantConfig) -> bool:
    """Check if a file should be excluded from checking."""
    for exc_dir in config.exclude_dirs:
        if f"/{exc_dir}/" in file_path or file_path.endswith(f"/{exc_dir}"):
            return True
    for exc_file in config.exclude_files:
        if file_path.endswith(exc_file):
            return True
    return False


def check_forbidden_imports(file_path: str, imports: list, config: InvariantConfig) -> list[Violation]:
    """Check imports against forbidden patterns."""
    violations = []
    for module, alias, line, is_from in imports:
        for pattern in config.forbidden_imports:
            if isinstance(pattern, dict):
                regex = pattern.get("pattern", "")
                severity = pattern.get("severity", "error")
                message = pattern.get("message", f"Forbidden import: {module}")
            else:
                regex = pattern
                severity = "error"
                message = f"Forbidden import: {module}"

            if re.search(regex, module):
                violations.append(Violation(file_path, line, "forbidden_import", severity, message))
    return violations


def check_layer_order(file_path: str, imports: list, config: InvariantConfig) -> list[Violation]:
    """Check that imports respect layer ordering."""
    violations = []
    if not config.layers:
        return violations

    source_layer = _determine_layer(file_path, config.layers)
    if source_layer is None:
        return violations

    # Build layer index for ordering
    layer_names = [l["name"] for l in config.layers]
    if source_layer not in layer_names:
        return violations

    source_index = layer_names.index(source_layer)

    for module, alias, line, is_from in imports:
        # Try to determine which layer the imported module belongs to
        # by checking the module name prefix against layer dirs
        for i, layer in enumerate(config.layers):
            layer_prefix = layer.get("module_prefix", layer["name"].replace("_", "."))
            if module.startswith(layer_prefix) or module.startswith(layer["name"]):
                # This import is from a specific layer
                target_index = i
                # Check dependency rules
                has_rule = source_layer in config.dependency_rules
                if has_rule:
                    allowed = config.dependency_rules[source_layer]
                    target_layer_name = layer["name"]
                    if target_layer_name not in allowed and target_index > source_index:
                        violations.append(Violation(
                            file_path, line, "layer_violation", "error",
                            f"Layer '{source_layer}' cannot import from layer '{target_layer_name}' "
                            f"(allowed: {allowed})",
                        ))
                break

    return violations


def check_circular_dependencies(import_graph: dict[str, list[str]], limit: int = 0) -> list[Violation]:
    """Detect circular dependencies in the import graph."""
    violations = []

    def find_cycles(start: str, visited: list[str]) -> list[list[str]]:
        cycles = []
        if start in visited:
            cycle_start = visited.index(start)
            cycle = visited[cycle_start:] + [start]
            if len(cycle) > 1:
                cycles.append(cycle)
            return cycles

        visited.append(start)
        for dep in import_graph.get(start, []):
            cycles.extend(find_cycles(dep, visited[:]))
        return cycles

    all_modules = set(import_graph.keys())
    for dep_list in import_graph.values():
        all_modules.update(dep_list)

    for module in all_modules:
        cycles = find_cycles(module, [])
        for cycle in cycles:
            # Normalize cycle to avoid duplicates
            min_idx = cycle.index(min(cycle[:-1]))
            normalized = cycle[min_idx:] + cycle[1:min_idx + 1]
            cycle_key = " -> ".join(normalized)
            cycle_len = len(normalized) - 1

            if limit > 0 and cycle_len > limit:
                continue

            violations.append(Violation(
                normalized[0], 0, "circular_dependency", "error",
                f"Circular dependency: {' -> '.join(normalized)}",
            ))

    # Deduplicate
    seen = set()
    unique = []
    for v in violations:
        key = v.message
        if key not in seen:
            seen.add(key)
            unique.append(v)

    return unique


def check_required_annotations(file_path: str, config: InvariantConfig) -> list[Violation]:
    """Check that public functions have type annotations where required."""
    violations = []

    # Check if this file's layer requires annotations
    source_layer = _determine_layer(file_path, config.layers)
    if source_layer is None:
        # Check global requirement
        if not config.required_annotations.get("all_public", False):
            return violations
    else:
        layer_config = config.required_annotations.get(source_layer, {})
        if not layer_config.get("require_return_types", False):
            return violations

    try:
        with open(file_path) as f:
            tree = ast.parse(f.read(), filename=file_path)
    except SyntaxError:
        return []

    visitor = FunctionAnnotationVisitor()
    visitor.visit(tree)

    for line, name, annotation_type in visitor.violations:
        violations.append(Violation(
            file_path, line, "missing_annotation", "warning",
            f"Public function '{name}' is missing return type annotation",
        ))

    return violations


def scan_project(scan_dir: str, config: InvariantConfig) -> dict:
    """
    Scan a project directory for structural invariant violations.

    Returns a report dict with violations, stats, and import graph.
    """
    violations = []
    import_graph = defaultdict(list)
    files_scanned = 0
    errors = []

    scan_path = Path(scan_dir)

    # Find all Python files
    py_files = []
    for root, dirs, files in os.walk(scan_path):
        # Filter excluded dirs
        dirs[:] = [d for d in dirs if d not in config.exclude_dirs]
        for f in files:
            if f.endswith(".py"):
                full_path = os.path.join(root, f)
                if not _is_excluded(full_path, config):
                    py_files.append(full_path)

    for file_path in py_files:
        files_scanned += 1
        try:
            with open(file_path) as f:
                source = f.read()
            tree = ast.parse(source, filename=file_path)
        except SyntaxError as e:
            errors.append({"file": file_path, "error": f"Syntax error: {e}"})
            continue

        # Collect imports
        visitor = ImportVisitor(file_path)
        visitor.visit(tree)

        # Build import graph (module name -> dependencies)
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        for imp_module, _, _, _ in visitor.imports:
            import_graph[module_name].append(imp_module.split(".")[0])

        # Check forbidden imports
        violations.extend(check_forbidden_imports(file_path, visitor.imports, config))

        # Check layer ordering
        violations.extend(check_layer_order(file_path, visitor.imports, config))

        # Check required annotations
        violations.extend(check_required_annotations(file_path, config))

    # Check circular dependencies
    violations.extend(check_circular_dependencies(dict(import_graph), config.circular_limit))

    # Sort violations by severity
    severity_order = {"error": 0, "warning": 1, "info": 2}
    violations.sort(key=lambda v: (severity_order.get(v.severity, 3), v.file, v.line))

    return {
        "scan_dir": scan_dir,
        "files_scanned": files_scanned,
        "total_violations": len(violations),
        "errors": len(errors),
        "violations": [v.to_dict() for v in violations],
        "parse_errors": errors,
        "import_graph": dict(import_graph),
    }


def fix_violations(report: dict, config: InvariantConfig) -> int:
    """
    Attempt to auto-fix violations. Returns count of fixes applied.

    Currently fixable: forbidden imports (by removing the import line).
    """
    fixes = 0
    for violation in report["violations"]:
        if violation["rule"] == "forbidden_import":
            file_path = violation["file"]
            line_num = violation["line"]
            try:
                with open(file_path) as f:
                    lines = f.readlines()
                if 0 < line_num <= len(lines):
                    lines[line_num - 1] = ""  # Remove the line
                    with open(file_path, "w") as f:
                        f.writelines(lines)
                    fixes += 1
            except (IOError, IndexError):
                continue
    return fixes


def main():
    parser = argparse.ArgumentParser(description="Structural Invariants Checker")
    parser.add_argument("--config", "-c", required=True, help="Path to invariants.yaml")
    parser.add_argument("--scan", "-s", required=True, help="Directory to scan")
    parser.add_argument("--fix", "-f", action="store_true", help="Auto-fix violations")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Output as JSON")
    parser.add_argument("--quiet", "-q", action="store_true", help="Only show errors")

    args = parser.parse_args()

    config = InvariantConfig.load(args.config)
    report = scan_project(args.scan, config)

    if args.fix:
        fixes = fix_violations(report, config)
        print(f"Applied {fixes} auto-fix(es).", file=sys.stderr)
        # Re-scan after fixes
        report = scan_project(args.scan, config)

    if args.json_output:
        print(json.dumps(report, indent=2))
    else:
        if report["parse_errors"]:
            print(f"Parse errors: {report['errors']}", file=sys.stderr)
            for e in report["parse_errors"]:
                print(f"  {e['file']}: {e['error']}", file=sys.stderr)

        if not report["violations"]:
            print(f"✅ No violations found ({report['files_scanned']} files scanned)")
        else:
            errors = sum(1 for v in report["violations"] if v["severity"] == "error")
            warnings = sum(1 for v in report["violations"] if v["severity"] == "warning")
            print(f"Found {report['total_violations']} violations ({errors} errors, {warnings} warnings) in {report['files_scanned']} files")

            if not args.quiet:
                for v in report["violations"]:
                    icon = "❌" if v["severity"] == "error" else "⚠️"
                    print(f"  {icon} {v['file']}:{v['line']} [{v['rule']}] {v['message']}")

    sys.exit(1 if any(v["severity"] == "error" for v in report["violations"]) else 0)


if __name__ == "__main__":
    main()
