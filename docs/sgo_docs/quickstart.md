# Quickstart

## 1. Get an API key
Sign up for a SportsGameOdds account (free tier works for dev) and grab the API key emailed to you. All requests must include:

```
X-API-Key: <your-key>
```

## 2. Make your first request
The `/v2/sports` endpoint is a lightweight call that confirms auth and shows which sports your key can access.

```bash
curl -s \
  -H "X-API-Key: $SPORTSGAMEODDS_API_KEY" \
  https://api.sportsgameodds.com/v2/sports | jq
```

### Python example
```python
import os
import requests

API_KEY = os.environ["SPORTSGAMEODDS_API_KEY"]
resp = requests.get(
    "https://api.sportsgameodds.com/v2/sports",
    headers={"X-API-Key": API_KEY},
    timeout=30,
)
resp.raise_for_status()
print(resp.json()["data"][0])
```

## 3. Pick the right identifiers
Use the local reference tables:

- [`sports.md`](sports.md) for `sportID`
- [`leagues.md`](leagues.md) for `leagueID`
- [`bookmakers.md`](bookmakers.md) for bookmaker IDs

You can always query the live `/v2/leagues` or `/v2/bookmakers` endpoints to confirm what your plan currently exposes.

## 4. Next steps
Head to [`events.md`](events.md) to pull schedules + odds with date filters and pagination.
