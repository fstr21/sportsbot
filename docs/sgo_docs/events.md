# Events Endpoint (`/v2/events`)

The `/v2/events` endpoint returns schedule, odds, and rich metadata for games, props, and novelty markets. Use it to build the daily snapshot join.

## Common query parameters
| Param | Required | Description |
| --- | --- | --- |
| `leagueID` | ? | Target league (see [`leagues.md`](leagues.md)) |
| `type` | optional | `match`, `prop`, or other categories. Default includes everything; set to `match` for schedule use cases. |
| `startsAfter` | optional | ISO timestamp filter (UTC). Combine with `startsBefore` to limit to a day window. |
| `startsBefore` | optional | Upper bound for start time. |
| `limit` | optional | Page size (max 50). Default 10. |
| `cursor` | optional | Pagination cursor returned in `nextCursor`. |
| `teamID`, `eventID`, `bookmakerID`, etc. | optional | Additional filters; see sport-specific docs for availability. |

### Building a day window in ET
```python
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
start_et = datetime.combine(target_date, time.min, tzinfo=ET)
end_et = start_et + timedelta(days=1)
params = {
    "leagueID": "NFL",
    "type": "match",
    "startsAfter": start_et.astimezone(ZoneInfo("UTC")).isoformat().replace("+00:00", "Z"),
    "startsBefore": end_et.astimezone(ZoneInfo("UTC")).isoformat().replace("+00:00", "Z"),
}
```

### Pagination loop
```javascript
let nextCursor = null;
const events = [];

do {
  const response = await axios.get("https://api.sportsgameodds.com/v2/events", {
    params: {
      leagueID: "NFL",
      type: "match",
      startsAfter: "2025-09-18T04:00:00Z",
      startsBefore: "2025-09-19T04:00:00Z",
      limit: 50,
      cursor: nextCursor,
    },
    headers: { "X-API-Key": process.env.SPORTSGAMEODDS_API_KEY },
  });

  events.push(...response.data.data);
  nextCursor = response.data.nextCursor;
} while (nextCursor);
```

### Odds payloads
Each event contains an `odds` object. Convert it to a list if you prefer array semantics:

```python
odds = event.get("odds", {})
markets = []
for odd_id, payload in odds.items():
    market = {
        "odd_id": odd_id,
        "market_name": payload.get("marketName"),
        "bet_type": payload.get("betTypeID"),
        "book_odds": payload.get("bookOdds"),
        "bookmakers": payload.get("byBookmaker", {}),
    }
    market["participants"] = [
        frag for frag in odd_id.split("-") if frag.endswith("_NFL")
    ]
    markets.append(market)
```

Refer back to the sport-specific sheets for any parameters unique to a league (e.g., baseball double-headers, soccer markets).
