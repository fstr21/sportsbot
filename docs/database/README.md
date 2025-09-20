# Sports Database Documentation

## Overview
The Railway MySQL instance exposes two schemas:
- `sports` (primary canonical store for leagues, teams, events, odds, and ingest logs)
- `railway` (Railway system schema; today it only holds a temporary `scratch_notes` table used for MCP connection tests)

Unless otherwise noted, all ingestion and mapping code should target the `sports` schema documented below.

## Connection & Credentials
- Host/Gateway: `tramway.proxy.rlwy.net`
- External port: `23052`
- Internal service DNS: `mysql.railway.internal:3306`
- Retrieve credentials from `.env.local` (`MYSQL_PUBLIC_URL`, `MYSQL_URL`, `MYSQLUSER`, `MYSQLPASSWORD`, `MYSQLDATABASE`).
- Quick check:
  ```bash
  python -c "import mysql.connector; conn=mysql.connector.connect(host='<HOST>', port=<PORT>, user='<USER>', password='<PASS>', database='sports'); cur=conn.cursor(); cur.execute('SHOW TABLES'); print(cur.fetchall()); cur.close(); conn.close()"
  ```

## Schema Summary (`sports`)
| Table | Rows | Purpose |
| --- | ---: | --- |
| `leagues` | 2 | Lookup of supported leagues and display metadata. |
| `conferences` | 5 | Conference directory tied to `leagues`, used for NCAAF groupings. |
| `teams` | 113 | Canonical team directory per league, including conference links. |
| `team_variation` | 0 | Alternate team spellings/aliases for mapping. |
| `team_provider_link` | 32 | Mapping of canonical teams to upstream provider identifiers. |
| `games` | 0 | Legacy string-keyed schedule records (home/away, kickoff timestamps). |
| `game_provider_link` | 0 | Mapping of `games` entries to provider game identifiers. |
| `events` | 21 | Primary event schedule table (auto-increment id, kickoff in UTC/ET). |
| `event_provider_link` | 21 | Mapping of `events` rows to provider event identifiers. |
| `markets` | 0 | Odds markets tied to events (scope, type, labels). |
| `market_selection` | 0 | Selections (sides/outcomes) within markets, optionally tied to teams/players. |
| `provider_fetch_log` | 0 | Audit log of upstream provider fetch attempts. |
| `ingest_runs` | 0 | Execution log for ingest pipelines by league/date. |
| `players` | 748 | Canonical player directory across leagues. |
| `player_variation` | 0 | Alternate spellings/aliases used for players. |
| `player_provider_link` | 1323 | Mapping of canonical players to provider identifiers. |
| `player_membership` | 748 | Team membership history for each player. |
| `player_game_stats` | 0 | Per-player game stat slices from providers. |
| `team_game_stats` | 0 | Per-team game stat slices from providers. |

## Table Details
### `leagues`
- **Purpose:** Lookup of supported leagues and display metadata.
- **Rows:** 2
- **Primary key:** (`league_id`)

| Column | Type | Null | Default | Extra |
| --- | --- | --- | --- | --- |
| `league_id` | varchar(16) | NO | None | - |
| `display_name` | varchar(64) | NO | None | - |
| `created_at_utc` | timestamp | NO | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
| `updated_at_utc` | timestamp | NO | CURRENT_TIMESTAMP | DEFAULT_GENERATED on update CURRENT_TIMESTAMP |

### `conferences`
- **Purpose:** Conference directory tied to `leagues`, used for NCAAF groupings.
- **Rows:** 5
- **Primary key:** (`conference_id`)
- **Indexes:** KEY `idx_conferences_league` (`league_id`)
- **Foreign keys:** CONSTRAINT `fk_conferences_league` FOREIGN KEY (`league_id`) REFERENCES `leagues` (`league_id`)

| Column | Type | Null | Default | Extra |
| --- | --- | --- | --- | --- |
| `conference_id` | varchar(36) | NO | None | - |
| `league_id` | varchar(16) | NO | None | - |
| `display_name` | varchar(128) | NO | None | - |
| `short_name` | varchar(32) | YES | None | - |
| `subdivision` | varchar(64) | YES | None | - |
| `created_at_utc` | timestamp | NO | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
| `updated_at_utc` | timestamp | NO | CURRENT_TIMESTAMP | DEFAULT_GENERATED on update CURRENT_TIMESTAMP |

