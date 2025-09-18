# `/games`

Returns schedule and final results. Used for building the daily schedule slice.

## Key parameters
| Param | Required | Notes |
| --- | --- | --- |
| `year` | ? (unless `id` provided) | Season year, e.g., `2024`. |
| `week` | optional | Numeric week (1+). Combine with `seasonType` if using postseason. |
| `seasonType` | optional | `regular`, `postseason`, `both`, `allstar`, `spring_regular`, `spring_postseason`. Default `regular`. |
| `team` | optional | Filter by team name (e.g., `Georgia`). |
| `conference` | optional | Filter by conference code (e.g., `SEC`). |
| `classification` | optional | `fbs`, `fcs`, `ii`, `iii`. |
| `startWeek`, `endWeek` | optional | Bound weeks within a season. |
| `id` | optional | Retrieve a single game by CFBD game id. |

## Request examples
### Full week
```bash
curl -s \
  -H "Authorization: Bearer $CFBD_API_KEY" \
  "https://api.collegefootballdata.com/games?year=2024&week=4&seasonType=regular"
```

### Team-specific slice
```bash
curl -s \
  -H "Authorization: Bearer $CFBD_API_KEY" \
  "https://api.collegefootballdata.com/games?year=2024&team=Notre%20Dame"
```

### Example response fields
- `id`, `season`, `week`, `seasonType`
- `startDate`, `venue`
- `homeTeam`, `homePoints`, `homeConference`, `homeLineScores`
- `awayTeam`, `awayPoints`, `awayConference`, `awayLineScores`
- `excitementIndex`, `highlights`

For team statistics tied to each game use [`games_teams.md`](games_teams.md).
