"""Beat schedule.

Define when the daily plan runs (before the day-ahead bidding deadline, leaving time for the
operator to review; VERIFY the deadline in configs/backtest.yaml) and the intraday re-plan
cadence. Times are IST; state the timezone explicitly in the schedule config.
"""

from __future__ import annotations
