Implementing Agents in Your Sports Betting Platform (Python + MCP + Discord + Railway)

This README is a hand‑off guide you can give to an LLM (or a teammate) to build production‑ready runtime agents for your sports betting intelligence platform. It’s written for Python beginners and maps directly to your stack: Discord bot → JSON‑RPC/HTTP → Railway‑hosted MCP services → External APIs → MySQL mapping DB.

0) Goals

Turn one‑off scripts into reusable, always‑on agents.

Keep the Discord bot thin; push logic into MCP services.

Standardize task schemas, tool adapters, observability, and deployment.

1) Quick definitions

Dev‑time agent (Codex/IDE): writes/refactors code for you in VS Code.

Runtime agent (this doc): a small service that accepts a task (JSON), calls tools/APIs/DB, and returns structured results. It’s invokable by the Discord bot, schedulers, or other services.

2) Where agents live

Inside MCP services on Railway (FastAPI app exposing /agent and/or /tools/call).

Called by: Discord (slash commands), cron/schedulers (morning pipeline), or other MCPs.

3) Agent logistics (checklist)

Task schema: define a minimal, versioned JSON shape for requests/responses.

Tool adapters: thin Python functions that call external systems (e.g., SportsGameOdds MCP, ESPN, DB).

Routing logic: map task.type → call the right tools → assemble response.

FastAPI endpoint: expose /agent (and health endpoints) for callers.

Observability: request IDs, structured logs, timing, error surfaces.

Caching & rate limits: short‑term cache on hot endpoints; centralize call budgets.

Config: all secrets/URLs via env vars; no hard‑coding.

Testing harness: local CLI to run tasks against the agent.

Deployment: Railway Procfile/Dockerfile, health route, env config.

Docs: contract examples for Discord/schedulers, error codes, and playbooks.

4) Repository layout (suggested)
/agents
  /odds
    agent.py           # routing (task.type → tools)
    tools.py           # API adapters (MCP, ESPN, DB)
    service.py         # FastAPI app (POST /agent, GET /health)
    heuristics.py      # optional simple rules for summaries
    models.py          # pydantic schemas for requests/responses
    settings.py        # env var parsing & constants
    README.md          # local run & contract examples


/shared
  db.py                # MySQL connector & helpers
  logging.py           # json logger, request-id middleware


/scripts
  cli_agent.py         # run tasks from CLI for local testing


infra/
  Dockerfile
  Procfile
  railway.json         # optional
5) Environment variables

Create .env (never commit secrets):

# external services
SPORTS_API_BASE=https://sports-production-b1af.up.railway.app
SPORTS_API_KEY=your_key_if_required


# database
DB_HOST=...  
DB_PORT=3306  
DB_USER=...  
DB_PASS=...  
DB_NAME=mapping


# service
PORT=8000
LOG_LEVEL=info
CACHE_TTL_SECONDS=60
RATE_LIMIT_PER_MINUTE=120
6) Task & response schemas (pydantic)
# models.py
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


class AgentTask(BaseModel):
    version: str = "1"
    type: str  # e.g., "odds_for_game" | "player_intel" | "embed_pack"
    params: Dict[str, Any] = Field(default_factory=dict)
    request_id: Optional[str] = None


class AgentResponse(BaseModel):
    ok: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    request_id: Optional[str] = None

Include an appendix with example payloads:

// request
{
  "version": "1",
  "type": "embed_pack",
  "params": {"league_id": "NFL", "game_id": "12345"},
  "request_id": "discord-abc-123"
}


// success response
{
  "ok": true,
  "data": {"embed": {"title": "Game 12345 Odds", "fields": [...] }},
  "request_id": "discord-abc-123"
}


// error response
{ "ok": false, "error": "player_not_found", "request_id": "discord-abc-123" }
7) Tool adapters (MCP, DB, ESPN)
# tools.py
import os, json, httpx, pymysql
from typing import Any, Dict


SPORTS_API = os.getenv("SPORTS_API_BASE")
SPORTS_KEY = os.getenv("SPORTS_API_KEY")


async def call_sportsgameodds_events(params: Dict[str, Any]) -> Dict[str, Any]:
    """Call your SportsGameOdds MCP /tools/call endpoint."""
    payload = {"name": "get_sportsgameodds_events", "arguments": params}
    headers = {"Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(f"{SPORTS_API}/tools/call", json=payload, headers=headers)
        r.raise_for_status()
        res = r.json()
        # normalize the MCP envelope → return the inner data consistently
        content = res.get("content", [])
        if content and isinstance(content, list) and isinstance(content[0], dict) and "text" in content[0]:
            inner = json.loads(content[0]["text"])  # { success, data, ... }
            if inner.get("success"):  # shape defined by your MCP
                return inner.get("data", {})
            raise RuntimeError(inner.get("error", "MCP error"))
        return res  # fallback (raw)


# DB helpers


def db_conn():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )


