#!/usr/bin/env python3
"""Load ESPN NFL teams into the sports database."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict

import mysql.connector

TEAMS_JSON = Path("mappings/data/teams/nfl/espn/teams.json")
LEAGUE_ID = "NFL"
LEAGUE_NAME = "National Football League"

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "tramway.proxy.rlwy.net"),
    "port": int(os.getenv("DB_PORT", "23052")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASS", "PFWnChSxWZNWRoBjsjcuniWPrKhLNsdh"),
    "database": os.getenv("DB_NAME", "sports"),
}


def load() -> Dict[str, Dict[str, str]]:
    data = json.loads(TEAMS_JSON.read_text(encoding="utf-8"))
    teams: Dict[str, Dict[str, str]] = {}
    for row in data:
        if not isinstance(row, dict):
            continue
        team_id = str(row.get("id"))
        if not team_id:
            continue
        teams[team_id] = {
            "display_name": row.get("displayName") or row.get("name") or "",
            "location": row.get("location") or "",
            "nickname": row.get("name") or "",
            "abbr": row.get("abbreviation") or "",
        }
    return teams


def ensure_league(conn) -> None:
    sql = (
        "INSERT INTO leagues (league_id, display_name) VALUES (%s, %s) "
        "ON DUPLICATE KEY UPDATE display_name = VALUES(display_name), updated_at_utc = CURRENT_TIMESTAMP"
    )
    with conn.cursor() as cur:
        cur.execute(sql, (LEAGUE_ID, LEAGUE_NAME))
        conn.commit()


def upsert(conn, teams: Dict[str, Dict[str, str]]) -> None:
    sql = (
        "INSERT INTO teams (team_id, league_id, display_name, location, nickname, abbr) "
        "VALUES (%s, %s, %s, %s, %s, %s) "
        "ON DUPLICATE KEY UPDATE display_name = VALUES(display_name), location = VALUES(location), "
        "nickname = VALUES(nickname), abbr = VALUES(abbr), updated_at_utc = CURRENT_TIMESTAMP"
    )
    with conn.cursor() as cur:
        inserted = updated = 0
        for team_id, fields in teams.items():
            cur.execute(
                sql,
                (
                    team_id,
                    LEAGUE_ID,
                    fields.get("display_name"),
                    fields.get("location"),
                    fields.get("nickname"),
                    fields.get("abbr"),
                ),
            )
            if cur.rowcount == 1:
                inserted += 1
            else:
                updated += 1
        conn.commit()
    print(f"Teams inserted: {inserted}, updated: {updated}")


def main() -> None:
    teams = load()
    if not teams:
        print("No teams found in JSON; aborting.")
        return
    conn = mysql.connector.connect(**DB_CONFIG)
    try:
        ensure_league(conn)
        upsert(conn, teams)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
