#!/usr/bin/env python3
"""Load SportsGameOdds player provider links (skill positions) into the DB."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict

import mysql.connector

CROSSWALK_PATH = Path("mappings/data/players/crosswalks/nfl_sgo_to_espn.json")
PROVIDER = "sportsgameodds"

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "tramway.proxy.rlwy.net"),
    "port": int(os.getenv("DB_PORT", "23052")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASS", "PFWnChSxWZNWRoBjsjcuniWPrKhLNsdh"),
    "database": os.getenv("DB_NAME", "sports"),
}


def load_crosswalk(path: Path) -> Dict[str, Dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError("Crosswalk file must contain a dict of mapping entries")
    return data


def upsert_links(conn, crosswalk: Dict[str, Dict[str, str]]) -> None:
    sql = (
        "INSERT INTO player_provider_link (player_id, provider, provider_entity_id) "
        "VALUES (%s, %s, %s) "
        "ON DUPLICATE KEY UPDATE player_id = VALUES(player_id), fetched_at_utc = CURRENT_TIMESTAMP"
    )
    with conn.cursor() as cur:
        inserted = updated = 0
        for entry in crosswalk.values():
            espn_pid = entry.get("espn_player_id")
            sgo_pid = entry.get("sgo_player_id")
            if not espn_pid or not sgo_pid:
                continue
            cur.execute(sql, (f"espn:{espn_pid}", PROVIDER, sgo_pid))
            if cur.rowcount == 1:
                inserted += 1
            else:
                updated += 1
        conn.commit()
    print(f"Player provider links inserted: {inserted}, updated: {updated}")


def main() -> None:
    crosswalk = load_crosswalk(CROSSWALK_PATH)
    conn = mysql.connector.connect(**DB_CONFIG)
    try:
        upsert_links(conn, crosswalk)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
