"""DAM and RTM price forecasters, block-wise.

Owns: P10/P50/P90 price paths per block for each market.

Must NOT: forecast outside the exchange's price caps (clip consistently with settlement; VERIFY caps).
Must NOT: treat DAM and RTM as the same problem; their information sets and timing differ.

DECISION(ADR-0004): modelling approach. Consider how price spikes (tails) enter the optimiser.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from blockwise.data.store import TimeSeriesStore
from blockwise.schemas import PriceForecast


def train(store: TimeSeriesStore, market: Literal["DAM", "RTM"], train_end: date) -> str:
    raise NotImplementedError


def forecast_prices(
    store: TimeSeriesStore, market: Literal["DAM", "RTM"], target_date: date, as_of: datetime
) -> PriceForecast:
    raise NotImplementedError
