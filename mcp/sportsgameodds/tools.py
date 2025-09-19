"""Tool definitions for the SportsGameOdds MCP service."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable


@dataclass(frozen=True)
class ToolSpec:
    name: str
    method: str
    endpoint: str
    description: str


TOOLS: Dict[str, ToolSpec] = {
    tool.name: tool
    for tool in [
        ToolSpec(
            name="sports",
            method="GET",
            endpoint="/sports",
            description="List supported sports available to the API key.",
        ),
        ToolSpec(
            name="leagues",
            method="GET",
            endpoint="/leagues",
            description="List leagues and their associated sport IDs.",
        ),
        ToolSpec(
            name="bookmakers",
            method="GET",
            endpoint="/bookmakers",
            description="Retrieve bookmaker metadata and IDs.",
        ),
        ToolSpec(
            name="bet_types",
            method="GET",
            endpoint="/bet-types",
            description="List available bet types and side identifiers.",
        ),
        ToolSpec(
            name="stats",
            method="GET",
            endpoint="/stats",
            description="Fetch stat ID reference data for a given sport or league.",
        ),
        ToolSpec(
            name="events",
            method="GET",
            endpoint="/events",
            description="Retrieve events (schedule + odds) with optional filters (leagueID, startsAfter, etc.).",
        ),
    ]
}


def list_tools() -> Iterable[ToolSpec]:
    return TOOLS.values()


def get_tool(name: str) -> ToolSpec:
    try:
        return TOOLS[name]
    except KeyError as exc:  # pragma: no cover
        raise KeyError(
            f"Unknown tool '{name}'. Available: {', '.join(sorted(TOOLS))}"
        ) from exc
