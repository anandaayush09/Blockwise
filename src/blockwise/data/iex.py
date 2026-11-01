"""IEX DAM and RTM price history ingestion.

Owns: turning whatever source ADR-0002 selects into validated block-level price rows
(market, date, block, price_inr_per_mwh, published_at).

Must NOT: drop the publication time. ``published_at`` is what makes as-of reads possible.
Must NOT: silently fill gaps; report them.

DECISION(ADR-0002): data source (public download, scraping within terms of use, paid feed).
VERIFY: RTM session structure and whether history is available at 15-minute resolution.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd


async def fetch_prices(market: str, start: date, end: date) -> pd.DataFrame:
    """Download raw price data for ``market`` ("DAM" or "RTM") between the dates (inclusive).

    Columns: market, date, block, price_inr_per_mwh, published_at.
    """
    raise NotImplementedError


def validate_prices(df: pd.DataFrame) -> pd.DataFrame:
    """Check block range 1..96, duplicates, missing blocks, and price caps. Raise on corruption; report gaps."""
    raise NotImplementedError


def save_prices(df: pd.DataFrame, root: Path) -> Path:
    """Write validated prices as parquet under ``root`` and return the path."""
    raise NotImplementedError
