# POC PLAN — Day Snapshots (LOCKED)

> Source-agnostic plan for producing one-day snapshots.  
> Changes require an entry in `docs/DECISIONS.md`.  
> This plan supersedes prior versions that assumed `YYYY-MM-DD` dates, snapshot tags, and provider-specific promises.

## 1) Purpose
For a single date and league, gather:
- the **schedule**,
- the **odds**,
- **recent team context**,
and write **JSON + a readable `.md`** so a human can review quickly.  
No database. No bots. No upstream specifics in this document.

## 2) Audience
- **You** (operator): to run/check the POC.
- **LLMs/agents**: to understand goals, constraints, and acceptance—without guessing about providers.

## 3) Hard Rules (non-negotiable)
- **Input date format**: `MM/DD/YYYY` (e.g., `09/21/2025`)  
  (Use `MM-DD-YYYY` only for folder names.)
- **Timezone**: **All displayed times in outputs must be ET**. Convert from UTC/Zulu if needed.
- **Snapshot tags**: **None** at this stage (do not invent MORNING/FINAL).
- **No placeholder or fabricated data**. If required slices are missing, **fail with a clear error**.
- **Odds source rate limit**: respect **10 requests per minute** during orchestration.
- **Idempotency**: re-running the same league/date must not duplicate content and should produce consistent counts.

## 4) Leagues & Policy
- **NFL**: schedule, odds, team context; may later add a basic player context file.  
- **NCAAF**: schedule, odds (teams only), team context; **never includes players**.  
*(Policy only—no provider details here.)*

## 5) Outputs (per run)
Write to: `artifacts/<league>/<MM-DD-YYYY>/`
- `events.json` — schedule entries with an attached **odds list** (consistent list format)
- `team_stats.json` — recent team context
- `summary.md` — human-readable summary **organized by matchup**
- `meta.json` *(optional)* — minimal run info (timestamps, durations)

### Presentation requirements
- All times shown in JSON and `.md` are **ET**.
- `summary.md` is **by matchup** (one section per game), stating:
  - kickoff time (ET),
  - whether odds are attached,
  - whether team context is present.

## 6) Run Flow (operator)
1) **Prompt for date** → accept only `MM/DD/YYYY`; reject others.
2) **Build the day frame** in ET (for display).
3) **Fetch slices** for the date:
   - schedule,
   - odds,
   - team context.  
   *(NFL may later add basic player context; NCAAF never includes players.)*
4) **Join** slices by (home team, away team, kickoff time in ET) with a small tolerance.
5) **Write** artifacts (JSON + `.md` by matchup).
6) **Verify** acceptance checklist; if any required slice is missing, **fail** (no placeholders).

## 7) Acceptance Checklist (pass/fail)
- [ ] Date accepted in `MM/DD/YYYY`; invalid formats rejected (`bad_params`).
- [ ] Artifacts folder created: `artifacts/<league>/<MM-DD-YYYY>/`.
- [ ] Files present: `events.json`, `team_stats.json`, `summary.md`.
- [ ] All displayed times are **ET**.
- [ ] `summary.md` is **by matchup** and includes counts:
      total scheduled games, games with odds attached, teams with context.
- [ ] No placeholder values; missing required slices cause a clear failure.
- [ ] Rate-limit discipline respected (≤ **10 req/min** to odds source).
- [ ] Idempotent re-run: same league/date → no duplicates; counts consistent.

## 8) Idempotency Protocol
- Re-run immediately with the same league/date.
- Confirm the same target folder is reused and counts remain stable.
- If differences appear, record a short note in `docs/STATUS_UPDATE.md` explaining expected vs. unexpected behavior.

## 9) Golden Snapshot
- When a run passes acceptance for a league, mark it as your **baseline** (copy to `artifacts/golden/<league>/<MM-DD-YYYY>/` or note its path in `STATUS_UPDATE.md`).  
- Use it later to compare changes at a glance.

## 10) Join Policy (POC level)
- Match by **home**, **away**, **kickoff time (ET)** with minimal tolerance.  
- Avoid fuzzy heuristics; if ambiguous, **fail** rather than guess.  
- Capture enough names/identifiers in artifacts for future mapping work (no DB yet).

## 11) Error Labels (exact tokens)
- `bad_params` — input missing/invalid (e.g., wrong date format)  
- `upstream_timeout` — a source call exceeded time budget  
- `mcp_error` — orchestrated fetch returned an error envelope  
- `rate_limited` — odds source limit exceeded (assume 10/min)  
- `unknown_task` — unrecognized task type

## 12) Status Update Template
Record quick notes after each run in `docs/STATUS_UPDATE.md`:
