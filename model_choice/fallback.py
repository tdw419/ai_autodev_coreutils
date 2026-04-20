"""Fallback chains -- retry with next provider on failure.

Enhanced with:
- Error classification (transient vs permanent)
- Retry-with-backoff for transient errors (429, timeout)
- Cooldown tracking to deprioritize recently-failed providers
- Fallback diagnostics for debugging
"""

import logging
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from .registry import Registry, Provider, COMPLEXITY_ORDER

logger = logging.getLogger("model_choice.fallback")


# ---- error classification ----

class ErrorKind(Enum):
    """Classification of provider errors for fallback decisions."""
    TRANSIENT = "transient"      # Retryable: 429, timeout, connection reset
    AUTH = "auth"                # Auth failure: bad key, revoked token
    PERMANENT = "permanent"      # Non-retryable: 404, model not found
    UNKNOWN = "unknown"          # Unclassified -- treat as transient


# Patterns that indicate specific error types (checked against error message)
_TRANSIENT_SIGNALS = (
    "429", "rate limit", "too many requests", "rate_limit",
    "timeout", "timed out", "connectionerror", "connection refused",
    "connection reset", "broken pipe", "temporary failure",
    "service unavailable", "503", "502", "bad gateway",
    "upstream", "retry", "capacity",
)
_AUTH_SIGNALS = (
    "401", "403", "unauthorized", "forbidden", "invalid api key",
    "authentication", "api key", "revoked", "credential",
    "multiple authentication",
)
_PERMANENT_SIGNALS = (
    "404", "not found", "model not found", "invalid model",
    "context length", "maximum context",
)


def classify_error(error: Exception) -> ErrorKind:
    """Classify an exception to determine fallback behavior.

    TRANSIENT: Worth retrying (possibly with backoff or different provider).
    AUTH: Provider is misconfigured, skip it entirely.
    PERMANENT: Provider fundamentally can't handle this request.
    UNKNOWN: Default to transient (safer to retry).
    """
    msg = str(error).lower()
    exc_type = type(error).__name__.lower()

    # Check for specific error types via class name
    if "timeout" in exc_type:
        return ErrorKind.TRANSIENT
    if "connection" in exc_type:
        return ErrorKind.TRANSIENT

    # Check message patterns
    for sig in _AUTH_SIGNALS:
        if sig in msg:
            return ErrorKind.AUTH
    for sig in _PERMANENT_SIGNALS:
        if sig in msg:
            return ErrorKind.PERMANENT
    for sig in _TRANSIENT_SIGNALS:
        if sig in msg:
            return ErrorKind.TRANSIENT

    return ErrorKind.UNKNOWN


def is_retryable(kind: ErrorKind) -> bool:
    """Whether this error kind is worth retrying (same provider or fallback)."""
    return kind in (ErrorKind.TRANSIENT, ErrorKind.UNKNOWN)


# ---- cooldown tracking ----

@dataclass
class ProviderHealth:
    """Tracks recent health of a provider for fallback decisions."""
    provider_name: str
    last_failure: float = 0.0
    last_success: float = 0.0
    consecutive_failures: int = 0
    total_failures: int = 0
    total_successes: int = 0

    def record_success(self):
        self.last_success = time.time()
        self.consecutive_failures = 0
        self.total_successes += 1

    def record_failure(self):
        self.last_failure = time.time()
        self.consecutive_failures += 1
        self.total_failures += 1

    @property
    def cooldown_remaining(self) -> float:
        """Seconds remaining until this provider is off cooldown."""
        if self.consecutive_failures == 0:
            return 0.0
        # Exponential backoff: 5s, 10s, 20s, 40s... max 300s
        cooldown = min(5 * (2 ** (self.consecutive_failures - 1)), 300)
        elapsed = time.time() - self.last_failure
        return max(0.0, cooldown - elapsed)

    @property
    def is_on_cooldown(self) -> bool:
        return self.cooldown_remaining > 0


