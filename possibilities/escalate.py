"""Provider escalation -- re-explore thin branches with progressively stronger models.

Uses model_choice for provider selection, fallback, and cost tracking.
Escalation walks through complexity tiers: balanced -> thorough -> thorough_strong.
"""

from typing import Optional

from .models import PossibilityNode, ExplorationConfig
from .scorer import compute_fertility


# Map escalation steps to model_choice complexity levels.
# Each step tries a stronger tier than the previous.
ESCALATION_COMPLEXITIES = ["balanced", "thorough", "thorough_strong"]

# Human-readable labels for display
COMPLEXITY_LABELS = {
    "balanced": "Balanced (e.g. ZAI glm-5.1)",
    "thorough": "Thorough (e.g. Gemini 2.5 Flash)",
    "thorough_strong": "Strong (e.g. Claude Sonnet)",
}


def generate_for_tier(complexity: str, prompt: str,
                      temperature: float = 0.9) -> list[dict]:
    """Generate branches using model_choice at the given complexity tier.

    Falls back to the next available provider automatically if the
    first choice fails.
    """
    from model_choice import generate_json, pick

    provider = pick(complexity=complexity)
    if not provider:
        return []

    try:
        result = generate_json(
            prompt,
            complexity=complexity,
            temperature=temperature,
            max_tokens=3000,
        )
    except (ValueError, RuntimeError):
        return []

    if isinstance(result, list):
        return result
    if isinstance(result, dict):
        return [result]
    return []


def _provider_label_for_complexity(complexity: str) -> str:
    """Get a display label showing which provider model_choice would pick."""
    from model_choice import pick
    provider = pick(complexity=complexity)
    if provider:
        return f"{provider.label} ({complexity})"
    return COMPLEXITY_LABELS.get(complexity, complexity)


def find_thin_nodes(
    tree: PossibilityNode,
    min_children: int = 2,
) -> list[PossibilityNode]:
    """Find nodes that could benefit from re-exploration.

    A node is "thin" if it's been explored but has fewer than
    min_children non-pruned children.
    """
    thin = []

    def walk(node: PossibilityNode):
        if node.pruned or node.depth == 0:
            pass  # skip root and pruned
        elif not node.children and not node.explored:
            thin.append(node)  # unexplored leaf
        elif node.explored and len([c for c in node.children if not c.pruned]) < min_children:
            thin.append(node)  # too few branches
        for child in node.children:
            walk(child)

    walk(tree)
    return thin


def _starting_complexity_index(starting_complexity: str) -> int:
    """Find where in the escalation chain to start."""
    try:
        return ESCALATION_COMPLEXITIES.index(starting_complexity)
    except ValueError:
        return 0


def escalate(
    tree: PossibilityNode,
    current_model: str = "openai/glm-5.1",
    project_path: str = ".",
    max_tiers: int = 3,
    min_children: int = 2,
    decay: float = 0.7,
    starting_complexity: str = "balanced",
) -> PossibilityNode:
    """Re-explore thin branches with progressively stronger models.

    Args:
        tree: Existing tree to improve.
        current_model: Model that was used for the initial exploration.
                       Kept for backwards compat -- no longer used for
                       tier lookup.
        project_path: Project directory for context.
        max_tiers: How many complexity levels to escalate (default 3).
        min_children: Nodes with fewer non-pruned children are "thin".
        decay: Fertility decay factor.
        starting_complexity: Complexity level the initial exploration used.
                             Escalation starts at the NEXT level up.

    Returns:
        The tree with expanded branches from stronger models.
    """
    # Build escalation chain starting after the current complexity
    start_idx = _starting_complexity_index(starting_complexity)
    chain = ESCALATION_COMPLEXITIES[start_idx + 1: start_idx + 1 + max_tiers]

    # Resolve labels and filter out tiers with no available provider
    tiers_to_try = []
    for c in chain:
        label = _provider_label_for_complexity(c)
        from model_choice import pick
        if pick(complexity=c):
            tiers_to_try.append((c, label))
        else:
            print(f"  Skipping {label}: no available provider")

    if not tiers_to_try:
        print("  No stronger tiers available. Install or auth a provider.")
        return tree

    # Initial score
    compute_fertility(tree, decay)
    prev_fertility = tree.fertility_score

    print(f"  Current fertility: {prev_fertility:.1f}")
    print(f"  Escalation chain: {' -> '.join(label for _, label in tiers_to_try)}")
    print()

    for tier_idx, (complexity, label) in enumerate(tiers_to_try):
        # Find thin nodes
        thin = find_thin_nodes(tree, min_children=min_children)
        if not thin:
            print(f"  Tier {tier_idx + 1}: No thin nodes found. Tree is healthy.")
            break

        print(f"  Tier {tier_idx + 1}: {label}")
        print(f"    Found {len(thin)} thin nodes, re-exploring...")

        # Get project context (same for all nodes in this tier)
        from .context import gather_project_context
        project_context = gather_project_context(project_path)

        # Figure out the actual model used (for model_used metadata)
        from model_choice import pick
        provider = pick(complexity=complexity)
        model_label = f"{provider.provider}/{provider.model}" if provider else complexity

        # Re-explore each thin node
        improved = 0
        for node in thin:
            node.explored = False
            node.children = []

            try:
                from .prompts import BRANCH_PROMPT, get_depth_guidance
                prompt = BRANCH_PROMPT.format(
                    project_context=project_context,
                    seed_question=node.description or node.title,
                    depth=node.depth,
                    depth_guidance=get_depth_guidance(node.depth),
                    n_min=3,
                    n_max=7,
                )
                branches_raw = generate_for_tier(complexity, prompt)
                if branches_raw:
                    for bd in branches_raw:
                        child = PossibilityNode(
                            title=bd.get("title", "Untitled"),
                            description=bd.get("description", ""),
                            enables=bd.get("enables", []),
                            risk=bd.get("risk", ""),
                            category=bd.get("category", ""),
                            depth=node.depth + 1,
                            parent_id=node.id,
                            model_used=model_label,
                        )
                        node.children.append(child)
                    improved += 1
                    print(f"      + {node.title}: {len(node.children)} new branches")
                else:
                    print(f"      [-] {node.title}: no valid branches returned")
            except Exception as e:
                print(f"      [!] {node.title}: {e}")

            node.explored = True

        print(f"    Improved {improved}/{len(thin)} nodes")

        # Re-score
        compute_fertility(tree, decay)
        new_fertility = tree.fertility_score
        delta = new_fertility - prev_fertility

        print(f"    Fertility: {prev_fertility:.1f} -> {new_fertility:.1f} ({'+' if delta >= 0 else ''}{delta:.1f})")
        print()

        if delta < 0.5 and tier_idx > 0:
            print("  Fertility plateau reached, stopping escalation.")
            break

        prev_fertility = new_fertility

    return tree
