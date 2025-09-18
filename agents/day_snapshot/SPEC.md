# SPEC — Day Snapshot Agent (LOCKED)

> Source-agnostic orchestration spec. No provider or DB details here.

## Purpose
Run a single-day snapshot for one league.

### High-level Steps
1) **Validate** input (`league`, `date`).
2) **Frame** the day using the input date; convert all displayed times to **ET**.
3) **Fetch** three slices for the date:
   - schedule
   - odds
   - recent team context (NFL may later add player context; NCAAF never includes players)
4) **Join** these slices at a simple, human-obvious level:
   - by matchup (home vs away) and kickoff time (tolerant match)
5) **Write artifacts** (machine-readable JSON + readable `.md` by matchup).
6) **Verify acceptance** and **summarize**.

## Non-Goals
- No database.
- No provider/API specifics in this file.
- No advanced mapping or analytics; only capture names/identifiers needed for future mapping.

## Inputs & Policy
- `league`: `NFL` or `NCAAF`
- `date`: **`MM/DD/YYYY`** (reject anything else)
- **No snapshot tags** at this stage.
- Display timezone is **ET** for all outputs.

## Outputs
Write to: `artifacts/<league>/<MM-DD-YYYY>/`
- `events.json` — schedule items with an attached **odds list** (uniform list structure)
- `team_stats.json` — recent team context
- `summary.md` — counts + short notes **by matchup**
- `meta.json` (optional) — minimal run metadata (timestamps, durations)

## Required Behaviors
- Input validation; bad input → `bad_params`.
- **No placeholders.** If any required slice (schedule OR odds OR team context) is missing, fail clearly.
- **Idempotency**: re-running the same league/date must not duplicate content.
- **Rate-limit discipline**: respect a practical **10 requests/min** cap to the odds source.
- Clean, by-matchup presentation in `summary.md`.

## Error labels
Use exactly: `bad_params`, `upstream_timeout`, `mcp_error`, `rate_limited`, `unknown_task`.

## Success Criteria
- All TESTPLAN acceptance checks pass.
- Human can open `summary.md` and understand what was produced and where.
