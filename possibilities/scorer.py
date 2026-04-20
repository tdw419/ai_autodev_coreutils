"""Fertility scoring and path ranking for the possibility tree."""

from typing import Optional
from .models import PossibilityNode


def compute_fertility(node: PossibilityNode, decay: float = 0.7) -> float:
    """
    Compute fertility score for a node and all its descendants.

    Fertility = how many doors this idea opens, weighted toward near-term.
    Leaf: 0 (dead end, no branching)
    Branch: sum over children of (1 + decay * child_fertility)

    Deeper branching cascades score higher. That's the point.
    """
    if not node.children:
        node.fertility_score = 0.0
        node.direct_fertility = 0
        node.total_descendants = 0
        return 0.0

    child_fertilities = []
    for child in node.children:
        if child.pruned:
            continue
        cf = compute_fertility(child, decay)
        child_fertilities.append(cf)

    if not child_fertilities:
        node.fertility_score = 0.0
        node.direct_fertility = 0
        node.total_descendants = 0
        return 0.0

    node.direct_fertility = len([c for c in node.children if not c.pruned])
    node.total_descendants = sum(
        c.total_descendants for c in node.children if not c.pruned
    ) + node.direct_fertility

    node.fertility_score = sum(
        1.0 + decay * cf for cf in child_fertilities
    )
    return node.fertility_score


def rank_paths(
    tree: PossibilityNode, top_n: int = 10
) -> list[tuple[float, list[PossibilityNode]]]:
    """
    Find root-to-leaf paths, score each by cumulative fertility.
    Returns top N paths ranked highest.
    """
    paths = []

    def dfs(node: PossibilityNode, path: list, score: float):
        path.append(node)
        visible_children = [c for c in node.children if not c.pruned]
        if not visible_children:
            # Leaf node -- this is a complete path
            paths.append((score, list(path)))
        else:
            for child in visible_children:
                dfs(child, path, score + child.fertility_score)
        path.pop()

    dfs(tree, [], tree.fertility_score)
    paths.sort(key=lambda x: x[0], reverse=True)
    return paths[:top_n]


def most_fertile_frontier(tree: PossibilityNode) -> Optional[PossibilityNode]:
    """Find the highest-fertility unexplored node (for guided exploration)."""
    best = None
    best_score = -1

    def walk(node: PossibilityNode):
        nonlocal best, best_score
        if not node.explored and not node.pruned and node.fertility_score > best_score:
            best = node
            best_score = node.fertility_score
        for child in node.children:
            walk(child)

    walk(tree)
    return best


def collect_all_paths(tree: PossibilityNode) -> list[list[PossibilityNode]]:
    """Collect all root-to-leaf paths (DFS)."""
    paths = []

    def dfs(node: PossibilityNode, path: list):
        path.append(node)
        visible = [c for c in node.children if not c.pruned]
        if not visible:
            paths.append(list(path))
        else:
            for child in visible:
                dfs(child, path)
        path.pop()

    dfs(tree, [])
    return paths


def lca_depth(path_a: list[PossibilityNode], path_b: list[PossibilityNode]) -> int:
    """Return depth of lowest common ancestor of two root-to-leaf paths.

    Higher = paths diverged later (more related).  0 = only share root.
    """
    depth = 0
    for na, nb in zip(path_a, path_b):
        if na.id == nb.id:
            depth = na.depth
        else:
            break
    return depth


def _is_question_node(node: PossibilityNode) -> bool:
    """Heuristic: is this node a question/grouping marker rather than a real idea?

    Merged trees create intermediate nodes (category='merged') at depth-1 that
    wrap entire subtrees.  Single-question trees have the root question at
    depth-0 and real ideas start at depth-1, so this returns False for those.

    Decision logic (category is the primary signal):
      1. category == 'merged' → definitely a grouping node (from merge.py)
      2. category in (obvious, contrarian, wildcard, foundational) → real idea
      3. category == '' → fall back to title heuristics
    """
    if node.category == "merged":
        return True
    if node.category != "":
        # Has a real category from BRANCH_PROMPT → it's an idea, regardless of title
        return False
    # category is '' -- check title for question signals
    title = node.title.strip()
    if title.endswith("?"):
        return True
    q_words = ("what ", "how ", "why ", "when ", "where ", "which ",
               "who ", "is ", "can ", "should ", "could ")
    if title.lower().startswith(q_words):
        return True
    # category="" but title doesn't look like a question → assume it's an idea
    return False


