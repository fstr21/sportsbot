# SportsGameOdds Usage Checker

Archived copy of `sgo_usage.py`, which scans `.env.local` for `SPORTSGAMEODDS_API_KEY` entries and reports usage via the `/account/usage` endpoint.

## Capabilities

- Parses commented and active keys in `.env.local` (email/status annotations supported).
- Calls `https://api.sportsgameodds.com/account/usage` for each key.
- Prints tier, active flag, and monthly entity consumption with helper warnings for high/over quota usage.

## Run

```bash
python sgo_usage.py
```

Add or update keys in `.env.local` before running. The script respects the 10 req/min limit, but checking many keys in quick succession can still hit 429 responses; rerun after a short pause if that happens.
