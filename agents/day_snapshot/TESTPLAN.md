# TESTPLAN — Day Snapshot Agent (LOCKED)

> Behavioral acceptance. Human-checkable. No provider details.

## A. Inputs & Formatting
- Reject non-`MM/DD/YYYY` dates; accept `MM/DD/YYYY`.
- Accept only `NFL` or `NCAAF` for `league`.
- All displayed times in outputs are **ET**.

## B. Artifacts & Layout
- Writes into: `artifacts/<league>/<MM-DD-YYYY>/`.
- Files exist: `events.json`, `team_stats.json`, `summary.md`.
- `events.json` includes schedule entries with an attached **odds list**.
- `team_stats.json` contains recent team context.

## C. By-Matchup Presentation
- `summary.md` is organized **by game matchup** (one section per game).
- Each game section mentions schedule (ET), odds presence, and context presence.

## D. No Placeholder Policy
- If schedule OR odds OR team context is missing for the date, the agent fails with a clear error.
- The run must **not** fabricate or stub values.

## E. Rate-Limit Discipline
- Orchestration respects a **10 requests/min** limit to the odds source (no bursts beyond this).

## F. Idempotency
- Re-running with the same `league` and `date`:
  - reuses/writes the same target folder,
  - does not duplicate content,
  - yields consistent counts in `summary.md`.

## G. Summary quality
- `summary.md` includes at least:
  - total scheduled games,
  - games with odds attached,
  - teams with context,
  - the artifact path used/written.

## Manual run protocol (for now)
1) Run once for an **NFL** date; confirm A–G.
2) Run again for the same NFL inputs; confirm **F**.
3) Repeat steps 1–2 for a **NCAAF** date.

## Out of scope (today)
- Database checks
- Provider/API details
- Automated schema validation (can be added later)

## Done / Not Done (printable checklist)
- [ ] Inputs valid (league/date)
- [ ] Outputs in ET
- [ ] events.json written
- [ ] team_stats.json written
- [ ] summary.md by matchup
- [ ] No placeholders; fail on missing required data
- [ ] Rate-limit respected
- [ ] Idempotent re-run
