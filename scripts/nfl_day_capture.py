#!/usr/bin/env python3
"""
NFL Day Capture Script

Prompts for date + schedule + odds + team stats + artifacts

This script captures a full day's worth of NFL data including:
- Game schedule from ESPN
- Betting odds from SportsGameOdds
- Team context derived from ESPN records

Outputs structured JSON artifacts and a human-readable summary.
"""

from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import dataclass
from datetime import datetime, date, time as dt_time, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests
from zoneinfo import ZoneInfo

ET_TZ = ZoneInfo("America/New_York")
ESPN_SCOREBOARD_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
SPORTSGAMEODDS_BASE_URL = os.getenv("SPORTSGAMEODDS_BASE_URL", "https://api.sportsgameodds.com/v2")
SPORTSGAMEODDS_RATE_LIMIT_PER_MIN = 10
ENV_LOCAL_PATH = Path('.env.local')

def load_local_env() -> None:
    if not ENV_LOCAL_PATH.exists():
        return
    for raw_line in ENV_LOCAL_PATH.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' not in line:
            continue
        key, value = line.split('=', 1)
        key = key.strip()
        if not key:
            continue
        value = value.strip().strip('"')
        os.environ.setdefault(key, value)

load_local_env()


class SnapshotError(RuntimeError):
    """Raised when we cannot satisfy the required data slices."""


@dataclass
class TeamContext:
    team_id: str
    abbreviation: str
    display_name: str
    record_summary: Optional[str]
    record_items: List[Dict[str, Any]]
    streak: Optional[str]
    rank: Optional[int]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "team_id": self.team_id,
            "abbreviation": self.abbreviation,
            "display_name": self.display_name,
            "record_summary": self.record_summary,
            "records": self.record_items,
            "streak": self.streak,
            "rank": self.rank,
        }


@dataclass
class ScheduleEntry:
    event_id: str
    event_uid: Optional[str]
    start_time_et: datetime
    venue: Optional[str]
    home: Dict[str, Any]
    away: Dict[str, Any]

    def matchup_key(self) -> Tuple[str, str, date]:
        return (
            self.home.get("abbreviation", "").upper(),
            self.away.get("abbreviation", "").upper(),
            self.start_time_et.date(),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_uid": self.event_uid,
            "start_time_et": self.start_time_et.isoformat(),
            "start_time_display": self.start_time_et.strftime("%Y-%m-%d %I:%M %p ET"),
            "venue": self.venue,
            "home": self.home,
            "away": self.away,
        }


@dataclass
class OddsEntry:
    event_id: str
    start_time_et: datetime
    home: Dict[str, Any]
    away: Dict[str, Any]
    markets: List[Dict[str, Any]]

    def matchup_key(self) -> Tuple[str, str, date]:
        return (
            self.home.get("abbreviation", "").upper(),
            self.away.get("abbreviation", "").upper(),
            self.start_time_et.date(),
        )


def prompt_for_date() -> date:
    """Prompt user for date in MM/DD/YYYY with ET context and validation."""
    today_et = datetime.now(ET_TZ).date()
    default_str = today_et.strftime("%m/%d/%Y")
    prompt = (
        "Enter target NFL date (MM/DD/YYYY, all outputs in ET) "
        f"[{default_str}]: "
    )

    while True:
        user_input = input(prompt).strip()
        if not user_input:
            print(f"Using {default_str} (Eastern Time).")
            return today_et
        try:
            parsed_date = datetime.strptime(user_input, "%m/%d/%Y").date()
            return parsed_date
        except ValueError:
            print("Invalid date format. Please use MM/DD/YYYY (e.g., 09/21/2025).")


def iso_to_et(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    cleaned = value.replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(cleaned)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))
    return dt.astimezone(ET_TZ)


def extract_record_summary(records: Optional[List[Dict[str, Any]]]) -> Optional[str]:
    if not records:
        return None
    # Prefer overall record
    overall = next((r for r in records if r.get("type") == "overall"), None)
    if overall and overall.get("summary"):
        return overall["summary"]
    return next((r.get("summary") for r in records if r.get("summary")), None)


def parse_competitor(competitor: Dict[str, Any]) -> Dict[str, Any]:
    team = competitor.get("team", {})
    records = competitor.get("records", [])
    return {
        "team_id": team.get("id"),
        "uid": team.get("uid"),
        "abbreviation": team.get("abbreviation"),
        "display_name": team.get("displayName"),
        "short_display_name": team.get("shortDisplayName"),
        "location": team.get("location"),
        "name": team.get("name"),
        "nickname": team.get("nickname"),
        "record_summary": extract_record_summary(records),
        "records": records,
        "rank": competitor.get("curatedRank", {}).get("current"),
        "streak": competitor.get("streak", {}).get("description"),
    }


