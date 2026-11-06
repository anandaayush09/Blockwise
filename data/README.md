# Data

Raw and processed data are gitignored. Only READMEs are committed. Fill the inventory in Phase 0, before designing anything.

| Series | Granularity | Source (URL) | Licence / terms | Period available | Gaps or revisions | Local path |
|---|---|---|---|---|---|---|
| IEX DAM MCP | 15 minutes | | | | | data/raw/ |
| IEX RTM price | 15 minutes | | | | | data/raw/ |
| Demand (state/SLDC proxy) |  | | | | | data/raw/ |
| Solar generation | _TODO_ | | | | | data/raw/ |
| Wind generation | _TODO_ | | | | | data/raw/ |
| Weather (forecast as issued, and observed) | _TODO_ | | | | | data/raw/ |
| DSM regulation text(s) | n/a | | | | amendments | data/regulations/ |

Folders: `raw/` as downloaded; `interim/` cleaned; `processed/` features and forecasts; `snapshots/` the frozen days used by the public demo; `regulations/` source PDFs (check redistribution terms before committing any).
