#!/usr/bin/env python3
"""Load SportsGameOdds NFL events into the canonical events table."""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict

import mysql.connector
from zoneinfo import ZoneInfo

EVENT_DIR = Path("mappings/data/odds/nfl/2025-09-20_2025-09-23")
LEAGUE_ID = "NFL"
PROVIDER = "sportsgameodds"
UTC = ZoneInfo("UTC")
ET = ZoneInfo("America/New_York")

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


def parse_start(status_block: dict) -> datetime:
    starts_at = status_block.get("startsAt") if isinstance(status_block, dict) else None
    if not starts_at:
        return datetime.now(tz=UTC)
    return datetime.fromisoformat(starts_at.replace("Z", "+00:00"))


def load_events() -> None:
    files = [p for p in EVENT_DIR.glob('*.json') if p.name != 'manifest.json']
    if not files:
        print(f"No event files found in {EVENT_DIR}")
        return

    conn = mysql.connector.connect(**DB_CONFIG)
    try:
        cur = conn.cursor()
        team_lookup = load_team_lookup(cur)
        inserted = updated = 0
        for path in files:
            data = json.loads(path.read_text(encoding='utf-8'))
            event_uid = data.get('eventID')
            if not event_uid:
                continue

            status = data.get('status') or {}
            start_time_utc = parse_start(status)
            start_time_et = start_time_utc.astimezone(ET)
            status_display = status.get('displayLong') if isinstance(status, dict) else 'scheduled'

            teams = data.get('teams') or {}
            home_block = teams.get('home') if isinstance(teams, dict) else {}
            away_block = teams.get('away') if isinstance(teams, dict) else {}
            home_name = (home_block.get('names') or {}).get('long') if isinstance(home_block, dict) else None
            away_name = (away_block.get('names') or {}).get('long') if isinstance(away_block, dict) else None
            home_team_id = resolve_team_id(home_name or '', team_lookup)
            away_team_id = resolve_team_id(away_name or '', team_lookup)

            if not home_team_id or not away_team_id:
                print(f"Warning: could not resolve teams for event {event_uid} ({home_name} vs {away_name})")
                continue

            cur.execute("SELECT internal_id FROM events WHERE event_uid = %s", (event_uid,))
            row = cur.fetchone()
            if row:
                internal_id = row[0]
                cur.execute(
                    "UPDATE events SET league_id=%s, start_time_utc=%s, start_time_et=%s, status=%s, home_team_id=%s, away_team_id=%s WHERE internal_id=%s",
                    (
                        LEAGUE_ID,
                        start_time_utc,
                        start_time_et,
                        status_display,
                        home_team_id,
                        away_team_id,
                        internal_id,
                    ),
                )
                updated += 1
            else:
                cur.execute(
                    "INSERT INTO events (event_uid, league_id, start_time_utc, start_time_et, status, home_team_id, away_team_id) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (
                        event_uid,
                        LEAGUE_ID,
                        start_time_utc,
                        start_time_et,
                        status_display,
                        home_team_id,
                        away_team_id,
                    ),
                )
                internal_id = cur.lastrowid
                inserted += 1

            cur.execute(
                "INSERT INTO event_provider_link (event_internal_id, provider, provider_entity_id) VALUES (%s, %s, %s) "
                "ON DUPLICATE KEY UPDATE fetched_at_utc = CURRENT_TIMESTAMP",
                (internal_id, PROVIDER, event_uid),
            )

        conn.commit()
        print(f"Inserted {inserted} events, updated {updated} events")
    finally:
        conn.close()


if __name__ == "__main__":
    load_events()
