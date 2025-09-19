#!/usr/bin/env python3
"""ESPN MCP snapshot replicating the espn_nfl_stats POC using MCP tools."""

from __future__ import annotations

import argparse
import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from mcp.espn.espn_client import shutdown_client
from mcp.espn.tools import invoke_tool


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _format_stat_value(entry: Dict[str, Any]) -> str:
    if not entry:
        return "--"
    value = entry.get("displayValue")
    if value in (None, ""):
        value = entry.get("value")
    return "--" if value in (None, "") else str(value)


def _build_team_summary(team_meta: Dict[str, Any], season_stats: Dict[str, Any], games: List[Dict[str, Any]]) -> str:
    name = team_meta.get("displayName") or team_meta.get("name") or f"Team {team_meta.get('id', '')}"
    lines: List[str] = [f"# {name} - Team Snapshot", ""]

    lines.append("## Season Totals")
    season_ref = season_stats.get("season")
    season_type = season_stats.get("seasonType")
    lines.append(f"Season: {season_ref} ({season_type})")
    stat_count = season_stats.get("statCount") or 0
    lines.append(f"Metrics captured: {stat_count}")
    lines.append("")

    stats_map: Dict[str, Dict[str, Any]] = season_stats.get("stats", {}) or {}
    if stats_map:
        lines.append("### Sample Metrics")
        for key, entry in list(stats_map.items())[:15]:
            label = entry.get("displayName") or key
            value = entry.get("displayValue") or entry.get("value")
            rank = entry.get("rank")
            rank_text = f" (rank {rank})" if rank not in (None, "") else ""
            lines.append(f"- **{label}**: {value}{rank_text}")
        lines.append("")

    if games:
        metric_labels: List[Tuple[str, str]] = [
            ("Total Yards", "totalYards"),
            ("Net Passing Yards", "netPassingYards"),
            ("Rushing Yards", "rushingYards"),
            ("Possession Time", "possessionTime"),
            ("First Downs", "firstDowns"),
        ]
        lines.append("## Recent Games (Team)")
        for game in games:
            lines.append(f"### Game {game.get('gameId')} - {game.get('date')}")
            team_stats = game.get("teamStats") or {}
            opp_stats = game.get("opponentStats") or {}
            for label, key in metric_labels:
                team_val = _format_stat_value(team_stats.get(key, {}))
                opp_val = _format_stat_value(opp_stats.get(key, {}))
                lines.append(f"- {label}: {team_val} (team) vs {opp_val} (opponent)")
            attendance = game.get("attendance")
            if attendance is not None:
                lines.append(f"- Attendance: {attendance}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _format_totals(totals: Dict[str, Any]) -> str:
    if not totals:
        return "Totals: --"
    parts: List[str] = []
    for entry in totals.values():
        if not isinstance(entry, dict):
            continue
        label = entry.get("label") or "--"
        value = entry.get("value")
        parts.append(f"{label}: {value}")
    return "Totals: " + (", ".join(parts) if parts else "--")


def _format_player_line(player: Dict[str, Any]) -> str:
    name = player.get("displayName") or "Unknown"
    position = player.get("position") or "--"
    stats_map = player.get("statistics") or {}
    parts: List[str] = []
    for entry in stats_map.values():
        if not isinstance(entry, dict):
            continue
        label = entry.get("label") or "--"
        value = entry.get("value")
        parts.append(f"{label}: {value}")
    stats_text = ", ".join(parts) if parts else "--"
    return f"- {name} ({position}): {stats_text}"


def _format_player_groups(title: str, groups: Iterable[Dict[str, Any]]) -> List[str]:
    lines: List[str] = []
    if title:
        lines.append(title)
    for group in groups:
        group_title = group.get("title") or group.get("category") or "Unnamed Group"
        lines.append(f"#### {group_title}")
        totals_map = group.get("totals")
        lines.append(_format_totals(totals_map if isinstance(totals_map, dict) else {}))
        for player in group.get("players", []) or []:
            lines.append(_format_player_line(player))
        lines.append("")
    return lines


def _build_player_summary(team_name: str, games: List[Dict[str, Any]]) -> str:
    lines: List[str] = ["# Player Box Scores", ""]
    for game in games:
        lines.append(f"## Game {game.get('gameId')} - {game.get('date')}")
        team_groups = game.get("teamPlayerStats") or []
        opponent_groups = game.get("opponentPlayerStats") or []
        if team_groups:
            lines.append("### Team Players")
            lines.extend(_format_player_groups("", team_groups))
        if opponent_groups:
            lines.append("### Opponent Players")
            lines.extend(_format_player_groups("", opponent_groups))
        lines.append("")
    return "\n".join(line for line in lines if line is not None).rstrip() + "\n"


async def _fetch_tool(tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    payload = await invoke_tool(tool_name, params)
    return payload.get("data")


async def gather_snapshot(team_id: int, season: int, game_limit: int) -> Dict[str, Any]:
    team_meta = await _fetch_tool("team_meta", {"teamId": team_id, "season": season})
    season_stats = await _fetch_tool("team_season_stats", {"teamId": team_id, "season": season})
    recent_games = await _fetch_tool(
        "team_recent_games",
        {"teamId": team_id, "season": season, "gameLimit": game_limit},
    )
    recent_players = await _fetch_tool(
        "team_recent_players",
        {"teamId": team_id, "season": season, "gameLimit": game_limit},
    )
    await shutdown_client()
    return {
        "team_meta": team_meta,
        "season_stats": season_stats,
        "team_recent_games": recent_games,
        "player_recent_games": recent_players,
    }


def persist_snapshot(root: Path, team_id: int, season: int, data: Dict[str, Any]) -> None:
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    root.mkdir(parents=True, exist_ok=True)

    team_meta = data["team_meta"]
    season_stats = data["season_stats"]
    team_games = data["team_recent_games"] or []
    player_games = data["player_recent_games"] or []

    base_dir = root / f"team_{team_id}_season_{season}"
    team_dir = base_dir / "team"
    players_dir = base_dir / "players"
    team_dir.mkdir(parents=True, exist_ok=True)
    players_dir.mkdir(parents=True, exist_ok=True)

    _write_json(root / f"team_{team_id}_meta.json", team_meta)
    _write_json(root / f"team_{team_id}_season_stats.json", season_stats)
    _write_json(root / f"team_{team_id}_recent_games.json", team_games)

    summary_payload = {
        "team": team_meta,
        "season": season,
        "seasonStats": season_stats,
        "recentGames": {
            "count": len(team_games),
            "games": team_games,
        },
        "recentPlayers": {
            "count": len(player_games),
            "games": player_games,
        },
        "generatedAt": timestamp,
    }
    _write_json(root / f"team_{team_id}_summary.json", summary_payload)

    _write_json(team_dir / "team_meta.json", team_meta)
    _write_json(team_dir / "season_stats.json", season_stats)
    _write_json(team_dir / "recent_games.json", team_games)
    _write_json(base_dir / "summary.json", summary_payload)

    team_md = _build_team_summary(team_meta, season_stats, team_games)
    (team_dir / "summary.md").write_text(team_md, encoding="utf-8")

    _write_json(players_dir / "recent_games_players.json", player_games)
    players_md = _build_player_summary(team_meta.get("displayName", "Team"), player_games)
    (players_dir / "summary.md").write_text(players_md, encoding="utf-8")


async def async_main(args: argparse.Namespace) -> None:
    snapshot = await gather_snapshot(args.team_id, args.season, args.game_limit)
    persist_snapshot(args.output, args.team_id, args.season, snapshot)
    print(
        "Saved ESPN MCP snapshot for team"
        f" {args.team_id} ({args.season}) -> {args.output.as_posix()}"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--team-id", type=int, default=22, help="ESPN team id (default: 22)")
    parser.add_argument(
        "--season",
        type=int,
        default=datetime.now().year,
        help="Season year (default: current year)",
    )
    parser.add_argument("--game-limit", type=int, default=3, help="Recent final games to include")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("espn_nfl_stats_output"),
        help="Root directory for snapshot artefacts",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    asyncio.run(async_main(args))


if __name__ == "__main__":
    main()
