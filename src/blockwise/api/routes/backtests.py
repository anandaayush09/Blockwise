"""Backtest endpoints.

POST /backtests        body: {config overrides} -> 202 + job id (runs in Celery worker)
GET  /backtests/{id}   -> status and, when done, the savings table

Long-running work never blocks the request; results are read from Postgres.
"""

from __future__ import annotations
