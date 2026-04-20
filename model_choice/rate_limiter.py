"""Per-provider rate limiting with cross-process coordination.

Uses SQLite to track active connections across processes. When max_concurrent
is reached, new requests wait (with timeout) instead of firing and getting 429'd.

Also tracks last_request_time per provider to enforce min_interval even after
a slot is released -- this is critical for cross-process correctness since
a released request leaves no trace in active_requests.

Config in tiers.yaml:
  providers:
    - provider: zai
      max_concurrent: 4       # max simultaneous connections
      min_interval: 1.0       # min seconds between requests

Or per-call:
  generate(prompt, max_concurrent=4)
"""

import os
import sqlite3
import time
import uuid
import logging
from typing import Optional
from contextlib import contextmanager

logger = logging.getLogger("model_choice.rate_limiter")

DEFAULT_DB_PATH = None  # set lazily


def _default_db_path() -> str:
    global DEFAULT_DB_PATH
    if DEFAULT_DB_PATH is None:
        cache_dir = os.environ.get(
            "XDG_CACHE_HOME",
            os.path.expanduser("~/.cache"),
        )
        DEFAULT_DB_PATH = os.path.join(cache_dir, "model_choice", "rate_limit.db")
    return DEFAULT_DB_PATH


class RateLimiter:
    """Cross-process rate limiter using SQLite.

    Tracks active requests per provider. When max_concurrent is reached,
    new requests poll until a slot opens or timeout expires.

    Also tracks last_request_time per provider in a separate table so
    min_interval is enforced correctly across acquire/release boundaries
    and across processes.
    """

    def __init__(self, db_path: Optional[str] = None):
        self._db_path = db_path or _default_db_path()
        os.makedirs(os.path.dirname(self._db_path), exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path, timeout=10)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA busy_timeout=5000")
        return conn

    def _init_db(self):
        conn = self._connect()
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS active_requests (
                    id TEXT PRIMARY KEY,
                    provider TEXT NOT NULL,
                    started REAL NOT NULL,
                    pid INTEGER NOT NULL
                )
            """)
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_provider "
                "ON active_requests(provider)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_started "
                "ON active_requests(started)"
            )
            # Track last request time per provider for min_interval enforcement.
            # This survives release() -- active_requests rows are deleted on
            # release, so without this table, min_interval would be unenforceable
            # across the acquire/release boundary and across processes.
            conn.execute("""
                CREATE TABLE IF NOT EXISTS last_request_time (
                    provider TEXT PRIMARY KEY,
                    last_time REAL NOT NULL
                )
            """)
            conn.commit()
        finally:
            conn.close()

    def _cleanup_stale(self, conn, max_age: float = 300):
        """Remove requests older than max_age seconds (stale/orphaned)."""
        cutoff = time.time() - max_age
        conn.execute(
            "DELETE FROM active_requests WHERE started < ?", (cutoff,)
        )
        conn.commit()

    def _record_last_request(self, conn, provider: str):
        """Update last_request_time for a provider (used by min_interval)."""
        conn.execute(
            "INSERT OR REPLACE INTO last_request_time (provider, last_time) "
            "VALUES (?, ?)",
            (provider, time.time()),
        )
        conn.commit()

    def _get_last_request_time(self, conn, provider: str) -> Optional[float]:
        """Get the last request time for a provider."""
        row = conn.execute(
            "SELECT last_time FROM last_request_time WHERE provider = ?",
            (provider,),
        ).fetchone()
        return row[0] if row else None

    def active_count(self, provider: str) -> int:
        """Count active requests for a provider."""
        conn = self._connect()
        try:
            self._cleanup_stale(conn)
            row = conn.execute(
                "SELECT COUNT(*) FROM active_requests WHERE provider = ?",
                (provider,),
            ).fetchone()
            return row[0]
        finally:
            conn.close()

    def acquire(
        self,
        provider: str,
        max_concurrent: int = 4,
        min_interval: float = 0.0,
        timeout: float = 60.0,
        poll_interval: float = 0.5,
    ) -> Optional[str]:
        """Wait for a rate limit slot. Returns request ID or None on timeout.

        Args:
            provider: Provider name (e.g. "zai").
            max_concurrent: Max simultaneous connections.
            min_interval: Min seconds between requests. 0 = no limit.
            timeout: Max seconds to wait for a slot.
            poll_interval: How often to check for an open slot.

        Returns:
            Request ID string (use for release()), or None if timed out.
        """
        request_id = uuid.uuid4().hex[:12]
        pid = os.getpid()
        deadline = time.time() + timeout

        while True:
            # Open a fresh connection per poll iteration. This avoids holding
            # a SQLite connection during sleep() and allows multiple threads
            # in the same process to poll concurrently (no _local_lock needed
            # -- SQLite WAL mode + busy_timeout handles cross-thread safety).
            conn = self._connect()
            try:
                self._cleanup_stale(conn)

                # Check min_interval using last_request_time table.
                # This works across processes because it's in the shared DB,
                # and it works across acquire/release because it persists.
                if min_interval > 0:
                    last = self._get_last_request_time(conn, provider)
                    if last is not None:
                        elapsed = time.time() - last
                        if elapsed < min_interval:
                            wait = min_interval - elapsed
                            if time.time() + wait > deadline:
                                logger.warning(
                                    f"Rate limit: {provider} min_interval "
                                    f"timeout ({wait:.1f}s needed)"
                                )
                                return None
                            # Sleep outside the connection scope
                            conn.close()
                            conn = None
                            time.sleep(wait)
                            continue

                # Count active
                count = conn.execute(
                    "SELECT COUNT(*) FROM active_requests "
                    "WHERE provider = ?",
                    (provider,),
                ).fetchone()[0]

                if count < max_concurrent:
                    # Slot available -- register
                    now = time.time()
                    conn.execute(
                        "INSERT INTO active_requests "
                        "(id, provider, started, pid) VALUES (?, ?, ?, ?)",
                        (request_id, provider, now, pid),
                    )
                    # Also record last_request_time for min_interval
                    if min_interval > 0:
                        self._record_last_request(conn, provider)
                    conn.commit()
                    logger.debug(
                        f"Rate limit: acquired {provider} slot "
                        f"({count + 1}/{max_concurrent})"
                    )
                    return request_id
            finally:
                if conn is not None:
                    conn.close()

            # No slot -- wait or timeout
            if time.time() >= deadline:
                logger.warning(
                    f"Rate limit: {provider} timed out waiting for "
                    f"slot ({timeout}s timeout)"
                )
                return None

            time.sleep(poll_interval)

    def release(self, provider: str, request_id: str):
        """Release a rate limit slot after call completes."""
        conn = self._connect()
        try:
            conn.execute(
                "DELETE FROM active_requests WHERE id = ?",
                (request_id,),
            )
            conn.commit()
            logger.debug(f"Rate limit: released {provider} slot {request_id}")
        finally:
            conn.close()

    @contextmanager
    def limit(
        self,
        provider: str,
        max_concurrent: int = 4,
        min_interval: float = 0.0,
        timeout: float = 60.0,
    ):
        """Context manager: acquire slot, yield, release on exit.

        Usage:
            with limiter.limit("zai", max_concurrent=4):
                result = call(provider, ...)
        """
        request_id = self.acquire(
            provider, max_concurrent, min_interval, timeout
        )
        if request_id is None:
            raise RuntimeError(
                f"Rate limit: timed out waiting for {provider} slot "
                f"(max_concurrent={max_concurrent}, timeout={timeout}s)"
            )
        try:
            yield
        finally:
            self.release(provider, request_id)

    def status(self) -> dict:
        """Get current rate limit status for all providers."""
        conn = self._connect()
        try:
            self._cleanup_stale(conn)
            rows = conn.execute(
                "SELECT provider, COUNT(*) FROM active_requests "
                "GROUP BY provider"
            ).fetchall()
            return {provider: count for provider, count in rows}
        finally:
            conn.close()

    def reset(self):
        """Clear all active requests (emergency reset)."""
        conn = self._connect()
        try:
            conn.execute("DELETE FROM active_requests")
            conn.commit()
        finally:
            conn.close()


# Module-level singleton (shared across all calls within a process)
_limiter: Optional[RateLimiter] = None


def get_limiter() -> RateLimiter:
    """Get the shared rate limiter instance."""
    global _limiter
    if _limiter is None:
        _limiter = RateLimiter()
    return _limiter
