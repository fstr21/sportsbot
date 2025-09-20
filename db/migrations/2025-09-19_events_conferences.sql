-- 2025-09-19 Add events and conference support

CREATE TABLE IF NOT EXISTS events (
  internal_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  event_uid VARCHAR(64) NOT NULL,
  league_id VARCHAR(16) NOT NULL,
  season SMALLINT UNSIGNED NULL,
  season_type VARCHAR(16) NULL,
  week VARCHAR(16) NULL,
  start_time_utc TIMESTAMP NOT NULL,
  start_time_et TIMESTAMP NULL,
  status VARCHAR(32) NOT NULL DEFAULT 'scheduled',
  venue VARCHAR(128) NULL,
  home_team_id VARCHAR(36) NOT NULL,
  away_team_id VARCHAR(36) NOT NULL,
  created_at_utc TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at_utc TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (internal_id),
  UNIQUE KEY uq_events_uid (event_uid),
  KEY idx_events_league_time (league_id, start_time_utc),
  CONSTRAINT fk_events_league FOREIGN KEY (league_id) REFERENCES leagues (league_id),
  CONSTRAINT fk_events_home_team FOREIGN KEY (home_team_id) REFERENCES teams (team_id),
  CONSTRAINT fk_events_away_team FOREIGN KEY (away_team_id) REFERENCES teams (team_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS event_provider_link (
  internal_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  event_internal_id BIGINT UNSIGNED NOT NULL,
  provider VARCHAR(32) NOT NULL,
  provider_entity_id VARCHAR(128) NOT NULL,
  fetched_at_utc TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (internal_id),
  UNIQUE KEY uq_event_provider (provider, provider_entity_id),
  KEY idx_event_provider_event (event_internal_id),
  CONSTRAINT fk_event_provider_event FOREIGN KEY (event_internal_id) REFERENCES events (internal_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS conferences (
  conference_id VARCHAR(36) NOT NULL,
  league_id VARCHAR(16) NOT NULL,
  display_name VARCHAR(128) NOT NULL,
  short_name VARCHAR(32) NULL,
  subdivision VARCHAR(64) NULL,
  created_at_utc TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at_utc TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (conference_id),
  KEY idx_conferences_league (league_id),
  CONSTRAINT fk_conferences_league FOREIGN KEY (league_id) REFERENCES leagues (league_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

ALTER TABLE teams
  ADD COLUMN conference_id VARCHAR(36) NULL AFTER abbr,
  ADD CONSTRAINT fk_teams_conference FOREIGN KEY (conference_id) REFERENCES conferences (conference_id);
