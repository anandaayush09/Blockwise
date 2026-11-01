"""Independent constraint checker for schedules.

Owns: verifying a ``Schedule`` against the DISCOM config and the forecasts WITHOUT touching
the optimiser model or the solver. Plain arithmetic on the schedule's numbers.

Why separate: if the model has a bug (wrong sign, missing constraint), a checker that shares
its code would repeat the bug. Written independently, a bug must appear twice to slip through.
The critic agent calls this as a tool and explains the result; it does not re-derive anything.

Checks to implement (each returns ConstraintViolation entries with units in ``detail``):
  * energy balance in every block (supply vs net-demand forecast, state which quantile)
  * PPA min/max per contract
  * DAM and RTM purchase limits
  * BESS power limits, SoC bounds, efficiency accounting, no simultaneous charge/discharge
  * SoC continuity between blocks
  * non-negativity where required
"""

from __future__ import annotations

from blockwise.config import DiscomConfig
from blockwise.schemas import ConstraintViolation, NetDemandForecast, Schedule


def check_schedule(
    schedule: Schedule, demand: NetDemandForecast, discom: DiscomConfig, tolerance_mw: float = 1e-6
) -> list[ConstraintViolation]:
    """Return all violations; an empty list means the schedule satisfies every constraint."""
    raise NotImplementedError
