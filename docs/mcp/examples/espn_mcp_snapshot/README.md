# ESPN MCP Snapshot Examples

Scripts and sample outputs demonstrating the ESPN MCP tooling.

## Scripts (scripts/)
- espn_mcp_snapshot.py: mirrors the legacy ESPN stats POC but sources data via MCP tools; writes JSON + Markdown summaries.
- un_espn_mcp_tests.py: quick harness hitting all four MCP tools for a Cardinals sample run.
- espn_mcp_limit_check.py: shows the gameLimit cap at 10 recent games.
- espn_mcp_error_check.py: exercises validation with a bad 	eamId.

## Notes
- espn_mcp_notes.md captures command lines, output folders, and quirks from each run.

## Outputs (outputs/)
- 	eam_22_season_2025/ and top-level JSON files: Cardinals 2025 snapshot via MCP.
- 	eam_1_season_2024/ and associated JSON: Falcons 2024 cross-check run.
- espn_mcp_20250919T061926Z/: raw harness output from un_espn_mcp_tests.py.

Times in ESPN payloads are UTC; convert to ET before surfacing in Day Snapshot flows. Player payloads are large—trim fields downstream as needed.