def _depth1_branch(path: list[PossibilityNode]) -> str:
    """Return the branch label for a path.

    Normally this is the title of the depth-1 node.  But in merged trees the
    depth-1 node is a question/grouping marker, not a real idea.  In that case
    we descend to the first real idea node on the path to get a meaningful
    branch label.

    This ensures paths under different subtrees of a merge get distinct,
    idea-level labels so convergence analysis can detect cross-subtree
    convergences.
    """
    for n in path:
        if n.depth == 1:
            if _is_question_node(n):
                # Look deeper for the first real idea node
                for deeper in path:
                    if deeper.depth > 1:
                        return deeper.title
                # Fallback: all deeper nodes are questions too (unlikely)
                return n.title
            return n.title
    return "root"


def paths_to_text(paths: list[list[PossibilityNode]]) -> str:
    """Format paths as human-readable text for the convergence prompt.

    Each path is annotated with its branch signature (depth-1 parent) so the
    LLM can distinguish same-branch siblings from genuinely independent paths.
    """
    lines = []
    for i, path in enumerate(paths, 1):
        branch = _depth1_branch(path)
        parts = []
        for n in path:
            if n.depth == 0:
                parts.append(f"[Root] {n.description[:60]}")
            else:
                enables = ", ".join(n.enables[:2]) if n.enables else "none"
                parts.append(f"{n.title} (enables: {enables})")
        lines.append(f"Path {i} [branch: {branch}]: {' -> '.join(parts)}")
    return "\n".join(lines)


def classify_convergence(
    convergences: list[dict],
    paths: list[list[PossibilityNode]],
) -> list[dict]:
    """Post-process LLM convergence results to classify surprise.

    For each convergence point, checks whether the cited evidence paths all
    come from the same depth-1 branch.  Adds a 'surprise' field:
      - 'genuine' = evidence spans different depth-1 branches (high surprise)
      - 'expected' = all evidence from same depth-1 branch (low surprise)
    """
    import re
    branch_map = {i + 1: _depth1_branch(p) for i, p in enumerate(paths)}

    for c in convergences:
        evidence = c.get("evidence", [])
        # Extract path numbers from evidence strings (e.g. "Path 3", "path 7")
        cited_branches = set()
        for e in evidence:
            for m in re.finditer(r"[Pp]ath\s*(\d+)", e):
                path_num = int(m.group(1))
                if path_num in branch_map:
                    cited_branches.add(branch_map[path_num])

        if len(cited_branches) <= 1:
            c["surprise"] = "expected"
        else:
            c["surprise"] = "genuine"

    return convergences


def converge(
    tree: PossibilityNode,
    model: str | None = None,
    complexity: str = "balanced",
) -> list[dict]:
    """Find convergence points across all paths in the tree.

    Returns a list of convergence dicts with title, evidence, strength, implication.
    """
    from .llm import LLMClient
    from .prompts import CONVERGENCE_PROMPT

    paths = collect_all_paths(tree)
    if len(paths) < 2:
        return [{"title": "Not enough paths to converge",
                 "evidence": ["Tree has fewer than 2 complete paths"],
                 "strength": "weak",
                 "implication": "Explore deeper before running convergence."}]

    paths_text = paths_to_text(paths)
    root_question = tree.description or tree.title

    prompt = CONVERGENCE_PROMPT.format(
        root_question=root_question,
        paths_text=paths_text,
    )

    llm = LLMClient(model=model, complexity=complexity)
    result = llm.generate_json(prompt)

    if not result:
        return [{"title": "Convergence analysis failed",
                 "evidence": ["LLM did not return valid JSON"],
                 "strength": "weak",
                 "implication": "Try again with a stronger model (-m)."}]

    result = classify_convergence(result, paths)
    return result
