#!/usr/bin/env python3
"""
NCAAF Day Capture Script

Prompts for a date (ET) and captures CollegeFootballData schedule data for
that day, limited to conferences defined in docs/ncaaf_conferences.md.
Optionally narrows results to a specific team matchup, fetches available
betting lines, normalises kickoff times to Eastern Time, and writes machine
readable + human readable artifacts under the standard path.
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import requests
from zoneinfo import ZoneInfo

ET_TZ = ZoneInfo("America/New_York")
CFBD_BASE_URL = "https://api.collegefootballdata.com"
ENV_LOCAL_PATH = Path(".env.local")
CONFERENCES_DOC = Path("docs/ncaaf_conferences.md")


class SnapshotError(RuntimeError):
    """Raised when the script cannot satisfy the required data slices."""


@dataclass
class CalendarSlot:
    season: int
    week: int
    season_type: str
    start: datetime
    end: datetime

    def contains(self, target: date) -> bool:
        return self.start.date() <= target <= self.end.date()


def load_local_env() -> None:
    if not ENV_LOCAL_PATH.exists():
        return
    for raw_line in ENV_LOCAL_PATH.read_text(encoding="utf-8").splitlines():
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


def get_cfbd_api_key() -> str:
    key = os.getenv("COLLEGE_FOOTBALL_DATA_API_KEY")
    if not key:
        raise SnapshotError(
            "COLLEGE_FOOTBALL_DATA_API_KEY must be set (see .env.local)."
        )
    return key


def load_conference_whitelist() -> Tuple[Set[str], Set[str]]:
    if not CONFERENCES_DOC.exists():
        raise SnapshotError(
            f"Required conference doc not found: {CONFERENCES_DOC.as_posix()}"
        )
    allowed_conferences: Set[str] = set()
    allowed_teams: Set[str] = set()
    current_conf: Optional[str] = None

    for raw_line in CONFERENCES_DOC.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if "conference" in line.lower():
            current_conf = normalise_conference(line)
            if current_conf:
                allowed_conferences.add(current_conf)
            continue
        allowed_teams.add(line)
    if not allowed_conferences or not allowed_teams:
        raise SnapshotError(
            "Unable to parse conferences or teams from docs/ncaaf_conferences.md."
        )
    return allowed_conferences, allowed_teams


def normalise_conference(header: str) -> Optional[str]:
    lowered = header.lower()
    if lowered.startswith("sec"):
        return "SEC"
    if lowered.startswith("big ten"):
        return "Big Ten"
    if lowered.startswith("acc"):
        return "ACC"
    if lowered.startswith("big 12"):
        return "Big 12"
    if lowered.startswith("aac") or "american athletic" in lowered:
        return "American Athletic"
    return None


def prompt_for_date() -> date:
    today_et = datetime.now(ET_TZ).date()
    default_str = today_et.strftime("%m/%d/%Y")
    prompt = (
        "Enter target NCAAF date (MM/DD/YYYY, all outputs in ET) "
        f"[{default_str}]: "
    )
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            print(f"Using {default_str} (Eastern Time).")
            return today_et
        try:
            parsed = datetime.strptime(user_input, "%m/%d/%Y").date()
            return parsed
        except ValueError:
            print("Invalid date format. Please use MM/DD/YYYY (e.g., 09/21/2025).")


def prompt_for_team_filter() -> Optional[str]:
    user_input = input(
        "Optional team filter (match home or away team, press Enter for all games): "
    ).strip()
    return user_input or None


def iso_to_et(timestamp: Optional[str]) -> Optional[datetime]:
    if not timestamp:
        return None
    cleaned = timestamp.replace("Z", "+00:00")
    try:
        dt_obj = datetime.fromisoformat(cleaned)
    except ValueError:
        return None
    if dt_obj.tzinfo is None:
        dt_obj = dt_obj.replace(tzinfo=ZoneInfo("UTC"))
    return dt_obj.astimezone(ET_TZ)


def resolve_cfbd_week(
    target_date: date, session: requests.Session, headers: Dict[str, str]
) -> CalendarSlot:
    candidate_years = (target_date.year, target_date.year - 1)
    for year in candidate_years:
        params = {"year": year}
        response = session.get(
            f"{CFBD_BASE_URL}/calendar", params=params, headers=headers, timeout=30
        )
        if response.status_code != 200:
            raise SnapshotError(
                f"Failed to resolve CFBD calendar for {year} (status {response.status_code})."
            )
        slots: List[CalendarSlot] = []
        for item in response.json():
            start = iso_to_et(item.get("startDate"))
            end = iso_to_et(item.get("endDate"))
            if not start or not end:
                continue
            slots.append(
                CalendarSlot(
                    season=item.get("season", year),
                    week=item.get("week"),
                    season_type=item.get("seasonType", "regular"),
                    start=start,
                    end=end,
                )
            )
        for slot in slots:
            if slot.contains(target_date):
                return slot
    raise SnapshotError(
        "Unable to locate a CFBD calendar week for the requested date."
    )


def fetch_cfbd_schedule(
    target_date: date,
    calendar_slot: CalendarSlot,
    session: requests.Session,
    headers: Dict[str, str],
) -> List[Dict[str, Any]]:
    params = {
        "year": calendar_slot.season,
        "week": calendar_slot.week,
        "seasonType": calendar_slot.season_type,
        "division": "fbs",
    }
    response = session.get(
        f"{CFBD_BASE_URL}/games", params=params, headers=headers, timeout=30
    )
    if response.status_code != 200:
        raise SnapshotError(
            f"CFBD games request failed (status {response.status_code})."
        )
    games_for_day: List[Dict[str, Any]] = []
    for game in response.json():
        kickoff = iso_to_et(game.get("startDate"))
        if not kickoff or kickoff.date() != target_date:
            continue
        games_for_day.append(game)
    if not games_for_day:
        raise SnapshotError(
            "No CFBD games found for the requested date within the resolved week."
        )
    return games_for_day


def filter_games_by_policy(
    games: List[Dict[str, Any]],
    allowed_conferences: Set[str],
    allowed_teams: Set[str],
    team_filter: Optional[str],
) -> List[Dict[str, Any]]:
    filtered: List[Dict[str, Any]] = []
    for game in games:
        home_conf = game.get("homeConference")
        away_conf = game.get("awayConference")
        home_team = game.get("homeTeam")
        away_team = game.get("awayTeam")

        include = False
        if home_conf in allowed_conferences or away_conf in allowed_conferences:
            include = True
        if not include:
            if (home_team and home_team in allowed_teams) or (
                away_team and away_team in allowed_teams
            ):
                include = True
        if not include:
            continue
        filtered.append(game)

    if team_filter:
        token = team_filter.lower()
        filtered = [
            game
            for game in filtered
            if token in (game.get("homeTeam") or "").lower()
            or token in (game.get("awayTeam") or "").lower()
        ]

    return filtered


def fetch_cfbd_lines(
    calendar_slot: CalendarSlot,
    session: requests.Session,
    headers: Dict[str, str],
) -> Dict[int, List[Dict[str, Any]]]:
    params = {
        "year": calendar_slot.season,
        "week": calendar_slot.week,
        "seasonType": calendar_slot.season_type,
    }
    response = session.get(
        f"{CFBD_BASE_URL}/lines", params=params, headers=headers, timeout=30
    )
    if response.status_code != 200:
        raise SnapshotError(
            f"CFBD lines request failed (status {response.status_code})."
        )
    odds_by_game: Dict[int, List[Dict[str, Any]]] = {}
    for record in response.json():
        game_id = record.get("id")
        if game_id is None:
            continue
        odds_entries: List[Dict[str, Any]] = []
        for line in record.get("lines") or []:
            odds_entries.append(
                {
                    "provider": line.get("provider"),
                    "spread": line.get("spread"),
                    "over_under": line.get("overUnder"),
                    "home_moneyline": line.get("homeMoneyline"),
                    "away_moneyline": line.get("awayMoneyline"),
                    "spread_open": line.get("spreadOpen"),
                    "over_under_open": line.get("overUnderOpen"),
                    "formatted_spread": line.get("formattedSpread"),
                    "last_updated": line.get("lastUpdated"),
                }
            )
        if odds_entries:
            odds_by_game[game_id] = odds_entries
    return odds_by_game


def build_schedule_entry(
    game: Dict[str, Any],
    kickoff_et: Optional[datetime],
    odds: List[Dict[str, Any]],
) -> Dict[str, Any]:
    venue = game.get("venue") or {}
    return {
        "game_id": game.get("id"),
        "season": game.get("season"),
        "week": game.get("week"),
        "season_type": game.get("seasonType"),
        "start_time_et": kickoff_et.isoformat() if kickoff_et else None,
        "start_time_display": kickoff_et.strftime("%Y-%m-%d %I:%M %p ET") if kickoff_et else None,
        "venue": {
            "name": venue.get("name") if isinstance(venue, dict) else venue,
            "city": venue.get("city") if isinstance(venue, dict) else None,
            "state": venue.get("state") if isinstance(venue, dict) else None,
            "capacity": venue.get("capacity") if isinstance(venue, dict) else None,
        },
        "home": {
            "team": game.get("homeTeam"),
            "conference": game.get("homeConference"),
            "classification": game.get("homeClassification"),
            "points": game.get("homePoints"),
            "line_scores": game.get("homeLineScores"),
            "pregame_elo": game.get("homePregameElo"),
            "postgame_elo": game.get("homePostgameElo"),
        },
        "away": {
            "team": game.get("awayTeam"),
            "conference": game.get("awayConference"),
            "classification": game.get("awayClassification"),
            "points": game.get("awayPoints"),
            "line_scores": game.get("awayLineScores"),
            "pregame_elo": game.get("awayPregameElo"),
            "postgame_elo": game.get("awayPostgameElo"),
        },
        "excitement_index": game.get("excitementIndex"),
        "notes": {
            "broadcast": game.get("tv") or game.get("broadcast"),
            "neutral_site": game.get("neutralSite"),
            "conference_game": game.get("conferenceGame"),
            "venue_id": game.get("venue_id"),
        },
        "odds": odds,
    }


def build_summary(
    target_date: date,
    schedule: List[Dict[str, Any]],
    games_with_odds: int,
    artifact_folder: Path,
) -> str:
    date_header = target_date.strftime("%B %d, %Y")
    lines: List[str] = []
    lines.append(f"# NCAAF Day Snapshot - {date_header}")
    lines.append("")
    lines.append(f"- Total scheduled games: {len(schedule)}")
    lines.append(f"- Games with odds attached: {games_with_odds}")
    lines.append(f"- Artifact path: {artifact_folder.as_posix()}/")
    lines.append("")

    for entry in schedule:
        home = entry.get("home", {})
        away = entry.get("away", {})
        kickoff_display = entry.get("start_time_display") or "TBD"
        lines.append(
            f"## {away.get('team') or 'Away'} at {home.get('team') or 'Home'}"
        )
        lines.append(f"- Kickoff (ET): {kickoff_display}")
        lines.append(
            "- Conferences: "
            f"{away.get('conference') or 'Unknown'} vs {home.get('conference') or 'Unknown'}"
        )
        odds = entry.get("odds") or []
        if odds:
            lines.append(f"- Odds markets: {len(odds)} provider(s)")
            for market in odds:
                provider = market.get("provider") or "Unknown"
                spread = market.get("formatted_spread") or market.get("spread")
                ou = market.get("over_under")
                home_ml = market.get("home_moneyline")
                away_ml = market.get("away_moneyline")
                pieces = [f"spread={spread}" if spread is not None else None]
                if ou is not None:
                    pieces.append(f"total={ou}")
                if home_ml is not None and away_ml is not None:
                    pieces.append(f"ML {home.get('team') or 'Home'} {home_ml}/"
                                  f"{away.get('team') or 'Away'} {away_ml}")
                pieces = [p for p in pieces if p]
                detail = "; ".join(pieces) if pieces else "available pricing"
                lines.append(f"  - {provider}: {detail}")
        else:
            lines.append("- Odds markets: none available")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def save_artifacts(
    target_date: date,
    calendar_slot: CalendarSlot,
    schedule: List[Dict[str, Any]],
    games_with_odds: int,
    summary_text: str,
) -> Dict[str, Path]:
    folder = Path("artifacts") / "NCAAF" / target_date.strftime("%m-%d-%Y")
    folder.mkdir(parents=True, exist_ok=True)
    payload = {
        "league": "NCAAF",
        "date": target_date.strftime("%m/%d/%Y"),
        "generated_at_et": datetime.now(ET_TZ).isoformat(),
        "calendar": {
            "season": calendar_slot.season,
            "week": calendar_slot.week,
            "season_type": calendar_slot.season_type,
            "window_start_et": calendar_slot.start.isoformat(),
            "window_end_et": calendar_slot.end.isoformat(),
        },
        "counts": {
            "games": len(schedule),
            "games_with_odds": games_with_odds,
        },
        "games": schedule,
    }
    events_path = folder / "events.json"
    summary_path = folder / "summary.md"

    with events_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
    with summary_path.open("w", encoding="utf-8") as handle:
        handle.write(summary_text)

    return {
        "events": events_path,
        "summary": summary_path,
    }


def main() -> None:
    print("NCAAF Day Capture Script")
    print("========================")

    load_local_env()

    try:
        api_key = get_cfbd_api_key()
        allowed_conferences, allowed_teams = load_conference_whitelist()
    except SnapshotError as err:
        print(f"ERROR: {err}")
        sys.exit(1)

    target_date = prompt_for_date()
    team_filter = prompt_for_team_filter()
    print("Target accepted. All displayed times will be in Eastern Time (ET).")

    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        with requests.Session() as session:
            calendar_slot = resolve_cfbd_week(target_date, session, headers)
            raw_games = fetch_cfbd_schedule(target_date, calendar_slot, session, headers)
            filtered_games = filter_games_by_policy(
                raw_games, allowed_conferences, allowed_teams, team_filter
            )
            if not filtered_games:
                raise SnapshotError(
                    "No games matched the conference policy for this date."
                )
            odds_map = fetch_cfbd_lines(calendar_slot, session, headers)
            schedule_entries: List[Dict[str, Any]] = []
            games_with_odds = 0
            for game in filtered_games:
                kickoff = iso_to_et(game.get("startDate"))
                game_id = game.get("id")
                odds = odds_map.get(game_id, []) if game_id is not None else []
                if odds:
                    games_with_odds += 1
                schedule_entries.append(build_schedule_entry(game, kickoff, odds))
    except SnapshotError as err:
        print(f"ERROR: {err}")
        sys.exit(1)
    except requests.RequestException as err:
        print(f"Network error while fetching CFBD data: {err}")
        sys.exit(1)

    artifact_folder = Path("artifacts") / "NCAAF" / target_date.strftime("%m-%d-%Y")
    summary_text = build_summary(target_date, schedule_entries, games_with_odds, artifact_folder)
    artifacts = save_artifacts(
        target_date,
        calendar_slot,
        schedule_entries,
        games_with_odds,
        summary_text,
    )

    print("Schedule capture complete.")
    print(f"- Games captured: {len(schedule_entries)}")
    print(f"- Games with odds: {games_with_odds}")
    print(f"- JSON artifact: {artifacts['events'].as_posix()}")
    print(f"- Summary artifact: {artifacts['summary'].as_posix()}")

    if games_with_odds < len(schedule_entries):
        missing = len(schedule_entries) - games_with_odds
        print(
            f"NOTE: {missing} game(s) did not have CFBD betting lines in the returned data."
        )

    print("Checklist:")
    checklist = [
        ("Inputs valid (date)", True),
        ("Outputs in ET", all(item.get("start_time_display") for item in schedule_entries)),
        ("events.json written", artifacts['events'].exists()),
        ("summary.md written", artifacts['summary'].exists()),
        ("Odds attached where available", True),
    ]
    for label, status in checklist:
        print(f"- [{'x' if status else ' '}] {label}")


if __name__ == "__main__":
    main()
