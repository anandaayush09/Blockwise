"""SQLAlchemy models. Design the schema yourself on paper first.

Tables to design (columns, keys, indexes, and what is JSON vs relational):
  plan_runs        id, target_date, status, created_at, model/prompt/rules versions, cost_inr
  schedules        id, plan_run_id, payload (JSON or normalised? decide), expected_cost_inr
  critic_reports   id, plan_run_id, passed, explanation, violations
  approvals        id, plan_run_id, decision, operator, decided_at, reason   (append-only audit)
  tool_calls       id, plan_run_id, tool, inputs, output_ref, latency_ms, called_at
  llm_calls        id, plan_run_id, model, prompt_version, tokens in/out, cost_inr, latency_ms
  preferences      operator, key, value, confirmed, updated_at              (ADR-0014)
  backtest_runs    id, config, status, results_ref, created_at

Write the cost-per-day / cost-per-operator SQL queries alongside as practice.
Migrations: Alembic, under db/migrations/.
"""

from __future__ import annotations
