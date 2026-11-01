"""Mechanical guardrails on LLM output.

Owns:
  * numeric grounding: every number in generated prose must be traceable to a tool result
    (after allowed formatting: rounding, Indian digit grouping like 1,23,45,678, ₹ crore/lakh
    conversions, % signs, units). Anything else is an ungrounded number and fails.
  * citation check: every cited clause must appear in the retrieved chunks.
  * injection screen on retrieved/tool text before it enters a prompt (heuristics + structure,
    not a promise of safety).

Must NOT: use an LLM to judge grounding. This is deterministic code so it can be unit-tested
and trusted. Decide your tolerance rules (rounding, lakh/crore) explicitly and test them.
"""

from __future__ import annotations

from pydantic import BaseModel


class GroundingResult(BaseModel):
    ok: bool
    ungrounded_numbers: list[str]


def extract_numbers(text: str) -> list[str]:
    """Pull numeric tokens from prose, understanding Indian grouping and unit suffixes."""
    raise NotImplementedError


def check_grounding(
    text: str, tool_result_numbers: list[float], rel_tol: float = 0.005
) -> GroundingResult:
    """Every number in ``text`` must match some tool-result value within ``rel_tol`` after unit normalisation."""
    raise NotImplementedError


def check_citations(cited_clause_refs: list[str], retrieved_clause_refs: list[str]) -> list[str]:
    """Return cited refs that were NOT retrieved."""
    raise NotImplementedError


def screen_untrusted_text(text: str) -> bool:
    """True if retrieved/tool text looks like it contains instructions aimed at the model."""
    raise NotImplementedError
