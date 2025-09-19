"""End-to-end smoke tests for the deployed CollegeFootballData MCP."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

import requests

from client import client

OUTPUT_DIR = Path("cfbd_mcp_test")
RESULTS_DIR = OUTPUT_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

TEST_CASES: Dict[str, Dict[str, str | int]] = {
    "games": {"year": 2024, "week": 1, "seasonType": "regular"},
    "lines": {"year": 2024, "week": 1, "seasonType": "regular"},
    "games_teams": {"year": 2024, "week": 1, "seasonType": "regular"},
    "games_players": {"year": 2024, "week": 1, "seasonType": "regular"},
    "teams": {"division": "fbs"},
    "calendar": {"year": 2024},
    "scoreboard": {"classification": "fbs", "year": 2024, "week": 1, "seasonType": "regular"},
    "stats_season": {"year": 2024, "team": "Georgia", "category": "offense"},
    "stats_game": {"year": 2024, "week": 1, "team": "Georgia"},
    "ratings_sp_plus": {"year": 2024},
    "ratings_massey": {"year": 2024},
    "ratings_sagarin": {"year": 2024},
    "recruiting_teams": {"year": 2024},
    "recruiting_players": {"year": 2024},
    "venues": {},
    "conferences": {},
}


def pretty_json(data: object) -> str:
    try:
        return json.dumps(data, indent=2, sort_keys=True)
    except Exception:  # pragma: no cover
        return str(data)


def summarize_payload(data: object) -> dict:
    if isinstance(data, list):
        return {
            "type": "list",
            "items": len(data),
            "sample": data[:1],
        }
    if isinstance(data, dict):
        return {
            "type": "dict",
            "keys": list(data)[:10],
        }
    return {"type": type(data).__name__}


def main() -> int:
    cli = client()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = RESULTS_DIR / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)

    report: List[dict] = []

    health_resp = cli.health()
    report.append(
        {
            "tool": "health",
            "status_code": health_resp.status_code,
            "body": health_resp.text,
        }
    )

    tools_resp = cli.list_tools()
    try:
        tools_payload = tools_resp.json()
    except ValueError:
        tools_payload = tools_resp.text
    report.append(
        {
            "tool": "tools",
            "status_code": tools_resp.status_code,
            "body": tools_payload,
        }
    )

    for tool, params in TEST_CASES.items():
        resp = cli.invoke(tool, params)
        entry = {
            "tool": tool,
            "status_code": resp.status_code,
            "params": params,
        }
        try:
            payload = resp.json()
        except ValueError:
            payload = {"raw": resp.text}
        entry["payload_summary"] = summarize_payload(payload)

        (run_dir / f"{tool}.response.json").write_text(pretty_json(payload), encoding="utf-8")
        entry["payload_path"] = f"{tool}.response.json"
        report.append(entry)

    report_path = run_dir / "report.json"
    report_path.write_text(pretty_json(report), encoding="utf-8")
    print(f"Test run captured in {run_dir.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