### `teams`
- **Purpose:** Canonical team directory per league, including conference links.
- **Rows:** 113
- **Primary key:** (`team_id`)
- **Indexes:** KEY `idx_teams_league_abbr` (`league_id`,`abbr`), KEY `idx_teams_league_display` (`league_id`,`display_name`), KEY `fk_teams_conference` (`conference_id`)
- **Foreign keys:** CONSTRAINT `fk_teams_conference` FOREIGN KEY (`conference_id`) REFERENCES `conferences` (`conference_id`), CONSTRAINT `fk_teams_league` FOREIGN KEY (`league_id`) REFERENCES `leagues` (`league_id`)

| Column | Type | Null | Default | Extra |
| --- | --- | --- | --- | --- |
| `team_id` | varchar(36) | NO | None | - |
| `league_id` | varchar(16) | NO | None | - |
| `display_name` | varchar(128) | NO | None | - |
| `location` | varchar(128) | YES | None | - |
| `nickname` | varchar(128) | YES | None | - |
| `abbr` | varchar(16) | YES | None | - |
| `conference_id` | varchar(36) | YES | None | - |
| `created_at_utc` | timestamp | NO | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
| `updated_at_utc` | timestamp | NO | CURRENT_TIMESTAMP | DEFAULT_GENERATED on update CURRENT_TIMESTAMP |

### `team_variation`
- **Purpose:** Alternate team spellings/aliases for mapping.
- **Rows:** 0
- **Primary key:** (`team_var_id`)
- **Indexes:** UNIQUE KEY `uq_team_variant` (`team_id`,`variant_name`)
- **Foreign keys:** CONSTRAINT `fk_team_variant_team` FOREIGN KEY (`team_id`) REFERENCES `teams` (`team_id`)

| Column | Type | Null | Default | Extra |
| --- | --- | --- | --- | --- |
| `team_var_id` | bigint unsigned | NO | None | auto_increment |
| `team_id` | varchar(36) | NO | None | - |
| `variant_name` | varchar(160) | NO | None | - |
| `created_at_utc` | timestamp | NO | CURRENT_TIMESTAMP | DEFAULT_GENERATED |

### `team_provider_link`
- **Purpose:** Mapping of canonical teams to upstream provider identifiers.
- **Rows:** 32
- **Primary key:** (`internal_id`)
- **Indexes:** UNIQUE KEY `uq_team_provider` (`provider`,`provider_entity_id`), KEY `idx_team_provider_team` (`team_id`)
- **Foreign keys:** CONSTRAINT `fk_team_provider_team` FOREIGN KEY (`team_id`) REFERENCES `teams` (`team_id`)

| Column | Type | Null | Default | Extra |
| --- | --- | --- | --- | --- |
| `internal_id` | bigint unsigned | NO | None | auto_increment |
| `team_id` | varchar(36) | NO | None | - |
| `provider` | varchar(32) | NO | None | - |
| `provider_entity_id` | varchar(128) | NO | None | - |
| `fetched_at_utc` | timestamp | NO | CURRENT_TIMESTAMP | DEFAULT_GENERATED |

### `games`
- **Purpose:** Legacy string-keyed schedule records (home/away, kickoff timestamps).
- **Rows:** 0
- **Primary key:** (`game_id`)
- **Indexes:** KEY `idx_games_league_kickoff` (`league_id`,`kickoff_utc`), KEY `idx_games_home_kickoff` (`home_team_id`,`kickoff_utc`), KEY `idx_games_away_kickoff` (`away_team_id`,`kickoff_utc`)
- **Foreign keys:** CONSTRAINT `fk_games_away` FOREIGN KEY (`away_team_id`) REFERENCES `teams` (`team_id`), CONSTRAINT `fk_games_home` FOREIGN KEY (`home_team_id`) REFERENCES `teams` (`team_id`), CONSTRAINT `fk_games_league` FOREIGN KEY (`league_id`) REFERENCES `leagues` (`league_id`)

| Column | Type | Null | Default | Extra |
| --- | --- | --- | --- | --- |
| `game_id` | varchar(64) | NO | None | - |
| `league_id` | varchar(16) | NO | None | - |
| `kickoff_utc` | timestamp | NO | None | - |
| `kickoff_et` | timestamp | NO | None | - |
| `home_team_id` | varchar(36) | NO | None | - |
| `away_team_id` | varchar(36) | NO | None | - |
| `venue` | varchar(128) | YES | None | - |
| `status` | varchar(32) | NO | scheduled | - |
| `created_at_utc` | timestamp | NO | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
| `updated_at_utc` | timestamp | NO | CURRENT_TIMESTAMP | DEFAULT_GENERATED on update CURRENT_TIMESTAMP |

