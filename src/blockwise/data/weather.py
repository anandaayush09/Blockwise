"""Weather data: forecasts as issued, and observations.

Owns: async fetching (httpx) with timeouts and retries, concurrent over locations/days
(asyncio.gather), validated into rows with ``issued_at``.

Must NOT: use observed weather as a feature for a past day's forecast. Features must use the
forecast that existed at the as-of time. Store both and keep them distinct.

Open-Meteo (free, no key) is a convenient starting point; check its historical-forecast
coverage before relying on it (VERIFY, ADR-0002).
"""

from __future__ import annotations

from datetime import date

import pandas as pd


async def fetch_weather_forecasts(lat: float, lon: float, start: date, end: date) -> pd.DataFrame:
    """Columns: valid_time, issued_at, temperature_c, cloud_cover_pct, wind_speed_ms, irradiance_wm2."""
    raise NotImplementedError


async def fetch_weather_observations(
    lat: float, lon: float, start: date, end: date
) -> pd.DataFrame:
    """Same columns without ``issued_at``. For evaluation only, never as features."""
    raise NotImplementedError
