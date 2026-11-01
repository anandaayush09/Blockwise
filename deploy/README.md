# Deploy

Hosting is ADR-0009. Notes to settle before Phase 10:

- **Demo mode:** the public demo serves a frozen snapshot day from `data/snapshots/`, with the LLM either replaying cached recorded runs or capped by a small budget. State this in the README; never let an anonymous visitor spend your API key.
- **Environments:** staging (auto on merge to `main`), production (manual approval). Same SHA-tagged image.
- **Free-tier limits** (cold starts, memory, no persistent disk, workers): check your platform against what Postgres, Redis, the worker and the console need. You may need to run the worker inline in demo mode.
- **Secrets:** platform secret manager / GitHub environment secrets. Not in the repo, not in image layers.
- **Rollback:** see `docs/runbook.md`; rehearse and time it.
