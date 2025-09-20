# Sports Database Documentation

## Overview
- Re-run `mappings/players/sync_sgo_players.py` against new SGO event snapshots each week and append matches (`--write`) before reloading provider links. This keeps skill players in sync across providers.
- Schema stored in the `sports` MySQL database on Railway.
- Tables cover canonical league/team/player data, odds markets, and ingest auditing.
- All timestamps are stored in UTC columns named with `_utc` suffix per repo conventions; where `_et` columns exist they are recorded in Eastern Time (ET).

## Connection & Environment
- Runtime env vars: `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQLPASSWORD`, `MYSQL_DATABASE`.
- External access uses `MYSQL_PUBLIC_URL`; internal Railway services use `MYSQL_URL`.
- Credentials live in `.env.local` (do not commit real secrets).

## Schema Summary
| Table | Rows | Purpose | Primary Key |
| --- | ---: | --- | --- |
| `game_provider_link` | 0 | Maps internal games to external provider identifiers and keeps the fetch timestamp. | `PRIMARY KEY (`game_provider_link_id`)` |
| `games` | 0 | Canonical schedule records with home/away teams, kickoff timestamps (UTC and ET), and status. | `PRIMARY KEY (`game_id`)` |
| `ingest_runs` | 0 | Execution log for ingest pipelines per league/date, including status and artifact path. | `PRIMARY KEY (`ingest_run_id`)` |
| `leagues` | 0 | Lookup table for supported leagues and their display names. | `PRIMARY KEY (`league_id`)` |
| `market_selection` | 0 | Odds selections (sides) attached to a market, optionally linked to teams or players. | `PRIMARY KEY (`selection_id`)` |
| `markets` | 0 | Odds markets for a game (scope, type, label). | `PRIMARY KEY (`market_id`)` |
| `player_game_stats` | 0 | Per-player stat slices for a game sourced from external providers. | `PRIMARY KEY (`player_game_stat_id`)` |
| `player_membership` | 0 | Team membership history for each player with start/end windows. | `PRIMARY KEY (`player_id`,`team_id`,`start_utc`)` |
| `player_provider_link` | 0 | Maps internal players to provider identifiers. | `PRIMARY KEY (`internal_id`)` |
| `player_variation` | 0 | Alternate spellings or aliases for player names. | `PRIMARY KEY (`player_var_id`)` |
| `players` | 0 | Canonical player directory by league. | `PRIMARY KEY (`player_id`)` |
| `provider_fetch_log` | 0 | Audit log of external provider fetches and their status/duration. | `PRIMARY KEY (`fetch_id`)` |
| `team_game_stats` | 0 | Per-team stat slices for a game from external providers. | `PRIMARY KEY (`team_game_stat_id`)` |
| `team_provider_link` | 0 | Maps internal teams to provider identifiers. | `PRIMARY KEY (`internal_id`)` |
| `team_variation` | 0 | Alternate spellings or aliases for team names. | `PRIMARY KEY (`team_var_id`)` |
| `teams` | 0 | Canonical team directory by league. | `PRIMARY KEY (`team_id`)` |
| `events` | 0 | Canonical event schedule (league, teams, start times). | `PRIMARY KEY (`internal_id`)` |
| `event_provider_link` | 0 | Maps events to provider identifiers. | `PRIMARY KEY (`internal_id`)` |
| `conferences` | 0 | League-specific conference directory (NCAAF etc.). | `PRIMARY KEY (`conference_id`)` |

---

### `game_provider_link`

Maps internal games to external provider identifiers and keeps the fetch timestamp.

