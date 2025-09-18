# TESTPLAN — Day Snapshot Agent

## Acceptance (must pass)
A. Inputs
  - Reject bad date formats; accept YYYY-MM-DD.
  - Only "NFL" and "NCAAF" accepted for league.
  - Default tag to "MORNING" if omitted.

B. Artifacts
  - Writes to: artifacts/<league>/<YYYY-MM-DD>_<TAG>/.
  - Files exist: events.json, team_stats.json, summary.md.
  - Each artifact includes a run timestamp and the tag.

C. Joining & Coverage
  - schedule entries present for the date.
  - odds list attached to schedule entries using simple, tolerant matching.
  - team context written.
  - **NFL only**: (when introduced) player context file is allowed; NCAAF must never produce player context.
  - Join coverage threshold noted in summary (e.g., "X/Y games with odds + context").

D. Idempotency
  - Re-running the same league/date/tag does not create duplicates and yields consistent counts.

E. Summary
  - `summary.md` includes clear counts and the path written.

## Manual run protocol (for now)
1) Run once for an NFL date; confirm A–E.
2) Run again for the same inputs; confirm idempotency.
3) Repeat steps 1–2 for one NCAAF date.

## Out of scope (today)
- Database checks
- Provider/API details
- Automated schema validation (we’ll add later)
