"""Phase 3. Settlement is the referee for every policy, so its invariants are strict.

Test-data contract (define it the same way in settlement.py): scheduled drawal in a block =
ppa + dam + rtm + bess_discharge - bess_charge (MW). Breakdown keys include "dam".
"""

import pytest

from blockwise.backtest.settlement import settle_day
from blockwise.schemas import DayActuals

pytestmark = pytest.mark.xfail(raises=NotImplementedError, reason="Phase 3 not implemented")


def _actuals(day, demand_mw=100.0, mcp=4000.0, rtm=4500.0) -> DayActuals:
    return DayActuals(
        target_date=day,
        actual_net_demand_mw=[demand_mw] * 96,
        dam_mcp_inr_per_mwh=[mcp] * 96,
        rtm_price_inr_per_mwh=[rtm] * 96,
    )


def test_schedule_matching_actual_demand_has_zero_dsm_cost(day, make_schedule, discom, dsm_rules):
    result = settle_day(make_schedule(), _actuals(day, demand_mw=100.0), discom, dsm_rules)
    assert result.dsm_cost_inr == 0.0


def test_dam_volume_settles_at_actual_mcp_not_forecast(day, make_schedule, discom, dsm_rules):
    # 30 MW * 0.25 h * 96 blocks * 4000 INR/MWh
    result = settle_day(make_schedule(dam_mw=30.0), _actuals(day, mcp=4000.0), discom, dsm_rules)
    assert result.breakdown_inr["dam"] == pytest.approx(30.0 * 0.25 * 96 * 4000.0)


def test_total_is_purchase_plus_dsm(day, make_schedule, discom, dsm_rules):
    r = settle_day(make_schedule(), _actuals(day, demand_mw=110.0), discom, dsm_rules)
    assert r.total_cost_inr == pytest.approx(r.purchase_cost_inr + r.dsm_cost_inr)


def test_larger_demand_miss_never_costs_less(day, make_schedule, discom, dsm_rules):
    costs = [
        settle_day(
            make_schedule(), _actuals(day, demand_mw=100.0 + d), discom, dsm_rules
        ).dsm_cost_inr
        for d in (0.0, 5.0, 20.0)
    ]
    assert costs == sorted(costs)
