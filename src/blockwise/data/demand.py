"""Load, solar and wind generation ingestion (the inputs to net demand).

Owns: validated block-level series for demand, solar and wind with their publication times,
and the definition of net demand = load - solar - wind (a pure function, easy to test).

Must NOT: assume the demand series includes behind-the-meter solar. State what it includes
in docs/assumptions.md (VERIFY).

DECISION(ADR-0002): which state/SLDC proxy and how it is scaled to a DISCOM.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd


async def fetch_demand(start: date, end: date) -> pd.DataFrame:
    """Columns: date, block, load_mw, solar_mw, wind_mw, published_at."""
    raise NotImplementedError


def net_demand_mw(load_mw: pd.Series, solar_mw: pd.Series, wind_mw: pd.Series) -> pd.Series:
    """Net demand in MW: load - solar - wind, aligned on (date, block)."""
    raise NotImplementedError


def save_demand(df: pd.DataFrame, root: Path) -> Path:
    raise NotImplementedError
