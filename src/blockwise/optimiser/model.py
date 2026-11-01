"""MILP model construction: variables, constraints, objective.

Owns: translating (net-demand forecast, price forecasts, DISCOM config, DSM rules) into a
solver model for 96 blocks across PPA, DAM, RTM and BESS.

Write the equations in docs/architecture.md FIRST. This file should read like that section.

Must NOT: contain solver-specific calls outside this file and solve.py (so the solver can be swapped).
Must NOT: model deliberate deviation as a profit source. DSM cost is a risk term to hedge, not an opportunity.
Must NOT: be imported by agents directly; they use the tool wrapper in agents/tools.py.

Things you must decide (ADR-0005): which demand quantile or scenarios drive the balance;
how expected DSM cost enters (piecewise-linear over scenarios?); whether any term is
non-convex and therefore needs binaries; whether BESS cycling cost is included; liquidity limits.
"""

from __future__ import annotations

from datetime import date

from blockwise.config import BessSpec, DiscomConfig, DsmRules
from blockwise.schemas import NetDemandForecast, PriceForecast


def build_model(
    demand: NetDemandForecast,
    dam: PriceForecast,
    rtm: PriceForecast,
    discom: DiscomConfig,
    dsm_rules: DsmRules,
    initial_soc_mwh: float,
):
    """Return a solver model object ready for ``solve.solve``."""
    raise NotImplementedError


def build_oracle_model(
    actual_net_demand_mw: list[float],
    dam_mcp_inr_per_mwh: list[float],
    rtm_price_inr_per_mwh: list[float],
    discom: DiscomConfig,
    target_date: date,
):
    """Perfect-foresight version of the same model: the upper bound on savings."""
    raise NotImplementedError


def bess_energy_bounds_mwh(bess: BessSpec) -> tuple[float, float]:
    """(min, max) usable state of charge in MWh derived from the fractions."""
    raise NotImplementedError
