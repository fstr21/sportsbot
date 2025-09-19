# MCP Access Guide

This guide covers the CollegeFootballData MCP service that is live today, plus the scaffolded (not yet deployed) SportsGameOdds service.

---

## CollegeFootballData MCP (live)

**Source:** `mcp/collegefootballdata`

### Architecture
```
mcp/collegefootballdata/
  config.py        # Pydantic settings (reads COLLEGE_FOOTBALL_DATA_API_KEY)
  cfbd_client.py   # Shared httpx.AsyncClient with Authorization header
  tools.py         # ToolSpec registry (games, lines, games_teams, ...)
  main.py          # FastAPI app => /health, /tools, /tools/{name}/invoke
```
Key behaviors:
- Config module validates env vars via `get_settings()`/`require_api_key()`.
- Client caches a single `httpx.AsyncClient` with auth header + timeout.
- `/tools` lists ToolSpecs; `/tools/{tool}/invoke` proxies requests and returns `{ "tool", "params", "data" }`.
- Upstream 4xx/5xx bubble through as FastAPI 502 responses.
- `/health` returns `{ "status": "ok" }`.

### Environment Variables
| Var | Purpose |
| --- | --- |
| `COLLEGE_FOOTBALL_DATA_API_KEY` | Required Bearer token for CFBD.
| `COLLEGE_FOOTBALL_DATA_BASE_URL` | Optional (default `https://api.collegefootballdata.com`).
| `CFBD_REQUEST_TIMEOUT` | Optional timeout (seconds, default `30`).

Railway handles `PORT`; do **not** set it manually.

### Dependencies & Local Run
```
pip install -r requirements.txt  # located in mcp/collegefootballdata
uvicorn main:app --reload --port 8080
```

### Tool Catalogue
| Tool | Endpoint | Notes |
| --- | --- | --- |
| `games` | `GET /games` | Schedule/results by season/week/team. |
| `lines` | `GET /lines` | Betting lines attached to games. |
| `games_teams` | `GET /games/teams` | Team box score stats. |
| `games_players` | `GET /games/players` | Player box score stats. |
| `teams` | `GET /teams` | Team metadata. |
| `calendar` | `GET /calendar` | Season weeks window. |
| `scoreboard` | `GET /scoreboard` | Live snapshot (still intermittently 502 from CFBD). |
| `stats_season` | `GET /stats/season` | Season-level stats. |
| `stats_game` | `GET /stats/game` | Game stats (currently 500 upstream). |
| `ratings_sp_plus` | `GET /ratings/sp+` | SP+ ratings (500 upstream). |
| `ratings_massey` | `GET /ratings/massey` | Massey ratings (500 upstream). |
| `ratings_sagarin` | `GET /ratings/sagarin` | Sagarin ratings (500 upstream). |
| `recruiting_teams` | `GET /recruiting/teams` | Team recruiting. |
| `recruiting_players` | `GET /recruiting/players` | Player recruiting. |
| `venues` | `GET /venues` | Venue metadata. |
| `conferences` | `GET /conferences` | Conference metadata. |

Example invoke payload:
```
POST /tools/games/invoke
{ "params": { "year": 2024, "week": 1, "seasonType": "regular" } }
```

### Deployment Notes (Railway)
- Build: `pip install -r requirements.txt`
- Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Healthcheck path: `/health` (ensure Railway health check path is exactly `/health`, not `GET /health`).
- Service variables: only `COLLEGE_FOOTBALL_DATA_API_KEY`.

Recent regression run (`python cfbd_mcp_test/run_tests.py`) stores artifacts under `cfbd_mcp_test/results/<timestamp>/`. Latest run `20250919T002338Z` shows all core tooling working; persistent upstream errors remain only on `scoreboard` (502) and ratings/stats endpoints (500).
Additional targeted example: `python cfbd_mcp_test/team_stats_example.py --team-id 133 --year 2024` (writes season + game-by-game stats under `cfbd_mcp_test/results/`). This runs against the Railway MCP deployment (`https://collegefootballdatamcp-production.up.railway.app`) via `cfbd_mcp_test/client.py`, so the artifacts under `cfbd_mcp_test/results/team_133_stats_<timestamp>/` are MCP-sourced.

---

## SportsGameOdds MCP (scaffold only)

**Source:** `mcp/sportsgameodds`

> Not deployed yet. FastAPI structure mirrors the CFBD service, but we need to finish configuration, health checks, and testing before pushing.

### Current Code Layout
```
mcp/sportsgameodds/
  config.py        # Pydantic settings (SPORTSGAMEODDS_API_KEY, etc.)
  sgo_client.py    # AsyncClient with X-API-Key header
  tools.py         # ToolSpec registry (sports, leagues, bookmakers, bet_types, stats, events)
  main.py          # FastAPI app => /health, /tools, /tools/{name}/invoke
```

### scripts/nfl_sgo_snapshot.py (MCP helper)