- **Row count:** 0
- **Keys & constraints:**
  - Primary: `PRIMARY KEY (`game_provider_link_id`)`
  - Unique: `UNIQUE KEY `uq_game_provider` (`provider`,`provider_game_id`)`
  - Index: `KEY `idx_game_provider_game` (`game_id`)`
  - Foreign: `CONSTRAINT `fk_game_provider_game` FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`)`

Columns:

| Column | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| `game_provider_link_id` | bigint unsigned | NO | PRI |  | auto_increment |
| `game_id` | varchar(64) | NO | MUL |  |  |
| `provider` | varchar(32) | NO | MUL |  |  |
| `provider_game_id` | varchar(128) | NO |  |  |  |
| `fetched_at_utc` | timestamp | NO |  | CURRENT_TIMESTAMP | DEFAULT_GENERATED |

### `games`

Canonical schedule records with home/away teams, kickoff timestamps (UTC and ET), and status.

- **Row count:** 0
- **Keys & constraints:**
  - Primary: `PRIMARY KEY (`game_id`)`
  - Index: `KEY `idx_games_league_kickoff` (`league_id`,`kickoff_utc`)`
  - Index: `KEY `idx_games_home_kickoff` (`home_team_id`,`kickoff_utc`)`
  - Index: `KEY `idx_games_away_kickoff` (`away_team_id`,`kickoff_utc`)`
  - Foreign: `CONSTRAINT `fk_games_away` FOREIGN KEY (`away_team_id`) REFERENCES `teams` (`team_id`)`
  - Foreign: `CONSTRAINT `fk_games_home` FOREIGN KEY (`home_team_id`) REFERENCES `teams` (`team_id`)`
  - Foreign: `CONSTRAINT `fk_games_league` FOREIGN KEY (`league_id`) REFERENCES `leagues` (`league_id`)`

Columns:

| Column | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| `game_id` | varchar(64) | NO | PRI |  |  |
| `league_id` | varchar(16) | NO | MUL |  |  |
| `kickoff_utc` | timestamp | NO |  |  |  |
| `kickoff_et` | timestamp | NO |  |  |  |
| `home_team_id` | varchar(36) | NO | MUL |  |  |
| `away_team_id` | varchar(36) | NO | MUL |  |  |
| `venue` | varchar(128) | YES |  |  |  |
| `status` | varchar(32) | NO |  | scheduled |  |
| `created_at_utc` | timestamp | NO |  | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
| `updated_at_utc` | timestamp | NO |  | CURRENT_TIMESTAMP | DEFAULT_GENERATED on update CURRENT_TIMESTAMP |

### `ingest_runs`

Execution log for ingest pipelines per league/date, including status and artifact path.

- **Row count:** 0
- **Keys & constraints:**
  - Primary: `PRIMARY KEY (`ingest_run_id`)`
  - Index: `KEY `fk_ingest_runs_league` (`league_id`)`
  - Foreign: `CONSTRAINT `fk_ingest_runs_league` FOREIGN KEY (`league_id`) REFERENCES `leagues` (`league_id`)`

Columns:

| Column | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| `ingest_run_id` | bigint unsigned | NO | PRI |  | auto_increment |
| `task` | varchar(64) | NO |  |  |  |
| `league_id` | varchar(16) | NO | MUL |  |  |
| `date_et` | date | NO |  |  |  |
| `started_utc` | timestamp | NO |  |  |  |
| `finished_utc` | timestamp | YES |  |  |  |
| `status` | varchar(32) | NO |  |  |  |
| `error_label` | varchar(64) | YES |  |  |  |
| `artifacts_path` | varchar(255) | YES |  |  |  |

### `leagues`

Lookup table for supported leagues and their display names.

- **Row count:** 0
- **Keys & constraints:**
  - Primary: `PRIMARY KEY (`league_id`)`

Columns:

| Column | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| `league_id` | varchar(16) | NO | PRI |  |  |
| `display_name` | varchar(64) | NO |  |  |  |
| `created_at_utc` | timestamp | NO |  | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
| `updated_at_utc` | timestamp | NO |  | CURRENT_TIMESTAMP | DEFAULT_GENERATED on update CURRENT_TIMESTAMP |

### `market_selection`

Odds selections (sides) attached to a market, optionally linked to teams or players.

- **Row count:** 0
- **Keys & constraints:**
  - Primary: `PRIMARY KEY (`selection_id`)`
  - Index: `KEY `idx_selection_market` (`market_id`)`
  - Index: `KEY `idx_selection_team` (`team_id`)`
  - Index: `KEY `idx_selection_player` (`player_id`)`
  - Foreign: `CONSTRAINT `fk_selection_market` FOREIGN KEY (`market_id`) REFERENCES `markets` (`market_id`)`
  - Foreign: `CONSTRAINT `fk_selection_player` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`)`
  - Foreign: `CONSTRAINT `fk_selection_team` FOREIGN KEY (`team_id`) REFERENCES `teams` (`team_id`)`

Columns:

| Column | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| `selection_id` | bigint unsigned | NO | PRI |  | auto_increment |
| `market_id` | bigint unsigned | NO | MUL |  |  |
| `side` | varchar(32) | NO |  |  |  |
| `team_id` | varchar(36) | YES | MUL |  |  |
| `player_id` | varchar(36) | YES | MUL |  |  |
| `line` | decimal(10,2) | YES |  |  |  |
| `price` | int | YES |  |  |  |
| `book` | varchar(64) | YES |  |  |  |
| `offered_at_utc` | timestamp | NO |  | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
| `last_seen_utc` | timestamp | NO |  | CURRENT_TIMESTAMP | DEFAULT_GENERATED |