### `game_provider_link`
- **Purpose:** Mapping of `games` entries to provider game identifiers.
- **Rows:** 0
- **Primary key:** (`game_provider_link_id`)
- **Indexes:** UNIQUE KEY `uq_game_provider` (`provider`,`provider_game_id`), KEY `idx_game_provider_game` (`game_id`)
- **Foreign keys:** CONSTRAINT `fk_game_provider_game` FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`)

| Column | Type | Null | Default | Extra |
| --- | --- | --- | --- | --- |
| `game_provider_link_id` | bigint unsigned | NO | None | auto_increment |
| `game_id` | varchar(64) | NO | None | - |
| `provider` | varchar(32) | NO | None | - |
| `provider_game_id` | varchar(128) | NO | None | - |
| `fetched_at_utc` | timestamp | NO | CURRENT_TIMESTAMP | DEFAULT_GENERATED |

### `events`
- **Purpose:** Primary event schedule table (auto-increment id, kickoff in UTC/ET).
- **Rows:** 21
- **Primary key:** (`internal_id`)
- **Indexes:** UNIQUE KEY `uq_events_uid` (`event_uid`), KEY `idx_events_league_time` (`league_id`,`start_time_utc`), KEY `fk_events_home_team` (`home_team_id`), KEY `fk_events_away_team` (`away_team_id`)
- **Foreign keys:** CONSTRAINT `fk_events_away_team` FOREIGN KEY (`away_team_id`) REFERENCES `teams` (`team_id`), CONSTRAINT `fk_events_home_team` FOREIGN KEY (`home_team_id`) REFERENCES `teams` (`team_id`), CONSTRAINT `fk_events_league` FOREIGN KEY (`league_id`) REFERENCES `leagues` (`league_id`)

| Column | Type | Null | Default | Extra |
| --- | --- | --- | --- | --- |
| `internal_id` | bigint unsigned | NO | None | auto_increment |
| `event_uid` | varchar(64) | NO | None | - |
| `league_id` | varchar(16) | NO | None | - |
| `season` | smallint unsigned | YES | None | - |
| `season_type` | varchar(16) | YES | None | - |
| `week` | varchar(16) | YES | None | - |
| `start_time_utc` | timestamp | NO | None | - |
| `start_time_et` | timestamp | YES | None | - |
| `status` | varchar(32) | NO | scheduled | - |
| `venue` | varchar(128) | YES | None | - |
| `home_team_id` | varchar(36) | NO | None | - |
| `away_team_id` | varchar(36) | NO | None | - |
| `created_at_utc` | timestamp | NO | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
| `updated_at_utc` | timestamp | NO | CURRENT_TIMESTAMP | DEFAULT_GENERATED on update CURRENT_TIMESTAMP |

### `event_provider_link`
- **Purpose:** Mapping of `events` rows to provider event identifiers.
- **Rows:** 21
- **Primary key:** (`internal_id`)
- **Indexes:** UNIQUE KEY `uq_event_provider` (`provider`,`provider_entity_id`), KEY `idx_event_provider_event` (`event_internal_id`)
- **Foreign keys:** CONSTRAINT `fk_event_provider_event` FOREIGN KEY (`event_internal_id`) REFERENCES `events` (`internal_id`)

| Column | Type | Null | Default | Extra |
| --- | --- | --- | --- | --- |
| `internal_id` | bigint unsigned | NO | None | auto_increment |
| `event_internal_id` | bigint unsigned | NO | None | - |
| `provider` | varchar(32) | NO | None | - |
| `provider_entity_id` | varchar(128) | NO | None | - |
| `fetched_at_utc` | timestamp | NO | CURRENT_TIMESTAMP | DEFAULT_GENERATED |

### `markets`
- **Purpose:** Odds markets tied to events (scope, type, labels).
- **Rows:** 0
- **Primary key:** (`market_id`)
- **Indexes:** KEY `idx_markets_game` (`game_id`)
- **Foreign keys:** CONSTRAINT `fk_markets_game` FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`)

| Column | Type | Null | Default | Extra |
| --- | --- | --- | --- | --- |
| `market_id` | bigint unsigned | NO | None | auto_increment |
| `game_id` | varchar(64) | NO | None | - |
| `scope` | varchar(32) | NO | None | - |
| `type` | varchar(64) | NO | None | - |
| `label` | varchar(128) | NO | None | - |
| `created_at_utc` | timestamp | NO | CURRENT_TIMESTAMP | DEFAULT_GENERATED |

