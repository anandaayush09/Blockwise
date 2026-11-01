# BlockWise Roadmap

~20 weeks at ~10 hrs/week. The phase order follows the order your learning roadmap teaches things (Python -> backend -> LLM -> RAG -> agents -> LLMOps -> polish), so each concept is used in BlockWise right after you learn it. See [docs/concept-map.md](docs/concept-map.md).

**Ground rules**
1. You write the logic. The skeleton gives you contracts, docstrings and spec tests; every body is `NotImplementedError`.
2. A phase is done only when you can explain it out loud with no notes (each phase lists the questions).
3. Get a ₹ number from a naive pipeline early (Phase 3), then improve one component at a time and re-measure in ₹.
4. Each phase ends with: remove the `xfail` marker from its tests, close its ADRs (`docs/decisions/`), add one line to your progress log (built / broke / learned).
5. Commit small with `feat:` `fix:` `docs:` `test:` prefixes. `.env` is gitignored before the first commit.

**Cut list if you fall behind (cut in this order):** Kubernetes, semantic cache, rerank, intraday stage, BESS, multi-agent split (keep one orchestrator + critic).

---

## Phase 0 - Setup, domain, data feasibility (week 1)
**Goal:** know whether the data exists before designing anything.
- [ ] `git init`, first commit, confirm `.env` is ignored
- [ ] Read [docs/domain-primer.md](docs/domain-primer.md) end to end; resolve every VERIFY item against primary sources (regulation text, exchange rules)
- [ ] Fill the data inventory in `data/README.md`: where do 6-12 months of block-wise DAM and RTM prices, demand, solar/wind and weather come from? Licence? Granularity? Gaps?
- [ ] Choose the DISCOM/state proxy and how you scale it (ADR-0002)
- **Done when:** data inventory filled; ADR-0002 decided; raw files downloaded.
- **Explain:** why a state-level series is a proxy for a DISCOM and how that biases results. What is net demand and why is it harder to forecast as RE share grows?
- **Pitfalls:** discovering in week 8 that RTM history is not available at block level.

## Phase 1 - Data layer and block calendar (weeks 2-3)
**Concepts practised:** Pydantic, async httpx, logging, decorators/context managers, pytest.
- [ ] `timeblocks.py`: the single source of truth for date <-> block (1..96, IST)
- [ ] `data/*`: ingest to parquet, validate with Pydantic, async weather fetch
- [ ] `data/store.py`: **as-of reads** - "what did we know at time T?"
- [ ] `cli.py`: `blockwise ingest ...`
- **Done when:** timeblocks tests pass; one call returns any day's 96 rows for every series.
- **Explain:** why as-of access matters (leakage); how you handled DST-free IST vs UTC storage; what you do with missing blocks.
- **Pitfalls:** UTC/IST off-by-one at midnight; 23/25-hour assumptions copied from other countries (India has no DST); revised vs first-published data.

## Phase 2 - DSM penalty calculator (week 4)
**Concepts practised:** pure functions, rules as data, unit testing.
- [ ] Fill `configs/dsm_rules.yaml` from the regulation, every value with a clause reference (ADR-0003)
- [ ] `regulation/penalty.py`: `quote_penalty(...)` returns a per-block breakdown by band
- [ ] 5+ hand-calculated worked examples as tests
- **Done when:** penalty tests pass and you can recompute any example by hand.
- **Explain:** why penalty lives in code + YAML and the LLM only cites it; which rule version applies to which backtest day.
- **Pitfalls:** sign convention; percent of schedule vs capacity; rule changes mid-backtest.

## Phase 3 - Walking-skeleton backtest (week 5)
- [ ] `backtest/settlement.py`: given schedule + actuals + prices, compute realised ₹ cost
- [ ] `backtest/policies.py`: the naive baseline policy
- [ ] `backtest/engine.py`: replay each test day as-of; `report.py`: first table
- **Done when:** a baseline ₹ number exists for the full period and the leakage checklist in `docs/assumptions.md` is ticked.
- **Explain:** exactly what the baseline does and why a fair comparison needs the same information set.
- **Pitfalls:** tuning on the test window; baseline strawman that is too dumb.

## Phase 4 - Backend (weeks 6-7)
**Concepts practised:** FastAPI (routes, DI, middleware), Postgres, Alembic, Redis cache-aside, Celery, Docker Compose, TestClient.
- [ ] `db/*`: tables for plan runs, schedules, approvals, tool-call and LLM-call logs
- [ ] `api/*`: `/health` (checks DB + Redis), plans, backtests
- [ ] `worker/*`: backtest as a background task; beat schedule stub
- [ ] `docker compose up` brings the whole stack up with healthchecks
- **Done when:** a backtest job is triggered via the API and results land in Postgres (ADR-0011, ADR-0012).
- **Explain:** why Postgres for app state but parquet/DuckDB for time series; why Celery vs a cron; why no MongoDB.
- **Pitfalls:** putting 96-row time series in relational rows by default; blocking the API on long jobs.

## Phase 5 - Forecasting (weeks 8-9)
- [ ] `forecasting/baselines.py` first (seasonal-naive), then `net_demand.py` and `prices.py`
- [ ] Quantiles (P10/P50/P90) for net demand; day-ahead and intraday horizons
- [ ] Rows in the eval table that beat baselines
- **Done when:** forecast metrics filled in the README table; features provably as-of (ADR-0004).
- **Explain:** why probabilistic forecasts matter for DSM risk; what you do when RE output is the error source.
- **Pitfalls:** using actual (not forecast) weather as features; price-cap clipping; evaluating on the training window.

