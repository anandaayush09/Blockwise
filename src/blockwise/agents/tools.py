"""Tool layer: the only way an agent touches numbers.

Owns: a ``BaseTool`` abstract class (name, description, pydantic input model, pydantic output
model, ``run``), concrete tools wrapping the deterministic components, and a registry that
produces ToolSpec lists for the LLM and executes calls with logging.

Tool descriptions are prompts. Write them like API docs for a careful colleague: what it
returns, units (MW vs MWh, INR vs INR crore), when NOT to use it. Test them with ambiguous
questions designed to make an agent pick the wrong tool (evals/datasets/tool_routing.jsonl).

Must NOT: let a tool do anything an agent should not decide alone. Tools that change state
(submit bids) are not registered here; they sit behind operator approval in the API.
Must NOT: return free text for numeric results. Return the typed models from schemas.py.

Planned tools: get_net_demand_forecast, get_price_forecast, penalty_quote, run_optimiser,
check_schedule, search_regulation, get_operator_preferences.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from pydantic import BaseModel

from blockwise.agents.llm import ToolSpec


class BaseTool(ABC):
    name: str
    description: str
    input_model: type[BaseModel]
    output_model: type[BaseModel]

    @abstractmethod
    async def run(self, inputs: BaseModel) -> BaseModel:
        """Execute deterministically and return the typed output."""

    def spec(self) -> ToolSpec:
        """Build the ToolSpec the LLM sees, from ``input_model``'s JSON schema."""
        raise NotImplementedError


class ToolRegistry:
    def __init__(self, tools: list[BaseTool]) -> None:
        raise NotImplementedError

    def specs(self) -> list[ToolSpec]:
        raise NotImplementedError

    async def execute(self, plan_run_id: str, name: str, arguments: dict) -> BaseModel:
        """Validate arguments against the tool's input model, run, record a ToolCallRecord, return the output.

        Invalid arguments or tool errors must come back to the model as an error result
        (so it can retry), not crash the run, and not be hidden from the log.
        """
        raise NotImplementedError


def default_registry() -> ToolRegistry:
    """Wire up the concrete tools."""
    raise NotImplementedError
