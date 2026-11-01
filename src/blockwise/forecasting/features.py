"""Feature construction for the forecasters.

Owns: turning an as-of frame into model features (calendar, lags, weather forecast at issue
time, recent errors).

Must NOT: read anything not passed in. Every function takes an already as-of-filtered frame
(``TimeSeriesStore.day_frame``), so leakage cannot enter here by accident.

Prefer simple, explainable features first; you must be able to say why each one is there.
"""

from __future__ import annotations

from datetime import date

import pandas as pd


def calendar_features(day: date) -> pd.DataFrame:
    """One row per block: block number, weekday, holiday flag, month, season. VERIFY the holiday source."""
    raise NotImplementedError


def lag_features(history: pd.DataFrame, target_day: date, lags_days: list[int]) -> pd.DataFrame:
    """Same-block values from ``lags_days`` days before ``target_day``. Only use lags that are known as-of."""
    raise NotImplementedError


def build_features(day_frame: pd.DataFrame, target_day: date) -> pd.DataFrame:
    """Assemble the full feature matrix for the 96 blocks of ``target_day``."""
    raise NotImplementedError
