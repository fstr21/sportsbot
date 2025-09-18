# SPEC — Day Snapshot Agent

## Purpose
Run a single-day snapshot for one league. Steps:
1) Validate input (league/date/tag).
2) Build the day window (date + tag context).
3) Fetch:
   - schedule
   - odds
   - recent context (teams for both leagues; players for NFL only)
4) Join the three at a simple, human-obvious level:
   - by matchup (home vs away) and kickoff time (lenient tolerance)
5) Write artifacts (JSON + a short Markdown summary).
6) Verify acceptance and return a concise result.

## Non-Goals
- No DB.
- No provider/API specifics here.
- No advanced mapping or analytics (capture names/ids for future work only).

## Inputs & Policy
- `league`: NFL or NCAAF
- `date`: YYYY-MM-DD (reject anything else)
- `tag`: MORNING|FINAL (default MORNING)
- Policy per league:
  - **NFL**: schedule + odds for teams AND players; team/player context allowed.
  - **NCAAF**: schedule + odds for teams ONLY; team context; no player odds/stats.

## Outputs
- `artifacts/<league>/<YYYY-MM-DD>_<TAG>/`
  - `events.json` — includes schedule entries with an attached odds list using a simple, consistent structure
  - `team_stats.json` — recent form/context at a shallow, comparable level
  - `summary.md` — itemized counts and short notes
  - `meta.json` (optional) — minimal run metadata (timestamps, durations)

## Invariants
- Each artifact contains a run timestamp and the snapshot tag.
- Re-running the same inputs is idempotent.
- Summary shows at least: #games scheduled, #games with odds attached, #teams with context written.

## Success Criteria
- All TESTPLAN acceptance checks pass.
- Human can open `summary.md` and understand what happened at a glance.
