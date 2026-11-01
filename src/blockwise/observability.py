"""Logging, timing, tracing hooks and cost accounting.

Owns: structured logging setup, a timing decorator, a run-context manager that attaches a
plan_run_id to every log line / tool call / LLM call, and per-run cost totals.

Must NOT: swallow exceptions or log secrets, API keys, or full prompts at INFO level.

DECISION(ADR-0013): tracing backend (LangSmith vs OpenTelemetry vs DIY logs).
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from typing import Any, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def configure_logging(level: str = "INFO") -> None:
    """Set up structlog with JSON output so container logs are queryable."""
    raise NotImplementedError


def timed(name: str) -> Callable[[F], F]:
    """Decorator: log the wrapped function's duration in ms under ``name``. Must work on async functions too."""
    raise NotImplementedError


@contextmanager
def run_context(plan_run_id: str) -> Iterator[None]:
    """Bind ``plan_run_id`` to all logs, tool-call records and LLM-call records inside the block."""
    raise NotImplementedError
    yield  # pragma: no cover


def record_llm_cost(plan_run_id: str, input_tokens: int, output_tokens: int, model: str) -> float:
    """Convert token usage to INR using the pricing table you maintain. Returns the INR cost."""
    raise NotImplementedError
