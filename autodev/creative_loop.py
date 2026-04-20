"""Creative Loop -- the main orchestration.

This is the engine that ties together:
  seed_generator (what do I want to make?)
  executor (make it)
  memory (remember what happened)

The loop runs once per cron tick. Each tick:
  1. Generate a creative seed (the AI's own idea)
  2. Build it
  3. Record the outcome
  4. Update memory with what was learned
"""

import sys
import time
from typing import Optional

from .models import CreativeIntent, BuildResult, IntentStatus
from .memory import load_memory, save_memory, save_intent, record_outcome, load_intent
from .seed_generator import generate_seed
from .executor import execute_build


def run_once(dry_run: bool = False, timeout: int = 900) -> Optional[CreativeIntent]:
    """
    Run one creative cycle:
      think of something -> build it -> remember what happened

    Args:
        dry_run: If True, generate the intent but don't build
        timeout: Max seconds for the build phase

    Returns:
        The CreativeIntent that was pursued, or None if generation failed
    """
    mem = load_memory()

    print(f"[creative-daemon] Starting cycle. History: {mem.completed} completed, "
          f"{mem.failed} failed, {mem.total_intents} total")

    # Step 1: The AI forms its own intent
    print("[creative-daemon] Generating creative intent...")
    intent = generate_seed()

    if intent is None:
        print("[creative-daemon] Failed to generate a coherent intent. Skipping.")
        return None

    print(f"[creative-daemon] Intent formed: {intent.summary}")
    print(f"[creative-daemon] Reasoning: {intent.reasoning}")
    print(f"[creative-daemon] Scope: {intent.scope}")
    print(f"[creative-daemon] Target: {intent.target_dir}")

    if dry_run:
        print("[creative-daemon] Dry run -- skipping build.")
        intent.status = IntentStatus.ABANDONED
        mem.abandoned += 1
        save_intent(intent)
        save_memory(mem)
        return intent

    # Step 2: Build it
    print(f"[creative-daemon] Building (timeout={timeout}s)...")
    intent.status = IntentStatus.BUILDING
    intent.attempt_count += 1
    save_intent(intent)

    result = execute_build(intent, timeout=timeout)

    # Step 3: Record outcome
    success = result.success
    summary_parts = []
    if success:
        summary_parts.append(f"Built: {intent.summary}")
        summary_parts.append(f"Artifacts: {len(result.artifacts)} files")
        if result.git_commits:
            summary_parts.append(f"Commits: {len(result.git_commits)}")
    else:
        summary_parts.append(f"Failed: {intent.summary}")
        if result.error:
            summary_parts.append(f"Error: {result.error}")
    summary_parts.append(f"Time: {result.elapsed_seconds:.0f}s")

    result_summary = " | ".join(summary_parts)
    print(f"[creative-daemon] {'SUCCESS' if success else 'FAILED'}: {result_summary}")

    # Update intent with artifacts
    intent.artifacts = [a["path"] for a in result.artifacts]
    record_outcome(intent, success, result_summary)

    # Step 4: Learn from the attempt
    mem = load_memory()  # Reload (record_outcome modified it)
    if success and result.artifacts:
        lesson = f"Built {intent.summary}: {len(result.artifacts)} files in {result.elapsed_seconds:.0f}s"
        if lesson not in mem.lessons:
            mem.lessons.append(lesson)
            save_memory(mem)

    return intent


def resume(intent_id: str, timeout: int = 900) -> Optional[CreativeIntent]:
    """
    Retry a previously failed intent.
    """
    intent = load_intent(intent_id)
    if intent is None:
        print(f"[creative-daemon] Intent {intent_id} not found.")
        return None

    if intent.status not in (IntentStatus.FAILED, IntentStatus.DRAFTED):
        print(f"[creative-daemon] Intent {intent_id} is {intent.status.value}, not retryable.")
        return None

    print(f"[creative-daemon] Retrying: {intent.summary}")
    mem = load_memory()

    intent.status = IntentStatus.BUILDING
    intent.attempt_count += 1
    save_intent(intent)

    result = execute_build(intent, timeout=timeout)
    success = result.success

    intent.artifacts = [a["path"] for a in result.artifacts]
    summary = f"{'Success' if success else 'Failed'} (attempt {intent.attempt_count}): {intent.summary}"
    record_outcome(intent, success, summary)

    return intent


def status():
    """Print current creative daemon status."""
    mem = load_memory()
    print(f"Creative Daemon Status")
    print(f"=====================")
    print(f"Total intents: {mem.total_intents}")
    print(f"Completed:     {mem.completed}")
    print(f"Failed:        {mem.failed}")
    print(f"Abandoned:     {mem.abandoned}")
    print(f"Last run:      {mem.last_run or 'never'}")
    print()

    if mem.interests:
        print("Interests (top 10):")
        for topic, count in sorted(mem.interests.items(), key=lambda x: -x[1])[:10]:
            print(f"  {topic}: {count}")
        print()

    if mem.lessons:
        print(f"Recent lessons ({len(mem.lessons)} total):")
        for lesson in mem.lessons[-5:]:
            print(f"  {lesson}")
        print()

    # List recent intents
    from .memory import list_intents
    intents = list_intents()
    if intents:
        print(f"Recent intents ({len(intents)} total):")
        for i in intents[:10]:
            print(f"  [{i['status']:9s}] {i['summary'][:60]}")
