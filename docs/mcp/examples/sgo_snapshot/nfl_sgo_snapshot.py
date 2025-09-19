#!/usr/bin/env python3
"""Interactive NFL snapshot via the SportsGameOdds MCP with rate-limit handling."""

from __future__ import annotations

import json
import re
import time
from copy import deepcopy
from datetime import date, datetime, time as dt_time, timedelta
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import requests
from zoneinfo import ZoneInfo

MCP_BASE_URL = "https://sportsgameoddsmcp-production.up.railway.app"
ET_TZ = ZoneInfo("America/New_York")
UTC_TZ = ZoneInfo("UTC")
PAGE_LIMIT = 1  # keep low while troubleshooting
LEAGUE_ID = "NFL"
RATE_LIMIT_PER_MIN = 3  # Very conservative - 3 requests per minute
RETRY_SLEEP_SECONDS = 90  # Wait 90 seconds between retries
MAX_RETRIES = 8  # Many more retries


class SnapshotError(RuntimeError):
    """Raised when the snapshot cannot be completed."""


def prompt_for_date() -> date:
    while True:
        raw = input("Enter target date (MM/DD/YYYY): ").strip()
        try:
            return datetime.strptime(raw, "%m/%d/%Y").date()
        except ValueError:
            print("Invalid date format. Please use MM/DD/YYYY (e.g., 09/21/2025).")


def build_window(target: date) -> Dict[str, str]:
    start_et = datetime.combine(target, dt_time.min, tzinfo=ET_TZ)
    end_et = start_et + timedelta(days=1)
    return {
        "startsAfter": start_et.astimezone(UTC_TZ).isoformat().replace("+00:00", "Z"),
        "startsBefore": end_et.astimezone(UTC_TZ).isoformat().replace("+00:00", "Z"),
    }


def is_upstream_rate_limit(response: requests.Response) -> bool:
    if response.status_code == 429:
        return True
    if response.status_code == 502:
        try:
            detail = response.json().get("detail")
            if isinstance(detail, str) and "429" in detail:
                return True
        except ValueError:
            pass
    return False


def invoke_events_tool(params: Dict[str, Any]) -> Dict[str, Any]:
    # Add delay before EVERY request to respect rate limits
    print(f"Waiting 12 seconds before MCP request to respect rate limits...")
    time.sleep(12)  # 12 seconds = 5 requests per minute (well under 10/min limit)

    attempt = 0
    while True:
        attempt += 1
        print(f"Making MCP request (attempt {attempt}/{MAX_RETRIES})...")
        print(f"Request URL: {MCP_BASE_URL}/tools/events/invoke")
        print(f"Request params: {params}")

        try:
            response = requests.post(
                f"{MCP_BASE_URL}/tools/events/invoke",
                json={"params": params},
                timeout=120,  # Increased timeout
            )
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            if response.status_code != 200:
                print(f"Response text: {response.text[:500]}")
        except Exception as e:
            print(f"Request exception: {e}")
            raise SnapshotError(f"MCP request failed with exception: {e}")
        if is_upstream_rate_limit(response) and attempt < MAX_RETRIES:
            print(
                f"Hit MCP rate limit (attempt {attempt}/{MAX_RETRIES}); waiting {RETRY_SLEEP_SECONDS}s."
            )
            time.sleep(RETRY_SLEEP_SECONDS)
            continue
        if is_upstream_rate_limit(response):
            raise SnapshotError(
                "Rate limit hit; SportsGameOdds MCP reported upstream 429 after retries."
            )

        # Handle 404 "No Events found" as successful completion of pagination
        if response.status_code == 502:
            try:
                error_detail = response.json()
                if ("No Events found" in str(error_detail) or
                    "404" in str(error_detail)):
                    print("Reached end of data (No Events found) - pagination complete.")
                    return {"data": {"data": [], "nextCursor": None}}
            except ValueError:
                pass

        if response.status_code != 200:
            raise SnapshotError(
                f"MCP request failed ({response.status_code}): {response.text}"
            )
        try:
            return response.json()
        except ValueError as exc:  # pragma: no cover
            raise SnapshotError("MCP returned non-JSON response") from exc


