"""Response caching -- avoid redundant LLM calls.

SQLite-backed persistent cache with LRU eviction and TTL expiry.
Survives process restarts. Same public API as the old in-memory version.
"""

import hashlib
import os
import sqlite3
import threading
import time
from typing import Optional


class ResponseCache:
    """Persistent cache keyed on (model, prompt, params).

    Thread-safe. Bounded to max_entries (LRU eviction).
    Stores entries in SQLite so cache survives process restarts.

    Enhancements over v1:
    - TTL expiry: stale entries are pruned on put/get
    - Read-optimized gets: last_access update is batched, not per-read
    - Connection cleanup via close() / context manager
    - Efficient eviction: uses row count from index, not full scan
    """

    def __init__(self, max_entries: int = 256, db_path: Optional[str] = None,
                 ttl_seconds: float = 0):
        self._lock = threading.Lock()
        self.max_entries = max_entries
        self.ttl_seconds = ttl_seconds  # 0 = no TTL (expire never)
        self.hits = 0
        self.misses = 0
        self._last_evict_time = time.time()  # throttle periodic cleanup
        self._pending_access_updates: dict[str, float] = {}

        if db_path is None:
            cache_dir = os.environ.get(
                "XDG_CACHE_HOME",
                os.path.expanduser("~/.cache"),
            )
            db_path = os.path.join(cache_dir, "model_choice", "cache.db")

        self._db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._conn = self._connect()
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path, check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA cache_size=-2000")  # 2MB page cache
        conn.execute("PRAGMA temp_store=MEMORY")
        return conn

    def _init_db(self):
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS cache (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                last_access REAL NOT NULL,
                created REAL NOT NULL
            )
        """)
        self._conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_last_access ON cache(last_access)"
        )
        self._conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_created ON cache(created)"
        )
        self._conn.commit()

    def close(self):
        """Flush pending writes and close the database connection."""
        with self._lock:
            self._flush_access_updates()
            try:
                self._conn.close()
            except Exception:
                pass

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def _key(self, model: str, prompt: str, temperature: float,
             max_tokens: int, json_mode: bool, system: Optional[str]) -> str:
        raw = f"{model}|{prompt}|{temperature}|{max_tokens}|{json_mode}|{system or ''}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def _flush_access_updates(self):
        """Batch-write pending last_access updates to reduce write amplification."""
        if not self._pending_access_updates:
            return
        now = time.time()
        for k, ts in self._pending_access_updates.items():
            self._conn.execute(
                "UPDATE cache SET last_access = ? WHERE key = ?",
                (ts, k),
            )
        self._pending_access_updates.clear()
        self._conn.commit()

    def _maybe_flush(self):
        """Flush pending access updates periodically (every ~2 seconds)."""
        now = time.time()
        if self._pending_access_updates and now - self._last_evict_time > 2.0:
            self._flush_access_updates()

    def _evict_expired(self):
        """Remove entries older than TTL. Called periodically."""
        if self.ttl_seconds <= 0:
            return
        cutoff = time.time() - self.ttl_seconds
        self._conn.execute(
            "DELETE FROM cache WHERE created < ?", (cutoff,)
        )

    def _evict_lru(self):
        """LRU eviction: remove oldest entries over the limit."""
        count = self._conn.execute("SELECT COUNT(*) FROM cache").fetchone()[0]
        if count > self.max_entries:
            excess = count - self.max_entries
            self._conn.execute(
                """DELETE FROM cache WHERE key IN (
                    SELECT key FROM cache ORDER BY last_access ASC
                    LIMIT ?
                )""",
                (excess,),
            )

    def _maybe_evict(self):
        """Run eviction checks periodically (throttled to ~every 5 seconds)."""
        now = time.time()
        if now - self._last_evict_time < 5.0:
            return
        self._last_evict_time = now
        self._flush_access_updates()
        self._evict_expired()
        self._evict_lru()
        self._conn.commit()

    def get(self, model: str, prompt: str, temperature: float,
            max_tokens: int, json_mode: bool, system: Optional[str]) -> Optional[str]:
        k = self._key(model, prompt, temperature, max_tokens, json_mode, system)
        with self._lock:
            row = self._conn.execute(
                "SELECT value, created FROM cache WHERE key = ?", (k,)
            ).fetchone()
            if row is not None:
                # Check TTL
                if self.ttl_seconds > 0:
                    age = time.time() - row[1]
                    if age > self.ttl_seconds:
                        # Expired -- delete and count as miss
                        self._conn.execute(
                            "DELETE FROM cache WHERE key = ?", (k,)
                        )
                        self._conn.commit()
                        self.misses += 1
                        return None
                # Defer the last_access write instead of committing immediately
                self._pending_access_updates[k] = time.time()
                self._maybe_flush()
                self._maybe_evict()
                self.hits += 1
                return row[0]
            else:
                self.misses += 1
                self._maybe_evict()
                return None

    def put(self, model: str, prompt: str, temperature: float,
            max_tokens: int, json_mode: bool, system: Optional[str],
            response: str):
        k = self._key(model, prompt, temperature, max_tokens, json_mode, system)
        now = time.time()
        with self._lock:
            self._flush_access_updates()  # flush before schema changes
            self._conn.execute(
                """INSERT OR REPLACE INTO cache (key, value, last_access, created)
                   VALUES (?, ?, ?, ?)""",
                (k, response, now, now),
            )
            self._evict_expired()
            self._evict_lru()
            self._conn.commit()

    def clear(self):
        with self._lock:
            self._pending_access_updates.clear()
            self._conn.execute("DELETE FROM cache")
            self._conn.commit()
            self.hits = 0
            self.misses = 0

    def stats(self) -> dict:
        with self._lock:
            count = self._conn.execute("SELECT COUNT(*) FROM cache").fetchone()[0]
            return {
                "entries": count,
                "hits": self.hits,
                "misses": self.misses,
                "hit_rate": self.hits / max(1, self.hits + self.misses),
            }

    def size_bytes(self) -> int:
        """Return approximate size of the cache database in bytes."""
        with self._lock:
            try:
                return os.path.getsize(self._db_path)
            except OSError:
                return 0
