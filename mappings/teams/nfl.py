#!/usr/bin/env python3
"""NFL team mapping fetcher for provider-specific exports.

Fetches NFL team metadata from ESPN endpoints (primary) with a core API
fallback, then writes normalized rows into provider-scoped directories so
additional data sources (e.g., SportsGameOdds) can live alongside ESPN.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List
from urllib import request

SITE_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"
CORE_URL = "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/teams?limit=1000"
USER_AGENT = {"User-Agent": "Mozilla/5.0 (team-id-fetcher/1.1)"}

DEFAULT_OUTPUT_ROOT = Path(__file__).resolve().parent.parent / "data" / "teams" / "nfl"
DEFAULT_PROVIDER = "espn"
TEAM_FIELDS = ("id", "abbreviation", "displayName", "location", "name", "slug", "uid")


def fetch_json(url: str) -> Dict[str, Any]:
    req = request.Request(url, headers=USER_AGENT)
    with request.urlopen(req, timeout=20) as resp:
        if resp.status != 200:
            raise RuntimeError(f"HTTP {resp.status} for {url}")
        return json.loads(resp.read().decode("utf-8"))


def load_from_site() -> List[Dict[str, str]]:
    data = fetch_json(SITE_URL)
    teams: List[Dict[str, str]] = []
    sports = data.get("sports", [])
    leagues = sports[0].get("leagues", []) if sports else []
    for league in leagues:
        for team_wrapper in league.get("teams", []):
            team = team_wrapper.get("team", {})
            teams.append({
                "id": str(team.get("id", "")).strip(),
                "abbreviation": team.get("abbreviation", ""),
                "displayName": team.get("displayName", team.get("name", "")),
                "location": team.get("location", ""),
                "name": team.get("name", ""),
                "slug": team.get("slug", ""),
                "uid": team.get("uid", ""),
            })
    deduped: List[Dict[str, str]] = []
    seen: set[str] = set()
    for team in teams:
        team_id = team.get("id")
        if team_id and team_id not in seen:
            seen.add(team_id)
            deduped.append(team)
    return deduped


def load_from_core() -> List[Dict[str, str]]:
    data = fetch_json(CORE_URL)
    teams: List[Dict[str, str]] = []
    for item in data.get("items", []):
        ref = item.get("$ref", "")
        match = re.search(r"/teams/(\d+)", ref)
        if match:
            entry = {field: "" for field in TEAM_FIELDS}
            entry["id"] = match.group(1)
            teams.append(entry)
    return teams


def save_csv(rows: Iterable[Dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=TEAM_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def save_json(rows: Iterable[Dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(list(rows), handle, indent=2, sort_keys=True)
        handle.write("\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch NFL team mappings")
    parser.add_argument(
        "--provider",
        default=DEFAULT_PROVIDER,
        help="Source tag for output directory (e.g., espn, sgo)",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help="Base directory for exports (provider subfolder appended)",
    )
    parser.add_argument(
        "--json",
        type=Path,
        help="Optional explicit JSON output path (overrides --out-dir/provider)",
    )
    parser.add_argument(
        "--csv",
        type=Path,
        help="Optional explicit CSV output path (overrides --out-dir/provider)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    provider = args.provider.lower()

    try:
        teams = load_from_site()
    except Exception:
        teams = load_from_core()

    teams.sort(key=lambda team: int(team["id"]))
    for team in teams:
        label = team.get("displayName") or team.get("name") or "(unknown)"
        print(f"{team['id']:>2}  {team['abbreviation']:<4}  {label}")

    target_dir = args.out_dir / provider
    json_path = args.json or (target_dir / "teams.json")
    csv_path = args.csv or (target_dir / "teams.csv")

    save_json(teams, json_path)
    save_csv(teams, csv_path)

    print(f"\nTotal teams: {len(teams)}")
    print(f"Provider: {provider}")
    print(f"JSON written to: {json_path}")
    print(f"CSV written to:  {csv_path}")


if __name__ == "__main__":
    main()
