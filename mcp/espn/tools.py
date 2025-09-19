"""Tool definitions for the ESPN MCP service."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable

from fastapi import HTTPException

from .espn_client import ESPNClient, ESPNClientError, get_client
from .utils import (
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
            description="Fetch player box scores for recent completed games.",
        ),
    ]
}


def list_tools() -> Iterable[ToolSpec]:
    return TOOLS.values()


async def invoke_tool(name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    spec = TOOLS.get(name)
    if not spec:
        raise HTTPException(status_code=404, detail=f"Unknown tool '{name}'")

    try:
        client = await get_client()
        if spec.method == "team_meta":
            return await _handle_team_meta(client, params)
        if spec.method == "team_season_stats":
            return await _handle_team_season_stats(client, params)
        if spec.method == "team_recent_games":
            return await _handle_team_recent_games(client, params)
        if spec.method == "team_recent_players":
            return await _handle_team_recent_players(client, params)
    except ESPNClientError as err:
        raise HTTPException(status_code=502, detail=str(err)) from err

    raise HTTPException(status_code=500, detail=f"Unhandled tool '{name}'")


def _parse_team_params(params: Dict[str, Any]) -> Dict[str, int]:
    try:
        team_id = int(params.get("teamId"))
        season = int(params.get("season"))
    except (TypeError, ValueError) as err:
        raise HTTPException(status_code=400, detail="teamId and season must be integers") from err
    if team_id <= 0:
        raise HTTPException(status_code=400, detail="teamId must be positive")
    if season <= 1900:
        raise HTTPException(status_code=400, detail="season must be > 1900")
    return {"teamId": team_id, "season": season}


async def _handle_team_meta(client: ESPNClient, params: Dict[str, Any]) -> Dict[str, Any]:
    parsed = _parse_team_params(params)
    team_meta = await fetch_team_metadata(client, parsed["teamId"], parsed["season"])
    return {
        "tool": "team_meta",
        "params": parsed,
        "data": team_meta,
    }


async def _handle_team_season_stats(client: ESPNClient, params: Dict[str, Any]) -> Dict[str, Any]:
    parsed = _parse_team_params(params)
    team_meta = await fetch_team_metadata(client, parsed["teamId"], parsed["season"])
    stats = await fetch_team_statistics(client, team_meta)
    return {
        "tool": "team_season_stats",
        "params": parsed,
        "data": stats,
    }


async def _collect_recent_games(
    client: ESPNClient,
    team_id: int,
    season: int,
    game_limit: int,
) -> Dict[str, Any]:
    schedule = await fetch_team_schedule(client, team_id, season)
    parsed_games = [parse_game_event(event, team_id) for event in schedule]
    completed_games = [g for g in parsed_games if g.get("status") == "STATUS_FINAL"]
    completed_games.sort(key=lambda game: game.get("date") or "")
    recent_games = completed_games[-game_limit:]

    game_details = []
    for game in recent_games:
        summary = await fetch_game_summary(client, game["gameId"])
        game_details.append(summarize_game(summary, team_id))

    return {
        "games": game_details,
        "teamGames": build_team_games(game_details),
        "playerGames": build_player_games(game_details),
    }


def _parse_game_limit(params: Dict[str, Any]) -> int:
    try:
        limit = int(params.get("gameLimit", 3))
    except (TypeError, ValueError) as err:
        raise HTTPException(status_code=400, detail="gameLimit must be an integer") from err
    if limit <= 0:
        raise HTTPException(status_code=400, detail="gameLimit must be positive")
    return min(limit, 10)


async def _handle_team_recent_games(client: ESPNClient, params: Dict[str, Any]) -> Dict[str, Any]:
    parsed = _parse_team_params(params)
    limit = _parse_game_limit(params)
    games_payload = await _collect_recent_games(client, parsed["teamId"], parsed["season"], limit)
    return {
        "tool": "team_recent_games",
        "params": {**parsed, "gameLimit": limit},
        "data": games_payload["teamGames"],
    }


async def _handle_team_recent_players(client: ESPNClient, params: Dict[str, Any]) -> Dict[str, Any]:
    parsed = _parse_team_params(params)
    limit = _parse_game_limit(params)
    games_payload = await _collect_recent_games(client, parsed["teamId"], parsed["season"], limit)
    return {
        "tool": "team_recent_players",
        "params": {**parsed, "gameLimit": limit},
        "data": games_payload["playerGames"],
    }
