"""Tool definitions for the ESPN MCP service - standalone version."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable

from fastapi import HTTPException

from espn_client import ESPNClient, ESPNClientError, get_client
from utils import (
    build_player_games,
    build_team_games,
    fetch_game_summary,
    fetch_team_metadata,
    fetch_team_schedule,
    fetch_team_statistics,
    parse_game_event,
    summarize_game,
)


@dataclass(frozen=True)
class ToolSpec:
    name: str
    method: str
    description: str


TOOLS: Dict[str, ToolSpec] = {
    tool.name: tool
    for tool in [
        ToolSpec(
            name="team_meta",
            method="team_meta",
            description="Fetch ESPN team metadata for a given season (logos, venue, references).",
        ),
        ToolSpec(
            name="team_season_stats",
            method="team_season_stats",
            description="Fetch flattened season metrics for a team (offense, defense, special teams).",
        ),
        ToolSpec(
            name="team_recent_games",
            method="team_recent_games",
            description="Fetch recent completed games with team/offense/defense totals.",
        ),
        ToolSpec(
            name="team_recent_players",
            method="team_recent_players",
            description="Fetch recent completed games with per-player stat lines.",
        ),
        ToolSpec(
            name="team_summary",
            method="team_summary",
            description="Fetch comprehensive team bundle (metadata + season stats + recent games).",
        ),
    ]
}


def list_tools() -> Iterable[ToolSpec]:
    return TOOLS.values()


async def invoke_tool(tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    if tool_name not in TOOLS:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")

    tool_spec = TOOLS[tool_name]
    client = get_client()

    try:
        if tool_spec.method == "team_meta":
            return await _team_meta(client, params)
        elif tool_spec.method == "team_season_stats":
            return await _team_season_stats(client, params)
        elif tool_spec.method == "team_recent_games":
            return await _team_recent_games(client, params)
        elif tool_spec.method == "team_recent_players":
            return await _team_recent_players(client, params)
        elif tool_spec.method == "team_summary":
            return await _team_summary(client, params)
        else:
            raise HTTPException(status_code=500, detail=f"Unknown method '{tool_spec.method}'")
    except ESPNClientError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


async def _team_meta(client: ESPNClient, params: Dict[str, Any]) -> Dict[str, Any]:
    team_id = params.get("team_id", 22)
    season = params.get("season", 2024)

    metadata = await fetch_team_metadata(client, team_id, season)
    return {
        "tool": "team_meta",
        "params": {"team_id": team_id, "season": season},
        "data": metadata
    }


async def _team_season_stats(client: ESPNClient, params: Dict[str, Any]) -> Dict[str, Any]:
    team_id = params.get("team_id", 22)
    season = params.get("season", 2024)
    season_type = params.get("season_type", "regular")

    stats = await fetch_team_statistics(client, team_id, season, season_type)
    return {
        "tool": "team_season_stats",
        "params": {"team_id": team_id, "season": season, "season_type": season_type},
        "data": stats
    }


async def _team_recent_games(client: ESPNClient, params: Dict[str, Any]) -> Dict[str, Any]:
    team_id = params.get("team_id", 22)
    season = params.get("season", 2024)
    game_limit = params.get("game_limit", 5)

    schedule = await fetch_team_schedule(client, team_id, season)
    recent_games = []

    for game in schedule.get("events", [])[:game_limit]:
        event = parse_game_event(game)
        if event["status"] == "STATUS_FINAL":
            summary = await fetch_game_summary(client, event["event_id"])
            game_data = build_team_games(summary)
            recent_games.append(game_data)

    return {
        "tool": "team_recent_games",
        "params": {"team_id": team_id, "season": season, "game_limit": game_limit},
        "data": recent_games
    }


async def _team_recent_players(client: ESPNClient, params: Dict[str, Any]) -> Dict[str, Any]:
    team_id = params.get("team_id", 22)
    season = params.get("season", 2024)
    game_limit = params.get("game_limit", 5)

    schedule = await fetch_team_schedule(client, team_id, season)
    recent_games = []

    for game in schedule.get("events", [])[:game_limit]:
        event = parse_game_event(game)
        if event["status"] == "STATUS_FINAL":
            summary = await fetch_game_summary(client, event["event_id"])
            game_data = build_player_games(summary)
            recent_games.append(game_data)

    return {
        "tool": "team_recent_players",
        "params": {"team_id": team_id, "season": season, "game_limit": game_limit},
        "data": recent_games
    }


async def _team_summary(client: ESPNClient, params: Dict[str, Any]) -> Dict[str, Any]:
    team_id = params.get("team_id", 22)
    season = params.get("season", 2024)
    season_type = params.get("season_type", "regular")
    game_limit = params.get("game_limit", 5)

    # Fetch all components
    metadata = await fetch_team_metadata(client, team_id, season)
    stats = await fetch_team_statistics(client, team_id, season, season_type)

    schedule = await fetch_team_schedule(client, team_id, season)
    recent_games = []

    for game in schedule.get("events", [])[:game_limit]:
        event = parse_game_event(game)
        if event["status"] == "STATUS_FINAL":
            summary = await fetch_game_summary(client, event["event_id"])
            game_data = build_team_games(summary)
            recent_games.append(game_data)

    return {
        "tool": "team_summary",
        "params": {"team_id": team_id, "season": season, "season_type": season_type, "game_limit": game_limit},
        "data": {
            "metadata": metadata,
            "season_stats": stats,
            "recent_games": recent_games
        }
    }