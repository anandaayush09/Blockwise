"""Celery tasks.

Owns: thin task wrappers that call components and persist results. Tasks must be idempotent
(retrying a plan run for the same day must not create two approvals) and set time limits.

Must NOT: contain domain logic.
"""

from __future__ import annotations


def run_backtest_task(job_id: str) -> None:
    raise NotImplementedError


def run_daily_plan_task(target_date: str, plan_run_id: str) -> None:
    raise NotImplementedError


def replan_intraday_task(target_date: str, plan_run_id: str, from_block: int) -> None:
    raise NotImplementedError
