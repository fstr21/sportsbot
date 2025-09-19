# NFL Day Capture (direct SGO + ESPN)

Artifacts archived here capture a working run of `scripts/nfl_day_capture.py` for 09/21/2025.

## Files

- `nfl_day_capture.py` — script snapshot as of 2025-09-18. Prompts for a date, pulls the ESPN schedule, fetches SportsGameOdds `/v2/events` directly (handles pagination + provider 10 req/min rate limit), and merges schedule/odds/team context.
- `events-20250921.json` — merged schedule+odds payload.
- `team_stats-20250921.json` — context per team derived from ESPN.
- `summary-20250921.md` — matchup-organised human summary (counts, kickoff in ET, odds availability).
- `meta-20250921.json` — run metadata and counts.

### Usage

```bash
python scripts/nfl_day_capture.py
# Enter date (MM/DD/YYYY), e.g. 09/21/2025
```

Outputs land in `artifacts/NFL/<MM-DD-YYYY>/`.

### Rate Limits

SportsGameOdds free tier allows **10 requests/minute**. The script tracks requests per window, sleeps to remain compliant, and retries if the provider responds with 429.
