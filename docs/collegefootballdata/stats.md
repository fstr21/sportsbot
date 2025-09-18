# Stats and analytics helpers

## `/stats/season`
Season-level team stats.

| Param | Required | Notes |
| --- | --- | --- |
| `year` | ? | Season year. |
| `team` | optional | Filter to a school. |
| `conference` | optional | Filter by conference. |
| `category` | optional | `offense`, `defense`, `specialteams`. Default returns all. |

Each record includes `statType`, `category`, `stat`, and `ranking` fields.

## `/stats/game`
Single-game metrics keyed by `team`, `opponent`, `teamPoints`, `opponentPoints`, plus stat breakdowns. Use `year`, `week`, `team`, `conference` filters similar to `/games`.

## `/ratings/sp+`, `/ratings/massey`, etc.
Advanced power ratings. Parameters generally accept `year` (required) and optional `team`. Consult [`cfbd_raw.md`](cfbd_raw.md) for full parameter lists until we consolidate them here.

Add more structured summaries here as we integrate additional endpoints.
