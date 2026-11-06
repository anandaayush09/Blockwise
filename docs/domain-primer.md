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

Option availaible for Single and Block Bids - 

Single bid - Individual 15-min slots and Multiple price-quantity pairs

Block bids are for continious blocks(or Multiple consecutive slots) - same price
Participants can sale / purchase power for delivery(T+1 Day) 
Bidding session are active from : 1000 hrs - 1200 hrs
By 1400 hrs, NLDC reverts with actual transmission corridor availability during all 15 minute time blocks across congestion prone bid areas

- **RTM (real-time market):** closer-to-delivery trading with shorter lead times. VERIFY session length, lead time, and whether historic data is block-level.

Real Time Market is physical delivery of electricity 1 hour after closure of market

The Real Time Market (RTM) is a market segment with physical delivery of electricity 1 hour after closure of market. The market features a new auction session every half an hour with electricity to be delivered after 4 time-blocks or an hour after gate closure of the auction. There are 48 RTM sessions run by Power exchanges in a day. The price and quantum of electricity trading is determined through a double-sided closed auction bidding process just like I-DAM.Historic data is block level

https://www.iexindia.com/products/real-time-market

- **Price caps:** the exchange imposes caps on bid prices. VERIFY current values; they clip your price distribution.

Floor price - Rs 0/MWh
Ceiling price - Rs 10/kWh
A cap limits the permitted auction price; it does not guarantee that a DISCOM's demand will be cleared

https://www.cercind.gov.in/2023/orders/5-SM-2023.pdf

- **Price-taker assumption:** a single DISCOM's bids are assumed not to move the clearing price. State this in `assumptions.md` and note it biases savings upward.

Aaumption was made regarding the price taker

## Net demand
- Net demand = load - solar - wind (what remains for conventional + market supply). More RE means more variance in the residual, hence larger forecast error and larger DSM exposure.
- Behind-the-meter solar may be invisible in the data you can get. VERIFY what your demand series includes.

## DSM (Deviation Settlement Mechanism)
- Deviation = actual drawal - scheduled drawal, per block. Positive = over-drawal. Penalty bands and rates depend on the size and direction of the deviation and a reference rate.
- **Everything numeric about DSM is VERIFY:** which regulation and amendment, effective dates, band thresholds, multipliers, reference rate definition, caps, whether the basis is % of schedule, % of capacity or absolute MW.
- Rules change over time. The backtest must apply the rules in force on each day (see `configs/dsm_rules.yaml`).

For your IEX–DISCOM electricity procurement optimisation project, the applicable central regulatory framework is the Central Electricity Regulatory Commission (Deviation Settlement Mechanism and Related Matters) Regulations

Regulation 6(3): How buyer deviations are measured.
Regulation 7: How the Normal Rate (NR) for DSM settlement is calculated.
Regulation 8(7): The deviation-volume bands and applicable charge multipliers.

Deviation is measured againts scheduled draeal not installed generation capacity

Deviation(%) = (Actual - Schedule/Actual)*100

Settlement rate depends on two variable
How much the discom has deviated from it scheduled(the volume band)
what is the grid frequency during that particular timeblock



## BESS (battery)
- Charge when prices are low, discharge when high or to cover forecast gaps. Constraints: power limit, energy capacity, round-trip efficiency, state-of-charge limits, no simultaneous charge and discharge. Cycling cost is a modelling choice (ADR-0005).

## Why savings can be fake
- Look-ahead (using information not available at decision time).
- Tuning on the test window.
- A baseline that is too weak.
- Ignoring the penalty regime in force that day.
- Price-taker assumption at scale.
