"""GET /health.

Must check what the service actually needs: Postgres reachable, Redis reachable, model
artefacts and the regulation index present. "Process is alive" is not a health check.
Return 200 only if all pass, 503 with the failing component named otherwise. Used by Compose
healthchecks, the staging smoke test and the platform's liveness probe.
"""

from __future__ import annotations

# router = APIRouter()
#
# @router.get("/health")
# async def health(): ...
