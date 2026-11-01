# Interview prep

Answers are deliberately blank. Write each in your own words, then say it aloud in under 60 seconds with no notes. "What a strong answer covers" is a hint, not an answer.

## The three near-certain questions, tailored

**1. "Your app gets 1M queries/day - how do you optimise cost?"**
Covers: where tokens go (measure per run), caching (prompt caching of static regulation context, answer cache), what runs deterministically instead of via the LLM, model choice by step, budget cap, batch for evals. Use your own cost-per-run numbers.
Your answer: _TODO_

**2. "Design a RAG system for [regulation Q&A]. How do you evaluate it?"**
Covers: clause-aware chunking, hybrid retrieval, citations, eval set built from real questions, context recall + faithfulness + citation accuracy, regression gate in CI.
Your answer: _TODO_

**3. "What's the difference between an agent and a simple LLM chain?"**
Covers: who decides the next step; workflow vs agent; why the daily plan is a workflow and what-if Q&A is an agent.
Your answer: _TODO_

## Design-defence questions (one per ADR)
- Why does the LLM never do arithmetic? What breaks if it does? _TODO_
- Why rules-as-code for DSM instead of RAG over the regulation? _TODO_
- Why this forecast model and how do you know it generalises? _TODO_
- Why MILP (vs heuristic or RL)? Is your penalty convex, and what follows? _TODO_
- Why raw loop vs LangGraph? What did LangGraph give you? _TODO_
- Why this vector store and chunking? What failed first? _TODO_
- How do you know the backtest savings are real? What would make them fake? _TODO_
- Why Postgres + parquet and no MongoDB? _TODO_
- Why Celery? Why not a cron job? _TODO_
- How do you stop the system from "gaming" the DSM with deliberate deviation? _TODO_

## Evidence questions
- "Is there an actual eval framework or is it vibes?" Point at the eval table and CI gate. _TODO_
- "What would you do differently if you started over?" _TODO_
- "What broke in production-like conditions?" (your failure post) _TODO_
- "How do you debug when there is no VS Code?" (logs, traces, Sentry) _TODO_

## Domain questions an energy person may ask
- Why is net demand harder to forecast with more solar/wind? _TODO_
- What is the reference rate in DSM and why does it matter? _TODO_
- What does the price-taker assumption cost you? _TODO_

## Anti-pattern to avoid
Enthusiasm without evidence. Every claim gets a number, a measured comparison, or a specific failure.