- Location: `scripts/nfl_sgo_snapshot.py`; calls the Railway-hosted SportsGameOdds MCP `/tools/events/invoke` endpoint.
- Flow: prompts for an MM/DD/YYYY date, builds the ET day window, paginates the MCP response (default `limit=1` during troubleshooting), and retries on upstream 429/502 with conservative backoff (12s pre-call delay, 90s between retries, up to 8 attempts).
- Output: writes a consolidated `events.json`, one JSON per matchup under `artifacts/nfl/<MM-DD-YYYY>/games/`, and a matchup-organised `summary.md`. Each game file preserves the full MCP payload as `raw_event` so every odds market/prop is captured.
- Rate limits: honours the shared SportsGameOdds free-tier (10 requests/min). Even with built-in spacing you may need to wait a full minute between runs if others are testing the MCP.
- Example: `python scripts/nfl_sgo_snapshot.py` -> enter `09/21/2025` -> outputs in `artifacts/nfl/09-21-2025/` (e.g. `games/game-1-pit-at-ne.json` is ~740 KB with all markets).

- Archived sample: see `docs/mcp/examples/sgo_snapshot/` (contains the script snapshot, `events-20250921.json`, and `game-1-pit-at-ne.json`).
- Archived NFL day-capture run (direct API): `docs/mcp/examples/nfl_day_capture/` (script + events/team_stats/meta for 09/21/2025).
- Archived NCAAF day-capture run: `docs/mcp/examples/ncaaf_day_capture/`.
- Usage checker (key health): `docs/mcp/examples/sgo_usage/` (scans `.env.local` and calls `/account/usage`).


### TODO Before Deploying
1. **Health Check** – Railway logs show requests hitting `/GET%20/health` when misconfigured. Set path to `/health` without the verb.
2. **Environment variable validation** – Address the pydantic warning (V2 renamed `allow_population_by_field_name` -> `populate_by_name`). Update config accordingly.
3. **Testing harness** – Replicate `cfbd_mcp_test` for SportsGameOdds once deployed.
4. **Provider coverage** – Confirm required endpoints (`/sports`, `/leagues`, `/bookmakers`, `/bet-types`, `/stats`, `/events`) match project requirements.

Once ready, deployment steps mirror CFBD: `pip install -r requirements.txt`, `uvicorn main:app --host 0.0.0.0 --port $PORT`, service variable `SPORTSGAMEODDS_API_KEY`, health path `/health`.

---

## Troubleshooting Cheat Sheet
- **401 Unauthorized (CFBD)** – Key expired/revoked; update env var and redeploy.
- **502 Bad Gateway (CFBD)** – Cloudflare host error; capture Ray ID, notify CFBD.
- **500 Internal Server Error** – Upstream bug (ratings/stats). Record timestamp, escalate if persistent.
- **Timeouts** – Upstream slow/unreachable; retry or check provider status.
- **400 errors (SGO)** – Review `docs/sgo_docs` reference for valid IDs.
- **Railway health check 404** – Ensure the health path is `/health` (no verb, no protocol).

## Maintenance Checklist
- Confirm Railway env vars before deploy.
- Run `python -m compileall mcp/<service>` after edits.
- Execute `python cfbd_mcp_test/run_tests.py` after each CFBD deploy; create an analogous suite for SportsGameOdds when live.
- Archive provider outage details in `cfbd_mcp_test/results/` for support tickets.

## Next Steps
- Finish deploying SportsGameOdds MCP (fix health check, Pydantic warning, add testing).
- Consider retry/backoff for transient provider 5xx responses.
- Capture provider Ray IDs/timestamps in logs to simplify escalation.
- Extend tool registries as new endpoints or sports are required.
- ESPN stats POC (teams + players): `docs/mcp/examples/espn_nfl_stats/` (ready to convert into a dedicated MCP).
---

## ESPN MCP (prototype)

**Source:** mcp/espn

> Proof-of-concept service wrapping ESPN NFL endpoints. Provides team metadata, season stats, and recent game/player box scores.

### Current Code Layout
`
mcp/espn/
  config.py        # Settings for ESPN site/core base URLs and request timeout
  espn_client.py   # Shared async client with rate-friendly headers
  utils.py         # Normalisers for team metadata, season stats, and box score summaries
  tools.py         # Tool registry (team_meta, team_season_stats, team_recent_games, team_recent_players)
  main.py          # FastAPI app => /health, /tools, /tools/{name}/invoke
`

### Tools
| Tool | Description |
| --- | --- |
| 	eam_meta | Returns ESPN team metadata (logos, venue, reference links). |
| 	eam_season_stats | Flattened season metrics (offense/defense/special teams) via ESPN splits. |
| 	eam_recent_games | Recent completed games with team/opponent totals. |
| 	eam_recent_players | Recent completed games with per-player box scores (passing, rushing, defense, ST). |

See docs/mcp/examples/espn_nfl_stats/ for the snapshot helper and sample outputs (season 2025, team 22).
