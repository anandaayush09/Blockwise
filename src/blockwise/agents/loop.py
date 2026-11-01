"""A plain-Python ReAct-style tool-use loop. Build this BEFORE graph.py.

Owns: while not done: call the LLM with messages + tool specs; if it asks for tools, execute
them via the registry and append results; stop on a final answer, a step limit, a token/cost
budget, or an error.

Why first: Anthropic's own guidance is to start with direct API calls and add a framework
only once you understand what it abstracts. Having written this loop, you can say exactly
what LangGraph gives you (state, checkpoints, interrupts) in ADR-0006.

Must NOT: loop without a hard step limit and a cost budget. Must NOT: swallow tool errors.
Must NOT: let the final text through unless guardrails.check_grounding passes.
"""

from __future__ import annotations

from pydantic import BaseModel

from blockwise.agents.llm import LlmClient, LlmMessage
from blockwise.agents.tools import ToolRegistry


class LoopResult(BaseModel):
    final_text: str | None
    messages: list[LlmMessage]
    steps: int
    stopped_because: str  # "final_answer" | "step_limit" | "budget" | "error"


async def run_loop(
    client: LlmClient,
    registry: ToolRegistry,
    system: str,
    user_message: str,
    plan_run_id: str,
    max_steps: int = 8,
    budget_inr: float | None = None,
) -> LoopResult:
    raise NotImplementedError
