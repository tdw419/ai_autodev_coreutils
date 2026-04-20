"""Prompts for LLM-driven possibility generation."""


BRANCH_PROMPT = """You are a possibility explorer. Your job is NOT to evaluate or rank ideas -- it is to generate diverse, generative directions that maximize future optionality.

PROJECT CONTEXT:
{project_context}

SEED QUESTION: {seed_question}

We are {depth} level(s) deep in exploration. {depth_guidance}

Generate {n_min}-{n_max} possible directions. Each must be a genuinely different KIND of idea, not a variation on the same theme.

For each direction, provide:

1. TITLE: Short name (5-8 words, specific not vague)
2. DESCRIPTION: What this IS (1-2 sentences, concrete)
3. ENABLES: What doors this OPENS. What becomes possible that was not possible before? List 2-3 specific capabilities or opportunities this unlocks. Think second-order: "if we do X, then Y and Z become possible."
4. RISK: What this might foreclose, break, or make harder.
5. CATEGORY: One of:
   - obvious: The natural next step most people would suggest
   - contrarian: Goes against conventional wisdom or the obvious path
   - wildcard: Unexpected, unconventional, potentially transformative
   - foundational: Infrastructure/enablers that make many other things possible

HARD RULES:
- "Improve UX" is not an idea. "Command palette with fuzzy search that learns from usage patterns" is.
- "Better performance" is not an idea. "Replace the rendering loop with a retained-mode scenegraph that supports incremental redraw" is.
- At least one idea MUST be contrarian and one MUST be wildcard.
- Think across dimensions: not just features, but architecture, distribution, community, business model, integration, abstraction level, target audience.
- If the project is a tool, think about: who else could use it? What would it look like as a platform? What if it did LESS? What if it did something adjacent?
- The ENABLES field is the most important part. Ideas that enable more future possibilities are more valuable.

Return a JSON array:
[{{
  "title": "...",
  "description": "...",
  "enables": ["...", "...", "..."],
  "risk": "...",
  "category": "obvious|contrarian|wildcard|foundational"
}}]"""

DEDUP_PROMPT = """Compare a new idea against already-explored ideas in this tree.

NEW IDEA:
  Title: {new_title}
  Description: {new_desc}

EXISTING IDEAS:
{existing_ideas}

Is the new idea substantially the same as any existing idea? Two ideas are duplicates if they would lead to the same exploration path -- even if worded differently. "Build a plugin system" and "add extension support" are duplicates. "Build a plugin system" and "create an API marketplace" are NOT duplicates.

Return JSON:
{{
  "is_duplicate": true or false,
  "duplicate_of": "title of matching idea or null",
  "similarity": 0.0,
  "reason": "one sentence explanation"
}}"""


CONVERGENCE_PROMPT = """You are analyzing a possibility tree -- a branching set of ideas generated for a project.

The tree has been explored from multiple divergent starting points. Your job is to find the CONVERGENCE POINTS: ideas, themes, or capabilities that appear across multiple independent branches.

ROOT QUESTION: {root_question}

ALL PATHS THROUGH THE TREE (each labeled with its depth-1 branch):
{paths_text}

Analyze these paths and identify 3-7 convergence points. A convergence point is:
- An idea or theme that appears in 3+ different paths (even if worded differently)
- A capability that multiple independent branches say "this enables"
- A shared assumption or constraint that keeps appearing
- A common "next step" that different paths independently arrive at

CRITICAL -- BRANCH DIVERSITY:
Each path is labeled [branch: X] showing which ideational direction it follows. Paths with the SAME branch label are closely related (they explore the same high-level idea), so convergence among them is EXPECTED and not surprising.

Paths with DIFFERENT branch labels represent genuinely independent starting directions. Convergence across different branches is a strong signal -- it means independent lines of thinking arrived at the same conclusion.

IMPORTANT -- MERGED TREES:
This tree may combine explorations from multiple seed questions. When that happens, branch labels reflect the actual IDEAS explored, not just the original question. Look at the IDEA TITLES in each path, not just the branch labels, to find thematic convergences. Two paths from entirely different starting questions can discover the same underlying need or capability.

When assessing convergence strength:
- Genuine convergence (different branches): HIGH value. This is a true signal.
- Expected convergence (same branch): LOW value. This just restates the parent's premise.
- Cross-question convergence (paths originally from different seed questions that arrive at the same insight): VERY HIGH value -- this is the strongest possible signal.
- Weight your STRENGTH ratings accordingly: 4+ DIFFERENT branches = "strong", 2-3 different branches = "moderate", all same branch = "weak" even if many paths agree.

For each convergence point:
1. TITLE: Short name (3-6 words)
2. EVIDENCE: Which paths converge here (cite specific ideas AND their branch labels, e.g. "Path 3 [branch: Plugin System] says X, Path 7 [branch: API Platform] says Y")
3. STRENGTH: Based on branch diversity (strong = 4+ different branches, moderate = 2-3 different branches, weak = all same branch)
4. IMPLICATION: What this convergence means -- if paths from different starting points all need X, then X is probably essential, not optional.

HARD RULES:
- Do NOT list generic observations ("all paths involve code"). Only list specific, non-obvious convergences.
- Cite actual idea titles from the tree as evidence.
- Always note whether the convergence is genuine (cross-branch) or expected (same-branch) in your analysis.
- The most valuable convergence points are "hidden requirements" -- things nobody explicitly asked for but that multiple independent branches discovered.

Return a JSON array:
[{{"title": "...", "evidence": ["Path N [branch: X] says Y", ...], "strength": "strong|moderate|weak", "implication": "..."}}]"""


def get_depth_guidance(depth: int) -> str:
    """Get guidance text for how deep we are in the tree."""
    if depth == 0:
        return "Think broad and diverse. Span multiple dimensions of possibility."
    elif depth == 1:
        return "Get more specific. What are the concrete sub-approaches within this direction?"
    else:
        return "Get very concrete. What are the specific technical or strategic choices at this level?"
