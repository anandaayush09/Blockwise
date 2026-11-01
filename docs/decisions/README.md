# Decisions (ADRs)

One file per decision, copied from [0000-template.md](0000-template.md). Status: **open** until you write the choice and the reasons. Options below are starting points; add your own. Your job is to be able to defend each one aloud in 60 seconds.

| ADR | Decision | Options to compare | Closed in phase |
|---|---|---|---|
| [0001](0001-llm-never-does-arithmetic.md) | LLM never does arithmetic | accepted (worked example) | 0 |
| 0002 | Data sources and DISCOM proxy | state SLDC series vs. synthetic DISCOM scaling; IEX public data vs. scraped vs. paid; what to do about gaps | 0 |
| 0003 | DSM encoding | rules-as-data (YAML) vs. code constants vs. RAG-extracted rules; versioning by effective date | 2 |
| 0004 | Forecast models and uncertainty | seasonal-naive vs. gradient boosting vs. quantile regression vs. neural; how to produce P10/P50/P90 | 5 |
| 0005 | Solver and DSM treatment | OR-Tools vs. PuLP/HiGHS; scenarios vs. piecewise-linear expected DSM; binaries vs. convexity; cycling cost; no deliberate deviation | 6 |
| 0006 | Agent runtime | plain SDK tool-use loop vs. LangGraph (state, checkpoints, interrupts) vs. other; decide after building both | 9 |
| 0007 | Retrieval and vector store | pgvector vs. Qdrant; chunking unit (clause vs. fixed); hybrid + rerank or not; embedding model | 8 |
| 0008 | Backtest protocol and baseline | naive baselines; expanding vs. rolling training; metrics; oracle definition | 3 |
| 0009 | Hosting and environments | Render vs. Cloud Run vs. other; free-tier limits; demo mode on a frozen snapshot | 10 |
| 0010 | LLM provider, model and budget | which model per step; effort/thinking settings; per-run ₹ budget; caching; routing | 7 |
| 0011 | Storage split | Postgres only vs. Postgres + parquet/DuckDB for time series | 4 |
| 0012 | Background jobs | Celery + Redis vs. cron/APScheduler vs. cloud scheduler | 4 |
| 0013 | Tracing and monitoring | LangSmith vs. OpenTelemetry-based vs. DIY logs; what is logged per tool call | 10 |
| 0014 | Operator memory | what is remembered, where, how it becomes constraints, how it is audited | 9 |