### `market_selection`
- **Purpose:** Selections (sides/outcomes) within markets, optionally tied to teams/players.
- **Rows:** 0
- **Primary key:** (`selection_id`)
- **Indexes:** KEY `idx_selection_market` (`market_id`), KEY `idx_selection_team` (`team_id`), KEY `idx_selection_player` (`player_id`)
- **Foreign keys:** CONSTRAINT `fk_selection_market` FOREIGN KEY (`market_id`) REFERENCES `markets` (`market_id`), CONSTRAINT `fk_selection_player` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`), CONSTRAINT `fk_selection_team` FOREIGN KEY (`team_id`) REFERENCES `teams` (`team_id`)

| Column | Type | Null | Default | Extra |
| --- | --- | --- | --- | --- |
| `selection_id` | bigint unsigned | NO | None | auto_increment |
| `market_id` | bigint unsigned | NO | None | - |
| `side` | varchar(32) | NO | None | - |
| `team_id` | varchar(36) | YES | None | - |
| `player_id` | varchar(36) | YES | None | - |
| `line` | decimal(10,2) | YES | None | - |
| `price` | int | YES | None | - |
| `book` | varchar(64) | YES | None | - |
| `offered_at_utc` | timestamp | NO | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
| `last_seen_utc` | timestamp | NO | CURRENT_TIMESTAMP | DEFAULT_GENERATED |

### `provider_fetch_log`
- **Purpose:** Audit log of upstream provider fetch attempts.
- **Rows:** 0
- **Primary key:** (`fetch_id`)

| Column | Type | Null | Default | Extra |
| --- | --- | --- | --- | --- |
| `fetch_id` | bigint unsigned | NO | None | auto_increment |
| `provider` | varchar(32) | NO | None | - |
| `endpoint` | varchar(255) | NO | None | - |
| `params_json` | json | YES | None | - |
| `status_code` | int | YES | None | - |
| `fetched_at_utc` | timestamp | NO | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
| `duration_ms` | int | YES | None | - |

### `ingest_runs`
- **Purpose:** Execution log for ingest pipelines by league/date.
- **Rows:** 0
- **Primary key:** (`ingest_run_id`)
- **Indexes:** KEY `fk_ingest_runs_league` (`league_id`)
- **Foreign keys:** CONSTRAINT `fk_ingest_runs_league` FOREIGN KEY (`league_id`) REFERENCES `leagues` (`league_id`)

| Column | Type | Null | Default | Extra |
| --- | --- | --- | --- | --- |
| `ingest_run_id` | bigint unsigned | NO | None | auto_increment |
| `task` | varchar(64) | NO | None | - |
| `league_id` | varchar(16) | NO | None | - |
| `date_et` | date | NO | None | - |
| `started_utc` | timestamp | NO | None | - |
| `finished_utc` | timestamp | YES | None | - |
| `status` | varchar(32) | NO | None | - |
| `error_label` | varchar(64) | YES | None | - |
| `artifacts_path` | varchar(255) | YES | None | - |

### `players`
- **Purpose:** Canonical player directory across leagues.
- **Rows:** 748
- **Primary key:** (`player_id`)
- **Indexes:** KEY `fk_players_league` (`league_id`)
- **Foreign keys:** CONSTRAINT `fk_players_league` FOREIGN KEY (`league_id`) REFERENCES `leagues` (`league_id`)

| Column | Type | Null | Default | Extra |
| --- | --- | --- | --- | --- |
| `player_id` | varchar(36) | NO | None | - |
| `league_id` | varchar(16) | NO | None | - |
| `full_name` | varchar(128) | NO | None | - |
| `position` | varchar(32) | YES | None | - |
| `created_at_utc` | timestamp | NO | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
| `updated_at_utc` | timestamp | NO | CURRENT_TIMESTAMP | DEFAULT_GENERATED on update CURRENT_TIMESTAMP |

### `player_variation`
- **Purpose:** Alternate spellings/aliases used for players.
- **Rows:** 0
- **Primary key:** (`player_var_id`)
- **Indexes:** UNIQUE KEY `uq_player_variant` (`player_id`,`variant_name`)
- **Foreign keys:** CONSTRAINT `fk_player_variant_player` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`)

| Column | Type | Null | Default | Extra |
| --- | --- | --- | --- | --- |
| `player_var_id` | bigint unsigned | NO | None | auto_increment |
| `player_id` | varchar(36) | NO | None | - |
| `variant_name` | varchar(160) | NO | None | - |
| `created_at_utc` | timestamp | NO | CURRENT_TIMESTAMP | DEFAULT_GENERATED |

