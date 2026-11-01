"""Deterministic DSM penalty calculator. No LLM, no network, no randomness.

Owns: given scheduled and actual drawal per block (or a proposed deviation) and the DSM
rules in force on that date, return the exact penalty with a per-band breakdown and the
clause that justifies each rate.

Must NOT: guess. If any rule value needed for the date is None in configs/dsm_rules.yaml,
raise a clear error naming the missing field. A silent default would corrupt every backtest number.
Must NOT: call the retriever. The regulation agent cites clauses; this module calculates.

Used by: the optimiser (expected DSM cost), settlement (realised DSM cost), and the
`penalty_quote` agent tool.

DECISION(ADR-0003): rules encoding and versioning by effective date.
VERIFY: sign convention, band basis (% of schedule vs capacity vs MW), reference rate.

Invariants (see tests/unit/test_penalty.py):
  * deviation == 0 in every block => total == 0
  * for over-drawal, a larger deviation never costs less (non-decreasing)
  * total == sum of segment amounts
"""

from __future__ import annotations

from datetime import date

from blockwise.config import DsmRules
from blockwise.schemas import PenaltyQuote


def rules_in_force(rules_by_period: list[DsmRules], day: date) -> DsmRules:
    """Pick the rule set whose effective period contains ``day``."""
    raise NotImplementedError


def quote_penalty(
    target_date: date,
    scheduled_mw: list[float],
    actual_mw: list[float],
    reference_rate_inr_per_mwh: list[float],
    rules: DsmRules,
) -> PenaltyQuote:
    """Penalty in INR for 96 blocks of scheduled vs actual drawal.

    Inputs are length-96 lists in MW (block 1 first). Energy per block = MW * 0.25 h.
    """
    raise NotImplementedError


def marginal_penalty_inr_per_mwh(
    deviation_mw: float, scheduled_mw: float, reference_rate_inr_per_mwh: float, rules: DsmRules
) -> float:
    """Slope of the penalty at a given deviation. Needed to check convexity (ADR-0005)."""
    raise NotImplementedError
