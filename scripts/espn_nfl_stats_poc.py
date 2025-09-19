#!/usr/bin/env python3
"""Experimental ESPN NFL stats snapshot (teams + players)."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

SEASON_TYPE_MAP = {
    "preseason": 1,
    "regular": 2,
    "postseason": 3,
}

SITE_BASE = "https://site.api.espn.com/apis/site/v2/sports/football/nfl"
CORE_BASE = "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl"


def get_json(url: str, **kwargs: Any) -> Dict[str, Any]:
    resp = requests.get(url, timeout=30, **kwargs)
    resp.raise_for_status()
    return resp.json()


def fetch_team_metadata(team_id: int, season: int) -> Dict[str, Any]:
    url = f"{CORE_BASE}/seasons/{season}/teams/{team_id}?lang=en&region=us"
    return get_json(url)


def fetch_team_statistics(team_meta: Dict[str, Any]) -> Dict[str, Any]:
    stats_ref = team_meta.get("statistics", {}).get("$ref")
    if not stats_ref:
        return {}
    stats_data = get_json(stats_ref)
    categories = stats_data.get("splits", {}).get("categories", [])
    flattened: Dict[str, Dict[str, Any]] = {}
    for category in categories:
        category_name = category.get("name")
        for stat in category.get("stats", []):
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


def fetch_team_schedule(team_id: int, season: int) -> List[Dict[str, Any]]:
    url = f"{SITE_BASE}/teams/{team_id}/schedule?season={season}"
    data = get_json(url)
    return data.get("events", [])


def parse_game_event(event: Dict[str, Any], team_id: int) -> Dict[str, Any]:
    competition = (event.get("competitions") or [{}])[0]
    competitors = competition.get("competitors", [])
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


def fetch_game_summary(game_id: str) -> Dict[str, Any]:
    url = f"{SITE_BASE}/summary?event={game_id}"
    return get_json(url)


def summarize_team_stats(team_entry: Dict[str, Any]) -> Dict[str, Any]:
    stats = {}
    for item in team_entry.get("statistics", []):
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
    keys = group_entry.get("keys", [])
    labels = group_entry.get("labels", [])
    result: Dict[str, Any] = {
        "category": group_entry.get("name"),
        "title": group_entry.get("text"),
        "players": [],
    }
    totals = group_entry.get("totals")
    if isinstance(totals, list):
        total_map = {}
        for idx, key in enumerate(keys):
            total_map[key] = {
                "label": labels[idx] if idx < len(labels) else key,
                "value": totals[idx] if idx < len(totals) else None,
            }
        result["totals"] = total_map
    for athlete_meta in group_entry.get("athletes", []):
        athlete = athlete_meta.get("athlete", {})
        stats_values = athlete_meta.get("stats", [])
        stat_map = {}
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
    teams = box.get("teams", [])
    players = box.get("players", [])

    team_stats_map = {team.get("team", {}).get("id"): summarize_team_stats(team) for team in teams}
    player_stats_map = {
        group.get("team", {}).get("id"): [summarize_player_stats(stat_group) for stat_group in group.get("statistics", [])]
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


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def build_team_markdown(team_meta: Dict[str, Any], season_stats: Dict[str, Any], games: List[Dict[str, Any]]) -> str:
    lines = [
        f"# {team_meta.get('displayName', team_meta.get('name', 'Team'))} - Team Snapshot",
        "",
        "## Season Totals",
        f"Season: {season_stats.get('season')} ({season_stats.get('seasonType')})",
        f"Metrics captured: {season_stats.get('statCount', 0)}",
        "",
        "### Sample Metrics",
    ]
    sample_stats = list(season_stats.get("stats", {}).items())[:15]
    for key, val in sample_stats:
        lines.append(f"- **{val.get('displayName', key)}**: {val.get('displayValue')} (rank {val.get('rank')})")
    lines.append("")
    lines.append("## Recent Games (Team)")
    for game in games:
        lines.append(f"### Game {game.get('gameId')} - {game.get('date')}")
        team_stats = game.get("teamStats") or {}
        opp_stats = game.get("opponentStats") or {}
        for stat_key in ("totalYards", "netPassingYards", "rushingYards", "possessionTime", "firstDowns"):
            team_val = team_stats.get(stat_key, {}).get("displayValue")
            opp_val = opp_stats.get(stat_key, {}).get("displayValue")
            if team_val or opp_val:
                label = stat_key.replace("Yards", " Yards").title()
                lines.append(f"- {label}: {team_val} (team) vs {opp_val} (opponent)")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def build_player_markdown(games: List[Dict[str, Any]]) -> str:
    lines = ["# Player Box Scores", ""]
    for game in games:
        lines.append(f"## Game {game.get('gameId')} - {game.get('date')}")
        for side, title in (("teamPlayerStats", "Team Players"), ("opponentPlayerStats", "Opponent Players")):
            lines.append(f"### {title}")
            categories = game.get(side) or []
            if not categories:
                lines.append("*(no data)*")
                continue
            for category in categories:
                lines.append(f"#### {category.get('title') or category.get('category')}")
                totals = category.get("totals", {})
                if totals:
                    total_line = ", ".join(f"{meta.get('label', key)}: {meta.get('value')}" for key, meta in totals.items())
                    lines.append(f"Totals: {total_line}")
                for player in category.get("players", [])[:5]:
                    stat_line = ", ".join(f"{meta.get('label', key)}: {meta.get('value')}" for key, meta in player.get("statistics", {}).items())
                    lines.append(f"- {player.get('displayName')} ({player.get('position')}): {stat_line}")
                lines.append("")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--team-id", type=int, default=22, help="ESPN team id")
    parser.add_argument("--season", type=int, default=datetime.now().year, help="Season year")
    parser.add_argument(
        "--season-type",
        choices=list(SEASON_TYPE_MAP.keys()),
        default="regular",
        help="Season type (preseason, regular, postseason)",
    )
    parser.add_argument("--game-limit", type=int, default=3, help="Number of recent completed games to include")
    parser.add_argument("--output", type=Path, default=Path("espn_nfl_stats_output"))
    args = parser.parse_args()

    snapshot_dir = args.output / f"team_{args.team_id}_season_{args.season}"
    team_dir = snapshot_dir / "team"
    player_dir = snapshot_dir / "players"
    team_dir.mkdir(parents=True, exist_ok=True)
    player_dir.mkdir(parents=True, exist_ok=True)

    team_meta = fetch_team_metadata(args.team_id, args.season)
    season_stats = fetch_team_statistics(team_meta)

    schedule = fetch_team_schedule(args.team_id, args.season)
    parsed_games = [parse_game_event(event, args.team_id) for event in schedule]
    completed_games = [g for g in parsed_games if g.get("status") == "STATUS_FINAL"]
    completed_games.sort(key=lambda g: g.get("date") or "")
    recent_games_meta = completed_games[-args.game_limit :]

    game_details = []
    for game in recent_games_meta:
        try:
            summary = fetch_game_summary(game["gameId"])
            game_details.append(summarize_game(summary, args.team_id))
        except requests.HTTPError:
            continue

    team_games = [
        {
            "gameId": game.get("gameId"),
            "date": game.get("date"),
            "attendance": game.get("attendance"),
            "teamStats": game.get("teamStats"),
            "opponentStats": game.get("opponentStats"),
        }
        for game in game_details
    ]

    player_games = [
        {
            "gameId": game.get("gameId"),
            "date": game.get("date"),
            "teamPlayerStats": game.get("teamPlayerStats"),
            "opponentPlayerStats": game.get("opponentPlayerStats"),
        }
        for game in game_details
    ]

    write_json(team_dir / "team_meta.json", team_meta)
    write_json(team_dir / "season_stats.json", season_stats)
    write_json(team_dir / "recent_games.json", team_games)

    write_json(player_dir / "recent_games_players.json", player_games)

    summary_payload = {
        "team": team_meta,
        "seasonStats": season_stats,
        "recentGames": game_details,
    }
    write_json(snapshot_dir / "summary.json", summary_payload)

    (team_dir / "summary.md").write_text(
        build_team_markdown(team_meta, season_stats, team_games), encoding="utf-8"
    )
    (player_dir / "summary.md").write_text(build_player_markdown(player_games), encoding="utf-8")

    print(f"Saved ESPN stats snapshot for team {args.team_id} ({args.season}) -> {snapshot_dir.as_posix()}")


if __name__ == "__main__":
    main()
