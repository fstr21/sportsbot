# Mapping Strategy Overview

## Why this exists
- Provide a single relational schema that keeps our canonical team/player/game IDs aligned with external providers.
- Keep odds and stat snapshots light-weight so Day Snapshot runs can persist data without guessing or fabricating values.
- Follow the locked guidance in oddsdb.md: minimal tables, optional columns wherever feeds may omit values, and policy-aligned timestamps.

## Design principles
- **Nullable everything that can be absent.** Only canonical identifiers, foreign keys, and key timestamps are NOT NULL.
- **Store stats as key/value pairs.** Different sports expose different metrics, so we capture only what a provider actually returns.
- **Provider links are additive.** We can insert the canonical team/game first and add the provider mapping later without schema failures.
- **Times in UTC; display ET elsewhere.** We store kickoff_utc and kickoff_et together for games; all other timestamps are UTC.

## Tables

### leagues
- league_id (PK, VARCHAR) – short key (
fl, 
caaf, etc.).
- display_name (VARCHAR).
- created_at_utc, updated_at_utc (TIMESTAMP DEFAULT CURRENT_TIMESTAMP / ON UPDATE).

### teams
- 	eam_id (PK, VARCHAR).
- league_id (FK → leagues.league_id).
- display_name, location, 
ickname, bbr (all VARCHAR, nullable except display_name).
- created_at_utc, updated_at_utc.
- Indexes: (league_id, abbr), (league_id, display_name) for quick lookups.

### team_variation
- 	eam_var_id (PK, BIGINT AUTO_INCREMENT).
- 	eam_id (FK → teams.team_id).
- ariant_name (VARCHAR) – store lower-cased/trimmed string from feeds.
- created_at_utc (TIMESTAMP DEFAULT CURRENT_TIMESTAMP).
- Unique: (team_id, variant_name).

### team_provider_link
- 	eam_provider_link_id (PK).
- 	eam_id (FK → teams.team_id).
- provider (VARCHAR) – e.g., ESPN, SGO, CFBD.
- provider_team_id (VARCHAR).
- etched_at_utc (TIMESTAMP DEFAULT CURRENT_TIMESTAMP).
- Unique: (provider, provider_team_id) to avoid duplicate links.

### players (NFL-first, extendable)
- player_id (PK, VARCHAR).
- league_id (FK → leagues.league_id).
- ull_name (VARCHAR), position (VARCHAR NULL).
- created_at_utc, updated_at_utc.

### player_membership
- player_id (FK → players.player_id).
- 	eam_id (FK → teams.team_id).
- start_utc (TIMESTAMP), end_utc (TIMESTAMP NULL).
- Unique: (player_id, team_id, start_utc) to block overlaps.

### player_variation / player_provider_link
- Mirrored structure of team variants/links so we can store alternate names/IDs for athletes without schema drift.

### games
- game_id (PK, VARCHAR) – stable opaque ID (hash of league + kickoff + home/away).
- league_id (FK → leagues.league_id).
- kickoff_utc, kickoff_et (TIMESTAMP NOT NULL).
- home_team_id, way_team_id (FK → teams.team_id).
- enue (VARCHAR NULL), status (VARCHAR DEFAULT scheduled).
- created_at_utc, updated_at_utc.
- Indexes: (league_id, kickoff_utc), (home_team_id, kickoff_utc), (away_team_id, kickoff_utc).

### game_provider_link
- game_provider_link_id (PK).
- game_id (FK → games.game_id).
- provider (VARCHAR).
- provider_game_id (VARCHAR).
- etched_at_utc (TIMESTAMP DEFAULT CURRENT_TIMESTAMP).
- Unique: (provider, provider_game_id).

### markets
- market_id (PK, BIGINT AUTO_INCREMENT).
- game_id (FK → games.game_id).
- scope (VARCHAR) – 	eam or player (leave open for future scopes).
- 	ype (VARCHAR) – moneyline, spread, 	otal, player_prop, etc.
- label (VARCHAR) – human-readable description (Team Moneyline, Passing Yards).
- created_at_utc (TIMESTAMP DEFAULT CURRENT_TIMESTAMP).

### market_selection
- selection_id (PK, BIGINT AUTO_INCREMENT).
- market_id (FK → markets.market_id).
- side (VARCHAR) – e.g., home, way, over, under, player.
- 	eam_id (FK → teams.team_id, NULL).
- player_id (FK → players.player_id, NULL).
- line (DECIMAL(10,2) NULL).
- price (INT NULL) – store American odds.
- ook (VARCHAR NULL).
- offered_at_utc, last_seen_utc (TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP).
- Indexes: (market_id), (team_id), (player_id).

### team_game_stats
- 	eam_game_stat_id (PK, BIGINT AUTO_INCREMENT).
- game_id (FK → games.game_id).
- 	eam_id (FK → teams.team_id).
- stat_name (VARCHAR).
- stat_value_numeric (DECIMAL(16,4) NULL).
- stat_value_text (VARCHAR NULL) – fallback when the value is non-numeric.
- source (VARCHAR).
- etched_at_utc (TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP).
- Unique: (game_id, team_id, stat_name) to keep the most recent entry per stat (upserts can update value/timestamp).

### player_game_stats
- Same layout as team stats but keyed on player_id.
- Allows sport-specific stats without schema changes.

### ingest_runs
- ingest_run_id (PK, BIGINT AUTO_INCREMENT).
- 	ask (VARCHAR) – e.g., ingest.day_snapshot.
- league_id (FK → leagues.league_id).
- date_et (DATE).
- started_utc, inished_utc (TIMESTAMP).
- status (VARCHAR) – success, ailed, etc.
- error_label (VARCHAR NULL) – use locked labels.
- rtifacts_path (VARCHAR NULL).

### provider_fetch_log (optional)
- etch_id (PK, BIGINT AUTO_INCREMENT).
- provider (VARCHAR).
- endpoint (VARCHAR).
- params_json (JSON NULL).
- status_code (INT NULL).
- etched_at_utc (TIMESTAMP DEFAULT CURRENT_TIMESTAMP).
- duration_ms (INT NULL).

## Implementation checklist
- [ ] Apply the sql/mapping_schema.sql migration to create the tables.
- [ ] Seed leagues and 	eams with canonical entries before ingesting feed data.
- [ ] When ingesting, create or update 	eams/players first, then attach *_provider_link rows if IDs are present.
- [ ] For missing fields, insert NULLs—never fabricate values to satisfy schema constraints.
- [ ] Add automated checks so duplicated provider IDs or ambiguous mappings fail fast with a clear log entry.
