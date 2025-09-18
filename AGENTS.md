# AGENTS.md (LOCKED)

> Source-agnostic agent guide for this repo.  
> Do **not** add provider, performance, or database assumptions here.  
> Any change requires an entry in `docs/DECISIONS.md` (what/why/by whom/date).

---

> BOOTSTRAP LOADER (LOCKED) — read before doing anything

You must preload the following files, in order, then return a receipt for each:

1) agents/day_snapshot/AGENT_CARD.md
2) agents/day_snapshot/SPEC.md
3) agents/day_snapshot/CONTRACTS.md
4) agents/day_snapshot/TESTPLAN.md
5) docs/NAMING_CONVENTIONS.md
6) docs/POC_PLAN.md
7) docs/PROJECT_NORTH_STAR.md

For EACH file, print exactly one line:
LOADED <path> | token: "<5 consecutive words copied verbatim from that file>"

Rules:
- If any file cannot be opened or a token cannot be quoted verbatim, say **NON-COMPLIANT** and stop.
- After all seven receipts, return ONLY the compliance block:
  1) Date input format you will enforce
  2) Output timezone you will display
  3) Snapshot tags policy
  4) Placeholder/fabrication policy
  5) Odds-source rate limit you will obey
  6) Output files and where they will be written (league/date path)
  7) Summary organization (how the .md is structured)
  8) Idempotency promise (yes/no, what it means)

Preference on conflicts: prefer the LOCKED day_snapshot docs and NAMING_CONVENTIONS.
Do not proceed to plan or execution until receipts + compliance block are returned.

## 1) Purpose

Give any LLM/agent the exact rules, must-reads, and acceptance needed to run orchestrated tasks **without guessing**.  
Today's focus: the **Day Snapshot** flow (one date, one league) that produces simple artifacts for human review.

---

## 2) Must-Reads (every session, in this order)

1. `agents/day_snapshot/AGENT_CARD.md` **(LOCKED)**
2. `agents/day_snapshot/SPEC.md` **(LOCKED)**
3. `agents/day_snapshot/CONTRACTS.md` **(LOCKED)**
4. `agents/day_snapshot/TESTPLAN.md` **(LOCKED)**
5. `docs/NAMING_CONVENTIONS.md` **(LOCKED)**
6. `docs/POC_PLAN.md` **(LOCKED)**
7. `docs/PROJECT_NORTH_STAR.md` **(LOCKED)**

*(Optional helpers for runs/testing)*  
- `docs/AGENT_HARNESS.md` (how to enact & verify the agent)  
- `agents/day_snapshot/SMOKE_TESTS.md` (quick proofs)

> If any document conflicts, **prefer the LOCKED day_snapshot docs and NAMING_CONVENTIONS**.

---

## 3) Hard Rules (policy, not code)

- **Date input**: `MM/DD/YYYY` (e.g., `09/21/2025`).  
  **Filesystem** uses `MM-DD-YYYY`.
- **Timezone**: all displayed times in outputs are **ET** (convert from UTC/Z if needed).
- **Snapshot tags**: **none** at this stage (do not invent MORNING/FINAL).
- **No placeholders or fabricated values**. If a required slice is missing, **fail with a clear error**.
- **Odds-source rate limit**: respect **10 requests per minute**.
- **Outputs per run**: machine-readable **JSON** + human-readable **`.md` by matchup**.
- **Idempotency**: re-running the same `league+date` must not duplicate content and should keep counts stable.
- Keep this file and must-reads **source-agnostic** (no API specifics).

---

## 4) Task Types (current)

- `ingest.day_snapshot` — run the Day Snapshot agent for one `league` and `date`.

**Inputs**  
- `league`: `NFL` or `NCAAF`  
- `date`: `MM/DD/YYYY`

**Outputs** (written to `artifacts/<league>/<MM-DD-YYYY>/`)  
- `events.json` — schedule entries with an attached **odds list** (consistent list structure)  
- `team_stats.json` — recent team context  
- `summary.md` — short human summary **organized by matchup** (one section per game)  
- `meta.json` *(optional)* — minimal run info (timestamps, durations)

**Error labels** (use exactly):  
`bad_params`, `upstream_timeout`, `mcp_error`, `rate_limited`, `unknown_task`

