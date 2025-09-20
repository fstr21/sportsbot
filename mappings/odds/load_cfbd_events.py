#!/usr/bin/env python3
"""Load CollegeFootballData events into the canonical events table."""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict

import mysql.connector
from zoneinfo import ZoneInfo

EVENT_PATH = Path("mappings/data/odds/ncaaf/2025-09-20/events.json")
LEAGUE_ID = "NCAAF"
PROVIDER = "collegefootballdata"
ET = ZoneInfo("America/New_York")
UTC = ZoneInfo("UTC")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "tramway.proxy.rlwy.net"),
    "port": int(os.getenv("DB_PORT", "23052")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASS", "PFWnChSxWZNWRoBjsjcuniWPrKhLNsdh"),
    "database": os.getenv("DB_NAME", "sports"),
}


def load_team_lookup(cur) -> Dict[str, str]:
    cur.execute("SELECT team_id, display_name FROM teams WHERE league_id = %s", (LEAGUE_ID,))
    lookup = {}
    for team_id, display_name in cur.fetchall():
        if display_name:
            lookup[display_name.lower()] = team_id
    return lookup


def resolve_team_id(name: str, lookup: Dict[str, str]) -> str | None:
    if not name:
        return None
    return lookup.get(name.lower())


def parse_start(value: str) -> datetime:
    return datetime.fromisoformat(value)


def load_events() -> None:
    if not EVENT_PATH.exists():
        print(f"Missing event file: {EVENT_PATH}")
        return

    payload = json.loads(EVENT_PATH.read_text(encoding='utf-8'))
    games = payload.get('games') or []
    if not games:
        print('No games in payload.')
        return

    conn = mysql.connector.connect(**DB_CONFIG)
    try:
        cur = conn.cursor()
        team_lookup = load_team_lookup(cur)
        inserted = updated = skipped = 0
        for game in games:
            game_id = game.get('game_id')
            if not game_id:
                skipped += 1
                continue
            event_uid = f"cfbd:{game_id}"
            start_et_str = game.get('start_time_et')
            if not start_et_str:
                skipped += 1
                continue
            start_et = parse_start(start_et_str)
            start_utc = start_et.astimezone(UTC)
            home_name = (game.get('home') or {}).get('team')
            away_name = (game.get('away') or {}).get('team')
            home_team_id = resolve_team_id(home_name or '', team_lookup)
            away_team_id = resolve_team_id(away_name or '', team_lookup)
            if not home_team_id or not away_team_id:
                print(f"Skipping game {game_id}: could not resolve teams {home_name} vs {away_name}")
                skipped += 1
                continue

            status = payload.get('status') or 'scheduled'
            status = game.get('status') or status

            cur.execute("SELECT internal_id FROM events WHERE event_uid = %s", (event_uid,))
            row = cur.fetchone()
            if row:
                internal_id = row[0]
                cur.execute(
                    "UPDATE events SET league_id=%s, start_time_utc=%s, start_time_et=%s, status=%s, home_team_id=%s, away_team_id=%s WHERE internal_id=%s",
                    (
                        LEAGUE_ID,
                        start_utc,
                        start_et,
                        status,
                        home_team_id,
                        away_team_id,
                        internal_id,
                    ),
                )
                updated += 1
            else:
                cur.execute(
                    "INSERT INTO events (event_uid, league_id, start_time_utc, start_time_et, status, home_team_id, away_team_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (
                        event_uid,
                        LEAGUE_ID,
                        start_utc,
                        start_et,
                        status,
                        home_team_id,
                        away_team_id,
                    ),
                )
                internal_id = cur.lastrowid
                inserted += 1

            cur.execute(
                "INSERT INTO event_provider_link (event_internal_id, provider, provider_entity_id) VALUES (%s, %s, %s) "
                "ON DUPLICATE KEY UPDATE fetched_at_utc = CURRENT_TIMESTAMP",
                (internal_id, PROVIDER, str(game_id)),
            )

        conn.commit()
        print(f"Inserted {inserted} games, updated {updated} games, skipped {skipped} games")
    finally:
        conn.close()


if __name__ == '__main__':
    load_events()
