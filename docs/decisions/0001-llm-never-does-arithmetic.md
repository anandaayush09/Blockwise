# ADR-0001: The LLM never does arithmetic

- **Status:** decided (worked example; rewrite the reasoning in your own words)
- **Phase:** 0

## Context
Procurement decisions involve money. A plausible-sounding but wrong number (a penalty, a total cost, a schedule total) in an operator-facing explanation is worse than no explanation. LLMs are unreliable at multi-step arithmetic and cannot show provenance for a number they "computed".

## Options considered
1. **LLM computes and explains.** Simple; unreliable and unauditable.
2. **LLM calls tools; tools compute; LLM explains and cites.** More plumbing; numbers are reproducible and testable.
3. **No LLM.** Fully deterministic; loses plain-language explanation, regulation Q&A and flexible what-if handling.

## Decision
Option 2. Forecasts, penalties, optimisation and constraint checks are deterministic tools. The LLM decides which to call and in what order, and writes the explanation using only values returned by tools.

## Why
- Reproducibility: the same inputs give the same ₹ number, and the backtest can use the same code path.
- Auditability: every number in an explanation maps to a recorded tool call.
- Testability: tools get unit tests; the LLM layer gets grounding checks.

## Consequences
- Need a numeric-grounding guardrail (`agents/guardrails.py`): any number in prose that is not in a tool result fails the run.
- Tool outputs must carry units; tool descriptions must be unambiguous (MW vs MWh, ₹ vs ₹ crore).
- The LLM cannot "fix" a wrong tool output; errors surface as errors.
- The critic and the optimiser use independent code (`optimiser/checks.py`), so a bug has to appear twice to slip through.

## What would make me revisit this
A task where the LLM's judgement, not arithmetic, is the product (e.g. ranking qualitative risks) - and even then, numbers still come from tools.

## 60-second defence
_TODO: say it in your words._
