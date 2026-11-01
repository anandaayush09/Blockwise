"""Celery application (broker/backend: Redis).

Referenced by docker-compose as `blockwise.worker.celery_app`. Define the `app` object here
and load tasks from tasks.py and the schedule from beat.py.

DECISION(ADR-0012): whether Celery is warranted vs a simpler scheduler. Be able to say what
you would lose by dropping it.
"""

from __future__ import annotations

# app = Celery("blockwise", broker=..., backend=...)
