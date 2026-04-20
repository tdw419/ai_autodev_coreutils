"""Data structures for the creative daemon."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class IntentStatus(Enum):
    DRAFTED = "drafted"
    BUILDING = "building"
    COMPLETED = "completed"
    FAILED = "failed"
    ABANDONED = "abandoned"


@dataclass
class CreativeIntent:
    """An idea the AI chose to pursue, with its own reasoning."""
    id: str
    summary: str  # What I want to build (one line)
    reasoning: str  # Why I chose this (my own words)
    scope: str  # What specifically I'll produce
    target_dir: str  # Where to build it
    status: IntentStatus = IntentStatus.DRAFTED
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    completed_at: Optional[str] = None
    result_summary: Optional[str] = None  # What actually happened
    artifacts: list = field(default_factory=list)  # Files produced
    attempt_count: int = 0


@dataclass
class CreativeMemory:
    """Persistent state across creative sessions."""
    total_intents: int = 0
    completed: int = 0
    failed: int = 0
    abandoned: int = 0
    recent_topics: list = field(default_factory=list)  # Last 10 topics explored
    interests: dict = field(default_factory=dict)  # topic -> count (what I gravitate toward)
    lessons: list = field(default_factory=list)  # Things I learned
    last_run: Optional[str] = None


@dataclass
class BuildResult:
    """Outcome of a creative build attempt."""
    success: bool
    output: str
    artifacts: list = field(default_factory=list)
    error: Optional[str] = None
    elapsed_seconds: float = 0.0
    git_commits: list = field(default_factory=list)
