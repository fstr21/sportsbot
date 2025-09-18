# DECISIONS.md (LOCKED)
Architecture/Policy Decision Log for sports-intel.
Keep entries short, factual, and outcome-oriented. No provider schemas or code here.

## How to use this file
- Add a new entry for any change that affects behavior, outputs, read order, or required rules.
- Do **not** edit past entries except to mark **Deprecated/Superseded**.
- When you add an entry, also update any LOCKED docs it impacts in the same commit.

## Decision lifecycle
- **Proposed** → **Accepted** → (optionally) **Deprecated** → **Superseded**
- Use the `Supersedes:` / `Superseded by:` fields to chain related decisions.

---

## Quick Index (latest first)
- DEC-2025-09-18-009 — Bootstrap loader uses receipts & compliance block — **Accepted**
- DEC-2025-09-18-008 — Add PROJECT_NORTH_STAR to must-reads & loader — **Deprecated**
- DEC-2025-09-18-008A — Add PROJECT_NORTH_STAR to must-reads & loader (corrected) — **Accepted**
- DEC-2025-09-18-007 — League folder names are lowercase (`nfl`, `ncaaf`) — **Accepted**
- DEC-2025-09-18-006 — Outputs = JSON + `.md` by matchup — **Accepted**
- DEC-2025-09-18-005 — Odds-source discipline: 10 requests/min — **Accepted**
- DEC-2025-09-18-004 — No placeholders; fail if required slice missing — **Accepted**
- DEC-2025-09-18-003 — Remove snapshot tags entirely — **Accepted**
- DEC-2025-09-18-002 — All displayed times in outputs are ET — **Accepted**
- DEC-2025-09-18-001 — Input date format is MM/DD/YYYY; filesystem uses MM-DD-YYYY — **Accepted**

---

## DEC-2025-09-18-009 — Bootstrap loader uses receipts & compliance block
**Status:** Accepted  
**Summary:** `AGENTS.md` starts with a LOCKED Bootstrap Loader that instructs the model to load specific files, print a one-line receipt per file (with a verbatim token), then return a compliance block.  
**Rationale:** Ensures the LLM actually reads the must-reads; prevents scope drift.  
**Impacted docs:** `AGENTS.md` (loader section)  
**Supersedes:** —  
**Superseded by:** —

---

## DEC-2025-09-18-008A — Add PROJECT_NORTH_STAR to must-reads & loader (corrected)
**Status:** Accepted  
**Summary:** `docs/PROJECT_NORTH_STAR.md` is required reading and added to the loader as item #7 (final item) in the bootstrap sequence.  
**Rationale:** Agents must understand the product intent (what users see and why) before planning/executing.  
**Impacted docs:** `AGENTS.md` (must-reads + loader section updated from 6 to 7 files)  
**Supersedes:** DEC-2025-09-18-008  
**Superseded by:** —

---

## DEC-2025-09-18-008 — Add PROJECT_NORTH_STAR to must-reads & loader
**Status:** Deprecated  
**Summary:** `docs/PROJECT_NORTH_STAR.md` is required reading and added to the loader as the first file.  
**Rationale:** Agents must understand the product intent (what users see and why) before planning/executing.  
**Impacted docs:** `AGENTS.md` (must-reads + loader), `PROJECT_NORTH_STAR.md` (new)  
**Supersedes:** —  
**Superseded by:** DEC-2025-09-18-008A

---

## DEC-2025-09-18-007 — League folder names are lowercase
**Status:** Accepted  
**Summary:** Artifact league folders use lowercase (`artifacts/nfl/`, `artifacts/ncaaf/`).  
**Rationale:** Avoid case-sensitive filesystem surprises; keep paths consistent.  
**Impacted docs:** `NAMING_CONVENTIONS.md`, `POC_PLAN.md`, `AGENTS.md`  
**Migration:** Rename any existing `NFL/` or `NCAAF/` folders to lowercase.  
**Supersedes:** —  
**Superseded by:** —

---

## DEC-2025-09-18-006 — Outputs = JSON + `.md` by matchup
**Status:** Accepted  
**Summary:** Each run produces machine-readable `events.json`, `team_stats.json` and a human-readable `summary.md` organized **by matchup**; optional `meta.json`.  
**Rationale:** Human inspection + simple automation, consistent with the product's snapshot-first approach.  
**Impacted docs:** `AGENT_CARD.md`, `SPEC.md`, `TESTPLAN.md`, `POC_PLAN.md`, `NAMING_CONVENTIONS.md`, `AGENTS.md`  
**Supersedes:** Any prior mention of JSON-only or alternate presentation.  
**Superseded by:** —

---

## DEC-2025-09-18-005 — Odds-source discipline: 10 requests/min
**Status:** Accepted  
**Summary:** Treat the odds source with a practical limit of **10 requests per minute** during orchestration.  
**Rationale:** Prevent throttling; encode conservative behavior early.  
**Impacted docs:** `AGENT_CARD.md`, `SPEC.md`, `TESTPLAN.md`, `AGENTS.md`  
**Supersedes:** —  
**Superseded by:** —

---

## DEC-2025-09-18-004 — No placeholders; fail if required slice missing
**Status:** Accepted  
**Summary:** If schedule **or** odds **or** team context is missing, the run fails with a clear error (no stub values).  
**Rationale:** Integrity > appearance; avoids misleading outputs.  
**Impacted docs:** `AGENT_CARD.md`, `SPEC.md`, `TESTPLAN.md`, `POC_PLAN.md`, `AGENTS.md`  
**Supersedes:** Any prior "graceful degradation with partial data" language.  
**Superseded by:** —

---

## DEC-2025-09-18-003 — Remove snapshot tags entirely
**Status:** Accepted  
**Summary:** Do not use tags like MORNING/FINAL in paths or content at this stage.  
**Rationale:** Simpler artifact story; tags can be reintroduced later if needed.  
**Impacted docs:** `AGENT_CARD.md`, `SPEC.md`, `POC_PLAN.md`, `AGENTS.md`  
**Supersedes:** Any earlier tag-based path conventions.  
**Superseded by:** —

---

## DEC-2025-09-18-002 — All displayed times in outputs are ET
**Status:** Accepted  
**Summary:** Outputs (JSON and `.md`) must display times in **Eastern Time (ET)**. Convert from UTC/Zulu as needed.  
**Rationale:** Consistent user-facing timezone.  
**Impacted docs:** `NAMING_CONVENTIONS.md`, `AGENT_CARD.md`, `SPEC.md`, `TESTPLAN.md`, `POC_PLAN.md`, `AGENTS.md`  
**Supersedes:** —  
**Superseded by:** —

---

## DEC-2025-09-18-001 — Input date format is MM/DD/YYYY; filesystem uses MM-DD-YYYY
**Status:** Accepted  
**Summary:** Prompt for `MM/DD/YYYY`; use `MM-DD-YYYY` for folder/file names.  
**Rationale:** Friendly input; filesystem-safe output.  
**Impacted docs:** `NAMING_CONVENTIONS.md`, `POC_PLAN.md`, `AGENTS.md`, `AGENT_CARD.md`, `SPEC.md`, `TESTPLAN.md`  
**Supersedes:** Any `YYYY-MM-DD` guidance.  
**Superseded by:** —

---

## Template for new decisions

Copy this block and fill it out for each new decision.