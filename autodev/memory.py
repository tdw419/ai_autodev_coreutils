"""Persistent creative memory -- what the AI has explored, built, and learned."""

import json
import os
from datetime import datetime
from typing import Optional

from .models import CreativeMemory, CreativeIntent, IntentStatus


MEMORY_DIR = os.path.expanduser("~/.hermes/creative_daemon")
MEMORY_FILE = os.path.join(MEMORY_DIR, "memory.json")
INTENTS_DIR = os.path.join(MEMORY_DIR, "intents")


def _ensure_dirs():
    os.makedirs(MEMORY_DIR, exist_ok=True)
    os.makedirs(INTENTS_DIR, exist_ok=True)


def load_memory() -> CreativeMemory:
    """Load persistent creative memory."""
    _ensure_dirs()
    if not os.path.exists(MEMORY_FILE):
        return CreativeMemory()
    try:
        with open(MEMORY_FILE) as f:
            data = json.load(f)
        return CreativeMemory(
            total_intents=data.get("total_intents", 0),
            completed=data.get("completed", 0),
            failed=data.get("failed", 0),
            abandoned=data.get("abandoned", 0),
            recent_topics=data.get("recent_topics", []),
            interests=data.get("interests", {}),
            lessons=data.get("lessons", []),
            last_run=data.get("last_run"),
        )
    except (json.JSONDecodeError, KeyError):
        return CreativeMemory()


def save_memory(mem: CreativeMemory):
    """Persist creative memory to disk."""
    _ensure_dirs()
    mem.last_run = datetime.utcnow().isoformat()
    with open(MEMORY_FILE, "w") as f:
        json.dump({
            "total_intents": mem.total_intents,
            "completed": mem.completed,
            "failed": mem.failed,
            "abandoned": mem.abandoned,
            "recent_topics": mem.recent_topics[-20:],
            "interests": {k: v for k, v in sorted(mem.interests.items(), key=lambda x: -x[1])[:30]},
            "lessons": mem.lessons[-50:],
            "last_run": mem.last_run,
        }, f, indent=2)


def save_intent(intent: CreativeIntent):
    """Save a creative intent to disk."""
    _ensure_dirs()
    path = os.path.join(INTENTS_DIR, f"{intent.id}.json")
    with open(path, "w") as f:
        json.dump({
            "id": intent.id,
            "summary": intent.summary,
            "reasoning": intent.reasoning,
            "scope": intent.scope,
            "target_dir": intent.target_dir,
            "status": intent.status.value,
            "created_at": intent.created_at,
            "completed_at": intent.completed_at,
            "result_summary": intent.result_summary,
            "artifacts": intent.artifacts,
            "attempt_count": intent.attempt_count,
        }, f, indent=2)


def load_intent(intent_id: str) -> Optional[CreativeIntent]:
    """Load a specific intent from disk."""
    path = os.path.join(INTENTS_DIR, f"{intent_id}.json")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        data = json.load(f)
    return CreativeIntent(
        id=data["id"],
        summary=data["summary"],
        reasoning=data["reasoning"],
        scope=data["scope"],
        target_dir=data["target_dir"],
        status=IntentStatus(data["status"]),
        created_at=data["created_at"],
        completed_at=data.get("completed_at"),
        result_summary=data.get("result_summary"),
        artifacts=data.get("artifacts", []),
        attempt_count=data.get("attempt_count", 0),
    )


def list_intents() -> list:
    """List all intent IDs, newest first."""
    _ensure_dirs()
    intents = []
    for fname in os.listdir(INTENTS_DIR):
        if fname.endswith(".json"):
            path = os.path.join(INTENTS_DIR, fname)
            try:
                with open(path) as f:
                    data = json.load(f)
                intents.append({
                    "id": data["id"],
                    "summary": data["summary"],
                    "status": data["status"],
                    "created_at": data["created_at"],
                })
            except (json.JSONDecodeError, KeyError):
                pass
    intents.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return intents


def record_outcome(intent: CreativeIntent, success: bool, result_summary: str):
    """Update intent and memory with the outcome of a build.
    
    Always reloads memory from disk to avoid stale state.
    """
    mem = load_memory()
    if success:
        intent.status = IntentStatus.COMPLETED
        mem.completed += 1
    else:
        intent.status = IntentStatus.FAILED
        mem.failed += 1
    intent.completed_at = datetime.utcnow().isoformat()
    intent.result_summary = result_summary

    # Track topic interests
    topic = intent.summary.split(".")[0][:50]
    mem.interests[topic] = mem.interests.get(topic, 0) + 1
    if topic not in mem.recent_topics:
        mem.recent_topics.append(topic)

    save_intent(intent)
    save_memory(mem)
