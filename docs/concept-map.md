# Concept map: learning roadmap -> BlockWise

Source: your `AI_Engineer_Roadmap_Complete.md`. This shows where each concept is used here, and in which BlockWise phase.

| Roadmap concept | Where in BlockWise | Phase |
|---|---|---|
| Pydantic models and validation | `schemas.py`, `config.py`, data validation on ingest | 1 |
| OOP / abstract base classes | `agents/tools.py::BaseTool` and subclasses per tool | 7 |
| Decorators, context managers | `observability.py`: timing decorator, run-context manager | 1, 10 |
| asyncio / gather | concurrent IEX and weather fetches in `data/*` | 1 |
| Logging and debugging (no print, no debugger in prod) | structlog everywhere; tool-call logs; tracing | 1, 10 |
| pytest, mocking, fixtures | spec tests; `FakeLLMClient`; no real API in tests | all |
| FastAPI: routes, DI, middleware | `api/*` | 4 |
| Postgres + SQL | `db/*`: plan runs, approvals, call logs, cost query | 4 |
| Redis cache-aside | `cache.py`: forecasts, regulation answers | 4 |
| Celery / queues | `worker/*`: backtests, D-1 run | 4 |
| MongoDB | **deliberately not used**: no document-store need (be ready to say why) | - |
| Tokens, context windows, cost | per-run cost logging, budget cap (ADR-0010) | 7 |
| Prompt engineering and harness | versioned prompts in `agents/prompts/`, scored by evals | 7 |
| Function calling / structured output | tools with strict schemas; `CriticReport` | 7 |
| Streaming | SSE explanation endpoint, console | 7 |
| Multi-provider routing | optional, ADR-0010 | stretch |
| Chunking strategies | clause-aware chunking of the regulation | 8 |
| Embeddings, vector DB | pgvector or Qdrant (ADR-0007) | 8 |
| Hybrid search (BM25 + dense, RRF) | clause-number queries embeddings miss | 8 |
| Reranking, query rewriting | `retriever.py` | 8 |
| RAGAS and eval sets | faithfulness, context recall, citation accuracy | 8 |
| Contextual retrieval | enrich each chunk with its clause path | 8 / stretch |
| ReAct loop by hand | `agents/loop.py` | 9 |
| LangGraph (state, edges, checkpoints) | `agents/graph.py` | 9 |
| Tool design and adversarial testing | tool descriptions tested with ambiguous prompts | 9 |
| Agent memory | operator preferences -> optimiser constraints (ADR-0014) | 9 |
| MCP | `mcp_server.py` exposing deterministic tools | 9 |
| Multi-agent (orchestrator + subagents) | market / regulation / critic agents | 9 |
| Human-in-the-loop | operator approval interrupt | 9 |
| Workflows vs agents (Anthropic) | `docs/system-design.md` table | 9 |
| AI system design (request flow, latency, cost triangle) | `docs/system-design.md` | 10, 11 |
| Docker multi-stage, non-root, no secrets | `Dockerfile`, `.dockerignore` | 10 |
| Compose | `docker-compose.yml` | 4 |
| CI (lint, test, audit, build) | `.github/workflows/ci.yml` | 10 |
| CD: SHA-tagged image, staging -> prod approval | `.github/workflows/cd.yml` | 10 |
| Health checks, smoke tests, rollback | `docs/runbook.md` | 10 |
| Tracing, Sentry, cost monitoring | `observability.py`, ADR-0013 | 10 |
| Prompt-injection security (OWASP LLM) | poisoned-regulation-chunk test | 10 |
| Eval gates in CI | `.github/workflows/evals.yml`, `evals/` | 10 |
| README that interviews well, ADR rehearsal | README, `docs/decisions`, `docs/interview-prep.md` | 11 |
| Kubernetes | stretch only | - |
| DSA | separate track; graph/topological-sort link: LangGraph node order | - |
