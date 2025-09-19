# ESPN NFL Stats Snapshot (POC)

This proof-of-concept shows how we can pull NFL team+player data directly from ESPN. It documents the exact endpoints, fields, and outputs we generated so we can promote this flow to an MCP later.

## Script

espn_nfl_stats_poc.py

`
python scripts/espn_nfl_stats_poc.py \
  --team-id 22 \
  --season 2025 \
  --season-type regular \
  --game-limit 2 \
  --output espn_nfl_stats_output
`

Flags:
- 	eam-id - ESPN team id (defaults to 22 for the Arizona Cardinals)
- season - integer season year
- season-type - egular, postseason, or preseason (maps to ESPN 	ypes/2, 	ypes/3, 	ypes/1)
- game-limit - # of most recent completed games to summarize (team + players)
- output - folder for raw artifacts

The script issues 4-6 HTTP GETs per run and does not require auth today, but we should add throttling/backoff if we expand beyond a few games.

Outputs are written to <output>/team_<id>_season_<year>/ with separate 	eam/ and players/ folders plus Markdown summaries.

## Endpoints / Data

1. **Team metadata**
   - https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{season}/teams/{teamId}?lang=en&region=us
   - Provides ids (id, uid, lternateIds), logos, venue info, links to stats, leaders, schedule, injuries, etc.
   - We store the full payload in 	eam/team_meta.json.

2. **Season stats (team)**
   - Follow the $ref from 	eam_meta['statistics'] - e.g. .../seasons/2025/types/2/teams/22/statistics.
   - The splits.categories[*].stats[*] array contains per-category values: each entry comes with 
ame, displayName, displayValue, per-game values, and league rank.
   - We flatten these into a single dictionary (statCount ˜ 228 metrics) in 	eam/season_stats.json (Markdown summary at 	eam/summary.md).

3. **Schedule / game list**
   - https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{teamId}/schedule?season={season}
   - Returns events[*] with game ids, week descriptors, competitor objects.
   - We keep the most recent N completed games (STATUS_FINAL).

4. **Game summaries (team + player box score)**
   - https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={eventId}
   - oxscore.teams[*] ? team-level stats (statistics list with 
ame, displayValue, alue).
   - oxscore.players[*] ? per-team stat tables grouped by category (passing, ushing, defensive, ...).
   - Regular-season samples now populate thletes for each category (e.g., Kyler Murray’s 21/31, 162 yards, 1 TD in Week 1).
   - Team-level outputs go to 	eam/recent_games.json; player-level outputs go to players/recent_games_players.json with an accompanying Markdown summary (players/summary.md).

5. **Summary bundle**
   - summary.json at the root bundles metadata + season stats + recent-game summaries for downstream MCP work.

## Sample Artifacts (team 22, season 2025)

| File | Contents |
| --- | --- |
| 	eam/team_meta.json | ESPN core team resource (ids, logos, venue, linked refs). |
| 	eam/season_stats.json | Flattened map of 228 season metrics with display names & ranks (Markdown overview in 	eam/summary.md). |
| 	eam/recent_games.json | Recent completed games with team + opponent stat dictionaries. |
| players/recent_games_players.json | Player stat categories for both teams (passing, rushing, defense, special teams) including per-player lines and team totals; summarized in players/summary.md. |
| summary.json | Combined output bundling metadata, season stats, and recent games. |

## Next Steps Toward an MCP

1. **Player stats verification** - ensure we handle cases where ESPN omits certain categories (e.g., preseason games) and add fallbacks.
2. **Endpoint hardening** - add request throttling and retries for production use.
3. **MCP scaffolding** - wrap these calls in a FastAPI service (mcp/espn), exposing tools for team metadata, season stats, and game stats.
4. **ID mappings** - tie ESPN ids to our existing team-id registry so snapshots join cleanly with odds/CFBD data.