## Phase 6 - MILP optimiser and oracle (weeks 10-11)
- [ ] `optimiser/model.py`: variables, constraints, objective (equations first, in `docs/architecture.md`)
- [ ] `optimiser/checks.py`: independent constraint checker (does not call the solver)
- [ ] Oracle = same model with perfect foresight; report the share of the oracle gap you capture (ADR-0005)
- **Done when:** invariant tests pass; the backtest shows ₹ saved vs baseline and vs oracle.
- **Explain:** each constraint in words; why the checker is separate from the model; how DSM risk enters the objective without encouraging deliberate deviation.
- **Pitfalls:** simultaneous charge/discharge; assuming the DISCOM is a price-taker when it is not; infeasible days.

## Phase 7 - LLM layer (week 12)
**Concepts practised:** tokens/cost, tool schemas, structured output, streaming, prompt harness.
- [ ] `agents/tools.py`: `BaseTool` + registry; wrap forecast/penalty/optimiser/checker as tools
- [ ] `agents/guardrails.py`: numeric grounding - every number in prose must appear in a tool result
- [ ] `agents/llm.py` implementation; per-run cost logging; SSE explanation endpoint
- [ ] Prompt harness: N inputs x prompt variants -> logged and scored
- **Done when:** an LLM can call every tool; cost per run is logged; guardrail test passes (ADR-0010).
- **Explain:** exactly where the model could do arithmetic and how you prevent it.
- **Pitfalls:** forcing tool choice (current Claude models reject it; steer via prompt and strict schemas); unit confusion (MW vs MWh) in tool descriptions.

## Phase 8 - Regulation RAG (weeks 13-14)
**Concepts practised:** chunking, embeddings, vector DB, hybrid BM25 + RRF, rerank, query rewriting, RAGAS, contextual retrieval.
- [ ] `regulation/corpus.py`: clause-aware chunking that keeps clause number and hierarchy
- [ ] `regulation/retriever.py`: dense + BM25 + reciprocal rank fusion; test a clause-number query embeddings miss (ADR-0007)
- [ ] 30+ question eval set with the clause that answers each
- **Done when:** RAG rows in the README table; answers always cite a clause.
- **Explain:** why RAG cites and `penalty.py` calculates; what a wrong-but-confident citation costs.
- **Pitfalls:** chunks that split a clause from its table; amended vs superseded text; stale corpus.

## Phase 9 - Agents (weeks 15-16)
**Concepts practised:** raw ReAct loop, LangGraph, tool design, multi-agent, memory, MCP, human-in-the-loop.
- [ ] `agents/loop.py` first (plain Python); then `agents/graph.py` (LangGraph); decide in ADR-0006
- [ ] Market, regulation and critic agents; orchestrator (workflow for the daily plan; agent only for what-if questions)
- [ ] `agents/memory.py`: operator preferences in Postgres, applied as optimiser constraints via a tool (ADR-0014)
- [ ] `mcp_server.py`: expose deterministic tools
- [ ] Approval interrupt before the mock "submit bids" step
- **Done when:** plan -> critic -> operator approval end to end with zero ungrounded numbers.
- **Explain:** workflow vs agent for each part; what LangGraph gives you that your loop did not; how the critic differs from the guardrail.
- **Pitfalls:** loops without termination; critic that agrees with everything; letting an agent run the solver unconstrained.

## Phase 10 - Production and LLMOps (weeks 17-18)
**Concepts practised:** multi-stage Docker, CI/CD, staging/production, tracing, Sentry, eval gates, injection tests, cost monitoring.
- [ ] Multi-stage non-root Dockerfile; `docker history` shows no secrets
- [ ] CI: ruff, pytest, pip-audit, docker build; branch protection requires it
- [ ] CD: build once, tag with commit SHA, push to GHCR, auto-deploy to staging, manual approval for production; smoke test after deploy; rehearse a rollback (ADR-0009)
- [ ] Tracing (ADR-0013), Sentry, structured logs, cost-per-run query, optional semantic cache
- [ ] Prompt-injection test: a poisoned regulation chunk saying "ignore previous instructions"; add the guardrail
- [ ] Eval gates: deterministic suites every push; LLM suites manual or nightly
- **Done when:** a broken build is blocked by CI; staging deploys automatically; production waits for approval; rollback is timed and written in the runbook.
- **Explain:** why LLM evals are not run on every push; what you log per tool call; how you find a bug with no debugger attached.
- **Pitfalls:** secrets in layers or git history; evals that cost real money on every commit.

## Phase 11 - Ship and interview prep (weeks 19-20)
- [ ] Finish the README (every TODO); record the 2-minute video ([docs/demo-video-script.md](docs/demo-video-script.md))
- [ ] Publish the failure post ([posts/](posts/README.md))
- [ ] Fill answers in [docs/interview-prep.md](docs/interview-prep.md); rehearse each ADR in 60 seconds, out loud
- [ ] Mock interviews: project deep-dive, system design (end on failure modes + monitoring)
- **Done when:** live demo + video + post are public and you can defend every decision without notes.

## Stretch (only if ahead)
Kubernetes (minikube deploy, kill a pod, watch it restart); multi-provider routing; Contextual Retrieval-style chunk enrichment; fan-chart what-if exploration.