### `markets`

Odds markets for a game (scope, type, label).

- **Row count:** 0
- **Keys & constraints:**
  - Primary: `PRIMARY KEY (`market_id`)`
  - Index: `KEY `idx_markets_game` (`game_id`)`
  - Foreign: `CONSTRAINT `fk_markets_game` FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`)`

Columns:

| Column | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| `market_id` | bigint unsigned | NO | PRI |  | auto_increment |
| `game_id` | varchar(64) | NO | MUL |  |  |
| `scope` | varchar(32) | NO |  |  |  |
| `type` | varchar(64) | NO |  |  |  |
| `label` | varchar(128) | NO |  |  |  |
| `created_at_utc` | timestamp | NO |  | CURRENT_TIMESTAMP | DEFAULT_GENERATED |

### `player_game_stats`

Per-player stat slices for a game sourced from external providers.

- **Row count:** 0
- **Keys & constraints:**
  - Primary: `PRIMARY KEY (`player_game_stat_id`)`
  - Unique: `UNIQUE KEY `uq_player_stat` (`game_id`,`player_id`,`stat_name`)`
  - Index: `KEY `idx_player_stats_player` (`player_id`)`
  - Foreign: `CONSTRAINT `fk_player_stats_game` FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`)`
  - Foreign: `CONSTRAINT `fk_player_stats_player` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`)`

Columns:

| Column | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| `player_game_stat_id` | bigint unsigned | NO | PRI |  | auto_increment |
| `game_id` | varchar(64) | NO | MUL |  |  |
| `player_id` | varchar(36) | NO | MUL |  |  |
| `stat_name` | varchar(128) | NO |  |  |  |
| `stat_value_numeric` | decimal(16,4) | YES |  |  |  |
| `stat_value_text` | varchar(128) | YES |  |  |  |
| `source` | varchar(32) | NO |  |  |  |
| `fetched_at_utc` | timestamp | NO |  | CURRENT_TIMESTAMP | DEFAULT_GENERATED |

### `player_membership`

Team membership history for each player with start/end windows.

- **Row count:** 0
- **Keys & constraints:**
  - Primary: `PRIMARY KEY (`player_id`,`team_id`,`start_utc`)`
  - Index: `KEY `fk_membership_team` (`team_id`)`
  - Foreign: `CONSTRAINT `fk_membership_player` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`)`
  - Foreign: `CONSTRAINT `fk_membership_team` FOREIGN KEY (`team_id`) REFERENCES `teams` (`team_id`)`

Columns:

| Column | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| `player_id` | varchar(36) | NO | PRI |  |  |
| `team_id` | varchar(36) | NO | PRI |  |  |
| `start_utc` | timestamp | NO | PRI |  |  |
| `end_utc` | timestamp | YES |  |  |  |

### `player_provider_link`

Maps internal players to provider identifiers.

- **Row count:** 0
- **Keys & constraints:**
  - Primary: `PRIMARY KEY (`internal_id`)`
  - Unique: `UNIQUE KEY `uq_player_provider` (`provider`,`provider_entity_id`)`
  - Index: `KEY `idx_player_provider_player` (`player_id`)`
  - Foreign: `CONSTRAINT `fk_player_provider_player` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`)`

Columns:

| Column | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| `internal_id` | bigint unsigned | NO | PRI |  | auto_increment |
| `player_id` | varchar(36) | NO | MUL |  |  |
| `provider` | varchar(32) | NO | MUL |  |  |
| `provider_entity_id` | varchar(128) | NO |  |  |  |
| `fetched_at_utc` | timestamp | NO |  | CURRENT_TIMESTAMP | DEFAULT_GENERATED |

### `player_variation`

Alternate spellings or aliases for player names.

- **Row count:** 0
- **Keys & constraints:**
  - Primary: `PRIMARY KEY (`player_var_id`)`
  - Unique: `UNIQUE KEY `uq_player_variant` (`player_id`,`variant_name`)`
  - Foreign: `CONSTRAINT `fk_player_variant_player` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`)`

Columns:

| Column | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| `player_var_id` | bigint unsigned | NO | PRI |  | auto_increment |
| `player_id` | varchar(36) | NO | MUL |  |  |
| `variant_name` | varchar(160) | NO |  |  |  |
| `created_at_utc` | timestamp | NO |  | CURRENT_TIMESTAMP | DEFAULT_GENERATED |

### `players`

Canonical player directory by league.

- **Row count:** 0
- **Keys & constraints:**
  - Primary: `PRIMARY KEY (`player_id`)`
  - Index: `KEY `fk_players_league` (`league_id`)`
  - Foreign: `CONSTRAINT `fk_players_league` FOREIGN KEY (`league_id`) REFERENCES `leagues` (`league_id`)`

