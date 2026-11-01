"""Typed contracts passed between components, tools, the API and the database.

These models ARE the tool contracts: an agent tool's input and output are these types, so
every number the LLM may quote has a unit-labelled field here.

Conventions
-----------
* All series are length 96, index 0 = block 1 (00:00-00:15 IST).
* Power in MW, energy in MWh, money in INR, prices in INR/MWh. Units are in field names.
* Deviation = actual - scheduled; positive = over-drawal (VERIFY against the regulation).
* ``as_of`` is the information cutoff used to produce an artefact (leakage control).

Must NOT contain behaviour beyond validation. Domain logic lives in the components.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Annotated, Literal

from pydantic import BaseModel, Field

BlockNumber = Annotated[int, Field(ge=1, le=96)]
Series96 = Annotated[list[float], Field(min_length=96, max_length=96)]


class NetDemandForecast(BaseModel):
    """Net demand = load - solar - wind, as quantiles per block."""

    target_date: date
    as_of: datetime
    horizon: Literal["day_ahead", "intraday"]
    p10_mw: Series96
    p50_mw: Series96
    p90_mw: Series96
    model_version: str


class PriceForecast(BaseModel):
    market: Literal["DAM", "RTM"]
    target_date: date
    as_of: datetime
    p10_inr_per_mwh: Series96
    p50_inr_per_mwh: Series96
    p90_inr_per_mwh: Series96
    model_version: str


class PenaltySegment(BaseModel):
    block: BlockNumber
    deviation_mw: float
    band_name: str
    rate_inr_per_mwh: float
    amount_inr: float
    clause_ref: str


class PenaltyQuote(BaseModel):
    """Result of the deterministic DSM calculator for a proposed deviation."""

    target_date: date
    segments: list[PenaltySegment]
    total_inr: float
    rules_version: str  # which regulation + amendment + effective date was applied


class ScheduleBlock(BaseModel):
    block: BlockNumber
    ppa_mw: dict[str, float]  # contract id -> MW
    dam_mw: float
    rtm_mw: float
    bess_charge_mw: float
    bess_discharge_mw: float
    bess_soc_mwh: float  # end-of-block state of charge


class Schedule(BaseModel):
    schedule_id: str
    target_date: date
    blocks: Annotated[list[ScheduleBlock], Field(min_length=96, max_length=96)]
    expected_cost_inr: float
    cost_breakdown_inr: dict[str, float]  # e.g. ppa, dam, rtm, expected_dsm, bess
    inputs: dict[str, str]  # ids/versions of the forecasts and rules it was built from


class DayActuals(BaseModel):
    target_date: date
    actual_net_demand_mw: Series96
    dam_mcp_inr_per_mwh: Series96
    rtm_price_inr_per_mwh: Series96


class DaySettlement(BaseModel):
    """Realised cost of running a schedule against what actually happened."""

    target_date: date
    purchase_cost_inr: float
    dsm_cost_inr: float
    total_cost_inr: float
    breakdown_inr: dict[str, float]


class ConstraintViolation(BaseModel):
    constraint: str  # e.g. "energy_balance", "bess_soc_max"
    block: BlockNumber | None
    detail: str
    magnitude: float | None  # in the constraint's own unit, stated in `detail`


class CriticReport(BaseModel):
    schedule_id: str
    passed: bool
    violations: list[ConstraintViolation]
    explanation: str  # plain language; every number must be grounded in tool results
    clause_citations: list[str]


class ApprovalRecord(BaseModel):
    plan_run_id: str
    decision: Literal["approved", "rejected"]
    operator: str
    decided_at: datetime
    reason: str | None


class ToolCallRecord(BaseModel):
    plan_run_id: str
    tool: str
    inputs: dict
    output_ref: str  # pointer to the stored output
    latency_ms: float
    called_at: datetime


class LlmCallRecord(BaseModel):
    plan_run_id: str
    model: str
    prompt_version: str
    input_tokens: int
    output_tokens: int
    cost_inr: float
    latency_ms: float
    called_at: datetime
