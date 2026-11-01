"""Scripted fake LLM for agent tests: tests YOUR routing and parsing logic, not the model."""

from __future__ import annotations

import pytest

from blockwise.agents.llm import LlmResponse, ToolCall


class FakeLLMClient:
    """Returns pre-scripted responses in order. Records what it was sent."""

    def __init__(self, script: list[LlmResponse]) -> None:
        self._script = list(script)
        self.calls: list[dict] = []

    async def complete(self, system, messages, tools, max_tokens) -> LlmResponse:
        self.calls.append({"system": system, "messages": messages, "tools": tools})
        if not self._script:
            raise AssertionError(
                "FakeLLMClient script exhausted: the loop made an unexpected extra call"
            )
        return self._script.pop(0)


def tool_call_response(name: str, **arguments) -> LlmResponse:
    return LlmResponse(
        text=None,
        tool_calls=[ToolCall(call_id="c1", name=name, arguments=arguments)],
        stop_reason="tool_use",
        input_tokens=10,
        output_tokens=5,
    )


def final_response(text: str) -> LlmResponse:
    return LlmResponse(
        text=text, tool_calls=[], stop_reason="end_turn", input_tokens=10, output_tokens=5
    )


@pytest.fixture
def fake_llm():
    """Usage: client = fake_llm([tool_call_response(...), final_response(...)])"""
    return FakeLLMClient


@pytest.fixture
def responses():
    return {"tool_call": tool_call_response, "final": final_response}
