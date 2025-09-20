#!/usr/bin/env python3
"""Load NFL skill-position player memberships from ESPN roster exports."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

import mysql.connector

ESPN_PLAYERS_DIR = Path("mappings/data/players/nfl/espn")
SKILL_POSITIONS = {"QB", "RB", "WR", "TE"}
NFL_LEAGUE_ID = "NFL"

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "tramway.proxy.rlwy.net"),
    "port": int(os.getenv("DB_PORT", "23052")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASS", "PFWnChSxWZNWRoBjsjcuniWPrKhLNsdh"),
    "database": os.getenv("DB_NAME", "sports"),
}


def load_rosters() -> Dict[str, List[Tuple[str, str]]]:
    """Return mapping of team_id -> list of (player_id, position)."""
    rosters: Dict[str, List[Tuple[str, str]]] = {}
    for path in ESPN_PLAYERS_DIR.glob("*.json"):
        team_id = path.stem  # filenames are ESPN team IDs
        data = json.loads(path.read_text(encoding="utf-8"))
        players: List[Tuple[str, str]] = []
        for row in data:
            if not isinstance(row, dict):
                continue
            position = (row.get("position") or "").upper()
            if position not in SKILL_POSITIONS:
                continue
            pid = row.get("id")
            if not pid:
                continue
            players.append((f"espn:{pid}", position))
        rosters[team_id] = players
    return rosters


def fetch_existing_player_ids(cur) -> set[str]:
    cur.execute("SELECT player_id FROM players WHERE league_id = %s", (NFL_LEAGUE_ID,))
    return {row[0] for row in cur.fetchall()}


def main() -> None:
    rosters = load_rosters()
    conn = mysql.connector.connect(**DB_CONFIG)
    try:
        cur = conn.cursor()
        known_players = fetch_existing_player_ids(cur)

        # flatten membership rows while skipping unknown players
        rows: List[Tuple[str, str, datetime]] = []
        missing: List[str] = []
        now = datetime.now(timezone.utc)
        for team_id, players in rosters.items():
            for player_id, _ in players:
                if player_id not in known_players:
                    missing.append(player_id)
                    continue
                rows.append((player_id, team_id, now))

        if missing:
            unique_missing = sorted(set(missing))
            print(f"Warning: {len(unique_missing)} players not in canonical table; skipping.")
            print("Sample:")
            for pid in unique_missing[:15]:
                print(f"  {pid}")

        print(f"Prepared {len(rows)} membership rows for {len(rosters)} teams.")

        if rows:
            # clear existing NFL memberships to avoid duplicates
            cur.execute(
                "DELETE pm FROM player_membership pm "
                "JOIN players p ON p.player_id = pm.player_id "
                "WHERE p.league_id = %s",
                (NFL_LEAGUE_ID,),
            )
            print(f"Deleted {cur.rowcount} existing NFL membership rows.")

            insert_sql = (
                "INSERT INTO player_membership (player_id, team_id, start_utc, end_utc) "
                "VALUES (%s, %s, %s, NULL)"
            )
            cur.executemany(insert_sql, rows)
            print(f"Inserted {cur.rowcount} memberships.")

        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    main()
