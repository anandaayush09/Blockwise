"""Command-line entry point: `blockwise ...`.

Owns: thin commands that call the same functions the API and worker call.
Must NOT: contain domain logic. If a command needs logic, it belongs in a component.

Planned commands (add as phases land):
    blockwise ingest <series> --start --end        (Phase 1)
    blockwise penalty --date --deviations-file      (Phase 2)
    blockwise backtest --config configs/backtest.yaml   (Phase 3)
    blockwise plan --date                           (Phase 6+)
    blockwise evals --suite ...                     (Phase 8+)
"""

from __future__ import annotations

import typer

app = typer.Typer(help="BlockWise power procurement copilot", no_args_is_help=True)


@app.command()
def ingest(series: str, start: str, end: str) -> None:
    """Download and validate a data series into the store."""
    raise NotImplementedError


@app.command()
def backtest(config: str = "configs/backtest.yaml") -> None:
    """Run the backtest and print the ₹ comparison table."""
    raise NotImplementedError
