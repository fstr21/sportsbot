#!/usr/bin/env python3
"""Scan SportsGameOdds event dumps for new NFL players and update the crosswalk."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

EVENTS_DIR = Path("mappings/data/odds/nfl")
CROSSWALK_PATH = Path("mappings/data/players/crosswalks/nfl_sgo_to_espn.json")
ESPN_PLAYERS_DIR = Path("mappings/data/players/nfl/espn")
ESPN_TEAMS_PATH = Path("mappings/data/teams/nfl/espn/teams.json")

SKILL_POSITIONS = {"QB", "RB", "WR", "TE"}


def normalize_name(raw: str) -> str:
    if not raw:
        return ""
    lowered = raw.lower()
    lowered = lowered.replace("'", "").replace(".", "")
    lowered = lowered.replace("-", " ")
    lowered = re.sub(r"[^a-z0-9 ]", "", lowered)
    lowered = re.sub(r"\s+", " ", lowered)
    return lowered.strip()


def load_espn_players() -> Dict[str, Dict[str, str]]:
    players: Dict[str, Dict[str, str]] = {}
    for path in ESPN_PLAYERS_DIR.glob("*.json"):
        team_id = path.stem
        data = json.loads(path.read_text(encoding="utf-8"))
        for row in data:
            if not isinstance(row, dict):
                continue
            pid = str(row.get("id"))
            if not pid:
                continue
            key = normalize_name(row.get("fullName") or row.get("displayName") or row.get("name") or "")
            if not key:
                continue
            players.setdefault(team_id, {})[key] = pid
    return players


def load_crosswalk() -> Dict[str, Dict[str, str]]:
    if CROSSWALK_PATH.exists():
        data = json.loads(CROSSWALK_PATH.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
    return {}


def load_espn_team_lookup() -> Dict[str, str]:
    data = json.loads(ESPN_TEAMS_PATH.read_text(encoding="utf-8"))
    reverse: Dict[str, str] = {}
    for row in data:
        if not isinstance(row, dict):
            continue
        tid = str(row.get("id"))
        if not tid:
            continue
        for option in (
            row.get("displayName"),
            row.get("name"),
        ):
            if option:
                reverse[option.lower()] = tid
    return reverse


def build_sgo_team_map(event_paths: Iterable[Path]) -> Dict[str, str]:
    reverse = load_espn_team_lookup()
    mapping: Dict[str, str] = {}
    for path in event_paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        teams = data.get("teams", {})
        for side in ("home", "away"):
            team = teams.get(side)
            if not isinstance(team, dict):
                continue
            team_id = team.get("teamID")
            names = team.get("names") if isinstance(team.get("names"), dict) else {}
            long_name = names.get("long") if isinstance(names, dict) else None
            if team_id and long_name and team_id not in mapping:
                mapping[team_id] = reverse.get(long_name.lower(), "")
    return mapping


def gather_sgo_players(event_paths: Iterable[Path]) -> Dict[str, Tuple[str, str]]:
    players: Dict[str, Tuple[str, str]] = {}
    for path in event_paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        roster = data.get("players")
        if not isinstance(roster, dict):
            continue
        for player_id, info in roster.items():
            if not isinstance(info, dict):
                continue
            name = info.get("name") or ""
            team_id = info.get("teamID") or ""
            players[player_id] = (name, team_id)
    return players


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync SGO players with crosswalk")
    parser.add_argument(
        "--events-dir",
        type=Path,
        default=EVENTS_DIR / "2025-09-20_2025-09-23",
        help="Directory containing SGO event JSON files",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Persist new matches into the crosswalk JSON",
    )
    args = parser.parse_args()

    event_files = sorted(p for p in args.events_dir.glob("*.json") if p.name != "manifest.json")
    if not event_files:
        print(f"No event files found in {args.events_dir}")
        return

    sgo_players = gather_sgo_players(event_files)
    team_map = build_sgo_team_map(event_files)
    espn_players = load_espn_players()
    crosswalk = load_crosswalk()

    new_matches: Dict[str, Dict[str, str]] = {}
    unmatched: Dict[str, Tuple[str, str]] = {}

    for sgo_pid, (name, sgo_team_id) in sgo_players.items():
        if sgo_pid in crosswalk or sgo_pid in new_matches:
            continue
        normalized = normalize_name(name)
        espn_team_id = team_map.get(sgo_team_id, "")
        espn_pid = None
        if espn_team_id:
            espn_pid = espn_players.get(espn_team_id, {}).get(normalized)
        if espn_pid:
            new_matches[sgo_pid] = {
                "espn_player_id": espn_pid,
                "sgo_player_id": sgo_pid,
                "name": name,
                "espn_team_id": espn_team_id,
                "sgo_team_id": sgo_team_id,
            }
        else:
            unmatched[sgo_pid] = (name, sgo_team_id)

    print(f"SGO players scanned: {len(sgo_players)}")
    print(f"New matches found: {len(new_matches)}")
    print(f"Still unmatched (total): {len(unmatched)}")

    if unmatched:
        sample = list(unmatched.items())[:25]
        print("Sample unmatched entries:")
        for pid, (name, team_id) in sample:
            print(f"  {pid} -> {name} ({team_id})")

    if new_matches and args.write:
        crosswalk.update(new_matches)
        CROSSWALK_PATH.write_text(json.dumps(crosswalk, indent=2) + "\n", encoding="utf-8")
        print(f"Crosswalk updated -> {CROSSWALK_PATH}")
        print("Run `python mappings/players/load_sgo_player_links.py` to upsert them into the DB.")
    elif new_matches:
        print("Use --write to persist these matches into the crosswalk.")


if __name__ == "__main__":
    main()
