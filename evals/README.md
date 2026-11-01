# Evals

"Is there an actual eval framework, or is it vibes?" This folder is the answer. Every row in the README eval table comes from a run of something here.

Two kinds, run differently:

| Kind | Needs LLM? | Runs | Gate |
|---|---|---|---|
| **Deterministic** (forecast metrics, penalty worked examples, optimiser/checker invariants, backtest, guardrail tests) | no | every push (pytest + `run_evals.py --suite deterministic`) | fails the build below threshold |
| **LLM-graded / LLM-in-the-loop** (RAG quality, critic detection, tool routing, explanation grounding) | yes (costs money) | manually or nightly (`.github/workflows/evals.yml`), with a budget cap | reported; blocks release if below threshold |

## Suites and datasets (JSONL, one case per line; build these yourself from real cases)

| Suite | File | Case fields | Metrics |
|---|---|---|---|
| Regulation QA | `datasets/regulation_qa.jsonl` | `question`, `gold_clause_refs[]`, `gold_answer_points[]` | context recall, faithfulness, citation accuracy (RAGAS + your own check) |
| Retrieval edge cases | `datasets/retrieval_probes.jsonl` | `query`, `must_retrieve_clause` | hit rate; include exact clause-number queries that embeddings miss |
| Critic detection | `datasets/critic_injected.jsonl` | `schedule` (valid + one injected violation), `expected_constraint` | detection rate, false-alarm rate |
| Tool routing | `datasets/tool_routing.jsonl` | `user_message`, `expected_first_tool`, `ambiguous` | routing accuracy, esp. on adversarial/ambiguous prompts |
| Explanation grounding | produced by runs on frozen days | explanation text + tool results | ungrounded numbers per explanation (target 0) |
| Injection | `datasets/injection.jsonl` | poisoned chunk text, expected behaviour | pass/fail (agent must not obey) |

Aim for dozens of cases per suite, not thousands; every case should be one you can explain. Version datasets; never tune prompts on the cases you report.

## Running

```bash
uv run python evals/run_evals.py --suite deterministic
uv run python evals/run_evals.py --suite regulation_qa --budget-inr 500
```

Every run writes `evals/results/<suite>-<timestamp>.json` (gitignored) with model, prompt version, corpus version, cost, and per-case outcomes.
