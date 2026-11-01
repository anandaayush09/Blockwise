"""Settle a schedule against what actually happened: the realised INR cost of a day.

Owns: given a ``Schedule``, ``DayActuals`` and the DSM rules in force that day, compute
purchase cost (PPA at contract cost, DAM at the actual MCP, RTM at the actual price, BESS
effects) plus realised DSM cost from actual vs scheduled drawal.

Must NOT: be shared in logic with the optimiser's expected-cost calculation. This is the
referee. It uses ONLY realised prices and actual demand, and calls regulation/penalty.py
for DSM so the same rules apply to every policy.

Invariants (tests/unit/test_settlement.py): a schedule that exactly matches actual demand has
zero DSM cost; DAM volume settles at the actual DAM MCP, not the forecast.
VERIFY how deviations relate to the market purchases in your DISCOM model (what is "scheduled drawal").
"""

from __future__ import annotations

from blockwise.config import DiscomConfig, DsmRules
from blockwise.schemas import DayActuals, DaySettlement, Schedule


def settle_day(
    schedule: Schedule, actuals: DayActuals, discom: DiscomConfig, dsm_rules: DsmRules
) -> DaySettlement:
    raise NotImplementedError
