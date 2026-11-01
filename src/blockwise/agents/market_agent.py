"""Market agent: interprets price forecasts for the plan.

Owns: pulling DAM/RTM history context and forecasts via tools, flagging anomalies (spikes,
cap clipping, stale data) and summarising price risk in plain language.

Must NOT: forecast prices itself or quote any price not returned by a tool. The forecast
comes from forecasting/prices.py; this agent decides which tool to call and what to flag.
Prompt lives in agents/prompts/market_agent.md (versioned; changes are evaluated).
"""

from __future__ import annotations

from datetime import date


async def assess_prices(target_date: date, plan_run_id: str) -> str:
    """Return a grounded plain-language price-risk note."""
    raise NotImplementedError
