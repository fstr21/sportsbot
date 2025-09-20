#!/usr/bin/env python3
"""Load SportsGameOdds team/provider mappings into the sports database."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict

import mysql.connector

SGO_EVENTS_PATH = Path("mappings/data/odds/nfl_sgo_events_2025-08-01_2025-09-24.json")
ESPN_TEAM_JSON = Path("mappings/data/teams/nfl/espn/teams.json")
PROVIDER = "sportsgameodds"
LEAGUE_ID = "NFL"

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "tramway.proxy.rlwy.net"),
    "port": int(os.getenv("DB_PORT", "23052")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASS", "PFWnChSxWZNWRoBjsjcuniWPrKhLNsdh"),
    "database": os.getenv("DB_NAME", "sports"),
}


def load_sgo_team_names(path: Path) -> Dict[str, str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    teams: Dict[str, str] = {}
    for event in payload.get("events", []):
        block = event.get("teams", {})
        for side in ("home", "away"):
            team = block.get(side)
            if isinstance(team, dict):
                team_id = team.get("teamID")
                names = team.get("names") if isinstance(team.get("names"), dict) else {}
                long_name = names.get("long") if isinstance(names, dict) else None
                if team_id and long_name:
                    teams.setdefault(team_id, long_name)
    return teams


def load_espn_teams(path: Path) -> Dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    mapping: Dict[str, str] = {}
    reverse = {}
    for row in data:
        if not isinstance(row, dict):
            continue
        team_id = str(row.get("id"))
        if not team_id:
            continue
        for option in (
            row.get("displayName"),
            row.get("name"),
        ):
            if option:
                reverse[option.lower()] = team_id
    for sgo_id, long_name in load_sgo_team_names(SGO_EVENTS_PATH).items():
        key = long_name.lower()
        espn_id = reverse.get(key)
        if espn_id:
            mapping[sgo_id] = espn_id
    return mapping


def upsert_team_links(conn, mapping: Dict[str, str]) -> None:
    sql = (
        "INSERT INTO team_provider_link (team_id, provider, provider_entity_id) "
        "VALUES (%s, %s, %s) "
        "ON DUPLICATE KEY UPDATE team_id=VALUES(team_id), fetched_at_utc=CURRENT_TIMESTAMP"
    )
    with conn.cursor() as cur:
        inserted = updated = 0
        for provider_entity_id, team_id in mapping.items():
            cur.execute(sql, (team_id, PROVIDER, provider_entity_id))
            if cur.rowcount == 1:
                inserted += 1
            else:
                updated += 1
        conn.commit()
    print(f"Team provider links inserted: {inserted}, updated: {updated}")


def ensure_league(conn) -> None:
    sql = (
        "INSERT INTO leagues (league_id, display_name) VALUES (%s, %s) "
        "ON DUPLICATE KEY UPDATE display_name = VALUES(display_name), updated_at_utc = CURRENT_TIMESTAMP"
    )
    with conn.cursor() as cur:
        cur.execute(sql, (LEAGUE_ID, "National Football League"))
        conn.commit()


def main() -> None:
    mapping = load_espn_teams(ESPN_TEAM_JSON)
    if not mapping:
        print("No team mappings derived; aborting.")
        return
    conn = mysql.connector.connect(**DB_CONFIG)
    try:
        ensure_league(conn)
        upsert_team_links(conn, mapping)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
