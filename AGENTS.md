# AGENTS — Must-Reads & Hard Rules

## Must-Reads (every session)
1) ./AGENTS.md (this file)
2) ./agents/day_snapshot/AGENT_CARD.md
3) ./agents/day_snapshot/SPEC.md
4) ./agents/day_snapshot/CONTRACTS.md
5) ./agents/day_snapshot/TESTPLAN.md

## Hard Rules (policy, not code)
- Services/tools are **fetch-only** (when they exist later). No business logic there.
- Agents **orchestrate**: validate → plan → fetch → normalize to simple snapshot shapes → write artifacts → verify → summarize.
- Reader (later) **only reads artifacts/DB**, never calls sources directly.
- Keep docs **source-agnostic** (no API specifics here).
- Use standard error labels: `bad_params`, `upstream_timeout`, `mcp_error`, `rate_limited`, `unknown_task`.
- Every change must satisfy the folder’s TESTPLAN. Acceptance > vibes.

## Snapshot policy (today)
- Work **one date at a time**.
- Two leagues:
  - **NFL**: schedule + odds for **teams and players**; stats for teams/players.
  - **NCAAF**: schedule + odds for **teams only**; stats for teams (no player odds/stats).
- Capture enough **names/identifiers** in artifacts for future mapping.
- Artifacts live at: `artifacts/<league>/<YYYY-MM-DD>_<TAG>/` with a short `summary.md`.

## Finish line (for any agent run)
- Clear pass on TESTPLAN acceptance.
- Concise human summary of what was produced and where.