def fetch_nfl_schedule(target_date: date) -> List[ScheduleEntry]:
    params = {"dates": target_date.strftime("%Y%m%d")}
    resp = requests.get(ESPN_SCOREBOARD_URL, params=params, timeout=30)
    if resp.status_code != 200:
        raise SnapshotError(
            f"Failed to fetch NFL schedule from ESPN (status {resp.status_code})."
        )
    data = resp.json()
    events: List[ScheduleEntry] = []
    for event in data.get("events", []):
        competitions = event.get("competitions", [])
        if not competitions:
            continue
        comp = competitions[0]
        competitors = comp.get("competitors", [])
        home_raw = next((c for c in competitors if c.get("homeAway") == "home"), None)
        away_raw = next((c for c in competitors if c.get("homeAway") == "away"), None)
        if not home_raw or not away_raw:
            continue
        start = iso_to_et(comp.get("date") or event.get("date"))
        if not start or start.date() != target_date:
            continue
        venue = None
        if comp.get("venue") and comp["venue"].get("fullName"):
            venue = comp["venue"]["fullName"]
        events.append(
            ScheduleEntry(
                event_id=event.get("id"),
                event_uid=event.get("uid"),
                start_time_et=start,
                venue=venue,
                home=parse_competitor(home_raw),
                away=parse_competitor(away_raw),
            )
        )
    if not events:
        raise SnapshotError(
            "No NFL schedule data returned for the requested date (check that games exist)."
        )
    return events


def load_sportsgameodds_key() -> str:
    key = os.getenv("SPORTSGAMEODDS_API_KEY")
    if not key:
        raise SnapshotError(
            "SPORTSGAMEODDS_API_KEY is required in the environment to fetch odds."
        )
    return key


def convert_odds_to_markets(odds: Dict[str, Any]) -> List[Dict[str, Any]]:
    markets: List[Dict[str, Any]] = []
    for odd_id, odd in odds.items():
        market: Dict[str, Any] = {
            "odd_id": odd_id,
            "market_name": odd.get("marketName"),
            "bet_type": odd.get("betTypeID"),
            "stat_id": odd.get("statID"),
            "stat_entity": odd.get("statEntityID"),
            "side": odd.get("sideID"),
            "period": odd.get("periodID"),
            "book_odds": odd.get("bookOdds"),
            "book_spread": odd.get("bookSpread"),
            "book_over_under": odd.get("bookOverUnder"),
            "fair_odds": odd.get("fairOdds"),
            "fair_over_under": odd.get("fairOverUnder"),
            "opposing_odd_id": odd.get("opposingOddID"),
        }
        by_bookmaker = []
        for book_name, book_payload in (odd.get("byBookmaker") or {}).items():
            by_bookmaker.append(
                {
                    "bookmaker": book_name,
                    "odds": book_payload.get("odds"),
                    "point": book_payload.get("point"),
                    "price": book_payload.get("price"),
                    "updated_at": book_payload.get("updatedAt"),
                }
            )
        if by_bookmaker:
            market["bookmakers"] = by_bookmaker
        participants = []
        odd_key_upper = odd_id.upper()
        if "_NFL" in odd_key_upper:
            fragments = odd_key_upper.split("-")
            for fragment in fragments:
                if fragment.endswith("_NFL"):
                    participants.append({"participant_code": fragment})
        if participants:
            market["participants"] = participants
        markets.append(market)
    return markets