### `player_provider_link`
- **Purpose:** Mapping of canonical players to provider identifiers.
- **Rows:** 1323
- **Primary key:** (`internal_id`)
- **Indexes:** UNIQUE KEY `uq_player_provider` (`provider`,`provider_entity_id`), KEY `idx_player_provider_player` (`player_id`)
- **Foreign keys:** CONSTRAINT `fk_player_provider_player` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`)

| Column | Type | Null | Default | Extra |
| --- | --- | --- | --- | --- |
| `internal_id` | bigint unsigned | NO | None | auto_increment |
| `player_id` | varchar(36) | NO | None | - |
| `provider` | varchar(32) | NO | None | - |
| `provider_entity_id` | varchar(128) | NO | None | - |
| `fetched_at_utc` | timestamp | NO | CURRENT_TIMESTAMP | DEFAULT_GENERATED |

### `player_membership`
- **Purpose:** Team membership history for each player.
- **Rows:** 748
- **Primary key:** (`player_id`,`team_id`,`start_utc`)
- **Indexes:** KEY `fk_membership_team` (`team_id`)
- **Foreign keys:** CONSTRAINT `fk_membership_player` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`), CONSTRAINT `fk_membership_team` FOREIGN KEY (`team_id`) REFERENCES `teams` (`team_id`)

| Column | Type | Null | Default | Extra |
| --- | --- | --- | --- | --- |
| `player_id` | varchar(36) | NO | None | - |
| `team_id` | varchar(36) | NO | None | - |
| `start_utc` | timestamp | NO | None | - |
| `end_utc` | timestamp | YES | None | - |

### `player_game_stats`
- **Purpose:** Per-player game stat slices from providers.
- **Rows:** 0
- **Primary key:** (`player_game_stat_id`)
- **Indexes:** UNIQUE KEY `uq_player_stat` (`game_id`,`player_id`,`stat_name`), KEY `idx_player_stats_player` (`player_id`)
- **Foreign keys:** CONSTRAINT `fk_player_stats_game` FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`), CONSTRAINT `fk_player_stats_player` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`)

| Column | Type | Null | Default | Extra |
| --- | --- | --- | --- | --- |
| `player_game_stat_id` | bigint unsigned | NO | None | auto_increment |
| `game_id` | varchar(64) | NO | None | - |
| `player_id` | varchar(36) | NO | None | - |
| `stat_name` | varchar(128) | NO | None | - |
| `stat_value_numeric` | decimal(16,4) | YES | None | - |
| `stat_value_text` | varchar(128) | YES | None | - |
| `source` | varchar(32) | NO | None | - |
| `fetched_at_utc` | timestamp | NO | CURRENT_TIMESTAMP | DEFAULT_GENERATED |

### `team_game_stats`
- **Purpose:** Per-team game stat slices from providers.
- **Rows:** 0
- **Primary key:** (`team_game_stat_id`)
- **Indexes:** UNIQUE KEY `uq_team_stat` (`game_id`,`team_id`,`stat_name`), KEY `fk_team_stats_team` (`team_id`)
- **Foreign keys:** CONSTRAINT `fk_team_stats_game` FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`), CONSTRAINT `fk_team_stats_team` FOREIGN KEY (`team_id`) REFERENCES `teams` (`team_id`)

| Column | Type | Null | Default | Extra |
| --- | --- | --- | --- | --- |
| `team_game_stat_id` | bigint unsigned | NO | None | auto_increment |
| `game_id` | varchar(64) | NO | None | - |
| `team_id` | varchar(36) | NO | None | - |
| `stat_name` | varchar(128) | NO | None | - |
| `stat_value_numeric` | decimal(16,4) | YES | None | - |
| `stat_value_text` | varchar(128) | YES | None | - |
| `source` | varchar(32) | NO | None | - |
| `fetched_at_utc` | timestamp | NO | CURRENT_TIMESTAMP | DEFAULT_GENERATED |

## Additional Schema
- `railway.scratch_notes` retains a single row captured during MCP testing. It can be dropped once no longer needed for connectivity checks.

## Maintenance Notes
- Apply migrations or documented SQL when altering structures; update this README afterward.
- All `_utc` timestamp columns store UTC values; `_et` columns store Eastern Time.
- Keep `.env.local` out of source control; rotate secrets when sharing access.
