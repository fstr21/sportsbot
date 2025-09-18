Project Overview — Snapshot-Only Sports Data Platform
Goal (1 sentence)

Take once-per-slate snapshots of odds, schedules/results, and stats for NFL, NCAAF, NBA, MLB, NHL, WNBA, and Soccer; write them to a database (source of truth) and also emit local JSON/MD artifacts you can open. No live polling. Discord (later) will read DB only.

Cadence & Timezone

Cadence: Manual — run once the morning of a slate (optional “FINAL” run after games).

Timezone: America/New_York (ET).

Snapshot tags: MORNING (primary), optional FINAL.

Data to Ingest (per league)

Odds — moneyline, spread, total; props can be added later.

Schedules & Results — start time, home/away, provider event IDs, final scores.

Team & Player Stats — season-to-date and/or recent splits; basic rosters as available.

(Optional later) Injuries and Weather for context.

MCP Jobs (thin, fetch-only; run on Railway)

sportsgameodds_mcp (Odds)

Tool examples: get_events (by league_id, ET window, include flags), get_game.

Purpose: consistent odds fetch across leagues.

espn_mcp (Stats / Schedules / Results)

Tool examples: get_schedule, get_team_stats, get_player_stats, get_boxscore (optional).

Purpose: single entry point for schedules/results/stats with a league parameter.

(Optional later) injuries_mcp, weather_mcp.

MCPs only fetch provider JSON. They do not perform ID mapping or DB writes. (OpenAI has embraced agent tooling that can call tools/services like these; you’ll sit MCPs alongside your agents.) 
OpenAI
+1

Agents (your workers)

Ingest Agents (per league, per data type: odds and stats):

Input: league + ET window + snapshot_tag.

Do: call MCPs → normalize → UPSERT into DB → emit local JSON/MD artifacts.

Output: durable DB rows + human-readable artifacts.

Reader/Intel Agents (later): strictly DB-only readers used by Discord. (Out of scope now.)

OpenAI’s Responses API + Agents SDK provide first-class building blocks for agentic apps (tool calls, web/file/computer tools, tracing). These are the current, recommended primitives for “agents.” 
OpenAI
+1

Mapping (names & IDs)

Maintain canonical leagues, teams, players with external IDs (e.g., ESPN IDs) plus name-variation tables.

During ingest, resolve provider entities → your IDs; if unknown, add a variation entry (or flag for review).

Keep mapping logic centralized and deterministic (not inside MCPs).

Database Plan (principles to review before build)

Entities: leagues, teams, players, team_name_variations, player_name_variations, games, markets (odds), team_stats, player_stats, plus ingest bookkeeping (e.g., ingest_runs).

Foreign Keys (FKs): enforce relationships (e.g., games.home_team_id → teams.id; markets.game_id → games.id; player_stats.player_id → players.id).

Snapshot metadata: each write includes as_of_utc and snapshot_tag so “latest” is well-defined and views are trivial later.

Indexes: by league, start time, game, and “latest per market/stat” patterns.

Optional raw store: keep compressed provider payloads per ingest run to debug without re-hitting providers.

(Views later): market_latest, player_stats_latest.

Secrets & Config (API Keys)

Local: .env files. Railway: Environment Variables.

Baseline variables:

SPORTSGAMEODDS_BASE, SPORTSGAMEODDS_KEY

ESPN_BASE (and key if required)

DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME

TZ=America/New_York, SNAPSHOT_TAG=MORNING (or FINAL)

(Optional) OUTPUT_DIR for artifacts

Least-privilege DB users:

ingest_writer (INSERT/UPDATE)

(Later) reader (SELECT-only) for Discord/intel.

What Runs on Railway (categories, not layout)

MCP services: sportsgameodds_mcp and espn_mcp (fetch-only).

Ingest jobs: per-league odds and stats jobs you trigger once, morning-of; they call MCPs, normalize, write DB, and emit artifacts.

(Later) Reader/Intel services for Discord (DB-only).

Artifacts (for human inspection)

Per snapshot (date/tag folder per league):

Odds slate JSON (+ optional per-game JSON) and small MD summaries.

Stats JSON (players/teams).

Artifacts are for visibility; the DB is the source of truth.

Testing (light but complete)

Goal: Prove each data path works end-to-end without hitting live users.

MCP contract tests

Verify request/response shapes for sportsgameodds_mcp.get_events and espn_mcp tools (happy path + common errors), using fixtures.

Normalization tests

Given sample MCP payloads, assert expected rows land in games, markets, team_stats, player_stats with correct as_of_utc / snapshot_tag.

Idempotency: re-running same window/tag updates, not duplicates.

Mapping tests

Variations resolve correctly (e.g., “Mahomes, P.” → your player ID).

Unknowns are captured for review.

DB constraint tests

FK integrity (bad game_id should fail).

Index/select sanity for “latest” queries (views can come later).

Artifact tests

After a dry run, assert expected JSON/MD files exist with required fields and snapshot labels.

Runbook test (dry run)

Simulate MORNING on a tiny window → MCP fixtures → ingest → DB rows → artifacts → counts/summary log.

Secrets/config tests

Missing/invalid env vars fail fast with clear errors.

Retry/backoff tests

Transient MCP failure retries with backoff and surfaces clear status if it ultimately fails.

How OpenAI “Agents” fit your plan (practical)

What “agent” means here: A system that can independently execute steps (call tools, transform data, handle multi-step flows) on your behalf. OpenAI provides the Responses API (for tool-use flows) and an Agents SDK with tracing (to orchestrate and observe). 
OpenAI
+1

Your use: Wrap each ingest job (odds/stats per league) as an agent task that:

calls the MCP tool(s),

normalizes & maps,

writes DB,

emits artifacts,

logs an ingest_runs summary.

Why use OpenAI’s agent stack? Built-in tool calling + observability/tracing simplify multi-step runs and future debugging/metrics. (OpenAI is actively positioning Responses API as the future for agentic apps; Assistants API v2 continues but is on a deprecation path once parity is reached.) 
OpenAI
+1

Using “Codex” in VS Code (what you’ll do day-to-day)

Treat Codex (the coding assistant inside VS Code) as your pair programmer for this project:

Scaffold ingest runners (odds/stats).

Write parsers/normalizers from MCP payloads to your row shapes.

Generate SQL migrations and FKs safely.

Draft tests (fixtures, normalization assertions, idempotency checks).

Produce runbooks/docs and quick JSON→MD summaries for artifacts.

Good prompts to use in VS Code with Codex:

“Create a function that maps ESPN team names and IDs to my teams table schema; include unit tests with fixtures.”

“Given this get_events JSON sample, emit rows for markets with (game_id, book, market_type, side, line_value, price) and add as_of_utc/snapshot_tag.”

“Write SQL for games, markets, team_stats, player_stats with FKs and suggested indexes; explain each FK in comments.”

Note: For agentic automation (multi-step runs, tracing, built-in tools), use OpenAI’s Responses API + Agents SDK in your code; for editing/writing code, use Codex in VS Code. (They’re complementary.)

OpenAI’s current, official guidance for building “agents” is via Responses API with built-in tools and the Agents SDK; this is the track to follow rather than legacy patterns. 
OpenAI

Future-proof notes

As OpenAI adds more built-in tools (web/file/computer) and improves agent orchestration, you can migrate your ingest runners to use those primitives with tracing/metrics out-of-the-box. 
OpenAI

MCP adoption is growing industry-wide, making your decision to keep MCPs “thin and fetch-only” a good long-term bet. 
Wikipedia