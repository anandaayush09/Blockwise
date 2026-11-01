"""The single source of truth for date <-> time-block conversion.

Owns: the mapping between timestamps and block numbers 1..96 in IST.
Block 1 = 00:00-00:15 IST, block 96 = 23:45-24:00 IST. India has no DST, so a day always
has 96 blocks.

Must NOT: be bypassed. No other module may do its own block arithmetic or timezone handling.
If a bug here shifts every block by one, every downstream number is wrong, so this module
is covered by the first spec tests (tests/unit/test_timeblocks.py).

Power/energy reminder: MWh in a block = MW * HOURS_PER_BLOCK.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

BLOCKS_PER_DAY = 96
BLOCK_MINUTES = 15
HOURS_PER_BLOCK = BLOCK_MINUTES / 60
IST = timezone(timedelta(hours=5, minutes=30), name="IST")


def block_start(day: date, block: int) -> datetime:
    """Start of ``block`` (1..96) on ``day`` as a tz-aware IST datetime.

    Raises ValueError if ``block`` is outside 1..96.
    """
    raise NotImplementedError


def block_of(ts: datetime) -> tuple[date, int]:
    """Return the (IST date, block number 1..96) that contains tz-aware ``ts``.

    ``ts`` may be in any timezone; it must be tz-aware. Naive datetimes are rejected
    (raise ValueError) rather than guessed.
    """
    raise NotImplementedError


def day_blocks(day: date) -> list[datetime]:
    """All 96 block start times for ``day``, in order, tz-aware IST."""
    raise NotImplementedError


def mw_to_mwh(mw: float) -> float:
    """Energy in one block for a constant power of ``mw`` MW."""
    raise NotImplementedError
