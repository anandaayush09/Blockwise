# Architecture

_Skeleton. You own this document: rewrite it in your own words as the design firms up._

## Components

| Component | Module | Owns | Must NOT |
|---|---|---|---|
| Time-block calendar | `timeblocks.py` | date <-> block 1..96 in IST | handle any other timezone logic elsewhere |
| Data store | `data/store.py` | as-of reads of every series | return data published after the as-of time |
| Net-demand forecast | `forecasting/net_demand.py` | P10/P50/P90 x 96 | use actuals from the target day |
| Price forecast | `forecasting/prices.py` | DAM and RTM x 96 | pretend to be exact |
| DSM penalty | `regulation/penalty.py` | ₹ penalty for a proposed deviation | call an LLM |
| Regulation retriever | `regulation/retriever.py` | clause lookup with citations | compute penalties |
| Optimiser | `optimiser/*` | PPA/DAM/RTM/BESS split | be reached by an LLM except through its tool wrapper |
| Constraint checker | `optimiser/checks.py` | independent validation of a schedule | share code paths with the model it checks |
| Agents | `agents/*` | choosing tools, explaining, citing | produce any number not in a tool result |
| API / worker | `api/*`, `worker/*` | serving, jobs, audit | contain domain logic |

## The contract: the LLM never does arithmetic

See [ADR-0001](decisions/0001-llm-never-does-arithmetic.md). Concretely:
1. Every quantity in an explanation (MW, MWh, ₹, %) must be copied from a tool result.
2. `agents/guardrails.py` checks that mechanically; an ungrounded number fails the run.
3. Tools return structured, unit-labelled values (Pydantic models in `schemas.py`).

## Data flow (daily plan)

1. D-1 early: ingest latest actuals and weather forecasts (as-of time recorded).
2. Forecast net demand and prices for D (96 blocks).
3. Orchestrator calls tools: penalty quotes for candidate deviations, optimiser for the split.
4. Constraint checker validates the schedule; critic agent reads the report and explains it.
5. Operator approves or rejects (recorded with who/when/why); only then is the mock "submit bids" step enabled.
6. Intraday: re-forecast, re-optimise the RTM/BESS part, repeat the check and approval.

## Optimiser formulation (YOU write this section before coding Phase 6)

For each block `t = 1..96` define your decision variables, parameters and constraints. Prompts to answer:
- Variables: PPA dispatch per contract, DAM purchase, RTM purchase, BESS charge/discharge/SoC. Which are continuous, which need binaries (and why)?
- Balance: supply = net-demand forecast (which quantile? P50 or scenario set?) + charging - discharging.
- PPA limits (min/max/ramp?), market liquidity limits, BESS power/energy/efficiency limits.
- Objective: PPA cost + DAM cost + RTM cost + expected DSM cost + BESS cost. How does expected DSM enter (scenarios, piecewise-linear)?
- Is the DSM function convex? If not, what does that force in the model? (ADR-0005)

```
TODO: write equations here
```

## What the oracle is

Same model solved with the true net demand and true prices (perfect foresight). It is the upper bound on savings; "% of oracle gap captured" is the fairest way to report improvement.
