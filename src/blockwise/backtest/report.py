"""Turn backtest results into the INR savings table and the README numbers.

Owns: totals and breakdowns by month/season/weekday, savings vs naive in INR and %, share of the
oracle gap captured, and confidence intervals (e.g. bootstrap over days) so a lucky month is
not reported as a result.

Must NOT: report a headline without the period, the baseline definition and the caveat list
(price-taker, proxy demand). Output must be reproducible from stored results.
"""

from __future__ import annotations

import pandas as pd


def savings_table(results: pd.DataFrame) -> pd.DataFrame:
    raise NotImplementedError


def oracle_gap_captured(results: pd.DataFrame) -> float:
    """(naive - blockwise) / (naive - oracle) over the period, in [0, 1] if the oracle is truly an upper bound."""
    raise NotImplementedError


def to_markdown(table: pd.DataFrame) -> str:
    raise NotImplementedError