Columns:

| Column | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| `player_id` | varchar(36) | NO | PRI |  |  |
| `league_id` | varchar(16) | NO | MUL |  |  |
| `full_name` | varchar(128) | NO |  |  |  |
| `position` | varchar(32) | YES |  |  |  |
| `created_at_utc` | timestamp | NO |  | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
| `updated_at_utc` | timestamp | NO |  | CURRENT_TIMESTAMP | DEFAULT_GENERATED on update CURRENT_TIMESTAMP |

### `provider_fetch_log`

Audit log of external provider fetches and their status/duration.

- **Row count:** 0
- **Keys & constraints:**
  - Primary: `PRIMARY KEY (`fetch_id`)`

Columns:

| Column | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| `fetch_id` | bigint unsigned | NO | PRI |  | auto_increment |
| `provider` | varchar(32) | NO |  |  |  |
| `endpoint` | varchar(255) | NO |  |  |  |
| `params_json` | json | YES |  |  |  |
| `status_code` | int | YES |  |  |  |
| `fetched_at_utc` | timestamp | NO |  | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
| `duration_ms` | int | YES |  |  |  |

### `team_game_stats`

Per-team stat slices for a game from external providers.

- **Row count:** 0
- **Keys & constraints:**
  - Primary: `PRIMARY KEY (`team_game_stat_id`)`
  - Unique: `UNIQUE KEY `uq_team_stat` (`game_id`,`team_id`,`stat_name`)`
  - Index: `KEY `fk_team_stats_team` (`team_id`)`
  - Foreign: `CONSTRAINT `fk_team_stats_game` FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`)`
  - Foreign: `CONSTRAINT `fk_team_stats_team` FOREIGN KEY (`team_id`) REFERENCES `teams` (`team_id`)`

Columns:

| Column | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| `team_game_stat_id` | bigint unsigned | NO | PRI |  | auto_increment |
| `game_id` | varchar(64) | NO | MUL |  |  |
| `team_id` | varchar(36) | NO | MUL |  |  |
| `stat_name` | varchar(128) | NO |  |  |  |
| `stat_value_numeric` | decimal(16,4) | YES |  |  |  |
| `stat_value_text` | varchar(128) | YES |  |  |  |
| `source` | varchar(32) | NO |  |  |  |
| `fetched_at_utc` | timestamp | NO |  | CURRENT_TIMESTAMP | DEFAULT_GENERATED |

### `team_provider_link`

Maps internal teams to provider identifiers.

- **Row count:** 0
- **Keys & constraints:**
  - Primary: `PRIMARY KEY (`internal_id`)`
  - Unique: `UNIQUE KEY `uq_team_provider` (`provider`,`provider_entity_id`)`
  - Index: `KEY `idx_team_provider_team` (`team_id`)`
  - Foreign: `CONSTRAINT `fk_team_provider_team` FOREIGN KEY (`team_id`) REFERENCES `teams` (`team_id`)`

Columns:

| Column | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| `internal_id` | bigint unsigned | NO | PRI |  | auto_increment |
| `team_id` | varchar(36) | NO | MUL |  |  |
| `provider` | varchar(32) | NO | MUL |  |  |
| `provider_entity_id` | varchar(128) | NO |  |  |  |
| `fetched_at_utc` | timestamp | NO |  | CURRENT_TIMESTAMP | DEFAULT_GENERATED |

### `team_variation`

Alternate spellings or aliases for team names.

- **Row count:** 0
- **Keys & constraints:**
  - Primary: `PRIMARY KEY (`team_var_id`)`
  - Unique: `UNIQUE KEY `uq_team_variant` (`team_id`,`variant_name`)`
  - Foreign: `CONSTRAINT `fk_team_variant_team` FOREIGN KEY (`team_id`) REFERENCES `teams` (`team_id`)`

Columns:

| Column | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| `team_var_id` | bigint unsigned | NO | PRI |  | auto_increment |
| `team_id` | varchar(36) | NO | MUL |  |  |
| `variant_name` | varchar(160) | NO |  |  |  |
| `created_at_utc` | timestamp | NO |  | CURRENT_TIMESTAMP | DEFAULT_GENERATED |

### `teams`

Canonical team directory by league.

- **Row count:** 0
- **Keys & constraints:**
  - Primary: `PRIMARY KEY (`team_id`)`
  - Index: `KEY `idx_teams_league_abbr` (`league_id`,`abbr`)`
  - Index: `KEY `idx_teams_league_display` (`league_id`,`display_name`)`
  - Foreign: `CONSTRAINT `fk_teams_league` FOREIGN KEY (`league_id`) REFERENCES `leagues` (`league_id`)`

Columns:

| Column | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| `team_id` | varchar(36) | NO | PRI |  |  |
| `league_id` | varchar(16) | NO | MUL |  |  |
| `display_name` | varchar(128) | NO |  |  |  |
| `location` | varchar(128) | YES |  |  |  |
| `nickname` | varchar(128) | YES |  |  |  |
| `abbr` | varchar(16) | YES |  |  |  |
| `conference_id` | varchar(36) | YES | MUL |  |  |
| `created_at_utc` | timestamp | NO |  | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
| `updated_at_utc` | timestamp | NO |  | CURRENT_TIMESTAMP | DEFAULT_GENERATED on update CURRENT_TIMESTAMP |
### `events`

Canonical event schedule for each league. Stores kickoff times in UTC and optional ET, along with the participating teams.

- **Row count:** 0
- **Keys & constraints:**
  - Primary: `PRIMARY KEY (`internal_id`)`
  - Unique: `UNIQUE KEY `uq_events_uid` (`event_uid`)`
  - Foreign: `CONSTRAINT `fk_events_league` FOREIGN KEY (`league_id`) REFERENCES `leagues` (`league_id`)`
  - Foreign: `CONSTRAINT `fk_events_home_team` FOREIGN KEY (`home_team_id`) REFERENCES `teams` (`team_id`)`
  - Foreign: `CONSTRAINT `fk_events_away_team` FOREIGN KEY (`away_team_id`) REFERENCES `teams` (`team_id`)`

Columns:

| Column | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| `internal_id` | bigint unsigned | NO | PRI |  | auto_increment |
| `event_uid` | varchar(64) | NO | UNI |  |  |
| `league_id` | varchar(16) | NO | MUL |  |  |
| `season` | smallint unsigned | YES |  |  |  |
| `season_type` | varchar(16) | YES |  |  |  |
| `week` | varchar(16) | YES |  |  |  |
| `start_time_utc` | timestamp | NO |  |  |  |
| `start_time_et` | timestamp | YES |  |  | Stored in Eastern Time (ET) |
| `status` | varchar(32) | NO |  | scheduled |  |
| `venue` | varchar(128) | YES |  |  |  |
| `home_team_id` | varchar(36) | NO | MUL |  |  |
| `away_team_id` | varchar(36) | NO | MUL |  |  |
| `created_at_utc` | timestamp | NO |  | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
| `updated_at_utc` | timestamp | NO |  | CURRENT_TIMESTAMP | DEFAULT_GENERATED on update CURRENT_TIMESTAMP |

### `event_provider_link`

Maps canonical events to provider-specific identifiers (e.g., SportsGameOdds event IDs).

- **Row count:** 0
- **Keys & constraints:**
  - Primary: `PRIMARY KEY (`internal_id`)`
  - Unique: `UNIQUE KEY `uq_event_provider` (`provider`,`provider_entity_id`)`
  - Foreign: `CONSTRAINT `fk_event_provider_event` FOREIGN KEY (`event_internal_id`) REFERENCES `events` (`internal_id`)`

Columns:

| Column | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| `internal_id` | bigint unsigned | NO | PRI |  | auto_increment |
| `event_internal_id` | bigint unsigned | NO | MUL |  |  |
| `provider` | varchar(32) | NO | MUL |  |  |
| `provider_entity_id` | varchar(128) | NO |  |  |  |
| `fetched_at_utc` | timestamp | NO |  | CURRENT_TIMESTAMP | DEFAULT_GENERATED |

### `conferences`

Conference directory for leagues that have subdivisions (e.g., NCAAF).

- **Row count:** 0
- **Keys & constraints:**
  - Primary: `PRIMARY KEY (`conference_id`)`
  - Foreign: `CONSTRAINT `fk_conferences_league` FOREIGN KEY (`league_id`) REFERENCES `leagues` (`league_id`)`

Columns:

| Column | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| `conference_id` | varchar(36) | NO | PRI |  |  |
| `league_id` | varchar(16) | NO | MUL |  |  |
| `display_name` | varchar(128) | NO |  |  |  |
| `short_name` | varchar(32) | YES |  |  |  |
| `subdivision` | varchar(64) | YES |  |  |  |
| `created_at_utc` | timestamp | NO |  | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
| `updated_at_utc` | timestamp | NO |  | CURRENT_TIMESTAMP | DEFAULT_GENERATED on update CURRENT_TIMESTAMP |



