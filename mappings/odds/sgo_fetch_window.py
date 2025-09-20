#!/usr/bin/env python3
"""Fetch NFL SportsGameOdds events for 2025-09-20 through 2025-09-23 via the MCP."""

from __future__ import annotations

import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Tuple

import requests
from zoneinfo import ZoneInfo

MCP_BASE_URL = "https://sportsgameoddsmcp-production.up.railway.app"
OUTPUT_DIR = Path("mappings/data/odds/nfl/2025-09-20_2025-09-23")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SUMMARY_PATH = OUTPUT_DIR / "manifest.json"

LEAGUE_ID = "NFL"
MAX_REQUESTS = 6
SLEEP_BETWEEN_REQUESTS = 7

# Date window (inclusive of start date, exclusive of end date)
START_DATE_ET = datetime(2025, 9, 20, tzinfo=ZoneInfo("America/New_York"))
END_DATE_ET = datetime(2025, 9, 24, tzinfo=ZoneInfo("America/New_York"))

params_base: Dict[str, Any] = {
    "leagueID": LEAGUE_ID,
    "type": "match",
    "startsAfter": START_DATE_ET.astimezone(ZoneInfo("UTC")).isoformat().replace("+00:00", "Z"),
    "startsBefore": END_DATE_ET.astimezone(ZoneInfo("UTC")).isoformat().replace("+00:00", "Z"),
    "limit": 50,
}


def invoke_events(cursor: str | None) -> Dict[str, Any]:
    payload = {"params": dict(params_base)}
    if cursor:
        payload["params"]["cursor"] = cursor

    time.sleep(SLEEP_BETWEEN_REQUESTS)
    response = requests.post(
        f"{MCP_BASE_URL}/tools/events/invoke",
        json=payload,
        timeout=120,
    )

    if response.status_code == 502:
        try:
            detail = response.json()
        except ValueError:
            detail = {}
        if "No Events found" in str(detail) or "404" in str(detail):
            return {"data": {"data": [], "nextCursor": None}}

    if response.status_code == 429:
        raise RuntimeError("SportsGameOdds MCP returned 429 (rate limited)")
    if response.status_code != 200:
        raise RuntimeError(f"MCP request failed ({response.status_code}): {response.text[:400]}")

    return response.json()


def collect_events() -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    events: List[Dict[str, Any]] = []
    cursor: str | None = None
    request_count = 0

    while True:
        if request_count >= MAX_REQUESTS:
            raise RuntimeError("Aborting after reaching MAX_REQUESTS guard")
        payload = invoke_events(cursor)
        body = payload.get("data")
        if not isinstance(body, dict):
            raise RuntimeError("Unexpected MCP payload structure")
        page_events = body.get("data") or []
        if not isinstance(page_events, list):
            raise RuntimeError("Unexpected MCP payload: data.data not list")
        events.extend(page_events)
        cursor = body.get("nextCursor")
        request_count += 1
        if not cursor:
            meta = {
                "league_id": LEAGUE_ID,
                "starts_after_utc": params_base["startsAfter"],
                "starts_before_utc": params_base["startsBefore"],
                "request_count": request_count,
                "generated_at_utc": datetime.now(tz=ZoneInfo("UTC")).isoformat(),
            }
            return events, meta


def save_events(events: List[Dict[str, Any]]) -> List[str]:
    manifest_entries: List[str] = []
    for event in events:
        event_id = event.get("eventID") or event.get("eventId")
        if not event_id:
            event_id = f"event_{len(manifest_entries):03d}"
        safe_id = event_id.replace("/", "-")
        path = OUTPUT_DIR / f"{safe_id}.json"
        with path.open("w", encoding="utf-8") as handle:
            json.dump(event, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        manifest_entries.append(str(path.name))
    return manifest_entries


def main() -> None:
    events, meta = collect_events()
    filenames = save_events(events)
    summary = {
        "meta": meta,
        "event_count": len(events),
        "files": filenames,
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(
        f"Saved {len(events)} events to {OUTPUT_DIR} using {meta['request_count']} MCP calls"
    )


if __name__ == "__main__":
    main()
