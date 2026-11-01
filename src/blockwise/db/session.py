"""Database engine and session factory.

Owns: building the engine from Settings.database_url, a session context manager with
commit/rollback, and a connectivity check used by /health.
Must NOT: read env vars directly (use config.Settings) or open connections at import time.
"""

from __future__ import annotations


def get_engine():
    raise NotImplementedError


def session_scope():
    """Context manager yielding a session; commit on success, rollback on error."""
    raise NotImplementedError


def check_connection() -> bool:
    raise NotImplementedError
