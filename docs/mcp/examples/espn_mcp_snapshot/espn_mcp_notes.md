# ESPN MCP Testing Notes (2025-09-19)

## Method
- Ran `python testing/run_espn_mcp_tests.py` which calls the async `mcp.espn.tools.invoke_tool` helpers directly (no HTTP server required).
- Script writes artefacts under `testing/results/<timestamp>/`; this run produced `testing/results/espn_mcp_20250919T061926Z`.
- Covered the four core tools with `teamId=22 (Cardinals)`, `season=2024`, `gameLimit=3` for the recent game endpoints.

## Working Outputs
- `team_meta` ? `testing/results/espn_mcp_20250919T061926Z/team_meta.json`
  - Includes 32 top-level fields (ids, logos, venue refs, links, ATS records, etc.).
  - Useful keys confirmed: `displayName`, `logos[..].href`, `venue.$ref`, `record.items`.
- `team_season_stats` ? `testing/results/espn_mcp_20250919T061926Z/team_season_stats.json`
  - `statCount` 228 with categories spanning offense/defense/special teams.
  - Each stat contains `displayName`, `displayValue`, numeric `value`, and `rank`.
- `team_recent_games` ? `testing/results/espn_mcp_20250919T061926Z/team_recent_games.json`
  - Returned 3 final games sorted by date with per-game `teamStats` + `opponentStats` blocks (e.g., 3rd-down efficiency, rushing yards, turnovers).
  - Attendance surfaced when available; kickoff times preserved as ESPN UTC strings.
- `team_recent_players` ? `testing/results/espn_mcp_20250919T061926Z/team_recent_players.json`
  - Mirrors the game set above; each game contains `teamPlayerStats` and `opponentPlayerStats` arrays grouped by category (`passing`, `rushing`, `defense`, `specialTeams`).
  - Player entries carry `displayName`, `position`, per-stat `label` + raw value, plus ESPN link metadata.

## Observations & Follow-ups
- Player payloads are large (~360 KB for 3 games); downstream consumers may need filtering.
- Kickoff timestamps remain in ESPN Zulu format; conversion to ET will be necessary when wiring into the Day Snapshot flow.
- Next extensions to test: alternate `seasonType` (postseason) and additional teams to ensure schema stability; optional error-path tests for bad `teamId`.
## Snapshot Script (2025-09-19)
- Added 	esting/espn_mcp_snapshot.py to mirror docs/mcp/examples/espn_nfl_stats/espn_nfl_stats_poc.py but route all fetches through the MCP tool layer.
- Usage: python testing/espn_mcp_snapshot.py --team-id 22 --season 2025 --game-limit 3 (outputs under espn_nfl_stats_output/).
- Artefacts: refreshed team metadata/season stats/recent games plus player box scores with Markdown summaries in espn_nfl_stats_output/team_22_season_2025/.
- Notes: positions missing in ESPN payloads surface as --; kickoff timestamps remain UTC and should be converted downstream when presenting in ET.
## Additional Testing (2025-09-19)
- Ran python testing/espn_mcp_snapshot.py --team-id 1 --season 2024 --game-limit 2 --output espn_mcp_runs to cover a different team/season; artefacts generated under espn_mcp_runs/team_1_season_2024/.
- Verified game-limit capping via python testing/espn_mcp_limit_check.py (requesting 12 recent games yields gameLimit 10 + current 2 finals).
- Exercised error handling with python testing/espn_mcp_error_check.py (negative teamId ? 400 	eamId must be positive).
