"""Net-demand forecaster (day-ahead and intraday), 96 blocks, with uncertainty.

Owns: training, loading and running the model; producing P10/P50/P90.

Must NOT: peek past ``as_of``. Must NOT: return point forecasts only; the optimiser and the
DSM risk term need the spread.

DECISION(ADR-0004): model family and how quantiles are produced.
Intraday: forecast residual blocks given actuals so far; the horizon shrinks through the day.
Evaluate with pinball loss for quantiles plus MAPE for P50, split by season and by hour.
"""

from __future__ import annotations

from datetime import date, datetime

from blockwise.data.store import TimeSeriesStore
from blockwise.schemas import NetDemandForecast


def train(store: TimeSeriesStore, train_end: date) -> str:
    """Fit on data up to ``train_end`` only. Return a model version id."""
    raise NotImplementedError


def forecast_day_ahead(
    store: TimeSeriesStore, target_date: date, as_of: datetime
) -> NetDemandForecast:
    raise NotImplementedError


def forecast_intraday(
    store: TimeSeriesStore, target_date: date, as_of: datetime, from_block: int
) -> NetDemandForecast:
    """Re-forecast blocks ``from_block``..96 given actuals up to ``as_of``."""
    raise NotImplementedError
