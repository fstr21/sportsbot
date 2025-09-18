# Agent Card — Day Snapshot (LOCKED)

> Do not add provider, performance, or database assumptions in this file.  
> Changes require an entry in `docs/DECISIONS.md`.

## Mission (what this agent does)
For a single **date (MM/DD/YYYY)** and **league**, produce a daily snapshot:
- the **schedule** for that date,
- the **odds** for that date,
- **recent team context** for that date  
(NFL may later include basic player context; NCAAF never includes players).

Outputs must include **machine-readable JSON** and a **human-readable `.md`** broken down **by matchup**.

## Scope Guardrails (policy, not tech)
- Supported leagues: **NFL**, **NCAAF**
- **No snapshot tags** at this stage (do not invent MORNING/FINAL).
- **All displayed times must be Eastern Time (ET)**; convert from UTC/Zulu if needed.
- **No placeholders or fabricated values**. If a required slice is missing, fail the run with a clear error.
- Respect a practical **10 requests per minute** limit to the *odds source*.
- Source-agnostic: this file must not encode upstream API specifics.
- No database, no bots.

## Inputs (required)
- `league` ∈ { `NFL`, `NCAAF` }
- `date` in **`MM/DD/YYYY`**  
(Reject any other format.)

## Outputs (artifacts)
Write to: `artifacts/<league>/<MM-DD-YYYY>/`
- `events.json` — schedule entries with an attached **odds list** (consistent list structure)
- `team_stats.json` — recent team context
- `summary.md` — short human summary **organized by matchup** (one section per game)
- `meta.json` *(optional)* — minimal run info (timestamps, durations)

Each output MUST use **ET** for displayed timestamps.

## Orchestration Flow (conceptual)
1) **Validate** inputs (`league`, `date` in `MM/DD/YYYY`).
2) **Frame** the day (convert/represent times in ET).
3) **Fetch** the three slices for the date: schedule, odds, team context  
   *(NFL may later add a basic player context file; NCAAF never includes players.)*
4) **Join** slices by a simple, human-obvious match (home/away names + kickoff time tolerance).
5) **Write** artifacts (JSON + `.md` by matchup).
6) **Verify** acceptance criteria; **summarize** clearly (counts + artifact path).

## Joining Policy (simple, explainable)
- Match by **home team**, **away team**, and **kickoff time (ET)** with a minimal tolerance.  
- Avoid fuzzy heuristics; if ambiguous, **fail with a clear error** rather than guessing.

## Required Behaviors
- Input validation; bad input → `bad_params`.
- **ET-only display** in outputs.
- **No placeholders**; if any required slice (schedule OR odds OR team context) is missing, fail.
- **Idempotent** re-run: same league/date writes the same paths without duplicates.
- Respect **10 req/min** to the odds source.
- Summaries are **by matchup** and list counts and artifact path.

## Error Labels (use exactly)
- `bad_params` — input missing/invalid (e.g., wrong date format)
- `upstream_timeout` — a source call exceeded time budget
- `mcp_error` — orchestrated fetch returned an error envelope
- `rate_limited` — odds source limit exceeded (assume 10/min)
- `unknown_task` — unrecognized task type

## Acceptance (must pass)
- Accepts only `MM/DD/YYYY` dates; rejects others.
- Writes to `artifacts/<league>/<MM-DD-YYYY>/`.
- Produces `events.json`, `team_stats.json`, `summary.md`; all times in **ET**.
- `summary.md` is organized **by matchup**, with counts:
  - total scheduled games,
  - games with odds attached,
  - teams with context.
- Re-run with the same inputs is clean and consistent (no dupes).

## Must-Reads (before any change)
- Root `AGENTS.md`
- This `AGENT_CARD.md` (LOCKED)
- `SPEC.md`, `CONTRACTS.md`, `TESTPLAN.md` in this folder (LOCKED)
