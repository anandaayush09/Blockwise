"""Procurement policies compared in the backtest.

A policy maps (target_date, as_of information) -> Schedule. All policies see the same
information set and are settled by the same ``settle_day``.

  * NaivePolicy: the baseline (ADR-0008), e.g. same-block-last-week demand, buy the gap at DAM,
    residual left to DSM. It must be a defensible baseline a real DISCOM might use.
  * BlockWisePolicy: forecasts -> optimiser (no LLM involved in the numbers).
  * OraclePolicy: optimiser with perfect foresight (upper bound; uses actuals, never deployable).

Must NOT: give BlockWisePolicy any information the naive policy lacks, or let the oracle leak
into the other two. Policies do not call LLMs; the agent layer wraps a policy's output.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Protocol

from blockwise.schemas import Schedule


class Policy(Protocol):
    name: str

    def schedule_for(self, target_date: date, as_of: datetime) -> Schedule: ...


class NaivePolicy:
    name = "naive"

    def schedule_for(self, target_date: date, as_of: datetime) -> Schedule:
        raise NotImplementedError


class BlockWisePolicy:
    name = "blockwise"

    def schedule_for(self, target_date: date, as_of: datetime) -> Schedule:
        raise NotImplementedError


class OraclePolicy:
    name = "oracle"

    def schedule_for(self, target_date: date, as_of: datetime) -> Schedule:
        raise NotImplementedError
