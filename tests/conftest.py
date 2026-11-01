"""Shared fixtures.

Everything here is TEST DATA, not the regulation and not a real DISCOM. In particular the
DSM rules fixture uses made-up numbers purely so invariants (zero deviation => zero penalty,
monotonicity, ...) can be exercised. When you settle your encoding of DSM rules (ADR-0003),
update `dsm_rules` so it matches your schema.
"""

from __future__ import annotations

from datetime import date, datetime

import pytest

from blockwise.config import (
    BessSpec,
    DiscomConfig,
    DsmBand,
    DsmRules,
    MarketLimits,
    PpaContract,
)
from blockwise.schemas import NetDemandForecast, Schedule, ScheduleBlock
from blockwise.timeblocks import IST

TEST_DAY = date(2025, 1, 15)


@pytest.fixture(autouse=True)
def _no_real_llm_calls(monkeypatch):
    """A test suite must never be able to make a paid API call."""
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)


@pytest.fixture
def day() -> date:
    return TEST_DAY


@pytest.fixture
def discom() -> DiscomConfig:
    return DiscomConfig(
        name="Test DISCOM",
        ppa=[
            PpaContract(id="ppa_a", capacity_mw=100.0, min_mw=0.0, variable_cost_inr_per_mwh=3000.0)
        ],
        bess=BessSpec(
            power_mw=20.0,
            energy_mwh=80.0,
            round_trip_efficiency=0.85,
            soc_min_frac=0.10,
            soc_max_frac=0.95,
            soc_initial_frac=0.50,
        ),
        market=MarketLimits(),
    )


@pytest.fixture
def dsm_rules() -> DsmRules:
    """FAKE rules for invariant tests only. Not from any regulation."""
    return DsmRules(
        name="TEST FIXTURE",
        effective_from=date(2020, 1, 1),
        reference_rate_definition="test",
        bands=[
            DsmBand(
                name="band_1",
                deviation_from_pct_of_schedule=0.0,
                deviation_to_pct_of_schedule=100.0,
                over_drawal_rate=1.0,
                under_drawal_rate=1.0,
                clause_ref="TEST",
            )
        ],
    )


@pytest.fixture
def flat_demand() -> NetDemandForecast:
    """100 MW in every block, tight quantiles."""
    return NetDemandForecast(
        target_date=TEST_DAY,
        as_of=datetime(2025, 1, 14, 9, 0, tzinfo=IST),
        horizon="day_ahead",
        p10_mw=[95.0] * 96,
        p50_mw=[100.0] * 96,
        p90_mw=[105.0] * 96,
        model_version="test",
    )


@pytest.fixture
def make_schedule():
    """Factory for a hand-built schedule that exactly meets a flat 100 MW demand."""

    def _make(**block_overrides) -> Schedule:
        base = dict(
            ppa_mw={"ppa_a": 60.0},
            dam_mw=30.0,
            rtm_mw=10.0,
            bess_charge_mw=0.0,
            bess_discharge_mw=0.0,
            bess_soc_mwh=40.0,  # 50% of 80 MWh, held constant
        )
        base.update(block_overrides)
        blocks = [ScheduleBlock(block=b, **base) for b in range(1, 97)]
        return Schedule(
            schedule_id="test-schedule",
            target_date=TEST_DAY,
            blocks=blocks,
            expected_cost_inr=0.0,
            cost_breakdown_inr={},
            inputs={},
        )

    return _make
