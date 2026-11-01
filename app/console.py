"""Operator console (Streamlit). Phase 7.

A thin client of the API (never imports blockwise components directly), so what you demo is
what runs in production.

Screens/sections to build:
  1. Date picker + "Create plan" (POST /plans) with status polling
  2. Net-demand fan chart (P10/P50/P90) and DAM/RTM price forecasts for the 96 blocks
  3. Schedule: stacked area of PPA / DAM / RTM / BESS dispatch per block, and BESS SoC
  4. Explanation panel: streamed text from /plans/{id}/explanation, with clause citations
     and a "show tool call" link for every number (provenance)
  5. Critic report: constraint checks passed/failed
  6. Approve / Reject (+ reason) -> POST /plans/{id}/decision; shows the audit entry
  7. What-if box -> POST /plans/{id}/what-if
  8. Demo-mode banner when serving a frozen snapshot day (public demo)

Public demo must run on data/snapshots/ with the LLM either cached or budget-capped.
"""

from __future__ import annotations


def main() -> None:
    raise NotImplementedError


if __name__ == "__main__":
    main()
