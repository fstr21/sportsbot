# CONTRACTS — Day Snapshot Agent

## AgentTask (input) — conceptual
- `type`: "ingest.day_snapshot"
- `params`:
  - `league`: "NFL" | "NCAAF"
  - `date`: "YYYY-MM-DD"
  - `tag`: "MORNING" | "FINAL" (default "MORNING")

## AgentResponse (output) — conceptual
- `ok`: boolean
- `summary`: short human text (counts + pointers)
- `artifacts`: list of relative paths written
- `error`: one of (if `ok=false`)
  - `bad_params`, `upstream_timeout`, `mcp_error`, `rate_limited`, `unknown_task`

## Snapshot Contents (conceptual)
- **Schedule**: list of games w/ home, away, kickoff time.
- **Odds**: per game, a simple list with the common categories (e.g., moneyline/spread/total) represented consistently.
- **Context**:
  - Teams: minimal recent form for both leagues.
  - Players: minimal recent form **NFL-only** (not present for NCAAF).
- **Join**: associate odds/context to schedule entries by (home, away, kickoff time, tolerant match).
- **Mapping capture**: record enough names/identifiers in artifacts for future team/player mapping (no DB now).

## Invariants
- Inputs validated before any work.
- Artifacts write to the league/date/tag path.
- Re-run produces an idempotent result (no duplicates).
- Summary reports: total scheduled games, games with odds attached, teams with context, basic join coverage (%).

## Errors (exact labels)
- `bad_params`: input missing/invalid (e.g., date format wrong)
- `upstream_timeout`: source fetch exceeded time budget
- `mcp_error`: orchestrated fetch returned an envelope error
- `rate_limited`: upstream says slow down
- `unknown_task`: task type not recognized by router

## Observability (lightweight)
- Add a run timestamp into artifacts.
- Keep a minimal `meta` file if helpful (e.g., durations).