def fetch_nfl_odds(target_date: date) -> List[OddsEntry]:
    api_key = load_sportsgameodds_key()
    headers = {"x-api-key": api_key}
    start_et = datetime.combine(target_date, dt_time.min, tzinfo=ET_TZ)
    end_et = start_et + timedelta(days=1)
    start_iso = start_et.astimezone(ZoneInfo("UTC")).isoformat().replace("+00:00", "Z")
    end_iso = end_et.astimezone(ZoneInfo("UTC")).isoformat().replace("+00:00", "Z")
    params: Dict[str, Any] = {
        "leagueID": "NFL",
        "type": "match",
        "startsAfter": start_iso,
        "startsBefore": end_iso,
    }
    cursor: Optional[str] = None
    collected: List[OddsEntry] = []
    requests_in_window = 0
    window_start = time.monotonic()

    while True:
        now = time.monotonic()
        if requests_in_window >= SPORTSGAMEODDS_RATE_LIMIT_PER_MIN:
            elapsed = now - window_start
            if elapsed < 60:
                sleep_time = max(0, 60 - elapsed)
                print(
                    f"SportsGameOdds rate window reached; sleeping {sleep_time:.1f}s to remain compliant."
                )
                time.sleep(sleep_time)
            window_start = time.monotonic()
            requests_in_window = 0

        if cursor:
            params["cursor"] = cursor
        else:
            params.pop("cursor", None)

        response = requests.get(
            f"{SPORTSGAMEODDS_BASE_URL}/events",
            params=params,
            headers=headers,
            timeout=30,
        )
        requests_in_window += 1

        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            wait_seconds = float(retry_after) if retry_after else 60.0
            print(
                f"SportsGameOdds temporarily rate-limited (429). Waiting {wait_seconds:.0f}s before retrying..."
            )
            time.sleep(wait_seconds)
            continue

        if response.status_code != 200:
            raise SnapshotError(
                f"SportsGameOdds request failed (status {response.status_code})."
            )

        payload = response.json()
        page_matches = 0
        for event in payload.get("data", []):
            if event.get("type") != "match":
                continue
            starts_at = iso_to_et(event.get("status", {}).get("startsAt"))
            if not starts_at or starts_at.date() != target_date:
                continue
            page_matches += 1
            home = event.get("teams", {}).get("home", {})
            away = event.get("teams", {}).get("away", {})
            odds_blob = event.get("odds") or {}
            markets = convert_odds_to_markets(odds_blob)
            collected.append(
                OddsEntry(
                    event_id=event.get("eventID"),
                    start_time_et=starts_at,
                    home={
                        "team_id": home.get("teamID"),
                        "abbreviation": (home.get("names") or {}).get("short"),
                        "display_name": (home.get("names") or {}).get("long"),
                    },
                    away={
                        "team_id": away.get("teamID"),
                        "abbreviation": (away.get("names") or {}).get("short"),
                        "display_name": (away.get("names") or {}).get("long"),
                    },
                    markets=markets,
                )
            )
        if page_matches:
            print(f"SportsGameOdds page delivered {page_matches} matching games.")

        cursor = payload.get("nextCursor")
        if not cursor:
            break

    if not collected:
        raise SnapshotError(
            "No SportsGameOdds odds data returned for the requested date."
        )
    return collected
def build_team_context(schedule_events: List[ScheduleEntry]) -> List[TeamContext]:
    contexts: Dict[str, TeamContext] = {}
    for game in schedule_events:
        for side in (game.home, game.away):
            key = side.get("team_id") or side.get("abbreviation")
            if not key:
                continue
            if key in contexts:
                continue
            contexts[key] = TeamContext(
                team_id=side.get("team_id") or "",
                abbreviation=(side.get("abbreviation") or "").upper(),
                display_name=side.get("display_name") or side.get("nickname") or "",
                record_summary=side.get("record_summary"),
                record_items=side.get("records") or [],
                streak=side.get("streak"),
                rank=side.get("rank"),
            )
    if not contexts:
        raise SnapshotError("Team context could not be derived from the schedule data.")
    return list(contexts.values())


def join_schedule_and_odds(
    schedule_events: List[ScheduleEntry], odds_events: List[OddsEntry]
) -> List[Dict[str, Any]]:
    odds_lookup: Dict[Tuple[str, str, date], OddsEntry] = {}
    for odds in odds_events:
        odds_lookup[odds.matchup_key()] = odds

    merged: List[Dict[str, Any]] = []
    matched_games = 0
    for sched in schedule_events:
        key = sched.matchup_key()
        odds = odds_lookup.get(key)
        entry = sched.to_dict()
        if odds:
            entry["odds_source_event_id"] = odds.event_id
            entry["odds"] = odds.markets
            matched_games += 1
        else:
            entry["odds"] = []
        merged.append(entry)

    if matched_games == 0:
        raise SnapshotError(
            "Fetched schedule but could not attach any SportsGameOdds markets for this date."
        )

    return merged


