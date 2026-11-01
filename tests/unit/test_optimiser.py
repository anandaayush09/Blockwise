"""Phase 6. Constraint-checker tests come first (they do not need the solver), then
solver-output tests. The checker is the referee for the model, so test it hardest.
"""

import pytest

from blockwise.optimiser.checks import check_schedule

pytestmark = pytest.mark.xfail(raises=NotImplementedError, reason="Phase 6 not implemented")


# ---- checker: independent of the solver --------------------------------------------------


def test_checker_accepts_feasible_hand_built_schedule(make_schedule, flat_demand, discom):
    assert check_schedule(make_schedule(), flat_demand, discom) == []


def test_checker_catches_energy_balance_violation(make_schedule, flat_demand, discom):
    bad = make_schedule(dam_mw=80.0)  # 60 + 80 + 10 = 150 MW against 100 MW demand
    violations = check_schedule(bad, flat_demand, discom)
    assert any(v.constraint == "energy_balance" for v in violations)


def test_checker_catches_ppa_above_capacity(make_schedule, flat_demand, discom):
    bad = make_schedule(ppa_mw={"ppa_a": 150.0}, dam_mw=0.0, rtm_mw=0.0)  # capacity is 100 MW
    assert any("ppa" in v.constraint for v in check_schedule(bad, flat_demand, discom))


def test_checker_catches_simultaneous_charge_and_discharge(make_schedule, flat_demand, discom):
    bad = make_schedule(bess_charge_mw=5.0, bess_discharge_mw=5.0)
    assert any("charge" in v.constraint for v in check_schedule(bad, flat_demand, discom))


def test_checker_catches_soc_above_max(make_schedule, flat_demand, discom):
    bad = make_schedule(bess_soc_mwh=79.0)  # max usable is 95% of 80 = 76 MWh
    assert any("soc" in v.constraint for v in check_schedule(bad, flat_demand, discom))


# ---- solver output ------------------------------------------------------------------------
# Fill these in once model.py/solve.py exist. They should assert on the *checker's* verdict,
# not on the model's own variables, so a model bug cannot hide itself.


def test_solved_schedule_passes_independent_checker():
    pytest.skip(
        "TODO(you): build forecasts, build_model, solve, then assert check_schedule(...) == []"
    )


def test_solved_cost_not_worse_than_naive_on_same_inputs():
    pytest.skip(
        "TODO(you): optimiser expected cost <= naive policy expected cost for the same forecasts"
    )
