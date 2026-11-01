"""Critic agent: checks the schedule against constraints and explains it in plain language.

Owns: calling the independent constraint checker, reading its violations, and writing the
operator-facing explanation: what the schedule does, why (cheapest mix, battery use,
exposure to DSM), what the risks are, which clauses matter.

Must NOT: re-derive costs or constraints itself, approve a schedule the checker failed, or
state a number that is not in a tool result. It is an evaluator, not a second optimiser.
Evaluate it by injecting known violations and measuring detection (evals/datasets/critic_injected.jsonl).
"""

from __future__ import annotations

from blockwise.schemas import CriticReport, Schedule


async def critique(schedule: Schedule, plan_run_id: str) -> CriticReport:
    raise NotImplementedError
