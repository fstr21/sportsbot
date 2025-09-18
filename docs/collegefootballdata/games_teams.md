# `/games/teams`

Team box score statistics for each game. This endpoint feeds the "team context" JSON in our snapshot flow.

## Key parameters
| Param | Required | Notes |
| --- | --- | --- |
| `year` | ? (unless `id` specified) | Season year. |
| `week` | conditionally | Required if `team` and `conference` not provided. |
| `team` | conditionally | Required if `week` and `conference` not provided. Team name (`Georgia`). |
| `conference` | conditionally | Required if `week` and `team` not provided. Conference code (`SEC`). |
| `classification` | optional | `fbs`, `fcs`, `ii`, `iii`. |
| `seasonType` | optional | Same values as `/games`. |
| `id` | optional | Pull stats for a single game id. |

CFBD enforces the conditional requirement: supply at least one of (`week`, `team`, `conference`) with `year`.

## Example
```bash
curl -s \
  -H "Authorization: Bearer $CFBD_API_KEY" \
  "https://api.collegefootballdata.com/games/teams?year=2024&week=4&seasonType=regular"
```

Typical fields (per team per game):
- `team`, `conference`, `homeAway`
- `stats`: array with `category` (`rushingYards`, `passAttempts`, `thirdDownConversions`, etc.) and `stat` values
- `points`, `drives`, `timeOfPossession`

Normalize the `stats` array into a dict keyed by `category` before writing artifacts.

For player-level box scores, see the raw reference in [`cfbd_raw.md`](cfbd_raw.md) (`/games/players`).
