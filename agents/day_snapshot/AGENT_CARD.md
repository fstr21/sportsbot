# Agent Card — Day Snapshot (LOCKED)

<!-- Do not add provider or performance assumptions. Keep this card generic. -->

## Purpose (what this agent does)
For a single **date** and **league**, produce a simple daily snapshot:
- schedule for that date,
- odds for that date,
- recent context for teams (and players only if the league allows),
then write human-readable artifacts and a brief summary.

## Scope Guardrails (policy, not tech)
- Leagues supported: **NFL**, **NCAAF**
- Snapshot tag: **MORNING** by default (FINAL may be used later)
- Player content: **NFL may include players**; **NCAAF never includes players**
- No database, no bots, no provider-specific details in this file

## Inputs (required)
- `league` ∈ { NFL, NCAAF }
- `date` in `YYYY-MM-DD`
- Optional: `tag` ∈ { MORNING, FINAL } (default MORNING)

## Outputs (artifacts folder)
Write to: `artifacts/<league>/<YYYY-MM-DD>_<TAG>/`
- `events.json` — schedule entries, each with an attached **odds list** (simple, consistent)
- `team_stats.json` — recent team context
- `summary.md` — short human summary (counts + where files were written)
- Optional: `meta.json` — minimal run info (timestamps, durations)

Each artifact must include:
- a run timestamp,
- the snapshot tag.

## Required Behaviors
- Validate inputs; if invalid, return `bad_params`.
- Join data using simple, human-obvious matching (home/away names + kickoff time).
- Be **idempotent**: re-running the same league/date/tag must not create duplicates.
- Summarize clearly (counts and artifact path).

## Errors (exact labels to use)
`bad_params`, `upstream_timeout`, `mcp_error`, `rate_limited`, `unknown_task`.

## Acceptance (must pass)
- Prompts/accepts `YYYY-MM-DD`; rejects other formats.
- Writes `events.json`, `team_stats.json`, `summary.md` in the path above.
- Summary includes: total games, games with odds attached, teams with context.
- Re-run with same inputs is clean and consistent.
- **NFL**: may include player context later; **NCAAF**: never includes player items.

## Must-Reads before any change
- Root `AGENTS.md`
- This `AGENT_CARD.md`
- `SPEC.md`, `CONTRACTS.md`, `TESTPLAN.md` in this folder

## Out of Scope (do not add here)
- Provider/API specifics
- Performance targets or quotas
- Schema names or validator details
- Mapping guarantees or DB details
