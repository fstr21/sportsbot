Project Goal (one-liner)

Create a reliable daily snapshot for each sport: get the day’s schedule, odds, and recent team/player context, save human-readable artifacts, and later evolve into small fetch-only services and agents that run the workflow end-to-end.

Scope (for now)

Work from proof-of-concept scripts that fetch schedule, odds, and recent stats for a single day.

Save artifacts you can eyeball and compare across days.

No database yet. No Discord/bot yet. No provider tech details in docs.

Non-Goals (for now)

No live streaming, in-game updates, or long-tail prop coverage.

No player-to-prop mapping logic beyond “we’ll design that in Phase 2+”.

No schema debates right now; snapshots first.

Phased Plan (conceptual only)

Phase 0 – POC (Today):
Small scripts fetch a single day’s schedule, odds, and recent stats → write artifacts (JSON + a short summary).

Phase 1 – Services (MCPs, fetch-only):
Wrap each source in a tiny service with one POST endpoint. Still artifacts-first.

Phase 2 – Ingest Orchestrator (Agents):
A small agent runs the day flow (fetch → join → write artifacts).

Phase 3 – Reader (Consumers):
A tiny API reads artifacts to answer “what are today’s lines for game X” (DB comes later).

Phase 4 – Database (Optional, later):
Swap the artifact writer/reader behind a common interface to write/read a DB.

Phase 5 – Bot & Extras:
Discord, alerts, and richer analysis once the pipeline is stable.

Document Set (what we’ll create and why)

Think of these as checklists and guardrails. They’re short and designed so any LLM must read them before writing anything.

Root-level docs (global)

docs/PROJECT_CHARTER.md
Purpose, scope, non-goals, phases, and success criteria in one page.

docs/LLM_KICKOFF.md
“How to work on this repo” for LLMs—what to read first, how to run, how to finish.

AGENTS.md (root)
The “must-reads” preamble and hard rules (e.g., services fetch-only; reader doesn’t fetch; artifact-first now).

POC docs (the immediate work)

docs/POC_PLAN.md
What a “day snapshot” is, what artifacts get written, how they’re organized, and how we decide it’s good.

docs/ARTIFACTS_GUIDE.md
Human-facing notes about what files you’ll see (events.json, team_stats.json, summary.md) and how to compare runs.

docs/QA_CHECKLIST_POC.md
A small checklist: “Prompts for date?”, “Writes artifacts to the right place?”, “Summary shows counts?”, “Re-run is idempotent?”

Service/Folder docs (reusable pattern later)

Each folder we build will carry the same mini-spec pack so the agent knows exactly what files do and how to prove them:

SPEC.md – purpose, non-goals, files & responsibilities, one-line “runtime surface” (if any), and a single verify command to run.

CONTRACTS.md – the agreed shapes and invariants of inputs/outputs for this folder (kept generic; no provider specifics).

TESTPLAN.md – named tests the folder must pass (happy path, edge cases, negative cases).

FIXTURES/ – tiny sample data for tests (later; for now, just note they exist).

We’ll create this mini-spec pack in each place we care about (first for the POC scripts folder; later for each service and agent folder).

Collaboration docs (to keep us in sync)

docs/DECISIONS.md
Very short date-stamped bullets: what we decided and why (e.g., “artifacts-first”, “DB later”).

docs/STATUS_UPDATE.md (template)
A tiny form you fill when you return: what’s working, what’s next, what’s blocked.

docs/NAMING_CONVENTIONS.md
Consistent names/tags (e.g., date formats, snapshot tags like MORNING/FINAL). No data schema—just naming rules.

Must-Reads (agents will open these first)

Put this block at the top of AGENTS.md so every LLM sees it before doing work.

# Must-Reads (every time)
- ./docs/PROJECT_CHARTER.md
- ./docs/POC_PLAN.md
- ./docs/LLM_KICKOFF.md
- The folder’s SPEC.md, CONTRACTS.md, TESTPLAN.md (when present)

# Hard Rules
- Services are fetch-only (later).
- Orchestrators (agents) coordinate steps; they don’t embed provider logic.
- Reader does not call providers; in early phases it reads artifacts.
- Keep docs non-technical about providers; no assumptions about upstream APIs.
- Every change must satisfy the folder's TESTPLAN (when available).

Roles & Responsibilities (clear mental model, no tech)

POC Scripts – do one day’s work: ask for a date, fetch the three ingredients (schedule, odds, recent stats), save artifacts + a human summary.

Services (later) – tiny wrappers that only fetch, nothing else.

Ingest Agent (later) – a conductor: “for date D, do fetch → join → write.”

Reader (later) – a viewer: answers questions from artifacts (or DB later), never from providers directly.

Docs – carry intent and acceptance criteria so any LLM can re-enter the project and succeed.

Acceptance (what “good” looks like, without tech)

I can run a simple flow for a single date and get:

A folder with clear artifacts (events, basic team context, a brief summary).

A repeatable outcome (re-running the same date doesn’t create junk).

A short QA checklist that says “pass/fail” on obvious things (counts present, file names correct).

When I’m ready to expand:

Each new area has SPEC / CONTRACTS / TESTPLAN / FIXTURES so agents understand exactly what to do without guessing.


