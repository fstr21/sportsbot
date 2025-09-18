# NFL Artifacts

Daily NFL game data captures.

## File Descriptions

### schedule.json
- Source: ESPN API
- Content: Daily NFL games with times, teams, and basic info
- Format: Array of game objects

### odds.json
- Source: SportsGameOdds API
- Content: Betting lines (moneyline, spread, total) for each game
- Format: Array of game odds objects

### team_stats.json
- Source: ESPN API
- Content: Team statistics for games played that day
- Format: Object with team stats by team ID

### player_stats.json
- Source: ESPN API
- Content: Key player statistics for games played that day
- Format: Object with player stats by player ID

### summary.md
- Source: Generated from above data
- Content: Human-readable daily summary of games, odds, and key stats
- Format: Markdown document