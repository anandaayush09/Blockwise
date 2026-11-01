"""Forecast endpoints.

GET /forecasts/net-demand?date=YYYY-MM-DD&horizon=day_ahead|intraday -> NetDemandForecast
GET /forecasts/prices?market=DAM|RTM&date=YYYY-MM-DD               -> PriceForecast

Validate dates (422 on bad input), use cache-aside (cache.py) keyed by date + as_of + model
version. No computation in the route.
"""

from __future__ import annotations
