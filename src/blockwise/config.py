"""Typed configuration: environment settings and the YAML files under configs/.

Owns: parsing and validating settings, the DISCOM portfolio, DSM rules and backtest protocol.

Must NOT: hide missing values. A null in a VERIFY field stays None and the code that needs
it must fail loudly (e.g. penalty.py refuses to quote with unfilled DSM rules) rather than
defaulting to a guess.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment variables (see .env.example). Secrets come only from the environment."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "local"
    log_level: str = "INFO"
    anthropic_api_key: str | None = None
    llm_model: str = "claude-opus-5-5"  # DECISION(ADR-0010)
    llm_budget_inr_per_run: float | None = None
    database_url: str | None = None
    redis_url: str | None = None
    sentry_dsn: str | None = None


class PpaContract(BaseModel):
    id: str
    capacity_mw: float
    min_mw: float
    variable_cost_inr_per_mwh: float


class BessSpec(BaseModel):
    power_mw: float
    energy_mwh: float
    round_trip_efficiency: float
    soc_min_frac: float
    soc_max_frac: float
    soc_initial_frac: float
    degradation_cost_inr_per_mwh: float | None = None


class MarketLimits(BaseModel):
    dam_price_cap_inr_per_mwh: float | None = None
    rtm_price_cap_inr_per_mwh: float | None = None
    max_dam_buy_mw: float | None = None
    max_rtm_buy_mw: float | None = None
    transmission_losses_frac: float | None = None


class DiscomConfig(BaseModel):
    name: str
    state: str | None = None
    ppa: list[PpaContract]
    bess: BessSpec
    market: MarketLimits


class DsmBand(BaseModel):
    name: str | None = None
    deviation_from_pct_of_schedule: float | None = None
    deviation_to_pct_of_schedule: float | None = None
    over_drawal_rate: str | float | None = None
    under_drawal_rate: str | float | None = None
    clause_ref: str | None = None


class DsmRules(BaseModel):
    """Mirror of configs/dsm_rules.yaml. Fields stay None until you fill them."""

    name: str | None = None
    effective_from: date | None = None
    reference_rate_definition: str | None = None
    bands: list[DsmBand] = []
    max_charge_inr_per_mwh: float | None = None
    min_charge_inr_per_mwh: float | None = None


class BacktestConfig(BaseModel):
    start: date | None = None
    end: date | None = None
    train_end: date | None = None
    dam_decision_time_ist: str | None = None
    naive_demand: str | None = None
    naive_procurement: str | None = None
    oracle_enabled: bool = True


def get_settings() -> Settings:
    """Return validated environment settings (cache the result)."""
    raise NotImplementedError


def load_discom_config(path: Path) -> DiscomConfig:
    """Parse and validate configs/discom.yaml."""
    raise NotImplementedError


def load_dsm_rules(path: Path) -> DsmRules:
    """Parse configs/dsm_rules.yaml. Do not fill gaps with defaults."""
    raise NotImplementedError


def load_backtest_config(path: Path) -> BacktestConfig:
    """Parse configs/backtest.yaml."""
    raise NotImplementedError
