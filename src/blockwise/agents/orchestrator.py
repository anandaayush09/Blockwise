"""Top-level procurement workflow and the human approval gate.

Daily plan = a WORKFLOW (fixed order, cheap, testable), not a free-roaming agent:
  1. get forecasts (net demand, DAM, RTM)              [tool calls]
  2. market agent: sanity-check price forecast, flag anomalies
  3. optimiser tool -> Schedule
  4. constraint checker tool -> violations
  5. if violations: re-solve with adjusted inputs (bounded retries) or escalate
  6. regulation agent: cite clauses relevant to the residual DSM exposure
  7. critic agent: CriticReport (pass/fail + plain-language explanation)
  8. guardrail: every number in the explanation grounded in tool results
  9. OPERATOR APPROVAL: record ApprovalRecord; nothing irreversible before this
 10. (mock) submit bids

What-if questions from the operator use the agent loop instead (open-ended).

Owns: sequencing, retries, persistence of every step, the approval gate.
Must NOT: do arithmetic, bypass guardrails, or proceed past step 9 without an approved record.
"""

from __future__ import annotations

from datetime import date

from blockwise.schemas import ApprovalRecord, CriticReport, Schedule


async def run_daily_plan(target_date: date, plan_run_id: str) -> tuple[Schedule, CriticReport]:
    """Run steps 1-8 and persist; return the schedule and critic report awaiting approval."""
    raise NotImplementedError


async def record_decision(approval: ApprovalRecord) -> None:
    """Persist the operator's decision (audit log). Only an 'approved' record enables submission."""
    raise NotImplementedError


async def answer_what_if(plan_run_id: str, question: str) -> str:
    """Agent-loop path for open-ended operator questions; grounded in tool results."""
    raise NotImplementedError