class FallbackHistory:
    """Thread-safe tracker of provider health across fallback attempts.

    Persists in-memory for the lifetime of the process. Used to:
    - Deprioritize providers on cooldown in fallback chains
    - Provide diagnostics about recent failures
    """

    def __init__(self):
        self._health: dict[str, ProviderHealth] = {}
        self._lock = threading.Lock()

    def record_success(self, provider_name: str):
        with self._lock:
            h = self._health.setdefault(provider_name,
                                        ProviderHealth(provider_name))
            h.record_success()

    def record_failure(self, provider_name: str):
        with self._lock:
            h = self._health.setdefault(provider_name,
                                        ProviderHealth(provider_name))
            h.record_failure()

    def is_on_cooldown(self, provider_name: str) -> bool:
        with self._lock:
            h = self._health.get(provider_name)
            return h.is_on_cooldown if h else False

    def get_health(self, provider_name: str) -> Optional[ProviderHealth]:
        with self._lock:
            h = self._health.get(provider_name)
            if h:
                # Return a copy so caller can read without holding lock
                return ProviderHealth(
                    provider_name=h.provider_name,
                    last_failure=h.last_failure,
                    last_success=h.last_success,
                    consecutive_failures=h.consecutive_failures,
                    total_failures=h.total_failures,
                    total_successes=h.total_successes,
                )
            return None

    def get_all_health(self) -> dict[str, ProviderHealth]:
        with self._lock:
            return {
                name: ProviderHealth(
                    provider_name=h.provider_name,
                    last_failure=h.last_failure,
                    last_success=h.last_success,
                    consecutive_failures=h.consecutive_failures,
                    total_failures=h.total_failures,
                    total_successes=h.total_successes,
                )
                for name, h in self._health.items()
            }

    def reset(self):
        with self._lock:
            self._health.clear()


# Module-level singleton
_history = FallbackHistory()


def get_fallback_history() -> FallbackHistory:
    """Get the shared fallback history tracker."""
    return _history


# ---- fallback chain building ----

def _canonical_complexity(complexity: str) -> str:
    """Map internal modes to their canonical complexity tier."""
    if complexity in ("balanced_only",):
        return "balanced"
    if complexity in ("thorough_strong",):
        return "thorough"
    return complexity


def _build_fallback_chain(registry: Registry, start_provider: Provider,
                          complexity: str,
                          skip_cooldown: bool = False) -> list[Provider]:
    """Build an ordered list of fallback providers after start_provider.

    Walks the providers list starting after start_provider, collecting
    available ones that match the complexity tier or higher.

    If skip_cooldown is False, providers on cooldown are deprioritized
    (moved to the end of the chain) rather than excluded entirely.
    """
    chain = []
    cooled = []  # providers on cooldown -- appended at end
    started = False
    requested = COMPLEXITY_ORDER.get(
        _canonical_complexity(complexity), 2
    )

    for p in registry.providers:
        if p is start_provider:
            started = True
            continue
        if not started:
            continue
        if not p.available:
            continue
        # Only include providers at or below the effective tier
        tier = COMPLEXITY_ORDER.get(p.complexity, 2)
        if tier <= requested:
            if not skip_cooldown and _history.is_on_cooldown(p.provider):
                cooled.append(p)
            else:
                chain.append(p)

    # Providers on cooldown go last (still tried, but deprioritized)
    return chain + cooled


# ---- retry configuration ----

@dataclass
class RetryConfig:
    """Configuration for retry behavior within fallback."""
    max_retries: int = 1              # retries on SAME provider for transient errors
    base_delay: float = 1.0           # initial backoff delay in seconds
    max_delay: float = 30.0           # max backoff delay
    backoff_factor: float = 2.0       # exponential multiplier
    retry_on: tuple[ErrorKind, ...] = (
        ErrorKind.TRANSIENT, ErrorKind.UNKNOWN
    )


DEFAULT_RETRY_CONFIG = RetryConfig()


def _compute_delay(attempt: int, config: RetryConfig) -> float:
    """Compute backoff delay for a given attempt number (0-indexed)."""
    delay = config.base_delay * (config.backoff_factor ** attempt)
    return min(delay, config.max_delay)


# ---- main fallback logic ----

@dataclass
class FallbackResult:
    """Detailed result from a fallback attempt chain."""
    text: str
    provider: Provider
    attempts: list[dict] = field(default_factory=list)
    # Each attempt: {"provider": str, "error_kind": str|None, "error": str|None,
    #                "retries": int, "succeeded": bool}


