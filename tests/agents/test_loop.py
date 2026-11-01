"""Phase 9. Tests the raw loop's control flow with a scripted fake model. No real API."""

import pytest
from pydantic import BaseModel

from blockwise.agents.loop import run_loop
from blockwise.agents.tools import BaseTool, ToolRegistry

pytestmark = pytest.mark.xfail(raises=NotImplementedError, reason="Phase 9 not implemented")


class _In(BaseModel):
    value: float


class _Out(BaseModel):
    doubled: float


class DoubleTool(BaseTool):
    name = "double"
    description = "Return twice the input value (unit-free test tool)."
    input_model = _In
    output_model = _Out

    async def run(self, inputs):
        return _Out(doubled=inputs.value * 2)


class BrokenTool(DoubleTool):
    name = "broken"

    async def run(self, inputs):
        raise RuntimeError("boom")


@pytest.mark.asyncio
async def test_loop_runs_tool_then_returns_final_answer(fake_llm, responses):
    client = fake_llm(
        [responses["tool_call"]("double", value=21.0), responses["final"]("done: 42")]
    )
    result = await run_loop(client, ToolRegistry([DoubleTool()]), "sys", "go", plan_run_id="t")
    assert result.stopped_because == "final_answer"
    assert result.final_text == "done: 42"
    assert result.steps == 2


@pytest.mark.asyncio
async def test_loop_stops_at_step_limit_when_model_never_finishes(fake_llm, responses):
    client = fake_llm([responses["tool_call"]("double", value=1.0)] * 20)
    result = await run_loop(
        client, ToolRegistry([DoubleTool()]), "sys", "go", plan_run_id="t", max_steps=3
    )
    assert result.stopped_because == "step_limit"
    assert result.steps == 3


@pytest.mark.asyncio
async def test_tool_error_is_returned_to_model_not_raised(fake_llm, responses):
    client = fake_llm(
        [responses["tool_call"]("broken", value=1.0), responses["final"]("could not compute")]
    )
    result = await run_loop(client, ToolRegistry([BrokenTool()]), "sys", "go", plan_run_id="t")
    assert result.stopped_because == "final_answer"
    assert any(m.role == "tool" and "boom" in (m.content or "") for m in result.messages)


@pytest.mark.asyncio
async def test_unknown_tool_name_is_an_error_result_not_a_crash(fake_llm, responses):
    client = fake_llm([responses["tool_call"]("does_not_exist"), responses["final"]("ok")])
    result = await run_loop(client, ToolRegistry([DoubleTool()]), "sys", "go", plan_run_id="t")
    assert result.stopped_because == "final_answer"
