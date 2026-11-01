# Assumptions and leakage checklist

Each assumption states how it could bias the result. Add the real ones as you make them.

| # | Assumption | Direction of bias | How to test or bound it |
|---|---|---|---|
| A1 | DISCOM is a price-taker in DAM/RTM | overstates savings | sensitivity: add price impact per MW |
| A2 | State-level demand series is a proxy for the DISCOM | unknown | document the scaling; check seasonality shape against any DISCOM data you have |
| A3 | _TODO_ | | |

## Leakage checklist (tick before trusting any ₹ number)
- [ ] Every feature for day D is available before the day-ahead decision time on D-1 (as-of read, not "latest").
- [ ] Weather features use forecasts as issued, not observed weather.
- [ ] Price and demand history use first-published values, or you document revisions.
- [ ] Model hyperparameters and thresholds were chosen using data before `train_end` only.
- [ ] Baseline and BlockWise see the same information set.
- [ ] DSM rules applied per day match the rules in force that day.
- [ ] Cap/clipping on prices applied the same way in forecast, optimiser and settlement.
- [ ] The oracle uses the same model and constraints, differing only in foresight.
