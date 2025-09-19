# NCAAF Day Capture Example

Snapshot of `scripts/ncaaf_day_capture.py` run for 09/19/2025.

## Files

- `ncaaf_day_capture.py` — script snapshot as of 2025-09-18. Prompts for a date, calls ESPN for the NCAAF slate, hits SportsGameOdds `/v2/events`, and merges schedule + odds (teams only).
- `events-20250919.json` — merged schedule/odds output.
- `summary-20250919.md` — matchup summary (ET kickoffs, odds presence, counts).

## Usage

```bash
python scripts/ncaaf_day_capture.py
# Enter MM/DD/YYYY (e.g. 09/19/2025)
```

Outputs land in `artifacts/NCAAF/<MM-DD-YYYY>/`.

Rate limit behaviour mirrors the NFL script (built-in sleep to stay under 10 requests/min).
