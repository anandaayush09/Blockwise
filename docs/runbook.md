# Runbook

_Write this before you need it (Phase 10). Time every rollback rehearsal._

## Environments
| Env | Deploys | Approval |
|---|---|---|
| local | `docker compose up` | none |
| staging | automatically on merge to `main` | none |
| production | same image (tagged with commit SHA) | manual approval (GitHub Environment reviewers) |

Never deploy `:latest`. Promote the identical SHA-tagged image through environments.

## Required configuration
All variables are listed in `.env.example`. Real values live in the platform's secret manager / GitHub Actions secrets, never in the repo or image layers. CI deploy tokens: least privilege (deploy only).

## Deploy
1. Merge to `main`; CI runs lint, tests, pip-audit, build.
2. CD pushes `ghcr.io/<you>/blockwise:<sha>` and deploys staging.
3. Smoke test (below). If green, approve production.

## Health and smoke tests
- `/health` must check Postgres, Redis and model artefacts, not only "process alive".
- Smoke test after each deploy: _TODO list 2-3 real endpoints_ (e.g. forecast for a frozen day, penalty quote for a known case, plan run on the frozen snapshot).

## Rollback
1. Identify the last good SHA.
2. Redeploy that image tag on the platform.
3. Verify with the smoke test.
4. _TODO: record the time it took in your last rehearsal._

## Debugging with no debugger
- Logs: `docker logs -f <container>`; platform log viewer; CI job logs.
- Traces: _TODO tool per ADR-0013_ - find the failing tool call and its inputs.
- Errors: Sentry.
- Per-run record in Postgres: tool calls, LLM calls, cost, approval.

## Common incidents
| Symptom | First checks |
|---|---|
| Plan not ready before the deadline | worker queue, data feed freshness, solver time limit |
| Explanation fails guardrail | which number was ungrounded; which tool result it should have come from |
| Cost spike | cost-per-run query; prompt size; retry loops |
