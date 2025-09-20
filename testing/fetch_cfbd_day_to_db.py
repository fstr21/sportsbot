#!/usr/bin/env python3
"""Fetch CFBD games for 09/20/2025 via MCP and upsert into the sports DB."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import mysql.connector
import requests
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

REPO_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = REPO_ROOT / ".env.local"
CONFERENCES_DOC = REPO_ROOT / "docs" / "ncaaf_conferences.md"
OUTPUT_ROOT = Path(__file__).resolve().parent / "cfbd_2025-09-20"
TARGET_DATE = date(2025, 9, 20)
ET_TZ = ZoneInfo("America/New_York")
UTC_TZ = ZoneInfo("UTC")
DEFAULT_MCP_BASE = "https://collegefootballdatamcp-production.up.railway.app"


@dataclass
class CalendarSlot:
    season: int
    week: int
    season_type: str
    start: datetime
    end: datetime

    def contains(self, target: date) -> bool:
        return self.start.date() <= target <= self.end.date()


@dataclass
class GameRecord:
    game_id: int
    season: int
    week: int
    season_type: str
    kickoff_utc: datetime
    kickoff_et: datetime
    venue: Optional[str]
    home_team: str
    away_team: str
    completed: bool
    raw: Dict[str, Any]


class SnapshotError(RuntimeError):
    """Raised when required data slices cannot be satisfied."""


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key:
            continue
        value = value.strip().strip('"')
        os.environ.setdefault(key, value)


def load_allowed_teams() -> Set[str]:
    if not CONFERENCES_DOC.exists():
        raise SnapshotError(f"Conference reference missing: {CONFERENCES_DOC.as_posix()}")
    allowed: Set[str] = set()
    for raw_line in CONFERENCES_DOC.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("-"):
            allowed.add(line.lstrip("- "))
    if not allowed:
        raise SnapshotError("No team entries found in docs/ncaaf_conferences.md")
    return allowed


def call_mcp(tool: str, params: Dict[str, Any]) -> Any:
    base_url = os.getenv("CFBD_MCP_BASE_URL", DEFAULT_MCP_BASE).rstrip("/")
    url = f"{base_url}/tools/{tool}/invoke"
    response = requests.post(url, json={"params": params}, timeout=60)
    response.raise_for_status()
    payload = response.json()
    return payload.get("data")


def parse_calendar_entry(entry: Dict[str, Any]) -> CalendarSlot:
    def parse_ts(value: str) -> datetime:
        cleaned = value.replace("Z", "+00:00")
        return datetime.fromisoformat(cleaned).astimezone(UTC_TZ)

    return CalendarSlot(
        season=int(entry["season"]),
        week=int(entry["week"]),
        season_type=str(entry["seasonType"]),
        start=parse_ts(entry["startDate"]),
        end=parse_ts(entry["endDate"]),
    )


def resolve_calendar_slot(target: date) -> CalendarSlot:
    calendar = call_mcp("calendar", {"year": target.year})
    if not calendar:
        raise SnapshotError("Calendar endpoint returned no data")
    slots = [parse_calendar_entry(item) for item in calendar]
    for slot in slots:
        if slot.contains(target):
            return slot
    raise SnapshotError(f"No calendar slot found for {target.isoformat()}")


def parse_game(raw_game: Dict[str, Any]) -> GameRecord:
    start = raw_game.get("startDate")
    if not start:
        raise SnapshotError(f"Game {raw_game.get('id')} missing startDate")
    kickoff_utc = datetime.fromisoformat(start.replace("Z", "+00:00")).astimezone(UTC_TZ)
    kickoff_et = kickoff_utc.astimezone(ET_TZ)
    return GameRecord(
        game_id=int(raw_game["id"]),
        season=int(raw_game["season"]),
        week=int(raw_game["week"]),
        season_type=str(raw_game["seasonType"]),
        kickoff_utc=kickoff_utc,
        kickoff_et=kickoff_et,
        venue=raw_game.get("venue"),
        home_team=str(raw_game.get("homeTeam")),
        away_team=str(raw_game.get("awayTeam")),
        completed=bool(raw_game.get("completed")),
        raw=raw_game,
    )


def fetch_games(slot: CalendarSlot, allowed: Set[str]) -> Tuple[List[GameRecord], List[Dict[str, Any]]]:
    params = {"year": slot.season, "week": slot.week, "seasonType": slot.season_type}
    games = call_mcp("games", params)
    if games is None:
        raise SnapshotError("Games endpoint returned no data")
    filtered: List[GameRecord] = []
    skipped_raw: List[Dict[str, Any]] = []
    for raw_game in games:
        try:
            game = parse_game(raw_game)
        except SnapshotError:
            skipped_raw.append(raw_game)
            continue
        if game.kickoff_et.date() != TARGET_DATE:
            continue
        if game.home_team not in allowed and game.away_team not in allowed:
            skipped_raw.append(raw_game)
            continue
        filtered.append(game)
    return filtered, skipped_raw


def build_team_lookup(cur) -> Dict[str, str]:
    cur.execute("SELECT team_id, display_name FROM teams WHERE league_id = %s", ("NCAAF",))
    lookup: Dict[str, str] = {}
    for team_id, display_name in cur.fetchall():
        if display_name:
            lookup[display_name.lower()] = team_id
    return lookup


def resolve_team_id(name: str, lookup: Dict[str, str]) -> Optional[str]:
    return lookup.get(name.lower())


def upsert_games(records: List[GameRecord]) -> Dict[str, int]:
    db_config = {
        "host": os.getenv("DB_HOST", os.getenv("MYSQL_HOST", os.getenv("MYSQLHOST", "tramway.proxy.rlwy.net"))),
        "port": int(os.getenv("DB_PORT", os.getenv("MYSQL_PORT", os.getenv("MYSQLPORT", "23052")))),
        "user": os.getenv("DB_USER", os.getenv("MYSQL_USER", os.getenv("MYSQLUSER", "root"))),
        "password": os.getenv("DB_PASSWORD", os.getenv("MYSQL_PASSWORD", os.getenv("MYSQLPASSWORD", ""))),
        "database": os.getenv("DB_NAME", os.getenv("SPORTS_DB_NAME", "sports")),
    }
    public_url = os.getenv("MYSQL_PUBLIC_URL")
    if public_url:
        parsed = urlparse(public_url)
        if parsed.hostname:
            db_config["host"] = parsed.hostname
        if parsed.port:
            db_config["port"] = parsed.port
        if parsed.username:
            db_config["user"] = parsed.username
        if parsed.password:
            db_config["password"] = parsed.password
    if "railway.internal" in db_config["host"]:
        db_config["host"] = "tramway.proxy.rlwy.net"
        db_config["port"] = 23052
    conn = mysql.connector.connect(**db_config)
    try:
        cur = conn.cursor()
        lookup = build_team_lookup(cur)
        inserted = updated = skipped = 0
        for record in records:
            home_id = resolve_team_id(record.home_team, lookup)
            away_id = resolve_team_id(record.away_team, lookup)
            if not home_id or not away_id:
                skipped += 1
                continue
            event_uid = f"cfbd:{record.game_id}"
            status = "final" if record.completed else "scheduled"
            start_utc = record.kickoff_utc.astimezone(UTC_TZ).replace(tzinfo=None)
            start_et = record.kickoff_et.astimezone(ET_TZ).replace(tzinfo=None)
            cur.execute("SELECT internal_id FROM events WHERE event_uid = %s", (event_uid,))
            existing = cur.fetchone()
            if existing:
                internal_id = existing[0]
                cur.execute(
                    "UPDATE events SET season=%s, season_type=%s, week=%s, start_time_utc=%s, start_time_et=%s, status=%s, venue=%s, home_team_id=%s, away_team_id=%s WHERE internal_id=%s",
                    (
                        record.season,
                        record.season_type,
                        str(record.week),
                        start_utc,
                        start_et,
                        status,
                        record.venue,
                        home_id,
                        away_id,
                        internal_id,
                    ),
                )
                updated += 1
            else:
                cur.execute(
                    "INSERT INTO events (event_uid, league_id, season, season_type, week, start_time_utc, start_time_et, status, venue, home_team_id, away_team_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (
                        event_uid,
                        "NCAAF",
                        record.season,
                        record.season_type,
                        str(record.week),
                        start_utc,
                        start_et,
                        status,
                        record.venue,
                        home_id,
                        away_id,
                    ),
                )
                internal_id = cur.lastrowid
                inserted += 1
            cur.execute(
                "INSERT INTO event_provider_link (event_internal_id, provider, provider_entity_id) VALUES (%s, %s, %s) "
                "ON DUPLICATE KEY UPDATE fetched_at_utc = CURRENT_TIMESTAMP",
                (internal_id, "collegefootballdata", str(record.game_id)),
            )
        conn.commit()
        return {"inserted": inserted, "updated": updated, "skipped": skipped}
    finally:
        conn.close()


def save_outputs(records: List[GameRecord], skipped: List[Dict[str, Any]], db_result: Dict[str, int]) -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    raw_path = OUTPUT_ROOT / "games_filtered.json"
    with raw_path.open("w", encoding="utf-8") as handle:
        json.dump([record.raw for record in records], handle, indent=2, ensure_ascii=False)
    skipped_path = OUTPUT_ROOT / "skipped_raw.json"
    with skipped_path.open("w", encoding="utf-8") as handle:
        json.dump(skipped, handle, indent=2, ensure_ascii=False)
    summary_lines = [
        f"Target date (ET): {TARGET_DATE.strftime('%m/%d/%Y')}",
        f"Games retained: {len(records)}",
        f"Database inserted: {db_result['inserted']}",
        f"Database updated: {db_result['updated']}",
        f"Skipped (missing teams or metadata): {db_result['skipped'] + len(skipped)}",
        f"Output JSON: {raw_path.as_posix()}",
    ]
    (OUTPUT_ROOT / "summary.txt").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")


def main() -> None:
    load_env(ENV_PATH)
    allowed = load_allowed_teams()
    slot = resolve_calendar_slot(TARGET_DATE)
    games, skipped_raw = fetch_games(slot, allowed)
    if not games:
        raise SnapshotError("No games matched the conference policy on the target date")
    db_result = upsert_games(games)
    save_outputs(games, skipped_raw, db_result)
    print(
        f"Done. Inserted {db_result['inserted']} updated {db_result['updated']} (skipped {db_result['skipped']} unresolved teams)."
    )


if __name__ == "__main__":
    try:
        main()
    except SnapshotError as err:
        print(f"ERROR: {err}")
        raise SystemExit(1)

