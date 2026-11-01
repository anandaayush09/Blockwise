"""Phase 1. Remove the xfail marker when you implement timeblocks.py."""

from datetime import UTC, date, datetime, timedelta

import pytest

from blockwise.timeblocks import IST, block_of, block_start, day_blocks, mw_to_mwh

pytestmark = pytest.mark.xfail(raises=NotImplementedError, reason="Phase 1 not implemented")

D = date(2025, 1, 15)


def test_day_has_96_blocks_15_minutes_apart():
    starts = day_blocks(D)
    assert len(starts) == 96
    assert all(b - a == timedelta(minutes=15) for a, b in zip(starts, starts[1:], strict=False))


def test_block_1_starts_at_midnight_ist_and_block_96_at_2345():
    assert block_start(D, 1) == datetime(2025, 1, 15, 0, 0, tzinfo=IST)
    assert block_start(D, 96) == datetime(2025, 1, 15, 23, 45, tzinfo=IST)


def test_utc_evening_belongs_to_next_ist_day_block_1():
    # 18:30 UTC == 00:00 IST next day
    ts = datetime(2025, 1, 14, 18, 30, tzinfo=UTC)
    assert block_of(ts) == (date(2025, 1, 15), 1)


def test_timestamp_inside_a_block_maps_to_that_block():
    ts = datetime(2025, 1, 15, 6, 7, tzinfo=IST)  # 06:00-06:15 is block 25
    assert block_of(ts) == (D, 25)


def test_roundtrip_every_block():
    for b in range(1, 97):
        assert block_of(block_start(D, b)) == (D, b)


@pytest.mark.parametrize("bad", [0, 97, -1])
def test_invalid_block_rejected(bad):
    with pytest.raises(ValueError):
        block_start(D, bad)


def test_naive_datetime_rejected_not_guessed():
    with pytest.raises(ValueError):
        block_of(datetime(2025, 1, 15, 6, 7))


def test_mw_to_mwh_is_quarter_hour():
    assert mw_to_mwh(100.0) == pytest.approx(25.0)
