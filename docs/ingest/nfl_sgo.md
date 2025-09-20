# NFL Odds Snapshot Ingest (SportsGameOdds)

This page tracks the proof-of-concept workflow we are using to pull SportsGameOdds data, store the raw JSON, and load canonical rows into the database. Once the workflow hardens we can relocate scripts, but these are the steps we run today.

## 1. Fetch the snapshot
- Script: `python mappings/odds/sgo_fetch_window.py --output-dir mappings/data/odds/nfl/<window>`
- What it does: Calls the SGO MCP `/tools/events/invoke` endpoint for the given date window. Stores one JSON per event and a `manifest.json` summary under `mappings/data/odds/nfl/<window>/`.
- Why it matters: Each MCP call counts against the shared 10 req/min quota. We make a single call per window to capture all upcoming games (schedule + odds + player blocks).

## 2. Load canonical events
- Script: `python mappings/odds/load_sgo_events.py`
- Reads the snapshot JSONs, resolves canonical team ids (via the `teams` table), converts the kickoff to both UTC and Eastern Time, and upserts into:
  - `events` (columns `event_uid`, `league_id`, `start_time_utc`, `start_time_et`, `status`, `home_team_id`, `away_team_id`).
  - `event_provider_link` (`provider='sportsgameodds'`, `provider_entity_id=<SGO event id>`).
- This keeps the schedule database aligned with each odds snapshot so future ingest (markets, summaries, etc.) can attach to canonical event ids.

## 3. Sync SGO player ids (skill positions)
- Script: `python mappings/players/sync_sgo_players.py --events-dir mappings/data/odds/nfl/<window>`
- Compares the SGO player ids in the snapshot against the ESPN crosswalk (`mappings/data/players/crosswalks/nfl_sgo_to_espn.json`).
- Use `--write` to append newly matched players before running `python mappings/players/load_sgo_player_links.py` to update `player_provider_link`.
- Focused on QB/RB/WR/TE only; defenders/special teams are ignored for now.

## 4. Refresh player memberships (optional but recommended each week)
- Script: `python mappings/players/load_nfl_memberships.py`
- Reloads `player_membership` from the ESPN skill-position rosters so every canonical player points to the correct team.

## Notes
- All scripts currently live under `mappings/` and are documented in `docs/scripts/README.md`.
- The raw SGO JSON is kept verbatim under `mappings/data/odds/` as our audit trail.
- Team conference data for NCAAF is managed separately (`mappings/teams/load_ncaaf_conferences.py`).
