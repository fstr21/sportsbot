"""Utility helpers for ESPN MCP tools."""

from __future__ import annotations

from typing import Any, Dict, List

from .espn_client import ESPNClient


def _strip_trailing(url: str) -> str:
    return url.rstrip("/")


async def fetch_team_metadata(client: ESPNClient, team_id: int, season: int) -> Dict[str, Any]:
    url = f"{client.core_base}/seasons/{season}/teams/{team_id}?lang=en&region=us"
    return await client.get_json(url)


async def fetch_team_statistics(client: ESPNClient, team_meta: Dict[str, Any]) -> Dict[str, Any]:
    stats_ref = team_meta.get("statistics", {}).get("$ref")
    if not stats_ref:
        return {}
    stats_data = await client.get_json(stats_ref)
    categories = stats_data.get("splits", {}).get("categories", []) or []
    flattened: Dict[str, Dict[str, Any]] = {}
    for category in categories:
        category_name = category.get("name")
        for stat in category.get("stats", []) or []:
            name = stat.get("name")
            if not name:
                continue
            flattened[name] = {
                "displayName": stat.get("displayName"),
                "displayValue": stat.get("displayValue"),
                "value": stat.get("value"),
                "rank": stat.get("rank"),
                "category": category_name,
            }
    return {
        "season": stats_data.get("season"),
        "seasonType": stats_data.get("seasonType"),
        "statCount": len(flattened),
        "stats": flattened,
    }


async def fetch_team_schedule(client: ESPNClient, team_id: int, season: int) -> List[Dict[str, Any]]:
    url = f"{client.site_base}/teams/{team_id}/schedule?season={season}"
    data = await client.get_json(url)
    return data.get("events", []) or []


def parse_game_event(event: Dict[str, Any], team_id: int) -> Dict[str, Any]:
    competition = (event.get("competitions") or [{}])[0]
    competitors = competition.get("competitors", []) or []
    status = competition.get("status", {}).get("type", {}).get("name")
    team_entry = None
    opponent_entry = None
    for comp in competitors:
        comp_team = comp.get("team", {})
        if comp_team.get("id") == str(team_id):
            team_entry = comp
        else:
            opponent_entry = comp
    return {
        "gameId": competition.get("id") or event.get("id"),
        "date": competition.get("date") or event.get("date"),
        "status": status,
        "team": team_entry,
        "opponent": opponent_entry,
    }


async def fetch_game_summary(client: ESPNClient, game_id: str) -> Dict[str, Any]:
    url = f"{client.site_base}/summary?event={game_id}"
    return await client.get_json(url)


def summarize_team_stats(team_entry: Dict[str, Any]) -> Dict[str, Any]:
    stats = {}
    for item in team_entry.get("statistics", []) or []:
        name = item.get("name")
        if not name:
            continue
        stats[name] = {
            "label": item.get("label"),
            "displayValue": item.get("displayValue"),
            "value": item.get("value"),
        }
    return stats


def summarize_player_stats(group_entry: Dict[str, Any]) -> Dict[str, Any]:
    keys = group_entry.get("keys", []) or []
    labels = group_entry.get("labels", []) or []
    result: Dict[str, Any] = {
        "category": group_entry.get("name"),
        "title": group_entry.get("text"),
        "players": [],
    }
    totals = group_entry.get("totals")
    if isinstance(totals, list):
        total_map: Dict[str, Any] = {}
        for idx, key in enumerate(keys):
            total_map[key] = {
                "label": labels[idx] if idx < len(labels) else key,
                "value": totals[idx] if idx < len(totals) else None,
            }
        result["totals"] = total_map
    for athlete_meta in group_entry.get("athletes", []) or []:
        athlete = athlete_meta.get("athlete", {})
        stats_values = athlete_meta.get("stats", []) or []
        stat_map: Dict[str, Any] = {}
        for idx, key in enumerate(keys):
            stat_map[key] = {
                "label": labels[idx] if idx < len(labels) else key,
                "value": stats_values[idx] if idx < len(stats_values) else None,
            }
        result["players"].append(
            {
                "id": athlete.get("id"),
                "displayName": athlete.get("displayName"),
                "position": athlete.get("position", {}).get("abbreviation"),
                "statistics": stat_map,
                "links": athlete.get("links"),
                "teamStarter": athlete_meta.get("teamStarter"),
            }
        )
    return result


def summarize_game(summary: Dict[str, Any], team_id: int) -> Dict[str, Any]:
    header = summary.get("header", {})
    comp = (header.get("competitions") or [{}])[0]
    box = summary.get("boxscore", {})
    teams = box.get("teams", []) or []
    players = box.get("players", []) or []

    team_stats_map = {team.get("team", {}).get("id"): summarize_team_stats(team) for team in teams}
    player_stats_map = {
        group.get("team", {}).get("id"): [summarize_player_stats(stat_group) for stat_group in group.get("statistics", []) or []]
        for group in players
    }

    tid = str(team_id)
    opponent_id = next((team.get("team", {}).get("id") for team in teams if team.get("team", {}).get("id") != tid), None)

    return {
        "gameId": comp.get("id"),
        "date": comp.get("date"),
        "attendance": comp.get("attendance"),
        "teamStats": team_stats_map.get(tid),
        "opponentStats": team_stats_map.get(opponent_id),
        "teamPlayerStats": player_stats_map.get(tid),
        "opponentPlayerStats": player_stats_map.get(opponent_id),
    }


def build_team_games(game_details: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        {
            "gameId": game.get("gameId"),
            "date": game.get("date"),
            "attendance": game.get("attendance"),
            "teamStats": game.get("teamStats"),
            "opponentStats": game.get("opponentStats"),
        }
        for game in game_details
    ]


def build_player_games(game_details: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        {
            "gameId": game.get("gameId"),
            "date": game.get("date"),
            "teamPlayerStats": game.get("teamPlayerStats"),
            "opponentPlayerStats": game.get("opponentPlayerStats"),
        }
        for game in game_details
    ]
