#!/usr/bin/env python3
"""Fetch season and game-by-game stats for a CollegeFootballData team via MCP."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from client import client

RESULTS_ROOT = Path(__file__).parent / "results"


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=False), encoding="utf-8")


def fetch_team_record(team_id: int) -> Dict[str, Any]:
    cli = client()
    resp = cli.invoke("teams", {"id": team_id})
    resp.raise_for_status()
    payload = resp.json()
    data = payload.get("data") if isinstance(payload, dict) else None
    if not data:
        raise RuntimeError(f"No team found for id={team_id}")
    return data[0]


def fetch_season_stats(team_name: str, year: int, season_type: str) -> List[Dict[str, Any]]:
    cli = client()
    params = {"year": year, "team": team_name, "seasonType": season_type}
    resp = cli.invoke("stats_season", params)
    resp.raise_for_status()
    payload = resp.json()
    return payload.get("data", []) if isinstance(payload, dict) else payload


def fetch_games_team_stats(team_id: int, team_name: str, year: int, season_type: str) -> List[Dict[str, Any]]:
    cli = client()
    params = {"year": year, "team": team_name, "seasonType": season_type}
    resp = cli.invoke("games_teams", params)
    resp.raise_for_status()
    payload = resp.json()
    games = payload.get("data", []) if isinstance(payload, dict) else payload

    def stats_list_to_dict(stats: List[Dict[str, Any]]) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for item in stats or []:
            cat = item.get("category")
            val = item.get("stat")
            if cat:
                result[cat] = val
        return result

    game_entries: List[Dict[str, Any]] = []
    for game in games:
        teams = game.get("teams", [])
        team_entry = None
        opponent_entry = None
        for entry in teams:
            if entry.get("teamId") == team_id or entry.get("team") == team_name:
                team_entry = entry
            else:
                opponent_entry = entry
        if not team_entry:
            continue
        game_entries.append(
            {
                "game_id": game.get("id"),
                "team": {
                    "teamId": team_entry.get("teamId"),
                    "team": team_entry.get("team"),
                    "conference": team_entry.get("conference"),
                    "homeAway": team_entry.get("homeAway"),
                    "points": team_entry.get("points"),
                    "stats": stats_list_to_dict(team_entry.get("stats", [])),
                },
                "opponent": (
                    {
                        "teamId": opponent_entry.get("teamId"),
                        "team": opponent_entry.get("team"),
                        "conference": opponent_entry.get("conference"),
                        "homeAway": opponent_entry.get("homeAway"),
                        "points": opponent_entry.get("points"),
                        "stats": stats_list_to_dict(opponent_entry.get("stats", [])),
                    }
                    if opponent_entry
                    else None
                ),
            }
        )
    return game_entries


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--team-id", type=int, default=133, help="CollegeFootballData team id (default: 133)")
    parser.add_argument("--year", type=int, default=datetime.now().year, help="Season year (default: current year)")
    parser.add_argument(
        "--season-type",
        type=str,
        default="regular",
        choices=["regular", "postseason", "both"],
        help="Season type filter",
    )
    args = parser.parse_args()

    RESULTS_ROOT.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = RESULTS_ROOT / f"team_{args.team_id}_stats_{timestamp}"
    run_dir.mkdir(parents=True, exist_ok=True)

    team_record = fetch_team_record(args.team_id)
    team_name = team_record.get("school") or team_record.get("mascot") or str(args.team_id)

    season_stats = fetch_season_stats(team_name, args.year, args.season_type)
    games_stats = fetch_games_team_stats(args.team_id, team_name, args.year, args.season_type)

    outputs = {
        "team": team_record,
        "season": {
            "params": {"year": args.year, "seasonType": args.season_type},
            "stat_count": len(season_stats),
            "stats": season_stats,
        },
        "games": {
            "game_count": len(games_stats),
            "games": games_stats,
        },
    }

    write_json(run_dir / "team.json", team_record)
    write_json(run_dir / "season_stats.json", season_stats)
    write_json(run_dir / "game_stats.json", games_stats)
    write_json(run_dir / "summary.json", outputs)

    print(f"Team: {team_name} (ID {args.team_id})")
    print(f"Season stats retrieved: {len(season_stats)} entries")
    print(f"Game entries retrieved: {len(games_stats)}")
    print(f"Artifacts written to {run_dir.as_posix()}")


if __name__ == "__main__":
    main()
