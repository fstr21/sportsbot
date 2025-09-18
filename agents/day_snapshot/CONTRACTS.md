# CONTRACTS — Day Snapshot Agent (LOCKED)

> Conceptual contracts only. No provider schemas here.

## AgentTask (input)
- `type`: `"ingest.day_snapshot"`
- `params`:
  - `league`: `"NFL"` | `"NCAAF"`
  - `date`: `"MM/DD/YYYY"`

## AgentResponse (output)
- `ok`: `true|false`
- `summary`: short human text (counts + artifact path)
- `artifacts`: list of relative paths written (should include `events.json` and `summary.md`)
- `error`: one of:
  - `bad_params`, `upstream_timeout`, `mcp_error`, `rate_limited`, `unknown_task`

## Snapshot contents (conceptual expectations)
- **Schedule**: list of games for the date (displayed in **ET**).
- **Odds**: per game, a **consistent list** of odds entries attached at join time.
- **Team context**: minimal recent form per team.
- **Player context**: **NFL-only (later)**; **NCAAF never includes players**.
- **Join**: associate odds/context to schedule entries by (home, away, kickoff time; tolerant match).
- **Mapping capture**: record enough names/identifiers in artifacts for future mapping (no DB now).

## Invariants
- Input `date` must be `MM/DD/YYYY`; outputs must display times in **ET**.
- **No placeholder data**; missing required slices → explicit error.
- Re-run for the same league/date is **idempotent**.
- Respect **10 requests/min** to the odds source.

## Errors (exact labels)
- `bad_params` — input missing/invalid (e.g., wrong date format)
- `upstream_timeout` — a source fetch exceeded time budget
- `mcp_error` — orchestrated fetch returned an error envelope
- `rate_limited` — upstream rate cap hit (e.g., 10/min)
- `unknown_task` — unrecognized task type

## Observability (minimal)
- Include a run timestamp in artifacts.
- Optional `meta.json` with durations and simple pointers.
