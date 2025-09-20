#!/usr/bin/env python3
"""
Export ESPN NCAAF (FBS) conferences, teams, and ESPN team IDs via the core API.

Usage:
  python ncaafteams.py --season 2025 --csv ncaaf_teams.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import time
import urllib.error
import urllib.request
from typing import Dict, Tuple

UA = {"User-Agent": "Mozilla/5.0 (ncaaf-conf-team-export/2.0)"}
TEAM_LIST = (
    "https://sports.core.api.espn.com/v2/sports/football/"
    "leagues/college-football/seasons/{season}/teams?limit=1000"
)


def get_json(url: str) -> Dict:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as resp:
        if resp.status != 200:
            raise RuntimeError(f"HTTP {resp.status} for {url}")
        return json.loads(resp.read().decode("utf-8"))


def fetch_team_refs(season: int):
    data = get_json(TEAM_LIST.format(season=season))
    return [item["$ref"] for item in data.get("items", [])]


def resolve_conference(team_json: Dict, cache: Dict[str, Dict]) -> Tuple[str, str]:
    group_ref = team_json.get("groups", {}).get("$ref")
    if not group_ref:
        return "", ""
    group = cache.setdefault(group_ref, get_json(group_ref))
    conference_name = group.get("name", "")

    parent_ref = group.get("parent", {}).get("$ref")
    parent_name = ""
    if parent_ref:
        parent = cache.setdefault(parent_ref, get_json(parent_ref))
        parent_name = parent.get("name", "")
    return conference_name, parent_name


def main() -> None:
    parser = argparse.ArgumentParser(description="Dump ESPN NCAAF FBS teams + conferences")
    parser.add_argument("--season", type=int, default=2025, help="Season year (default: 2025)")
    parser.add_argument("--csv", help="Optional CSV output path")
    args = parser.parse_args()

    team_refs = fetch_team_refs(args.season)
    cache: Dict[str, Dict] = {}
    rows = []

    for ref in team_refs:
        team = get_json(ref)
        conference, subdivision = resolve_conference(team, cache)
        # Only keep FBS teams (parent subdivision == 'FBS (I-A)')
        if subdivision != "FBS (I-A)":
            continue
        rows.append(
            {
                "team_id": str(team.get("id", "")),
                "displayName": team.get("displayName", ""),
                "abbreviation": team.get("abbreviation", ""),
                "slug": team.get("slug", ""),
                "conference": conference,
                "subdivision": subdivision,
            }
        )
        time.sleep(0.01)  # polite pacing

    rows.sort(key=lambda r: (r["conference"], r["displayName"]))

    last_conf = None
    for row in rows:
        if row["conference"] != last_conf:
            print(f"\n=== {row['conference']} ===")
            last_conf = row["conference"]
        print(
            f"{row['displayName']} (id={row['team_id']}, abbr={row['abbreviation']}, "
            f"slug={row['slug']})"
        )
    print(f"\nTotal FBS teams: {len(rows)}")

    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "conference",
                    "team_id",
                    "displayName",
                    "abbreviation",
                    "slug",
                    "subdivision",
                ],
            )
            writer.writeheader()
            writer.writerows(rows)
        print(f"Saved CSV to {args.csv}")


if __name__ == "__main__":
    main()
