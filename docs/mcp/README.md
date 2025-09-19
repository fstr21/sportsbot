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