def resolve_player(name_or_id: str):
    sql_by_id = """
        SELECT * FROM players WHERE espn_id=%s OR mlb_id=%s LIMIT 1
    """
    sql_by_name = """
        SELECT p.* FROM players p
        LEFT JOIN player_name_variations v ON v.player_id=p.id
        WHERE LOWER(p.full_name)=LOWER(%s) OR LOWER(v.name_variant)=LOWER(%s)
        LIMIT 1
    """
    with db_conn() as conn, conn.cursor() as cur:
        if name_or_id.isdigit():
            cur.execute(sql_by_id, (name_or_id, name_or_id))
            row = cur.fetchone()
            if row: return row
        cur.execute(sql_by_name, (name_or_id, name_or_id))
        return cur.fetchone()

Tip: Keep adapters thin and deterministic; add retries/backoff where appropriate.

8) Agent routing logic
# agent.py
from typing import Dict, Any
from .tools import call_sportsgameodds_events, resolve_player
from .heuristics import quicklines  # optional


async def betting_intel_agent(task: Dict[str, Any]) -> Dict[str, Any]:
    t = task.get("type")
    p = task.get("params", {})


    if t == "odds_for_game":
        league = p.get("league_id", "NFL")
        game_id = p["game_id"]
        # if your MCP supports direct by-id, call it; otherwise query a date window first
        data = await call_sportsgameodds_events({"league_id": league, "limit": 1, "id": game_id})
        return {"ok": True, "data": {"odds": data}}


    if t == "embed_pack":
        league = p.get("league_id", "NFL")
        game_id = p["game_id"]
        data = await call_sportsgameodds_events({"league_id": league, "limit": 1, "id": game_id})
        markets = data.get("markets") or data.get("odds", {})  # accommodate different shapes
        fields = []
        for m in list(markets)[:6]:
            if isinstance(m, dict):
                fields.append({"name": m.get("market", "market"), "value": str(m.get("price", "-"))})
        embed = {
            "title": f"Game {game_id} Odds",
            "description": ", ".join(quicklines({"markets": markets})) if markets else "No markets available.",
            "fields": fields
        }
        return {"ok": True, "data": {"embed": embed}}


    if t == "player_intel":
        q = p["query"]
        player = resolve_player(q)
        if not player:
            return {"ok": False, "error": "player_not_found"}
        return {"ok": True, "data": {"player": player}}


    return {"ok": False, "error": "unknown_task"}
9) FastAPI service
# service.py
import uvicorn
from fastapi import FastAPI, Request
from .models import AgentTask, AgentResponse
from .agent import betting_intel_agent


app = FastAPI()


@app.get("/health")
async def health():
    return {"ok": True}


@app.post("/agent", response_model=AgentResponse)
async def run_agent(task: AgentTask, request: Request):
    try:
        data = await betting_intel_agent(task.dict())
        return AgentResponse(ok=data.get("ok", False), data=data.get("data"), error=data.get("error"), request_id=task.request_id)
    except Exception as e:
        return AgentResponse(ok=False, error=str(e), request_id=task.request_id)


if __name__ == "__main__":
    uvicorn.run("service:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
10) Discord bot integration (slash commands)
# discord_handlers.py
import os, aiohttp
import discord
from discord import app_commands
from discord.ext import commands


AGENT_URL = os.getenv("AGENT_URL")  # e.g., https://your-railway-app.up.railway.app/agent


class Odds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="odds", description="Show odds for a game")
    @app_commands.describe(league_id="NFL/MLB/...", game_id="Provider game id")
    async def odds(self, interaction: discord.Interaction, game_id: str, league_id: str = "NFL"):
        await interaction.response.defer(thinking=True)
        payload = {"version": "1", "type": "embed_pack", "params": {"league_id": league_id, "game_id": game_id}}
        async with aiohttp.ClientSession() as s:
            async with s.post(AGENT_URL, json=payload, timeout=30) as resp:
                data = await resp.json()
        if not data.get("ok"):
            return await interaction.followup.send("Sorry, could not fetch odds.")
        e = data["data"]["embed"]
        # Simple text fallback (or create a proper discord.Embed)
        lines = [e.get("description", "")] + [f"**{f['name']}**: {f['value']}" for f in e.get("fields", [])]
        await interaction.followup.send("\n".join(lines))


