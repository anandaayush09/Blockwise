"""Time-series store with as-of reads.

Owns: the one place that reads series for forecasting and backtesting. The key API is
``read_as_of``: "give me this series for these blocks, using only data published at or
before ``as_of``".

Must NOT: expose a "latest" read to the forecasting or backtest code. Leakage prevention
depends on this being impossible by construction.

DECISION(ADR-0011): parquet files + DuckDB queries vs. Postgres tables for time series.
"""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

import pandas as pd


class TimeSeriesStore:
    def __init__(self, root: Path) -> None:
        raise NotImplementedError

    def read_as_of(self, series: str, start: date, end: date, as_of: datetime) -> pd.DataFrame:
        """Rows for ``series`` in [start, end] whose ``published_at`` <= ``as_of``.

        If a value was revised, return the version known at ``as_of``.
        """
        raise NotImplementedError

    def day_frame(self, day: date, as_of: datetime) -> pd.DataFrame:
        """One row per block (96) with every series joined, as known at ``as_of``."""
        raise NotImplementedError
