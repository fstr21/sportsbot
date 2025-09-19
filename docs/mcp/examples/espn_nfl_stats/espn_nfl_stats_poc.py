#!/usr/bin/env python3
"""Experimental ESPN NFL stats snapshot (teams + players)."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import requests

ETC = {
    "regular": 2,
    "postseason": 3,
    "preseason": 1,
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


def fetch_team_statistics(team_meta: Dict[str, Any], season_type: str) -> Dict[str, Any]:
    stats_ref = team_meta.get("statistics", {}).get("$ref")
    if not stats_ref:
        return {}
    # stats_ref already includes season type (e.g., types/2 for regular)
    stats_data = get_json(stats_ref)
    categories = stats_data.get("splits", {}).get("categories", [])
    flattened: Dict[str, Dict[str, Any]] = {}
    for category in categories:
        for stat in category.get("stats", []):
            name = stat.get("name")
            if not name:
                continue
            flattened[name] = {
                "displayName": stat.get("displayName"),
                "displayValue": stat.get("displayValue"),
                "value": stat.get("value"),
                "rank": stat.get("rank"),
                "category": category.get("name"),
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
    game_id = event.get("id")
    competition = (event.get("competitions") or [{}])[0]
    competitors = competition.get("competitors", [])
    team_comp = None
    opp_comp = None
    for comp in competitors:
        comp_team = comp.get("team", {})
        if comp_team.get("id") == str(team_id):
            team_comp = comp
        else:
            opp_comp = comp
    date = competition.get("date") or event.get("date")
    status = competition.get("status", {}).get("type", {}).get("name")
    return {
        "gameId": game_id,
        "date": date,
        "status": status,
        "team": team_comp,
        "opponent": opp_comp,
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
    result: Dict[str, Any] = {
        "name": group_entry.get("name"),
        "text": group_entry.get("text"),
        "athletes": [],
    }
    keys = group_entry.get("keys", [])
    labels = group_entry.get("labels", [])
    totals = group_entry.get("totals")
    if isinstance(totals, list):
        total_map: Dict[str, Any] = {}
        for idx, key in enumerate(keys):
            value = totals[idx] if idx < len(totals) else None
            total_map[key] = {"label": labels[idx] if idx < len(labels) else key, "value": value}
        result["totals"] = total_map
    for athlete_meta in group_entry.get("athletes", []):
        athlete = athlete_meta.get("athlete", {})
        stats_values = athlete_meta.get("stats", [])
        stat_map: Dict[str, Any] = {}
        for idx, key in enumerate(keys):
            value = stats_values[idx] if idx < len(stats_values) else None
            stat_map[key] = {"label": labels[idx] if idx < len(labels) else key, "value": value}
        result["athletes"].append({
            "id": athlete.get("id"),
            "displayName": athlete.get("displayName"),
            "position": athlete.get("position", {}).get("abbreviation"),
            "statistics": stat_map,
            "links": athlete.get("links"),
            "teamStarter": athlete_meta.get("teamStarter"),
        })
    return result


def summarize_game(summary: Dict[str, Any], team_id: int) -> Dict[str, Any]:
    header = summary.get("header", {})
    comp = (header.get("competitions") or [{}])[0]
    date = comp.get("date")
    attendance = comp.get("attendance")
    game_id = comp.get("id")

    box = summary.get("boxscore", {})
    team_entries = box.get("teams", [])
    players_entries = box.get("players", [])

    team_stats_map = {}
    for team in team_entries:
        tid = team.get("team", {}).get("id")
        team_stats_map[tid] = summarize_team_stats(team)

    player_stats_map = {}
    for group in players_entries:
        tid = group.get("team", {}).get("id")
        player_stats_map[tid] = [summarize_player_stats(stat_group) for stat_group in group.get("statistics", [])]

    tid_str = str(team_id)
    opp_entry = next((team for team in team_entries if team.get("team", {}).get("id") != tid_str), None)

    return {
        "gameId": game_id,
        "date": date,
        "attendance": attendance,
        "teamStats": team_stats_map.get(tid_str),
        "opponentStats": team_stats_map.get(opp_entry.get("team", {}).get("id")) if opp_entry else None,
        "teamPlayerStats": player_stats_map.get(tid_str),
        "opponentPlayerStats": player_stats_map.get(opp_entry.get("team", {}).get("id")) if opp_entry else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--team-id", type=int, default=22, help="ESPN team id (default: 22 for Arizona)")
    parser.add_argument("--season", type=int, default=datetime.now().year, help="Season year (default: current year)")
    parser.add_argument("--season-type", choices=list(ETC.keys()) + ["both"], default="regular")
    parser.add_argument("--game-limit", type=int, default=3, help="How many recent games to fetch summaries for")
    parser.add_argument("--output", type=Path, default=Path("espn_nfl_stats_output"))
    args = parser.parse_args()

    output_dir = args.output
    output_dir.mkdir(parents=True, exist_ok=True)

    team_meta = fetch_team_metadata(args.team_id, args.season)
    season_stats = fetch_team_statistics(team_meta, args.season_type)

    schedule = fetch_team_schedule(args.team_id, args.season)
    parsed_games = [parse_game_event(event, args.team_id) for event in schedule]

    completed_games = [g for g in parsed_games if g.get("status") == "STATUS_FINAL"]
    completed_games.sort(key=lambda g: g.get("date") or "")
    recent_games = completed_games[-args.game_limit:]

    game_details = []
    for game in recent_games:
        summary = fetch_game_summary(game["gameId"])
        game_details.append(summarize_game(summary, args.team_id))

    team_output = {
        "team": team_meta,
        "seasonStats": season_stats,
        "recentGames": {
            "count": len(game_details),
            "games": game_details,
        },
    }

    (output_dir / f"team_{args.team_id}_meta.json").write_text(json.dumps(team_meta, indent=2), encoding="utf-8")
    (output_dir / f"team_{args.team_id}_season_stats.json").write_text(json.dumps(season_stats, indent=2), encoding="utf-8")
    (output_dir / f"team_{args.team_id}_recent_games.json").write_text(json.dumps(game_details, indent=2), encoding="utf-8")
    (output_dir / f"team_{args.team_id}_summary.json").write_text(json.dumps(team_output, indent=2), encoding="utf-8")

    print(f"Saved ESPN stats snapshot for team {args.team_id} -> {output_dir.as_posix()}")


if __name__ == "__main__":
    main()