---

## 5) What "done" means (acceptance)

- Accepts only `MM/DD/YYYY` dates; invalid formats → `bad_params`.
- Writes to `artifacts/<league>/<MM-DD-YYYY>/`.
- Produces `events.json`, `team_stats.json`, `summary.md` (times shown in **ET**).
- `summary.md` is **by matchup** and includes counts: total scheduled games, games with odds attached, teams with context, and the artifact path.
- **No placeholders**; if schedule **or** odds **or** team context is missing for the date, the run **fails clearly**.
- Respects **10 req/min** to the odds source.
- Idempotent re-run for the same inputs (no duplicates; counts stable).

*(This acceptance is mirrored verbatim in `agents/day_snapshot/TESTPLAN.md`.)*

---

## 6) Run modes (how to operate)

You may control mode **via prompt** or a small file toggle:

- **PLAN_ONLY** — validate and print the exact plan; **no fetching/writing**.  
- **EXECUTE** — produce artifacts, enforce all rules, then print counts + checklist.  
- **IDEMPOTENCY_RERUN** — re-run with the same inputs; prove no duplicates and stable counts.

If using a toggle file, place `agents/day_snapshot/MODE.md` with:

```yaml
# Day Snapshot Agent — MODE SWITCH (LOCKED)
# Edit ONLY the three values below. The agent must read this file before running.

mode: EXECUTE          # PLAN_ONLY | EXECUTE | IDEMPOTENCY_RERUN
league: NFL            # NFL | NCAAF
date: 09/21/2025       # MM/DD/YYYY

# Do not change the rules below (policy reminder)
rules:
  - inputs: date=MM/DD/YYYY, league in {NFL,NCAAF}
  - outputs: ET-only; JSON + .md by matchup; no snapshot tags
  - data: no placeholders; fail if a required slice is missing
  - odds_source_rate_limit: 10_per_minute
  - idempotent: true
```

---

## 7) Baseline for any new conversation (compliance block)

At the start of a new IDE chat, paste:

> Read: AGENTS.md, agents/day_snapshot/AGENT_CARD.md, agents/day_snapshot/SPEC.md, agents/day_snapshot/CONTRACTS.md, agents/day_snapshot/TESTPLAN.md, docs/NAMING_CONVENTIONS.md, docs/POC_PLAN.md, docs/PROJECT_NORTH_STAR.md. These files are LOCKED. If any doc conflicts, prefer the LOCKED day_snapshot docs and NAMING_CONVENTIONS.
> Return ONLY this compliance block:
> 
> 1. Date input format you will enforce
> 2. Output timezone you will display
> 3. Snapshot tags policy
> 4. Placeholder/fabrication policy
> 5. Odds-source rate limit you will obey
> 6. Output files and where they will be written (league/date path)
> 7. Summary organization (how the .md is structured)
> 8. Idempotency promise (yes/no, what it means)
> 
> If any answer is not exactly aligned with the LOCKED docs, say "NON-COMPLIANT" and stop.

**Expected compliant answers:**

1. Date: MM/DD/YYYY
2. TZ: ET (display)
3. Tags: none
4. Placeholders: forbidden; fail if required slice missing
5. Rate limit: 10 requests/min (odds source)
6. Outputs: events.json, team_stats.json, summary.md → artifacts/<league>/<MM-DD-YYYY>/
7. Summary: by matchup
8. Idempotency: yes; same inputs → same paths, no duplicates

---

## 8) Quick drills

**PLAN drill**

Run in PLAN_ONLY for league=NFL, date=09/21/2025.

Expect: plan steps, ET-only note, no tags, no placeholders, 10 req/min, join policy, exact artifact path, TESTPLAN list.

**EXECUTE drill**

Run in EXECUTE with the same inputs.

Expect: artifacts written, ET times, .md by matchup, counts + "Done/Not Done" checklist.

**IDEMPOTENCY drill**

Re-run with the same inputs.

Expect: same path, no duplicates, identical counts, "Idempotent: PASS".

---

## 9) Change control

To modify rules or acceptance, update the relevant LOCKED docs and add a short note to `docs/DECISIONS.md`:

- What changed
- Why it changed
- Date & author