def call_with_fallback(
    registry: Registry,
    provider: Provider,
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 2000,
    json_mode: bool = False,
    system: str | None = None,
    complexity: str = "balanced",
    retry_config: RetryConfig | None = None,
) -> tuple[str, Provider]:
    """Call provider, fall back to next available on failure.

    Returns (GenerateResult, provider_that_succeeded).
    Raises RuntimeError only if ALL providers in the chain fail.

    Enhancement over basic fallback:
    - Retries transient errors on the same provider with exponential backoff
    - Tracks provider health in FallbackHistory
    - Deprioritizes providers on cooldown
    - Classifies errors for smarter retry/failover decisions
    """
    from .backends import call as backend_call

    if retry_config is None:
        retry_config = DEFAULT_RETRY_CONFIG

    errors = []
    attempts = []
    tried_providers = set()

    # --- Try the primary provider (with retry for transient errors) ---
    primary_result = _try_provider_with_retry(
        backend_call, provider, prompt, temperature, max_tokens,
        json_mode, system, retry_config, attempts,
    )
    if primary_result is not None:
        _history.record_success(provider.provider)
        return primary_result, provider

    tried_providers.add(provider.provider)

    # --- Build fallback chain and try each ---
    fallbacks = _build_fallback_chain(registry, provider, complexity)
    for fallback in fallbacks:
        # Skip providers we've already tried (avoid duplicates)
        if fallback.provider in tried_providers:
            continue

        fb_result = _try_provider_with_retry(
            backend_call, fallback, prompt, temperature, max_tokens,
            json_mode, system, retry_config, attempts,
        )
        if fb_result is not None:
            _history.record_success(fallback.provider)
            return fb_result, fallback

        tried_providers.add(fallback.provider)

    # All failed
    error_msgs = [f"{a['provider']}: {a['error']}" for a in attempts
                  if a.get("error")]
    raise RuntimeError(
        f"All providers failed: {'; '.join(error_msgs)}"
    )


def _try_provider_with_retry(
    backend_call,
    provider: Provider,
    prompt: str,
    temperature: float,
    max_tokens: int,
    json_mode: bool,
    system: str | None,
    config: RetryConfig,
    attempts: list,
) -> str | None:
    """Try calling a provider, retrying transient errors with backoff.

    Returns the result text on success, None on failure.
    Appends attempt records to `attempts` list.
    """
    last_error = None
    last_kind = None

    for attempt in range(config.max_retries + 1):
        try:
            result = backend_call(provider, prompt, temperature, max_tokens,
                                  json_mode, system)
            attempts.append({
                "provider": provider.provider,
                "error_kind": None,
                "error": None,
                "attempt": attempt,
                "retries": config.max_retries,
                "succeeded": True,
            })
            return result
        except Exception as e:
            last_error = e
            last_kind = classify_error(e)

            # Don't retry non-retryable errors
            if not is_retryable(last_kind):
                logger.debug(
                    f"Provider {provider.provider} failed with "
                    f"{last_kind.value} error, not retrying: {e}"
                )
                break

            # Don't retry if this is the last attempt
            if attempt >= config.max_retries:
                break

            # Wait before retry
            delay = _compute_delay(attempt, config)
            logger.debug(
                f"Provider {provider.provider} failed with transient error "
                f"(attempt {attempt + 1}/{config.max_retries + 1}), "
                f"retrying in {delay:.1f}s: {e}"
            )
            time.sleep(delay)

    # All retries exhausted
    _history.record_failure(provider.provider)
    attempts.append({
        "provider": provider.provider,
        "error_kind": last_kind.value if last_kind else "unknown",
        "error": str(last_error) if last_error else "unknown",
        "attempt": config.max_retries,
        "retries": config.max_retries,
        "succeeded": False,
    })
    return None


# ---- diagnostics ----

def fallback_diagnostics(
    registry: Registry,
    complexity: str = "balanced",
    template: str | None = None,
) -> dict:
    """Get diagnostic info about fallback chains for debugging.

    Returns a dict with:
    - chain: ordered list of provider names in the fallback chain
    - provider_health: health status for each provider
    - complexity: the resolved complexity tier
    """
    providers = registry.providers
    if template:
        providers = registry._filter_providers(template)

    resolved = _canonical_complexity(complexity)
    requested = COMPLEXITY_ORDER.get(resolved, 2)

    chain_info = []
    for p in providers:
        tier = COMPLEXITY_ORDER.get(p.complexity, 2)
        health = _history.get_health(p.provider)

        chain_info.append({
            "provider": p.provider,
            "model": p.model,
            "complexity": p.complexity,
            "tier_level": tier,
            "available": p.available,
            "eligible": tier <= requested and p.available,
            "on_cooldown": _history.is_on_cooldown(p.provider) if p.available else False,
            "health": {
                "consecutive_failures": health.consecutive_failures if health else 0,
                "total_failures": health.total_failures if health else 0,
                "total_successes": health.total_successes if health else 0,
                "cooldown_remaining": round(health.cooldown_remaining, 1) if health else 0.0,
            } if health else {
                "consecutive_failures": 0,
                "total_failures": 0,
                "total_successes": 0,
                "cooldown_remaining": 0.0,
            },
        })

    return {
        "complexity": resolved,
        "requested_tier": requested,
        "template": template,
        "providers": chain_info,
    }
