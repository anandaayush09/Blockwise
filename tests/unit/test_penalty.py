"""Phase 2. Invariants that must hold for ANY correct DSM implementation.

Hand-calculated worked examples from the real regulation belong in this file too once you
have filled configs/dsm_rules.yaml: add them yourself, with the clause cited in a comment.
"""

import pytest

from blockwise.config import DsmRules
from blockwise.regulation.penalty import marginal_penalty_inr_per_mwh, quote_penalty

pytestmark = pytest.mark.xfail(raises=NotImplementedError, reason="Phase 2 not implemented")

SCHEDULE = [100.0] * 96
REF_RATE = [5000.0] * 96


def _quote(day, rules, deviation_mw):
    actual = [100.0 + deviation_mw] * 96
    return quote_penalty(day, SCHEDULE, actual, REF_RATE, rules)


def test_zero_deviation_costs_nothing(day, dsm_rules):
    assert _quote(day, dsm_rules, 0.0).total_inr == 0.0


def test_total_equals_sum_of_segments(day, dsm_rules):
    q = _quote(day, dsm_rules, 7.0)
    assert q.total_inr == pytest.approx(sum(s.amount_inr for s in q.segments))


def test_over_drawal_penalty_never_decreases_with_size(day, dsm_rules):
    totals = [_quote(day, dsm_rules, d).total_inr for d in (0.0, 2.0, 5.0, 10.0, 25.0)]
    assert totals == sorted(totals)


def test_every_segment_names_the_clause_it_came_from(day, dsm_rules):
    q = _quote(day, dsm_rules, 10.0)
    assert q.segments and all(s.clause_ref for s in q.segments)


def test_refuses_to_quote_with_unfilled_rules(day):
    """Missing rule values must raise a ValueError naming the field, never fall back to a default."""
    with pytest.raises(ValueError):
        quote_penalty(day, SCHEDULE, [110.0] * 96, REF_RATE, DsmRules())


def test_marginal_penalty_non_decreasing_convexity_check(dsm_rules):
    """VERIFY against the real rules. If this fails for your real encoding, the penalty is
    non-convex and the optimiser needs binaries (ADR-0005)."""
    slopes = [
        marginal_penalty_inr_per_mwh(d, 100.0, 5000.0, dsm_rules) for d in (1.0, 5.0, 10.0, 20.0)
    ]
    assert slopes == sorted(slopes)
