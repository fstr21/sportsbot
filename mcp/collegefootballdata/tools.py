"""Tool metadata for the CollegeFootballData MCP service."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List


@dataclass(frozen=True)
class ToolSpec:
    """Describe a single MCP tool backed by a CFBD endpoint."""

    name: str
    method: str
    endpoint: str
    description: str


TOOLS: Dict[str, ToolSpec] = {
    tool.name: tool
    for tool in [
        ToolSpec(
            name="games",
            method="GET",
            endpoint="/games",
            description="Retrieve game schedule and results for a given season/week/team.",
        ),
        ToolSpec(
            name="lines",
            method="GET",
            endpoint="/lines",
            description="Fetch betting lines (spreads, totals, moneylines) for games.",
        ),
        ToolSpec(
            name="games_teams",
            method="GET",
            endpoint="/games/teams",
            description="Pull team box score statistics for games.",
        ),
        ToolSpec(
            name="games_players",
            method="GET",
            endpoint="/games/players",
            description="Pull player box score statistics for games.",
        ),
        ToolSpec(
            name="teams",
            method="GET",
            endpoint="/teams",
            description="List team metadata for an NCAA division or conference.",
        ),
        ToolSpec(
            name="calendar",
            method="GET",
            endpoint="/calendar",
            description="Retrieve the season calendar (weeks with start/end dates).",
        ),
        ToolSpec(
            name="scoreboard",
            method="GET",
            endpoint="/scoreboard",
            description="Live scoreboard snapshot for a given classification/season/week.",
        ),
        ToolSpec(
            name="stats_season",
            method="GET",
            endpoint="/stats/season",
            description="Season-level team statistics across offense/defense/special teams.",
        ),
        ToolSpec(
            name="stats_game",
            method="GET",
            endpoint="/stats/game",
            description="Single-game team statistics for a given season/week/team.",
        ),
        ToolSpec(
            name="ratings_sp_plus",
            method="GET",
            endpoint="/ratings/sp+",
            description="Bill Connelly SP+ ratings for teams (season level).",
        ),
        ToolSpec(
            name="ratings_massey",
            method="GET",
            endpoint="/ratings/massey",
            description="Massey power ratings for teams.",
        ),
        ToolSpec(
            name="ratings_sagarin",
            method="GET",
            endpoint="/ratings/sagarin",
            description="Jeff Sagarin ratings for teams.",
        ),
        ToolSpec(
            name="recruiting_teams",
            method="GET",
            endpoint="/recruiting/teams",
            description="Historical recruiting rankings by team.",
        ),
        ToolSpec(
            name="recruiting_players",
            method="GET",
            endpoint="/recruiting/players",
            description="Player recruiting ratings and commitments.",
        ),
        ToolSpec(
            name="venues",
            method="GET",
            endpoint="/venues",
            description="Venue metadata including capacity and location.",
        ),
        ToolSpec(
            name="conferences",
            method="GET",
            endpoint="/conferences",
            description="Conference metadata (names, IDs, divisions).",
        ),
    ]
}


def list_tools() -> Iterable[ToolSpec]:
    return TOOLS.values()


def get_tool(name: str) -> ToolSpec:
    try:
        return TOOLS[name]
    except KeyError as exc:  # pragma: no cover - runtime validation
        raise KeyError(f"Unknown tool '{name}'. Available: {', '.join(sorted(TOOLS))}") from exc
