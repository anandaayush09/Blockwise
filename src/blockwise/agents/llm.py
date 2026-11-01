"""The LLM client interface the rest of the agent code depends on.

Owns: a small Protocol (messages + tool schemas in, text and/or tool calls out) so the raw
loop (loop.py), the LangGraph version (graph.py) and the tests' FakeLLMClient are
interchangeable, and so the provider/model (ADR-0010) can change in one place.

Must NOT: leak provider SDK types into the rest of the code, or log full prompts at INFO.

Notes for the real implementation (check the current provider docs, do not rely on memory):
  * Default model comes from Settings.llm_model (claude-opus-5-5 by default).
  * Current Claude models may reject forced tool choice (tool_choice "any"/"tool"). Use
    automatic tool choice and steer with the prompt; use strict tool schemas so arguments
    are valid. If you need guaranteed JSON back, use structured outputs instead of a forced tool call.
  * Check the response stop reason before reading content (refusals, max-tokens cut-offs).
  * Record token usage for every call (observability.record_llm_cost).
  * Stream long answers; set a sensible max_tokens.
"""

from __future__ import annotations

from typing import Any, Protocol

from pydantic import BaseModel


class ToolSpec(BaseModel):
    name: str
    description: str
    input_schema: dict[str, Any]  # JSON schema generated from the tool's pydantic input model


class ToolCall(BaseModel):
    call_id: str
    name: str
    arguments: dict[str, Any]


class LlmMessage(BaseModel):
    role: str  # "user" | "assistant" | "tool"
    content: str | None = None
    tool_calls: list[ToolCall] = []
    tool_call_id: str | None = None  # for role == "tool"


class LlmResponse(BaseModel):
    text: str | None
    tool_calls: list[ToolCall]
    stop_reason: str
    input_tokens: int
    output_tokens: int


class LlmClient(Protocol):
    async def complete(
        self,
        system: str,
        messages: list[LlmMessage],
        tools: list[ToolSpec],
        max_tokens: int,
    ) -> LlmResponse: ...
