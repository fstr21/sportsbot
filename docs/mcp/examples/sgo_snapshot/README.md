# SportsGameOdds MCP Snapshot Example

This folder archives a working copy of the interactive snapshot helper that drives the NFL Day Snapshot experiments, plus sample artifacts from 09/21/2025.

## Files

- `nfl_sgo_snapshot.py` — snapshot script (as-of 2025-09-18). Prompts for a date, calls the Railway-hosted SportsGameOdds MCP `/tools/events/invoke`, applies conservative retry/backoff for upstream 429/502, and writes:
  - `events.json` (all games for the date).
  - One JSON per matchup under `artifacts/nfl/<MM-DD-YYYY>/games/` (each retaining the raw MCP payload in `raw_event`).
  - `summary.md` organised by matchup.
- `events-20250921.json` — sample consolidated output for 09/21/2025.
- `game-1-pit-at-ne.json` — sample per-game file (PIT @ NE) showing the full odds payload.

## Rate Limit Notes

- SportsGameOdds free tier allows **10 requests/min** per API key. The MCP shares one upstream key for all consumers, so space out runs (=1 minute) or bump `PAGE_LIMIT` once debugging is complete.
- The script already waits ~12 seconds before each call and retries (up to 8 times) with 90 second sleeps when the MCP bubbles a 429/502.
- A one-off range pull (08/01-09/24 2025) returned 96 events with populated team/player blocks. Treat it as a reference snapshot and avoid rerunning unless you desperately need a refresh (each run consumes the shared quota).

## Usage

```bash
python scripts/nfl_sgo_snapshot.py
# Enter date in MM/DD/YYYY (e.g. 09/21/2025)
```

Outputs land in `artifacts/nfl/<MM-DD-YYYY>/`.
