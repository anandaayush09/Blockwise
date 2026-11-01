"""Plan endpoints (the operator workflow).

POST /plans                       body: {date}  -> 202 + plan_run_id; the run executes in the worker
GET  /plans/{id}                  -> status, Schedule, CriticReport
GET  /plans/{id}/explanation      -> SSE stream of the explanation
POST /plans/{id}/decision         body: {decision, operator, reason} -> records ApprovalRecord
POST /plans/{id}/what-if          body: {question} -> grounded answer

Rules: a plan cannot reach "submitted" without an approved ApprovalRecord. Failure paths
(unknown id, solver infeasible, guardrail failure) return typed errors, never a stack trace.
"""

from __future__ import annotations
