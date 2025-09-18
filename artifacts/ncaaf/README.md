# NCAAF Artifacts

Daily NCAAF game data captures.

## File Descriptions

### schedule.json
- Source: CollegeFootballData API
- Content: Daily NCAAF games with times, teams, and basic info
- Format: Array of game objects

### odds.json
- Source: SportsGameOdds API
- Content: Betting lines (moneyline, spread, total) for each game
- Format: Array of game odds objects

### team_stats.json
- Source: ESPN API
- Content: Team statistics for games played that day
- Format: Object with team stats by team ID

### summary.md
- Source: Generated from above data
- Content: Human-readable daily summary of games, odds, and key stats
- Format: Markdown document

## Note
NCAAF POC does not include individual player statistics - team-level data only.