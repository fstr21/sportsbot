#!/usr/bin/env python3
"""Load NCAAF conferences and team assignments into the database."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

import mysql.connector

DATA_PATH = Path("mappings/data/teams/ncaaf/conferences.json")
LEAGUE_ID = "NCAAF"

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "tramway.proxy.rlwy.net"),
    "port": int(os.getenv("DB_PORT", "23052")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASS", "PFWnChSxWZNWRoBjsjcuniWPrKhLNsdh"),
    "database": os.getenv("DB_NAME", "sports"),
}


def slug_to_team_id(name: str) -> str:
    text = name.lower().replace("&", "and")
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return f"ncaaf:{text}"


def load_conference_payload() -> List[Dict[str, str]]:
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise RuntimeError("Conference payload must be a list")
    return payload


def ensure_league(cur) -> None:
    sql = (
        "INSERT INTO leagues (league_id, display_name) VALUES (%s, %s) "
        "ON DUPLICATE KEY UPDATE display_name = VALUES(display_name), updated_at_utc = CURRENT_TIMESTAMP"
    )
    cur.execute(sql, (LEAGUE_ID, "College Football (FBS)"))


def upsert_conferences(cur, conferences: List[Dict[str, str]]) -> Tuple[int, int]:
    sql = (
        "INSERT INTO conferences (conference_id, league_id, display_name, short_name, subdivision) "
        "VALUES (%s, %s, %s, %s, %s) "
        "ON DUPLICATE KEY UPDATE display_name = VALUES(display_name), short_name = VALUES(short_name), "
        "subdivision = VALUES(subdivision), updated_at_utc = CURRENT_TIMESTAMP"
    )
    inserted = updated = 0
    for conf in conferences:
        cur.execute(
            sql,
            (
                conf["conference_id"],
                conf.get("league_id", LEAGUE_ID),
                conf.get("display_name"),
                conf.get("short_name"),
                conf.get("subdivision"),
            ),
        )
        if cur.rowcount == 1:
            inserted += 1
        else:
            updated += 1
    return inserted, updated


def upsert_teams(cur, conferences: List[Dict[str, str]]) -> Tuple[int, int, List[str]]:
    sql = (
        "INSERT INTO teams (team_id, league_id, display_name, location, nickname, abbr, conference_id) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s) "
        "ON DUPLICATE KEY UPDATE display_name = VALUES(display_name), conference_id = VALUES(conference_id), "
        "updated_at_utc = CURRENT_TIMESTAMP"
    )
    inserted = updated = 0
    warnings: List[str] = []
    for conf in conferences:
        conf_id = conf["conference_id"]
        for team_name in conf.get("teams", []):
            team_id = slug_to_team_id(team_name)
            cur.execute(
                sql,
                (
                    team_id,
                    LEAGUE_ID,
                    team_name,
                    None,
                    None,
                    None,
                    conf_id,
                ),
            )
            if cur.rowcount == 1:
                inserted += 1
            else:
                updated += 1
    return inserted, updated, warnings


def main() -> None:
    conferences = load_conference_payload()
    conn = mysql.connector.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cur:
            ensure_league(cur)
            conf_inserted, conf_updated = upsert_conferences(cur, conferences)
            team_inserted, team_updated, _ = upsert_teams(cur, conferences)
        conn.commit()
    finally:
        conn.close()
    print(
        f"Conferences inserted: {conf_inserted}, updated: {conf_updated}. "
        f"Teams inserted: {team_inserted}, updated: {team_updated}."
    )


if __name__ == "__main__":
    main()
