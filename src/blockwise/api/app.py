"""FastAPI application factory.

Owns: creating the app, registering routers, middleware (request id, logging, timing,
error mapping), Sentry init, and startup/shutdown of DB and Redis connections.

Must NOT: hold domain logic. Routes call components; components know nothing about HTTP.
Run with: uvicorn blockwise.api.app:create_app --factory
"""

from __future__ import annotations


def create_app():  # -> fastapi.FastAPI
    raise NotImplementedError
