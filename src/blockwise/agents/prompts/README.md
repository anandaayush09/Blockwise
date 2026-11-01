# Prompts

One file per prompt: `market_agent.md`, `regulation_agent.md`, `critic_agent.md`, `orchestrator_whatif.md`. Each starts with a version line (`version: 1`), which is logged with every LLM call (`LlmCallRecord.prompt_version`) and is part of any cache key.

Rules for writing them:
- State the one rule: only use numbers returned by tools; never calculate.
- State units and the sign convention.
- Say what to do when a tool errors or evidence is missing (say so; do not guess).
- Change prompts only with an eval run before/after (`evals/`); record the result in the commit message.
