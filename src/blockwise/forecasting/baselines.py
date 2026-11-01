"""Naive forecasters. Build these FIRST; every model must beat them to earn its place.

Owns: seasonal-naive style baselines for net demand and prices (e.g. same block last week).
These are also the backtest's naive baseline inputs (ADR-0008).

Must NOT: be weak on purpose. A strawman baseline makes savings meaningless.
"""

from __future__ import annotations

from datetime import date, datetime

from blockwise.data.store import TimeSeriesStore
from blockwise.schemas import NetDemandForecast, PriceForecast


def seasonal_naive_demand(
    store: TimeSeriesStore, target_date: date, as_of: datetime
) -> NetDemandForecast:
    raise NotImplementedError


def seasonal_naive_price(
    store: TimeSeriesStore, market: str, target_date: date, as_of: datetime
) -> PriceForecast:
    raise NotImplementedError
