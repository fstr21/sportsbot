# Team metadata endpoints

## `/teams`
Returns team info for a given subdivision.

| Param | Required | Notes |
| --- | --- | --- |
| `division` | optional | `fbs` (default), `fcs`, `ii`, `iii`. |
| `conference` | optional | Filter to a conference. |
| `id` | optional | Numeric id lookup. |

Example:
```bash
curl -s \
  -H "Authorization: Bearer $CFBD_API_KEY" \
  "https://api.collegefootballdata.com/teams?division=fbs"
```

Useful fields: `school`, `mascot`, `alt_name1/2/3`, `conference`, `logos` (array), `location`, `twitter`

## `/teams/matchup`
Find all previous meetings between two teams.

| Param | Required | Notes |
| --- | --- | --- |
| `team1`, `team2` | ? | Team names. |

Returns head-to-head record with an array of game summaries.

## `/teams/fbs`
Shorthand list of FBS schools with `school`, `conference`, `division` fields.

## Other endpoints
The raw dump (`cfbd_raw.md`) includes details for rosters (`/teams/roster`), recruiting (`/teams/recruiting`), etc. Add curated summaries here as we adopt them.
