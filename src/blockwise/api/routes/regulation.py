"""Regulation endpoints.

POST /regulation/ask      body: {question} -> RegulationAnswer (answer + clause citations)
POST /regulation/penalty  body: {date, scheduled_mw[96], actual_mw[96]} -> PenaltyQuote (deterministic, no LLM)

The penalty endpoint must work with no LLM configured: it is the same code the backtest uses.
"""

from __future__ import annotations
