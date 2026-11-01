# Domain primer

Written from general knowledge to get you started. **Anything marked VERIFY must be confirmed against the regulation text, exchange rules or your data source before you rely on it.** Resolving these is Phase 0, and you should be able to cite where each answer came from.

## Time blocks
- A day has 96 blocks of 15 minutes. Block 1 = 00:00-00:15 IST, block 96 = 23:45-24:00 IST. India has no daylight saving, so a day is always 96 blocks.
- Store timestamps in UTC if you like, but convert through `timeblocks.py` only. VERIFY that every series you use is block-aligned the same way (start-of-block vs end-of-block labels differ between sources).

## Energy vs power
- MW is power in a block. MWh in one block = MW x 0.25. Mixing these up is the classic bug. Price is ₹/MWh; a block's cost = MW x 0.25 x price.

## Markets
- **PPA:** long-term bilateral contract. Cheaper, mostly fixed commitment, with minimum take / capacity limits. VERIFY terms you assume in `configs/discom.yaml`.
- **DAM (day-ahead market):** bids for day D are placed on D-1; one clearing price (MCP) per block. VERIFY gate-closure time and bid rules.
- **RTM (real-time market):** closer-to-delivery trading with shorter lead times. VERIFY session length, lead time, and whether historic data is block-level.
- **Price caps:** the exchange imposes caps on bid prices. VERIFY current values; they clip your price distribution.
- **Price-taker assumption:** a single DISCOM's bids are assumed not to move the clearing price. State this in `assumptions.md` and note it biases savings upward.

## Net demand
- Net demand = load - solar - wind (what remains for conventional + market supply). More RE means more variance in the residual, hence larger forecast error and larger DSM exposure.
- Behind-the-meter solar may be invisible in the data you can get. VERIFY what your demand series includes.

## DSM (Deviation Settlement Mechanism)
- Deviation = actual drawal - scheduled drawal, per block. Positive = over-drawal. Penalty bands and rates depend on the size and direction of the deviation and a reference rate.
- **Everything numeric about DSM is VERIFY:** which regulation and amendment, effective dates, band thresholds, multipliers, reference rate definition, caps, whether the basis is % of schedule, % of capacity or absolute MW.
- Rules change over time. The backtest must apply the rules in force on each day (see `configs/dsm_rules.yaml`).

## BESS (battery)
- Charge when prices are low, discharge when high or to cover forecast gaps. Constraints: power limit, energy capacity, round-trip efficiency, state-of-charge limits, no simultaneous charge and discharge. Cycling cost is a modelling choice (ADR-0005).

## Why savings can be fake
- Look-ahead (using information not available at decision time).
- Tuning on the test window.
- A baseline that is too weak.
- Ignoring the penalty regime in force that day.
- Price-taker assumption at scale.
