# System design notes

_Skeleton to fill as you build; this is the document you narrate in a system-design interview._

## 1. Request flows

**Daily plan (deadline-driven batch).** Scheduler -> worker -> forecast tools -> optimiser -> checker -> critic -> Postgres -> operator console. Latency budget is "ready before the day-ahead bidding deadline" (VERIFY the time), not milliseconds.
- Where is the cache? (forecasts keyed by as-of time; regulation answers keyed by question + corpus version)
- Where are the safety checks? (input validation, constraint checker, numeric-grounding guardrail, human approval)

**What-if question (interactive).** Operator asks "what if the evening peak is 5% higher?" -> agent chooses tools -> streamed answer. Here first-token latency matters; list what in the pipeline threatens it.

_TODO: draw both flows with caching and safety checkpoints marked._

## 2. Workflow or agent?

| Part | Pattern | Why |
|---|---|---|
| Daily plan | Prompt chaining + orchestrator-workers | steps are known; a fixed order is cheaper and testable |
| Critic | Evaluator-optimiser | a separate check on the optimiser's output, can send back for re-solve |
| What-if Q&A | Agent (ReAct) | open-ended; the tool sequence is not known in advance |
| Regulation lookup | RAG | needs citations to source text |

## 3. Cost, latency, accuracy

Narrate the same design three ways (optimise cost, latency, accuracy) and note what you would change each time. _TODO_

Prefill vs decode: a long regulation context is a prefill cost (parallel); long explanations are decode cost (sequential). Which of your prompts is which? Is prompt caching worth it for the static regulation context?

## 4. Data tiers

| Tier | Holds | Store (ADR-0011) |
|---|---|---|
| Hot / app state | plan runs, approvals, operator preferences, call logs | Postgres |
| Time series | prices, demand, weather, forecasts | parquet + DuckDB |
| Cache | forecasts, regulation answers | Redis |
| Retrieval | regulation chunks + embeddings | pgvector or Qdrant (ADR-0007) |

## 5. Failure modes (list yours)

- Data feed late or revised -> ?
- Optimiser infeasible or times out -> ?
- LLM provider down or over budget -> ?
- Retrieval returns a superseded clause -> ?
- Operator unavailable at the deadline -> ?

## 6. What changes at scale

One DISCOM -> many DISCOMs (multi-tenant data, per-tenant rules), per-block intraday re-planning, model registry, drift monitoring. _TODO_