def extract_page(payload: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    body = payload.get("data")
    if not isinstance(body, dict):
        raise SnapshotError("Unexpected MCP payload; missing 'data' dictionary")
    page_events = body.get("data") or []
    if not isinstance(page_events, list):
        raise SnapshotError("Unexpected MCP payload; 'data.data' is not a list")
    next_cursor = body.get("nextCursor") if body.get("success") else None
    return page_events, next_cursor


def collect_events(base_params: Dict[str, Any]) -> List[Dict[str, Any]]:
    events: List[Dict[str, Any]] = []
    cursor: Optional[str] = None
    page_count = 0
    max_pages = 1  # Limit to 1 page for testing

    while True:
        params = dict(base_params)
        if cursor:
            params["cursor"] = cursor
        payload = invoke_events_tool(params)
        page_events, cursor = extract_page(payload)
        events.extend(page_events)
        page_count += 1

        print(f"Collected page {page_count} with {len(page_events)} events (total: {len(events)})")

        # Stop after max_pages or if no more data
        if page_count >= max_pages or not cursor:
            print(f"Stopping after {page_count} page(s) - collected {len(events)} total events")
            break

    return events


def safe_team_name(team_payload: Dict[str, Any]) -> Dict[str, Optional[str]]:
    names = team_payload.get("names", {}) if isinstance(team_payload, dict) else {}
    return {
        "team_id": team_payload.get("teamID") if isinstance(team_payload, dict) else None,
        "long": names.get("long"),
        "medium": names.get("medium"),
        "short": names.get("short"),
    }


def to_et_display(iso_utc: Optional[str]) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    if not iso_utc:
        return None, None, None
    try:
        dt_utc = datetime.fromisoformat(iso_utc.replace("Z", "+00:00"))
    except ValueError:
        return iso_utc, None, None
    dt_et = dt_utc.astimezone(ET_TZ)
    return dt_utc.isoformat(), dt_et.isoformat(), dt_et.strftime("%Y-%m-%d %I:%M %p ET")


def format_event(event: Dict[str, Any]) -> Dict[str, Any]:
    raw_event = deepcopy(event)
    start_utc, start_et, start_display = to_et_display(event.get("startTimeUTC") or event.get("startTime"))
    teams = event.get("teams") if isinstance(event, dict) else {}
    home_payload = teams.get("home") if isinstance(teams, dict) else {}
    away_payload = teams.get("away") if isinstance(teams, dict) else {}
    odds_payload = event.get("odds") if isinstance(event, dict) else None
    market_count = len(odds_payload) if isinstance(odds_payload, dict) else 0
    bookmakers: List[str] = []
    if isinstance(odds_payload, dict):
        seen: set[str] = set()
        for market in odds_payload.values():
            by_book = market.get("byBookmaker") if isinstance(market, dict) else None
            if isinstance(by_book, dict):
                seen.update(by_book.keys())
        bookmakers = sorted(seen)
    return {
        "event_id": event.get("eventID"),
        "type": event.get("type"),
        "start_time_utc": start_utc,
        "start_time_et": start_et,
        "start_time_display": start_display,
        "venue": event.get("venue", {}).get("name") if isinstance(event.get("venue"), dict) else None,
        "home": safe_team_name(home_payload),
        "away": safe_team_name(away_payload),
        "market_count": market_count,
        "bookmakers": bookmakers,
        "raw_event": raw_event,
    }


def build_summary(events: Iterable[Dict[str, Any]], artifacts_path: Path, target_date: str) -> str:
    events_list = list(events)
    lines = [
        f"SportsGameOdds MCP snapshot for {target_date}",
        f"Total games: {len(events_list)}",
        f"Artifacts: {artifacts_path.as_posix()}",
        "",
    ]
    for idx, event in enumerate(events_list, start=1):
        home = event["home"]
        away = event["away"]
        matchup = f"{away.get('long') or away.get('medium') or away.get('short') or 'Away'} at " \
            f"{home.get('long') or home.get('medium') or home.get('short') or 'Home'}"
        lines.append(f"## Game {idx}: {matchup}")
        if event.get("start_time_display"):
            lines.append(f"- Kickoff: {event['start_time_display']}")
        lines.append(f"- Odds markets: {event.get('market_count', 0)}")
        books = event.get("bookmakers") or []
        if books:
            lines.append(f"- Bookmakers: {', '.join(books)}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "game"


def build_match_slug(event: Dict[str, Any], index: int) -> str:
    home = event.get("home") or {}
    away = event.get("away") or {}
    home_slug = slugify(home.get("short") or home.get("medium") or home.get("long") or f"home-{index}")
    away_slug = slugify(away.get("short") or away.get("medium") or away.get("long") or f"away-{index}")
    kickoff = event.get("start_time_et") or event.get("start_time_utc") or ""
    kickoff_slug = slugify(kickoff[:16]) if kickoff else f"game-{index}"
    return f"{kickoff_slug}-{away_slug}-at-{home_slug}"


def save_outputs(target_date: date, events: List[Dict[str, Any]]) -> None:
    folder = Path("artifacts") / LEAGUE_ID.lower() / target_date.strftime("%m-%d-%Y")
    games_folder = folder / "games"
    folder.mkdir(parents=True, exist_ok=True)
    games_folder.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now(tz=ET_TZ).isoformat()
    events_payload = {
        "league": LEAGUE_ID,
        "date": target_date.strftime("%m/%d/%Y"),
        "generated_at_et": generated_at,
        "event_count": len(events),
        "events": events,
    }

    events_path = folder / "events.json"
    events_path.write_text(json.dumps(events_payload, indent=2), encoding="utf-8")

    for idx, event in enumerate(events, start=1):
        slug = build_match_slug(event, idx)
        path = games_folder / f"{slug}.json"
        payload = {
            "league": LEAGUE_ID,
            "date": target_date.strftime("%m/%d/%Y"),
            "generated_at_et": generated_at,
            "event": event,
        }
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    summary_path = folder / "summary.md"
    summary_path.write_text(
        build_summary(events, folder, target_date.strftime("%m/%d/%Y")),
        encoding="utf-8",
    )

    print(f"Saved {len(events)} events to {events_path.as_posix()}")
    print(f"Wrote per-game files to {games_folder.as_posix()}")
    print(f"Wrote summary to {summary_path.as_posix()}")


def main() -> None:
    print("SportsGameOdds MCP — NFL Snapshot")
    print("---------------------------------")
    target_date = prompt_for_date()
    window = build_window(target_date)
    base_params = {
        "leagueID": LEAGUE_ID,
        "type": "match",
        "limit": PAGE_LIMIT,
    }
    base_params.update(window)

    try:
        raw_events = collect_events(base_params)
    except SnapshotError as err:
        print(f"ERROR: {err}")
        return

    if not raw_events:
        print("No events returned for that date.")
        return

    formatted_events = [format_event(event) for event in raw_events]
    save_outputs(target_date, formatted_events)


if __name__ == "__main__":
    main()