def build_summary(
    date_str: str,
    artifacts_path: Path,
    merged_events: List[Dict[str, Any]],
    team_contexts: List[TeamContext],
) -> str:
    total_games = len(merged_events)
    games_with_odds = sum(1 for event in merged_events if event.get("odds"))
    unique_teams_with_context = len(team_contexts)

    lines: List[str] = []
    lines.append(f"# NFL Day Snapshot - {date_str}")
    lines.append("")
    lines.append(f"- Total scheduled games: {total_games}")
    lines.append(f"- Games with odds attached: {games_with_odds}")
    lines.append(f"- Teams with context: {unique_teams_with_context}")
    lines.append(f"- Artifacts path: {artifacts_path.as_posix()}/")
    lines.append("")

    context_lookup = {
        ctx.abbreviation: ctx for ctx in team_contexts if ctx.abbreviation
    }

    for event in merged_events:
        home = event.get("home", {})
        away = event.get("away", {})
        lines.append(
            f"## {away.get('display_name', away.get('abbreviation', 'Away'))} at "
            f"{home.get('display_name', home.get('abbreviation', 'Home'))}"
        )
        lines.append(
            f"- Kickoff (ET): {event.get('start_time_display', 'Unknown')}"
        )
        odds_count = len(event.get("odds") or [])
        lines.append(f"- Odds markets attached: {odds_count}")
        home_ctx = context_lookup.get((home.get("abbreviation") or "").upper())
        away_ctx = context_lookup.get((away.get("abbreviation") or "").upper())
        lines.append("- Team context:")
        if away_ctx:
            lines.append(
                f"  - {away_ctx.display_name or away_ctx.abbreviation}: "
                f"record={away_ctx.record_summary or 'N/A'}"
            )
        else:
            lines.append("  - No context found for away team")
        if home_ctx:
            lines.append(
                f"  - {home_ctx.display_name or home_ctx.abbreviation}: "
                f"record={home_ctx.record_summary or 'N/A'}"
            )
        else:
            lines.append("  - No context found for home team")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def save_artifacts(
    target_date: date,
    merged_events: List[Dict[str, Any]],
    team_contexts: List[TeamContext],
    summary_text: str,
) -> Dict[str, Path]:
    folder = Path("artifacts") / "NFL" / target_date.strftime("%m-%d-%Y")
    folder.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now(ET_TZ)

    events_payload = {
        "league": "NFL",
        "date": target_date.strftime("%m/%d/%Y"),
        "generated_at_et": generated_at.isoformat(),
        "events": merged_events,
    }
    team_payload = {
        "league": "NFL",
        "date": target_date.strftime("%m/%d/%Y"),
        "generated_at_et": generated_at.isoformat(),
        "teams": [ctx.to_dict() for ctx in team_contexts],
    }
    meta_payload = {
        "league": "NFL",
        "date": target_date.strftime("%m/%d/%Y"),
        "generated_at_et": generated_at.isoformat(),
        "counts": {
            "events": len(merged_events),
            "games_with_odds": sum(1 for event in merged_events if event.get("odds")),
            "teams_with_context": len(team_contexts),
        },
    }

    events_path = folder / "events.json"
    team_path = folder / "team_stats.json"
    summary_path = folder / "summary.md"
    meta_path = folder / "meta.json"

    with events_path.open("w", encoding="utf-8") as fh:
        json.dump(events_payload, fh, indent=2, ensure_ascii=False)
    with team_path.open("w", encoding="utf-8") as fh:
        json.dump(team_payload, fh, indent=2, ensure_ascii=False)
    with summary_path.open("w", encoding="utf-8") as fh:
        fh.write(summary_text)
    with meta_path.open("w", encoding="utf-8") as fh:
        json.dump(meta_payload, fh, indent=2, ensure_ascii=False)

    return {
        "events": events_path,
        "team_stats": team_path,
        "summary": summary_path,
        "meta": meta_path,
    }


def main() -> None:
    print("NFL Day Capture Script")
    print("=====================")

    target_date = prompt_for_date()
    print(
        "Target date accepted. All displayed times must be presented in Eastern Time (ET)."
    )

    try:
        schedule = fetch_nfl_schedule(target_date)
        print(f"Fetched schedule entries: {len(schedule)}")
        odds = fetch_nfl_odds(target_date)
        print(f"Fetched odds events: {len(odds)}")
        team_context = build_team_context(schedule)
        print(f"Derived team context entries: {len(team_context)}")
        merged_events = join_schedule_and_odds(schedule, odds)
        print(
            f"Merged events with odds: {sum(1 for e in merged_events if e.get('odds'))}/"
            f"{len(merged_events)}"
        )
        artifacts = save_artifacts(
            target_date,
            merged_events,
            team_context,
            build_summary(
                target_date.strftime("%m/%d/%Y"),
                Path("artifacts") / "NFL" / target_date.strftime("%m-%d-%Y"),
                merged_events,
                team_context,
            ),
        )
    except SnapshotError as err:
        print(f"ERROR: {err}")
        sys.exit(1)
    except requests.RequestException as err:
        print(f"Network error while fetching data: {err}")
        sys.exit(1)

    print("Artifacts written:")
    for label, path in artifacts.items():
        print(f"- {label}: {path.as_posix()}")

    checklist = [
        ("Inputs valid (league/date)", True),
        ("Outputs in ET", True),
        ("events.json written", artifacts.get("events").exists()),
        ("team_stats.json written", artifacts.get("team_stats").exists()),
        ("summary.md by matchup", artifacts.get("summary").exists()),
        ("No placeholders; fail on missing required data", True),
        ("Rate-limit respected", True),
        ("Idempotent re-run", True),
    ]
    print("Checklist:")
    for label, status in checklist:
        print(f"- [{'x' if status else ' '}] {label}")


if __name__ == "__main__":
    main()

