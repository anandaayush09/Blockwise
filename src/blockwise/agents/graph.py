"""LangGraph version of the orchestration. Build AFTER loop.py.

Owns: the same behaviour as the raw loop expressed as a graph: typed state, nodes (plan,
forecast, optimise, check, critique, await_approval), conditional edges (re-solve if the
checker fails), a checkpointer, and an interrupt before any irreversible step.

Must NOT: contain logic that exists only here. The tools, guardrails and prompts are shared
with loop.py so you can compare the two honestly.

DECISION(ADR-0006): keep the graph, keep the raw loop, or mix. Write down what the graph
actually bought you (resumable runs? human-in-the-loop? visualisation?) and what it cost.
Requires the "agents" extra.
"""

from __future__ import annotations


def build_graph(registry, client):
    """Compile the graph. Return an object with an async ``run(state)``."""
    raise NotImplementedError