what an “agent” is (in our project)

An agent is a small, goal-driven orchestrator. It takes a task (with a type and parameters), decides which steps to run in which order, calls the right tools/services, and produces a verified outcome (artifacts now; DB later). It does not contain provider-specific scraping logic—that lives in tools/services.

Think: conductor (agent) vs musicians (tools/services).

the cast of characters (and boundaries)

Tools / Services (later “MCPs”)
Fetch-only. Single responsibility: “given arguments, return source data.” No normalization, no mapping, no DB writes.

Agents (what we’re defining here)
Decide the workflow and call tools/services. They normalize, (later) map, and write outputs. They enforce acceptance checks.

Reader (later)
Serves answers from artifacts now (and optionally DB later). Never calls providers directly.

the agent contract (what every agent agrees to)

Input (AgentTask)

type — what job to run (e.g., “ingest.nfl.morning”, “reader.embed_pack”)

params — the knobs (date, league, tag, etc.)

context — request id, timezone, phase (artifacts|db), timeouts/budgets

Output (AgentResponse)

ok (true/false)

summary (human short text)

artifacts (paths/pointers written this run) — for POC, this is the main output

errors (standard labels) — bad_params, upstream_timeout, mcp_error, rate_limited, unknown_task

Invariants

Idempotent re-runs for the same date/tag (no duplicates)

Deterministic within a run (same inputs → same outputs)

Separation of concerns: agents orchestrate; services fetch; reader reads

lifecycle of an agent run (step-by-step)

Validate task

Check required params (e.g., a date for day snapshots)

Build the execution window (ET) and tag (MORNING/FINAL)

Plan

Decide which tools/services to call (based on league + phase)

Set guardrails (timeouts, retry policy, quotas)

Execute

Call tools/services → receive raw data

Normalize into our predictable shapes (still source-referenced)

(Later) Map to our canonical IDs (teams/players)

Write outputs: artifacts now; DB later via the same interface

Verify

Run acceptance checks (counts present, shapes valid, idempotency keys, “latest” pointers updated)

Emit a short human summary

Respond

Return a structured AgentResponse with pointers to what was produced

agent “jobs” we’ll eventually have

Think of these as named task types. Each will later get a one-page mini-spec and a small file the agent reads first.

ingest.<league>.morning / ingest.<league>.final
Run the day’s flow for a league: schedule → odds → context → write artifacts (and later DB).

ingest.backfill
Same as ingest, but for a date range.

reader.embed_pack
Produce a compact, human-readable bundle for one game (from artifacts now, DB later).

reader.player_intel
Return a recent snapshot for a player (from artifacts/DB).

maintenance.mapping_review (later)
Help reconcile unknown name variations discovered during ingest.

how agents decide “what to call”

Routing is by task type. A tiny router maps type → handler (e.g., ingest.nfl.morning → handle_ingest_nfl_morning).

Handlers use a league→provider plan that we set at a policy level (not in code here):
example policy: “NCAAF uses Service A for schedule/odds and Service B for stats.”

No guessing: if a required provider or param is missing, the agent returns bad_params with a short hint.

how agents stay aligned (even across multiple LLMs)

A file each agent reads first (per-folder AGENTS.md or SPEC.md) stating:

the goal & non-goals,

the files it is allowed to touch,

the standard errors,

the acceptance checklist for “done”.

Root must-reads (top of the repo AGENTS.md): point every agent to the global project docs and the folder’s mini-spec pack before any change.

Acceptance > vibes: every agent run ends with the same checklist (artifacts present, summary present, idempotent, no unknown task types, etc.).

what agents log (observability you’ll care about later)

request_id (trace a whole run)

task.type and params (what/when)

durations for each step (plan/fetch/normalize/write)

counts (games, markets, stats) & any unknowns discovered (for follow-up)

the artifact paths written (so you can open them quickly)

how this fits the POC → MCP → orchestrator path

Today (POC): you build small scripts that do the steps manually for a single date and write artifacts.

Soon (services/MCPs): we wrap each source fetch in a tiny service with one POST endpoint; still artifacts-first.

Then (agents): we package the POC steps into a named task type with the lifecycle above. The same acceptance checks apply; only the fetch layer changes (now calling services).

what to capture in each agent’s mini-spec (when we get there)

(No provider assumptions—just the agent’s responsibilities.)

Goal (one sentence)

Non-goals (what it must not do)

Inputs (required params, e.g., date/tag/league)

Outputs (what it produces or returns; artifacts list)

Errors (the standard labels; when to use each)

Acceptance checks (binary list the agent must satisfy)

Must-reads (the files to open before executing changes)

how you’ll “talk” to an agent (human-level prompts)

“Run the morning snapshot for NFL on <date>. If any required parameter is missing, ask for it once, otherwise return bad_params.”

“Summarize what you produced and where it lives. If you didn’t produce anything, return ok=false with error and a one-line reason.”

how we’ll use this together

You’ll finish the POC scripts that fetch a single day and write artifacts.

You’ll drop a quick status note (what worked, where the artifacts are).

I’ll turn that into agent mini-specs (one page each) and a short must-read file per agent, so any LLM can perform the job consistently.