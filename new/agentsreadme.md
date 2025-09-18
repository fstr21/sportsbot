Agents & AGENTS.md — Full Guide
1. What Agents Are

Agents are services or workflows that use LLMs (like Codex 5) to carry out tasks.

Two main kinds in your workflow:

Dev-time agents (Codex in VS Code/CLI): Help scaffold, refactor, test, and review code.

Runtime agents (services): FastAPI or Node apps that expose /agent endpoints, accept JSON tasks, call tools/APIs/DB, and return structured results.

Codex can operate as both: a coding assistant in VS Code and a runtime orchestrator when configured with tools and instructions.

2. What AGENTS.md Is

A machine-readable guide inside your repo that tells agents (like Codex) how to behave.

Not a README replacement — README is for humans, AGENTS.md is for agents.

Codex reads AGENTS.md automatically before making changes, scaffolding, or testing.

Where to put it:

Root of the repo: ./AGENTS.md (global rules).

Optional subfolders: ./agents/ingest/AGENTS.md (local overrides).

Precedence: nearest file wins → local overrides root.

3. Best Practices for AGENTS.md

Clarity: Use short, unambiguous bullet points.

Actionable commands: Show exact CLI commands, not vague instructions.

Consistency: Keep rules in sync with actual build/test setup.

Scope & limits: State what the agent must not do.

Living document: Update whenever your stack changes.

Examples: Include “good vs bad” code patterns.

Common sections:

Project Overview (short context, architecture, domain)

Dev Environment (Python version, dependencies, local setup)

Build & Test Instructions (pytest, linters, migrations)

Code Style Guidelines (naming, logging, file layout)

Database Expectations (FKs, snapshot_tag, mapping rules)

Env Variables & Secrets (never hard-code; list required vars)

PR & Commit Guidelines (titles, branches, description style)

Artifacts & Logging (what to emit, naming, JSON/MD)

Deployment Rules (Dockerfile, Procfile, Railway env vars)

Safety Restrictions (no schema changes without review, no secrets in logs)

4. Example AGENTS.md

Here’s a starter you can adapt:

# AGENTS.md

## Project Overview
- This repo powers a sports data platform (odds, stats, schedules).
- Agents: ingest (fetch from MCPs, normalize, map, write DB, emit artifacts), and readers (DB-only for Discord).

## Dev Environment
- Python 3.11
- Use `pip install -r requirements.txt`
- Run locally: `uvicorn agents.odds.service:app --reload`

## Build & Test
- Run all tests: `pytest -q`
- Run style checks: `black --check . && flake8 .`
- Run type checks: `mypy .`

## Code Style
- Snake_case for Python variables, PascalCase for classes.
- Logging must include `request_id`.
- Prefer composition over inheritance for tools/adapters.

## Database & Mapping
- Always UPSERT (no duplicate rows).
- Enforce foreign keys.
- Include `as_of_utc` and `snapshot_tag` for every ingest write.

## Env Vars
- `DB_HOST`, `DB_USER`, `DB_PASS`, `DB_NAME`
- `SPORTS_API_BASE`, `SPORTS_API_KEY`
- `PORT`, `LOG_LEVEL`

## PR Guidelines
- PR titles: `[agent] short description`
- Must include tests and migration notes if schema changes.
- Link relevant issue/ticket.

## Artifacts
- Emit per-snapshot JSON and MD summaries in `artifacts/{league}/{date}/`.
- JSON must validate against schema in `/schemas/artifacts.json`.

## Deployment
- Railway: must expose `/health` and `/agent`.
- Bind to `$PORT`.

## Safety
- Do not hard-code secrets.
- Do not modify schema without migration + review.
- If unsure, ask for clarification instead of guessing.

5. How Codex Uses AGENTS.md

When you run Codex in VS Code or CLI, it loads the nearest AGENTS.md to the file you’re working in.

It merges rules (local overrides root).

It follows build/test commands to validate code before proposing commits.

It obeys PR guidelines when drafting commits.

6. Testing Agents

Local CLI test

codex run
> Scaffold ingest agent for NFL odds


Codex creates files → runs pytest/black → checks against AGENTS.md rules.

Runtime test
Run FastAPI locally:

uvicorn agents.odds.service:app --reload
curl -X POST http://localhost:8000/agent \
  -d '{"type":"embed_pack","params":{"league_id":"NFL","game_id":"12345"}}'


CI check
Add CI to run:

pytest && black --check . && mypy .


This ensures Codex outputs always pass your pipeline.

7. Putting It All Together

Agents = your runtime services (FastAPI on Railway).

Codex 5 = your dev-time pair programmer and agent orchestrator.

AGENTS.md = the rulebook Codex reads before touching your code.

Testing ensures what Codex generates matches your rules and actually runs.

Deployment puts the agents live on Railway with healthchecks + env vars.