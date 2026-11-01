# Multi-stage, non-root. Practised in Phase 10 (ROADMAP.md).
# Secrets are NEVER passed with ARG/COPY here - only as runtime env vars.
# Verify with: docker history <image>   (no key or password in any layer)

# ---- builder: install deps into a venv --------------------------------------
FROM python:3.12-slim AS builder
ENV PIP_NO_CACHE_DIR=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /build
COPY pyproject.toml README.md ./
COPY src ./src
# TODO(Phase 10): choose extras per image (api/worker need different ones).
RUN python -m venv /opt/venv && /opt/venv/bin/pip install ".[api,worker,forecast,optimise,rag,agents]"

# ---- runtime: copy only what is needed --------------------------------------
FROM python:3.12-slim AS runtime
ENV PATH="/opt/venv/bin:$PATH" PYTHONUNBUFFERED=1
RUN useradd --create-home --uid 10001 appuser
COPY --from=builder /opt/venv /opt/venv
COPY configs /app/configs
WORKDIR /app
USER appuser
EXPOSE 8000
# TODO(Phase 10): HEALTHCHECK hitting /health (checks DB + Redis + model artefacts, not just "process alive")
CMD ["uvicorn", "blockwise.api.app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
