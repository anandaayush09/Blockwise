"""Eval runner.

Owns: loading a suite's dataset, running the system under test, scoring, recording
cost/latency/versions, writing the result file, and returning a non-zero exit code if
thresholds are missed.

Must NOT: run LLM suites without a budget cap, or tune on the cases it reports.
Thresholds live in a config file you create (evals/thresholds.yaml); choose them from a
baseline run, not from hope.
"""

from __future__ import annotations

import argparse

SUITES = [
    "deterministic",
    "regulation_qa",
    "retrieval_probes",
    "critic_injected",
    "tool_routing",
    "grounding",
    "injection",
]


def run_suite(name: str, budget_inr: float | None) -> dict:
    """Run one suite and return its result dict (metrics, cost, per-case outcomes)."""
    raise NotImplementedError


def main() -> int:
    parser = argparse.ArgumentParser(description="Run BlockWise evals")
    parser.add_argument("--suite", choices=SUITES, required=True)
    parser.add_argument("--budget-inr", type=float, default=None)
    args = parser.parse_args()
    run_suite(args.suite, args.budget_inr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
