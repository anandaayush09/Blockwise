"""Backtest engine: replay every day in the test window, as-of, for each policy.

Owns: for each day D: set as_of = the decision time on D-1 (backtest.yaml), ask each policy
for a Schedule, settle against actuals, store per-day results.

Must NOT: use the training window as test data, retrain on test days, or let a policy read
anything the store would not have returned at ``as_of``. Run the leakage checklist in
docs/assumptions.md before believing a number.
Results must be reproducible: fixed seeds, recorded model versions and rules versions.
"""

from __future__ import annotations

from datetime import date

import pandas as pd

from blockwise.backtest.policies import Policy


def run_backtest(policies: list[Policy], start: date, end: date) -> pd.DataFrame:
    """One row per (date, policy): purchase_cost_inr, dsm_cost_inr, total_cost_inr, plus model/rules versions."""
    raise NotImplementedError