async def setup(bot):
    await bot.add_cog(Odds(bot))
11) Caching & rate limits (starter)
# settings.py
import os
CACHE_TTL = int(os.getenv("CACHE_TTL_SECONDS", "60"))
RATE_LIMIT_PER_MIN = int(os.getenv("RATE_LIMIT_PER_MINUTE", "120"))

Add a simple in‑memory cache (or Redis in production). Wrap tool calls with a token‑bucket limiter if the external API has quotas.

12) Observability

Structured logs: log JSON with request_id, task.type, latency, error.

/health: lightweight readiness route for Railway.

/agent: include request_id in responses to correlate with Discord.

13) Local dev & testing

Create virtual env, install deps: pip install fastapi uvicorn httpx pymysql python-dotenv.

Run service: uvicorn agents.odds.service:app --reload.

Test with curl:

curl -X POST "$AGENT_URL/agent" \
  -H "Content-Type: application/json" \
  -d '{"version":"1","type":"embed_pack","params":{"league_id":"NFL","game_id":"12345"}}'

Run CLI harness (scripts/cli_agent.py) to send sample tasks and print responses.

14) Deploy on Railway

Containerize with Dockerfile or use Python Buildpack.

Expose port $PORT.

Set env vars in Railway dashboard (DB, API base, keys).

Add health check to /health.

Procfile (example):

web: uvicorn agents.odds.service:app --host 0.0.0.0 --port $PORT
15) Migration of existing scripts → agents

Identify reusable logic (e.g., date window creation, MCP call, market extraction).

Move that logic into tool adapters and agent routing.

Keep the original script as a test harness that now calls the agent endpoint instead of the MCP directly.

16) Error codes (suggested)

player_not_found, unknown_task, mcp_error, upstream_timeout, rate_limited, bad_params.

Return HTTP 200 with { ok:false, error:code } to keep Discord happy; log full details server‑side.

17) Security & safety

Never hard‑code keys. Use env vars.

Validate and sanitize all params (types, lengths, allowed values).

Enforce per‑route timeouts.

Add CORS rules if needed (usually callers are server‑to‑server).

18) Hand‑off prompts (use with an LLM)

You can paste these directly into Codex/ChatGPT while the repo is open in VS Code:

Prompt 1 — Create service skeleton

Create a Python package agents/odds with files agent.py, tools.py, models.py, service.py, heuristics.py, and settings.py as described in our README. Implement the /agent FastAPI endpoint and the three task types: odds_for_game, embed_pack, player_intel. Use env vars for config and add a /health route.

Prompt 2 — Tool adapter to SportsGameOdds MCP

Implement call_sportsgameodds_events(params) that POSTs to ${SPORTS_API_BASE}/tools/call with { name:"get_sportsgameodds_events", arguments: params }. Parse the MCP envelope and return { success, data } semantics.

Prompt 3 — Discord integration

Add a slash command /odds to our Discord bot that calls the agent’s embed_pack task and prints a compact text fallback with top 6 markets.

Prompt 4 — Tests & logging

Add structured JSON logging with request_id and timings around each tool call; write unit tests for resolve_player and the MCP adapter using pytest and httpx mocking.

Prompt 5 — Dockerfile/Procfile

Add a Dockerfile and Procfile suitable for Railway. Ensure the app binds to $PORT and exposes /health.

19) Next steps

Ship /odds first. Then /player (mapping + last‑5 stats). Finally, the morning pipeline as a small DAG that calls agents and persists results.

Expand the odds agent to accept league_id and reuse the same flow for MLB/CFB/NFL.

End of README — this is designed for immediate implementation by an LLM or engineer. Copy it into your repo as agents/odds/README.md and iterate.

I put a detailed, copy-pasteable README in the canvas for you. It’s tailored to your stack (Discord → JSON-RPC/HTTP → Railway MCP → external APIs → MySQL) and includes task schemas, tool adapters, FastAPI service, Discord integration, deployment, and LLM prompts to hand off.

Key parts are aligned with your project docs:

Architecture (Discord → MCP servers like MLB/NFL/CFB/Odds; external APIs incl. SportsGameOdds, ESPN; Railway MySQL schema with players/teams/variations) 

ARCHITECTURE_OVERVIEW

PROJECT_MISSION

Your current SportsGameOdds MCP calling pattern and proof-of-concept flow (date window → /tools/call → parse → critical markets)