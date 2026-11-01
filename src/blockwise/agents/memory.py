"""Operator memory: preferences that persist across sessions and become optimiser constraints.

Example: "never discharge the battery below 30% before the evening peak" or "cap RTM exposure
at X MW". Stored in Postgres, applied through a tool/parameter, and shown to the operator.

Must NOT: let free-text memory silently change the optimiser. A preference must be parsed into
a typed constraint, confirmed by the operator, and logged with who set it and when.

DECISION(ADR-0014): what is remembered, schema, expiry, audit.
"""

from __future__ import annotations

from pydantic import BaseModel


class OperatorPreference(BaseModel):
    operator: str
    key: str  # e.g. "bess_min_soc_frac_before_peak"
    value: float | str
    confirmed: bool


async def save_preference(pref: OperatorPreference) -> None:
    raise NotImplementedError


async def load_preferences(operator: str) -> list[OperatorPreference]:
    raise NotImplementedError
