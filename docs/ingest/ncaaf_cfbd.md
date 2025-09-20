# NCAAF Odds Snapshot Ingest (CollegeFootballData)

Interim flow for pulling CollegeFootballData (CFBD) schedule + odds via our Railway MCP deployment.

## 1. Fetch the snapshot
- Script: `python docs/mcp/examples/ncaaf_day_capture/ncaaf_day_capture.py`
- Input sequence (in the shell):
  ```bash
  $env:COLLEGE_FOOTBALL_DATA_API_KEY='<cfbd_key>'
  "09/20/2025`n`n" | python docs/mcp/examples/ncaaf_day_capture/ncaaf_day_capture.py \
      --mcp-url https://collegefootballdatamcp-production.up.railway.app
  ```
  (First line answers the date prompt; second blank line skips the optional team filter.)
- Output: writes `events.json` and `summary.md` under `artifacts/NCAAF/<MM-DD-YYYY>/`.
- After the run, copy the artifacts into `mappings/data/odds/ncaaf/<YYYY-MM-DD>/` so ingest scripts have a stable path.

## 2. Load canonical events
- Script: `python mappings/odds/load_cfbd_events.py`
- Reads `mappings/data/odds/ncaaf/<date>/events.json`, resolves canonical `teams` entries (only conferences listed in `docs/ncaaf_conferences.md` are expected), and upserts into:
  - `events` (`event_uid = cfbd:<game_id>`, kickoff stored in both UTC and ET).
  - `event_provider_link` (`provider='collegefootballdata'`, `provider_entity_id=<game_id>`).
- Skips games whose teams are not in our conference mapping (e.g., FCS opponents). Review warnings and add teams as needed.

## 3. Player/odds integration
- CFBD odds payloads contain provider lines (DraftKings, Bovada, etc.) but no player IDs. We only store schedule data; odds ingestion will map into our market tables later.
- NCAAF team conference assignments are managed via `mappings/teams/load_ncaaf_conferences.py`.

Update this document once we automate the date prompts or move the scripts.
