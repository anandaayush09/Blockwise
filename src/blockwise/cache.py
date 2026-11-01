"""Cache-aside helpers on Redis.

Owns: keys, TTLs and invalidation rules for cached forecasts and regulation answers.
Cache key rule: include everything that changes the answer (target date, as_of, model
version, rules version, corpus version). A stale hit is worse than a miss.

Must NOT: cache anything that depends on operator approval state, or cache LLM output
without the prompt version in the key.

Optional later: a semantic cache for repeated regulation questions (cut-list item).
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any


async def get_or_compute(key: str, ttl_seconds: int, compute: Callable[[], Awaitable[Any]]) -> Any:
    """Return the cached value for ``key`` or compute, store with TTL, and return it."""
    raise NotImplementedError


def forecast_key(kind: str, target_date: str, as_of: str, model_version: str) -> str:
    """Build a deterministic cache key for a forecast."""
    raise NotImplementedError
