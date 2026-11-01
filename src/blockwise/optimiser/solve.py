"""Run the solver and convert its solution to a typed Schedule.

Owns: solver configuration (time limit, gap), status handling, extraction of the solution
into ``schemas.Schedule``, and the cost breakdown.

Must NOT: return a schedule when the solver reports infeasible or timed out without saying so.
A missing schedule is an explicit result (raise a typed error), never a silent fallback.
The pipeline decides what to do on infeasibility (e.g. relax a soft constraint, alert the operator).

DECISION(ADR-0005): OR-Tools vs PuLP/HiGHS.
"""

from __future__ import annotations

from blockwise.schemas import Schedule


class InfeasibleScheduleError(RuntimeError):
    """Raised when no feasible schedule exists or the time limit passed with no incumbent."""


def solve(model, time_limit_s: float, schedule_id: str) -> Schedule:
    raise NotImplementedError
