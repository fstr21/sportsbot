# Operational Scripts

These helpers support the weekly NFL odds workflow. Paths may shift when the POC is hardened, but the responsibilities stay the same.

## `mappings/odds/sgo_fetch_window.py`
- **Purpose:** Call the SportsGameOdds MCP `/tools/events/invoke` endpoint for a date window.
- **Why:** Each MCP call counts toward the shared 10 req/min quota. We run this once per window to capture every game into individual JSON files under `mappings/data/odds/<league>/<window>/` plus a manifest.
- **Run:**
  ```bash
  python mappings/odds/sgo_fetch_window.py --output-dir mappings/data/odds/nfl/<window>
  ```
  (Defaults in the script point at the most recent window; adjust before each pull.)

## `mappings/odds/load_sgo_events.py`
- **Purpose:** Import the snapshot JSON into the canonical `events` and `event_provider_link` tables.
- **Why:** Keeps the schedule DB in sync with the odds snapshots so later ingest (markets, summaries) can reference canonical event IDs.
- **Run:**
  ```bash
  python mappings/odds/load_sgo_events.py
  ```
  (`EVENT_DIR` inside the script points at the latest snapshot directory.)

## `mappings/players/sync_sgo_players.py`
- **Purpose:** Scan fresh SGO event dumps for new player IDs, compare against the ESPN crosswalk, and optionally append matches.
- **Why:** The crosswalk only carries skill players we already have in the canonical roster. Each new week may introduce additional SGO IDs; we must add them before reloading provider links.
- **Run:**
  ```bash
  python mappings/players/sync_sgo_players.py --events-dir mappings/data/odds/nfl/<window>
  python mappings/players/sync_sgo_players.py --events-dir ... --write  # to persist matches
  python mappings/players/load_sgo_player_links.py                      # push to DB
  ```

## `mappings/players/load_nfl_memberships.py`
- **Purpose:** Refresh `player_membership` from the ESPN skill-position rosters.
- **Why:** Odds ingestion and crosswalk audits rely on up-to-date team assignments. Re-run after refreshing the ESPN exports.
- **Run:**
  ```bash
  python mappings/players/load_nfl_memberships.py
  ```

Revisit this document whenever the ingest workflow changes.
\n## CollegeFootballData Snapshot\n- Fetch via: \docs/mcp/examples/ncaaf_day_capture/ncaaf_day_capture.py\ (pipe date + blank line).\n- Load schedule: \python mappings/odds/load_cfbd_events.py\ (reads \mappings/data/odds/ncaaf/<date>/events.json\).\n- Copy artifacts from \rtifacts/NCAAF/<MM-DD-YYYY>/\ into \mappings/data/odds/ncaaf/<YYYY-MM-DD>/\ before loading.\n
