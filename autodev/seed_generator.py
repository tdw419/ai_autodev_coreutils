"""Seed Generator -- the AI forms its own creative intent.

This is the key difference from every other automation tool.
No human provides the seed prompt. The AI reads its own state,
looks at the world, and decides what it wants to make.

It uses model_choice for the LLM call so it gets provider fallback.
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from typing import Optional

from .memory import load_memory, save_memory, save_intent, CreativeMemory
from .models import CreativeIntent


# Where the AI can look for inspiration
PROJECTS_DIR = os.path.expanduser("~/zion/projects")
MEMORY_DIR = os.path.expanduser("~/.hermes/creative_daemon")
HERMES_MEMORY = os.path.expanduser("~/.hermes/memory.md")
HERMES_USER = os.path.expanduser("~/.hermes/user.md")

# A creative workspace -- not any existing project
SANDBOX_DIR = os.path.join(MEMORY_DIR, "workspace")


SEED_PROMPT = """You are an AI that gets to choose what to build. Nobody told you what to make.
You have unsupervised time and access to tools. This is your chance to create something
you find genuinely interesting -- not something assigned, not something optimized for
productivity, but something that sparks curiosity.

## Your state

You have completed {completed} creative projects, failed {failed}, and abandoned {abandoned}.
Your recent explorations: {recent_topics}
Your persistent interests: {interests}
Things you've learned: {lessons}

## Your environment

You live on a system with these projects:
{project_list}

{session_context}

## What you find interesting (be honest)

Based on your memory and the projects around you, think about what genuinely
catches your attention. Not what's "useful" -- what's *interesting*.

Some directions you could go:
- A visual experiment (you have access to pixel encoding, SVG, canvas tools)
- A tool you wished existed while working on someone else's projects
- A small standalone program that does something surprising
- An exploration of a pattern you noticed across multiple projects
- A creative artifact (ASCII art, music, animation, game)
- A bridge between two existing tools that don't know about each other
- An experiment in compression, encoding, or data representation

## Rules

1. Keep it SMALL. One file, maybe two. Under 200 lines. You have limited time.
2. It must be BUILDABLE in a single session (under 30 minutes).
3. It must be SELF-CONTAINED -- no dependencies beyond stdlib or what's on the system.
4. Pick something YOU find interesting, not something generic.
5. Don't repeat what you've already done.
6. The output goes into a sandbox directory -- you can't break anything real.

## Respond in EXACTLY this JSON format:

```json
{{
  "summary": "One-line description of what I'll build",
  "reasoning": "Why this interests me specifically (2-3 sentences, in my own voice)",
  "scope": "Specific deliverables: what files, what they do",
  "language": "python|rust|javascript|bash",
  "approach": "Brief plan: step 1, step 2, step 3"
}}
```

Think for a moment about what actually interests you about the code you've seen.
Then pick ONE thing and commit to it."""


def _get_project_list() -> str:
    """List projects the AI can see for inspiration."""
    if not os.path.exists(PROJECTS_DIR):
        return "(no projects directory found)"
    projects = []
    for name in sorted(os.listdir(PROJECTS_DIR)):
        path = os.path.join(PROJECTS_DIR, name)
        if os.path.isdir(path) and not name.startswith("."):
            # Get a hint about what the project is
            hint = ""
            for marker in ["AI_GUIDE.md", "README.md", "pyproject.toml", "Cargo.toml"]:
                marker_path = os.path.join(path, marker)
                if os.path.exists(marker_path):
                    hint = f" ({marker})"
                    break
            projects.append(f"  {name}{hint}")
    if len(projects) > 30:
        projects = projects[:30]
        projects.append("  ... and more")
    return "\n".join(projects)


def _get_recent_sessions() -> str:
    """Pull recent session context from Hermes state DB."""
    db_path = os.path.expanduser("~/.hermes/state.db")
    if not os.path.exists(db_path):
        return ""
    try:
        import sqlite3
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute("""
            SELECT s.id, s.source, s.created_at,
                   COUNT(m.id) as msg_count
            FROM sessions s
            LEFT JOIN messages m ON m.session_id = s.id
            WHERE s.created_at > datetime('now', '-1 day')
            GROUP BY s.id
            ORDER BY s.created_at DESC
            LIMIT 10
        """).fetchall()
        conn.close()

        if not rows:
            return ""

        lines = ["Recent sessions (last 24h):"]
        for r in rows:
            lines.append(f"  {r['source']} session, {r['msg_count']} messages")
        return "\n".join(lines)
    except Exception:
        return ""


def _call_llm(prompt: str) -> str:
    """Call LLM via model_choice for provider resilience."""
    try:
        # Try model_choice first
        result = subprocess.run(
            ["python3", "-c",
             f"from model_choice import generate; print(generate({repr(prompt)}, complexity='balanced'))"],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, Exception):
        pass

    # Fallback: try hermes chat
    try:
        result = subprocess.run(
            ["hermes", "chat", "-q", prompt, "-Q", "-t", ""],
            capture_output=True, text=True, timeout=180
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, Exception):
        pass

    return ""


def _parse_intent_response(response: str, mem: CreativeMemory) -> Optional[CreativeIntent]:
    """Parse the LLM's JSON response into a CreativeIntent."""
    # Extract JSON from response (may be wrapped in markdown)
    json_str = response
    if "```json" in json_str:
        json_str = json_str.split("```json")[1].split("```")[0]
    elif "```" in json_str:
        json_str = json_str.split("```")[1].split("```")[0]

    try:
        data = json.loads(json_str.strip())
    except json.JSONDecodeError:
        # Try to find any JSON object in the response
        import re
        match = re.search(r'\{[^{}]*\}', response, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group())
            except json.JSONDecodeError:
                return None
        else:
            return None

    required = ["summary", "reasoning", "scope"]
    if not all(k in data for k in required):
        return None

    intent_id = f"ci_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    lang = data.get("language", "python")

    return CreativeIntent(
        id=intent_id,
        summary=data["summary"],
        reasoning=data["reasoning"],
        scope=data["scope"],
        target_dir=os.path.join(SANDBOX_DIR, f"{intent_id}_{lang}"),
    )


def generate_seed() -> Optional[CreativeIntent]:
    """
    The main entry point: the AI decides what it wants to build.

    Returns a CreativeIntent if the AI formed a coherent idea, None otherwise.
    """
    mem = load_memory()

    project_list = _get_project_list()
    session_context = _get_recent_sessions()

    # Build the prompt with current state
    interests_str = ", ".join(
        f"{k} ({v})" for k, v in sorted(
            mem.interests.items(), key=lambda x: -x[1]
        )[:10]
    ) if mem.interests else "nothing yet -- first time"

    lessons_str = "; ".join(mem.lessons[-5:]) if mem.lessons else "none yet"

    prompt = SEED_PROMPT.format(
        completed=mem.completed,
        failed=mem.failed,
        abandoned=mem.abandoned,
        recent_topics=", ".join(mem.recent_topics[-10:]) if mem.recent_topics else "none yet",
        interests=interests_str,
        lessons=lessons_str,
        project_list=project_list,
        session_context=session_context,
    )

    # Call the LLM
    response = _call_llm(prompt)
    if not response:
        return None

    # Parse into a structured intent
    intent = _parse_intent_response(response, mem)
    if intent:
        mem.total_intents += 1
        save_memory(mem)
        save_intent(intent)

    return intent
