# College Football Data API – Quick Reference (v5.11.5)

**Base URL:** `https://api.collegefootballdata.com/`
**Auth:** API key (see CFBD docs)
**Spec:** OAS 3.0

## Python Client Library
**Repository:** https://github.com/CFBD/cfbd-python
**Installation:** `pip install cfbd`
**Purpose:** Pre-built Python client for simplified API integration

## Planned Integration
**Goal:** Create MCP server on Railway using cfbd-python library
**Status:** Documentation phase - implementation planned
**Architecture:** Discord Bot → MCP Protocol → CFB MCP Server → cfbd-python → College Football Data API

## Legend
- **Req.** = Required parameter
- **Enum** values shown when present
- Response = shape highlights (not full schema)

---

## games — Game scores and stats

### `GET /games` — Historical game data
| Param | Type | Req. | Notes |
|---|---|---:|---|
| `year` | int | **Yes*** | Required except when `id` is set |
| `week` | int |  |  |
| `seasonType` | string |  | Enum: `regular`, `postseason`, `both`, `allstar`, `spring_regular`, `spring_postseason` |
| `classification` | string |  | Enum: `fbs`, `fcs`, `ii`, `iii` |
| `team`, `home`, `away` | string |  | Filters |
| `conference` | string |  |  |
| `id` | int |  | Get single game |

**Response (array):** game objects with teams, scores, venue, Elo, etc.

---

### `GET /games/teams` — Team box score stats
| Param | Type | Req. | Notes |
|---|---|---:|---|
| `year` | int | **Yes*** | “Year + one of (`week` \| `team` \| `conference`) unless `id` is set” |
| `week` | int |  | See rule above |
| `team` | string |  | See rule above |
| `conference` | string |  | See rule above |
| `classification` | string |  | Enum: `fbs`, `fcs`, `ii`, `iii` |
| `seasonType` | string |  | Enum as above |
| `id` | int |  | Single game |

**Response (array):** `{ id, teams:[ { teamId, team, conference, homeAway, points, stats:[{category, stat}] } ] }`.

---

### `GET /games/players` — Player box score stats
| Param | Type | Req. | Notes |
|---|---|---:|---|
| `year` | int | **Yes*** | Same “year + one of …” rule as above unless `id` |
| `week`, `team`, `conference` |  |  |  |
| `classification` | string |  | Enum: `fbs`, `fcs`, `ii`, `iii` |
| `seasonType` | string |  | Enum as above |
| `category` | string |  | Player stat category |
| `id` | int |  | Single game |

**Response (array):** per-team categories → types → athletes with stats.

---

### `GET /games/media` — TV/Radio/Web listings
| Param | Type | Req. | Notes |
|---|---|---:|---|
| `year` | int | **Yes** |  |
| `seasonType` | string |  | Enum as above |
| `week`, `team`, `conference` |  |  |  |
| `mediaType` | string |  | Enum: `tv`, `radio`, `web`, `ppv`, `mobile` |
| `classification` | string |  | Enum: `fbs`, `fcs`, `ii`, `iii` |

**Response:** start time, home/away, outlet, type.

---

### `GET /games/weather` — Game weather (Patreon)
| Param | Type | Req. | Notes |
|---|---|---:|---|
| `year` | int | **Yes*** | Required if `gameId` not specified |
| `seasonType`, `week`, `team`, `conference` |  |  |  |
| `classification` | string |  | Enum: `fbs`, `fcs`, `ii`, `iii` |
| `gameId` | int |  | Single game |

**Response:** weather metrics per game (temp, wind, precipitation, etc.).

---

### `GET /records` — Historical team records
| Param | Type | Req. |
|---|---|---:|
| `year` | int | **Yes*** (if `team` not set) |
| `team` | string | **Yes*** (if `year` not set) |
| `conference` | string |  |

**Response:** totals, conference/home/away/neutral splits.

---

### `GET /calendar` — Calendar by year
| Param | Type | Req. |
|---|---|---:|
| `year` | int | **Yes** |

**Response:** season/week windows (start & end dates).

---

### `GET /scoreboard` — Live scoreboard
| Param | Type | Req. | Notes |
|---|---|---:|---|
| `classification` | string |  | Enum default `fbs` |
| `conference` | string |  |  |

**Response:** status, clock, venue, weather, and `betting` (spread, O/U, moneylines).

---

### `GET /game/box/advanced` — Advanced box score
| Param | Type | Req. |
|---|---|---:|
| `id` | int | **Yes** |

**Response:** team and player advanced metrics (EPA/PPA, success rates, havoc, etc.).

---

## drives — Drive data

### `GET /drives`
Common game filters with:
| Param | Notes |
|---|---|
| `year` (**Yes**) |  |
| `seasonType`, `week`, `team`, `offense`, `defense` |  |
| `conference`, `offenseConference`, `defenseConference` |  |
| `classification` (enum) |  |

**Response:** per-drive start/end context, result, scores, elapsed, yards.

---

## plays — Play-by-play

### `GET /plays`
| Param | Type | Req. | Notes |
|---|---|---:|---|
| `year` | int | **Yes** |
| `week` | int | **Yes** |
| `team`, `offense`, `defense`, `conference` |  |  |
| `offenseConference`, `defenseConference` |  |  |
| `playType` | string |  | Abbrev filter |
| `seasonType`, `classification` | string |  | Enums as above |

**Response:** rich PBP with down/distance, yardline, play text, PPA/EPA, wallclock.

### `GET /plays/types` — Play types (id/text/abbr)

### `GET /plays/stats` — Player↔play associations (limit 2000)
Optional filters: `year, week, team, gameId, athleteId, statTypeId, seasonType, conference`.  
**Response:** rows linking players to plays with stat values.

### `GET /plays/stats/types` — Stat type names (id/name)

### `GET /live/plays` — Live PBP + advanced
| Param | Type | Req. |
|---|---|---:|
| `gameId` | int | **Yes** |

**Response:** live teams/drives/plays with EPA & success metrics.

---

## teams — Team info

### `GET /teams`
| Param | Type | Req. |
|---|---|---:|
| `conference` | string |  |
| `year` | int |  |

**Response:** team metadata (logos, colors, location with stadium/timezone).

### `GET /teams/fbs` — FBS teams (optional `year`)

### `GET /teams/matchup`
| Param | Type | Req. |
|---|---|---:|
| `team1` | string | **Yes** |
| `team2` | string | **Yes** |
| `minYear`, `maxYear` | int |  |

**Response:** head-to-head games + win totals.

---

## players — Player data

### `GET /player/search`
Req: `searchTerm`. Opt: `year`, `team`, `position`. Returns top 100.

### `GET /player/usage`
Req: `year`. Opt: `conference`, `position`, `team`, `playerId`, `excludeGarbageTime`.  
**Response:** usage splits (passing/rushing, downs).

### `GET /player/returning`
Req: `year` or `team`. Opt: `conference`. Returns PPA retention and usage.

### `GET /player/portal`
Req: `year`. Transfer entries with origin/destination and ratings.

---

## rankings — Historical polls

### `GET /rankings`
Req: `year`. Opt: `seasonType`, `week`.  
**Response:** polls with ranked teams and points.

---

## betting — Lines & markets

### `GET /lines`
| Param | Type | Req. | Notes |
|---|---|---:|---|
| `gameId` | int |  | If not set, `year` is typically needed |
| `year` | int | **Yes*** | When `gameId` not provided |
| `seasonType` | string |  | Enum as above |
| `week`, `team`, `home`, `away`, `conference` |  |  |
| `provider` | string |  | Book name filter |

**Response:** per game lines by provider (spread, OU, ML; open & current).

---

## ratings — SP+, SRS, Elo, FPI

- `GET /ratings/sp` — SP+ by year or team  
- `GET /ratings/sp/conferences` — SP+ aggregated by conference  
- `GET /ratings/srs` — SRS  
- `GET /ratings/elo` — Elo (opt: `year`, `week`, `seasonType`, `team`, `conference`)  
- `GET /ratings/fpi` — FPI with resume/efficiency components  
All return arrays of rating objects with team/conference and value(s).

---

## metrics — PPA, WP, FG expected points

- `GET /ppa/predicted` — **Req:** `down`, `distance`.  
- `GET /ppa/teams` — season PPA (team or year required).  
- `GET /ppa/games` — team PPA by game (year required).  
- `GET /ppa/players/games` — player PPA by game (year required; then `week` or `team`).  
- `GET /ppa/players/season` — player PPA by season (`year` or `playerId`).  
- `GET /metrics/wp` — play win probability by `gameId`.  
- `GET /metrics/wp/pregame` — pregame win probabilities (opt `year`, `week`, `seasonType`, `team`).  
- `GET /metrics/fg/ep` — FG expected points table.

---

## recruiting — Players, teams, grouped

- `GET /recruiting/players` — **Req:** `year` or `team`; opt `position`, `state`, `classification` (enum: `JUCO`, `PrepSchool`, `HighSchool`).  
- `GET /recruiting/teams` — opt `year`, `team`.  
- `GET /recruiting/groups` — opt `team`, `conference`, `recruitType`, `startYear`, `endYear`.

---

## adjustedMetrics — Opponent-adjusted (WEPA)

- `GET /wepa/team/season` — team season metrics (opt `year`, `team`, `conference`).  
- `GET /wepa/players/passing` — player passing WEPA (opt year/team/conf/position).  
- `GET /wepa/players/rushing` — player rushing WEPA.  
- `GET /wepa/players/kicking` — kicker PAAR (schema listed).

---

## draft — NFL Draft

- `GET /draft/teams` — NFL teams list  
- `GET /draft/positions` — position categories  
- `GET /draft/picks` — draft history (opt `year`, `team`, `school`, `conference`, `position`)

---

## info

### `GET /info` — User info & rate limits
No params. Returns patron level and remaining calls, or null if not authenticated.

---

## Common Enums & Types (select)

- **`seasonType`**: `regular`, `postseason`, `both`, `allstar`, `spring_regular`, `spring_postseason`  
- **`classification`**: `fbs`, `fcs`, `ii`, `iii`  
- **`mediaType`**: `tv`, `radio`, `web`, `ppv`, `mobile`  
- **Betting line item**: `{ provider, spread, formattedSpread, spreadOpen, overUnder, overUnderOpen, homeMoneyline, awayMoneyline }`  
- **Scoreboard betting**: `{ spread, overUnder, homeMoneyline, awayMoneyline }`

---

## Notes & gotchas
- Some endpoints enforce **mutual-requirement rules** (e.g., *“year + one of week/team/conference”*). Respect these to avoid 400s.  
- Live endpoints and weather may require elevated access (Patreon).

---

## Schemas
### `AdjustedTeamMetrics`
| Field | Notes |
|---|---|
| `year` | [...] |
| `teamId` | [...] |
| `team` | [...] |
| `conference` | [...] |
| `epa` | {... |

### `PlayerWeightedEPA`
| Field | Notes |
|---|---|
| `year` | [...] |
| `athleteId` | [...] |
| `athleteName` | [...] |
| `position` | [...] |
| `team` | [...] |
| `conference` | [...] |
| `wepa` | [...] |
| `plays` | [...] |

### `KickerPAAR`
| Field | Notes |
|---|---|
| `year` | [...] |
| `athleteId` | [...] |
| `athleteName` | [...] |
| `team` | [...] |
| `conference` | [...] |
| `paar` | [...] |
| `attempts` | [...] |

### `Venue`
| Field | Notes |
|---|---|
| `id` | [...] |
| `name` | [...] |
| `city` | [...] |
| `state` | [...] |
| `zip` | [...] |
| `countryCode` | [...] |
| `timezone` | [...] |
| `latitude` | [...] |
| `longitude` | [...] |
| `elevation` | [...] |
| `capacity` | [...] |
| `constructionYear` | [...] |
| `grass` | [...] |
| `dome` | [...] |

### `Team`
| Field | Notes |
|---|---|
| `id` | [...] |
| `school` | [...] |
| `mascot` | [...] |
| `abbreviation` | [...] |
| `alternateNames` | [...] |
| `conference` | [...] |
| `division` | [...] |
| `classification` | [...] |
| `color` | [...] |
| `alternateColor` | [...] |
| `logos` | [...] |
| `twitter` | [...] |
| `location` | {... |

### `MatchupGame`
| Field | Notes |
|---|---|
| `season` | [...] |
| `week` | [...] |
| `seasonType` | [...] |
| `date` | [...] |
| `neutralSite` | [...] |
| `venue` | [...] |
| `homeTeam` | [...] |
| `homeScore` | [...] |
| `awayTeam` | [...] |
| `awayScore` | [...] |
| `winner` | [...] |

### `Matchup`
| Field | Notes |
|---|---|
| `team1` | [...] |
| `team2` | [...] |
| `startYear` | [...] |
| `endYear` | [...] |
| `team1Wins` | [...] |
| `team2Wins` | [...] |
| `ties` | [...] |
| `games` | [...] |

### `RosterPlayer`
| Field | Notes |
|---|---|
| `id` | [...] |
| `firstName` | [...] |
| `lastName` | [...] |
| `team` | [...] |
| `height` | [...] |
| `weight` | [...] |
| `jersey` | [...] |
| `year` | [...] |
| `position` | [...] |
| `homeCity` | [...] |
| `homeState` | [...] |
| `homeCountry` | [...] |
| `homeLatitude` | [...] |
| `homeLongitude` | [...] |
| `homeCountyFIPS` | [...] |
| `recruitIds` | [...] |

### `Conference`
| Field | Notes |
|---|---|
| `id` | [...] |
| `name` | [...] |
| `shortName` | [...] |
| `abbreviation` | [...] |
| `classification` | [...] |

### `TeamTalent`
| Field | Notes |
|---|---|
| `year` | [...] |
| `team` | [...] |
| `talent` | [...] |

### `PlayerStat`
| Field | Notes |
|---|---|
| `season` | [...] |
| `playerId` | [...] |
| `player` | [...] |
| `position` | [...] |
| `team` | [...] |
| `conference` | [...] |
| `category` | [...] |
| `statType` | [...] |
| `stat` | [...] |

### `TeamStat`
| Field | Notes |
|---|---|
| `season` | [...] |
| `team` | [...] |
| `conference` | [...] |
| `statName` | [...] |
| `statValue` | {... |

### `AdvancedSeasonStat`
| Field | Notes |
|---|---|
| `season` | [...] |
| `team` | [...] |
| `conference` | [...] |
| `offense` | {... |

### `AdvancedGameStat`
| Field | Notes |
|---|---|
| `gameId` | [...] |
| `season` | [...] |
| `week` | [...] |
| `team` | [...] |
| `opponent` | [...] |
| `offense` | {... |

### `Recruit`
| Field | Notes |
|---|---|
| `id` | [...] |
| `athleteId` | [...] |
| `recruitType` | RecruitClassification[...] |
| `year` | [...] |
| `ranking` | [...] |
| `name` | [...] |
| `school` | [...] |
| `committedTo` | [...] |
| `position` | [...] |
| `height` | [...] |
| `weight` | [...] |
| `stars` | [...] |
| `rating` | [...] |
| `city` | [...] |
| `stateProvince` | [...] |
| `country` | [...] |
| `hometownInfo` | {... |

### `TeamRecruitingRanking`
| Field | Notes |
|---|---|
| `year` | [...] |
| `rank` | [...] |
| `team` | [...] |
| `points` | [...] |

### `AggregatedTeamRecruiting`
| Field | Notes |
|---|---|
| `team` | [...] |
| `conference` | [...] |
| `positionGroup` | [...] |
| `averageRating` | [...] |
| `totalRating` | [...] |
| `commits` | [...] |
| `averageStars` | [...] |

### `TeamSP`
| Field | Notes |
|---|---|
| `year` | [...] |
| `team` | [...] |
| `conference` | [...] |
| `rating` | [...] |
| `ranking` | [...] |
| `secondOrderWins` | [...] |
| `sos` | [...] |
| `offense` | {... |

### `ConferenceSP`
| Field | Notes |
|---|---|
| `year` | [...] |
| `conference` | [...] |
| `rating` | [...] |
| `secondOrderWins` | [...] |
| `sos` | [...] |
| `offense` | {... |

### `TeamSRS`
| Field | Notes |
|---|---|
| `year` | [...] |
| `team` | [...] |
| `conference` | [...] |
| `division` | [...] |
| `rating` | [...] |
| `ranking` | [...] |

### `TeamElo`
| Field | Notes |
|---|---|
| `year` | [...] |
| `team` | [...] |
| `conference` | [...] |
| `elo` | [...] |

### `TeamFPI`
| Field | Notes |
|---|---|
| `year` | [...] |
| `team` | [...] |
| `conference` | [...] |
| `fpi` | [...] |
| `resumeRanks` | {... |

### `PollRank`
| Field | Notes |
|---|---|
| `rank` | [...] |
| `teamId` | [...] |
| `school` | [...] |
| `conference` | [...] |
| `firstPlaceVotes` | [...] |
| `points` | [...] |

### `Poll`
| Field | Notes |
|---|---|
| `poll` | [...] |
| `ranks` | [...] |

### `PollWeek`
| Field | Notes |
|---|---|
| `season` | [...] |
| `seasonType` | SeasonType[...] |
| `week` | [...] |
| `polls` | [...] |

### `Play`
| Field | Notes |
|---|---|
| `id` | [...] |
| `driveId` | [...] |
| `gameId` | [...] |
| `driveNumber` | [...] |
| `playNumber` | [...] |
| `offense` | [...] |
| `offenseConference` | [...] |
| `offenseScore` | [...] |
| `defense` | [...] |
| `home` | [...] |
| `away` | [...] |
| `defenseConference` | [...] |
| `defenseScore` | [...] |
| `period` | [...] |
| `clock` | {... |

### `PlayType`
| Field | Notes |
|---|---|
| `id` | [...] |
| `text` | [...] |
| `abbreviation` | [...] |

### `PlayStat`
| Field | Notes |
|---|---|
| `gameId` | [...] |
| `season` | [...] |
| `week` | [...] |
| `team` | [...] |
| `conference` | [...] |
| `opponent` | [...] |
| `teamScore` | [...] |
| `opponentScore` | [...] |
| `driveId` | [...] |
| `playId` | [...] |
| `period` | [...] |
| `clock` | {... |

### `PlayStatType`
| Field | Notes |
|---|---|
| `id` | [...] |
| `name` | [...] |

### `PlayerSearchResult`
| Field | Notes |
|---|---|
| `id` | [...] |
| `team` | [...] |
| `name` | [...] |
| `firstName` | [...] |
| `lastName` | [...] |
| `weight` | [...] |
| `height` | [...] |
| `jersey` | [...] |
| `position` | [...] |
| `hometown` | [...] |
| `teamColor` | [...] |
| `teamColorSecondary` | [...] |

### `PlayerPPAChartItem`
| Field | Notes |
|---|---|
| `playNumber` | [...] |
| `avgPPA` | [...] |

### `PlayerUsage`
| Field | Notes |
|---|---|
| `season` | [...] |
| `id` | [...] |
| `name` | [...] |
| `position` | [...] |
| `team` | [...] |
| `conference` | [...] |
| `usage` | {... |

### `ReturningProduction`
| Field | Notes |
|---|---|
| `season` | [...] |
| `team` | [...] |
| `conference` | [...] |
| `totalPPA` | [...] |
| `totalPassingPPA` | [...] |
| `totalReceivingPPA` | [...] |
| `totalRushingPPA` | [...] |
| `percentPPA` | [...] |
| `percentPassingPPA` | [...] |
| `percentReceivingPPA` | [...] |
| `percentRushingPPA` | [...] |
| `usage` | [...] |
| `passingUsage` | [...] |
| `receivingUsage` | [...] |
| `rushingUsage` | [...] |

### `PlayerTransfer`
| Field | Notes |
|---|---|
| `season` | [...] |
| `firstName` | [...] |
| `lastName` | [...] |
| `position` | [...] |
| `origin` | [...] |
| `destination` | [...] |
| `transferDate` | [...] |
| `rating` | [...] |
| `stars` | [...] |
| `eligibility` | [...] |

### `PredictedPointsValue`
| Field | Notes |
|---|---|
| `yardLine` | [...] |
| `predictedPoints` | [...] |

### `TeamSeasonPredictedPointsAdded`
| Field | Notes |
|---|---|
| `season` | [...] |
| `conference` | [...] |
| `team` | [...] |
| `offense` | {... |

### `TeamGamePredictedPointsAdded`
| Field | Notes |
|---|---|
| `gameId` | [...] |
| `season` | [...] |
| `week` | [...] |
| `seasonType` | SeasonType[...] |
| `team` | [...] |
| `conference` | [...] |
| `opponent` | [...] |
| `offense` | {... |

### `PlayerGamePredictedPointsAdded`
| Field | Notes |
|---|---|
| `season` | [...] |
| `week` | [...] |
| `seasonType` | SeasonType[...] |
| `id` | [...] |
| `name` | [...] |
| `position` | [...] |
| `team` | [...] |
| `opponent` | [...] |
| `averagePPA` | {... |

### `PlayerSeasonPredictedPointsAdded`
| Field | Notes |
|---|---|
| `season` | [...] |
| `id` | [...] |
| `name` | [...] |
| `position` | [...] |
| `team` | [...] |
| `conference` | [...] |
| `averagePPA` | {... |

### `PlayWinProbability`
| Field | Notes |
|---|---|
| `gameId` | [...] |
| `playId` | [...] |
| `playText` | [...] |
| `homeId` | [...] |
| `home` | [...] |
| `awayId` | [...] |
| `away` | [...] |
| `spread` | [...] |
| `homeBall` | [...] |
| `homeScore` | [...] |
| `awayScore` | [...] |
| `yardLine` | [...] |
| `down` | [...] |
| `distance` | [...] |
| `homeWinProbability` | [...] |
| `playNumber` | [...] |

### `PregameWinProbability`
| Field | Notes |
|---|---|
| `season` | [...] |
| `seasonType` | SeasonType[...] |
| `week` | [...] |
| `gameId` | [...] |
| `homeTeam` | [...] |
| `awayTeam` | [...] |
| `spread` | [...] |
| `homeWinProbability` | [...] |

### `FieldGoalEP`
| Field | Notes |
|---|---|
| `yardsToGoal` | [...] |
| `distance` | [...] |
| `expectedPoints` | [...] |

### `LiveGameTeam`
| Field | Notes |
|---|---|
| `teamId` | [...] |
| `team` | [...] |
| `homeAway` | [...] |
| `lineScores` | [...] |
| `points` | [...] |
| `drives` | [...] |
| `scoringOpportunities` | [...] |
| `pointsPerOpportunity` | [...] |
| `averageStartYardLine` | [...] |
| `plays` | [...] |
| `lineYards` | [...] |
| `lineYardsPerRush` | [...] |
| `secondLevelYards` | [...] |
| `secondLevelYardsPerRush` | [...] |
| `openFieldYards` | [...] |
| `openFieldYardsPerRush` | [...] |
| `epaPerPlay` | [...] |
| `totalEpa` | [...] |
| `passingEpa` | [...] |
| `epaPerPass` | [...] |
| `rushingEpa` | [...] |
| `epaPerRush` | [...] |
| `successRate` | [...] |
| `standardDownSuccessRate` | [...] |
| `passingDownSuccessRate` | [...] |
| `explosiveness` | [...] |
| `deserveToWin` | [...] |

### `LiveGamePlay`
| Field | Notes |
|---|---|
| `id` | [...] |
| `homeScore` | [...] |
| `awayScore` | [...] |
| `period` | [...] |
| `clock` | [...] |
| `wallClock` | [...] |
| `teamId` | [...] |
| `team` | [...] |
| `down` | [...] |
| `distance` | [...] |
| `yardsToGoal` | [...] |
| `yardsGained` | [...] |
| `playTypeId` | [...] |
| `playType` | [...] |
| `epa` | [...] |
| `garbageTime` | [...] |
| `success` | [...] |
| `rushPass` | [...] |
| `downType` | [...] |
| `playText` | [...] |

### `LiveGameDrive`
| Field | Notes |
|---|---|
| `id` | [...] |
| `offenseId` | [...] |
| `offense` | [...] |
| `defenseId` | [...] |
| `defense` | [...] |
| `playCount` | [...] |
| `yards` | [...] |
| `startPeriod` | [...] |
| `startClock` | [...] |
| `startYardsToGoal` | [...] |
| `endPeriod` | [...] |
| `endClock` | [...] |
| `endYardsToGoal` | [...] |
| `duration` | [...] |
| `scoringOpportunity` | [...] |
| `result` | [...] |
| `pointsGained` | [...] |
| `plays` | [...] |

### `LiveGame`
| Field | Notes |
|---|---|
| `id` | [...] |
| `status` | [...] |
| `period` | [...] |
| `clock` | [...] |
| `possession` | [...] |
| `down` | [...] |
| `distance` | [...] |
| `yardsToGoal` | [...] |
| `teams` | [...] |
| `drives` | [...] |

### `GameLine`
| Field | Notes |
|---|---|
| `provider` | [...] |
| `spread` | [...] |
| `formattedSpread` | [...] |
| `spreadOpen` | [...] |
| `overUnder` | [...] |
| `overUnderOpen` | [...] |
| `homeMoneyline` | [...] |
| `awayMoneyline` | [...] |

### `BettingGame`
| Field | Notes |
|---|---|
| `id` | [...] |
| `season` | [...] |
| `seasonType` | SeasonType[...] |
| `week` | [...] |
| `startDate` | [...] |
| `homeTeam` | [...] |
| `homeConference` | [...] |
| `homeClassification` | [...] |
| `homeScore` | [...] |
| `awayTeam` | [...] |
| `awayConference` | [...] |
| `awayClassification` | [...] |
| `awayScore` | [...] |
| `lines` | [...] |

### `UserInfo`
| Field | Notes |
|---|---|
| `patronLevel` | [...] |
| `remainingCalls` | [...] |

### `Game`
| Field | Notes |
|---|---|
| `id` | [...] |
| `season` | [...] |
| `week` | [...] |
| `seasonType` | SeasonType[...] |
| `startDate` | [...] |
| `startTimeTBD` | [...] |
| `completed` | [...] |
| `neutralSite` | [...] |
| `conferenceGame` | [...] |
| `attendance` | [...] |
| `venueId` | [...] |
| `venue` | [...] |
| `homeId` | [...] |
| `homeTeam` | [...] |
| `homeConference` | [...] |
| `homeClassification` | [...] |
| `homePoints` | [...] |
| `homeLineScores` | [...] |
| `homePostgameWinProbability` | [...] |
| `homePregameElo` | [...] |
| `homePostgameElo` | [...] |
| `awayId` | [...] |
| `awayTeam` | [...] |
| `awayConference` | [...] |
| `awayClassification` | [...] |
| `awayPoints` | [...] |
| `awayLineScores` | [...] |
| `awayPostgameWinProbability` | [...] |
| `awayPregameElo` | [...] |
| `awayPostgameElo` | [...] |
| `excitementIndex` | [...] |
| `highlights` | [...] |
| `notes` | [...] |

### `GameTeamStatsTeamStat`
| Field | Notes |
|---|---|
| `category` | [...] |
| `stat` | [...] |

### `GameTeamStatsTeam`
| Field | Notes |
|---|---|
| `teamId` | [...] |
| `team` | [...] |
| `conference` | [...] |
| `homeAway` | [...] |
| `points` | [...] |
| `stats` | [...] |

### `GameTeamStats`
| Field | Notes |
|---|---|
| `id` | [...] |
| `teams` | [...] |

### `GamePlayerStatPlayer`
| Field | Notes |
|---|---|
| `id` | [...] |
| `name` | [...] |
| `stat` | [...] |

### `GamePlayerStatTypes`
| Field | Notes |
|---|---|
| `name` | [...] |
| `athletes` | [...] |

### `GamePlayerStatCategories`
| Field | Notes |
|---|---|
| `name` | [...] |
| `types` | [...] |

### `GamePlayerStatsTeam`
| Field | Notes |
|---|---|
| `team` | [...] |
| `conference` | [...] |
| `homeAway` | [...] |
| `points` | [...] |
| `categories` | [...] |

### `GamePlayerStats`
| Field | Notes |
|---|---|
| `id` | [...] |
| `teams` | [...] |

### `GameMedia`
| Field | Notes |
|---|---|
| `id` | [...] |
| `season` | [...] |
| `week` | [...] |
| `seasonType` | SeasonType[...] |
| `startTime` | [...] |
| `isStartTimeTBD` | [...] |
| `homeTeam` | [...] |
| `homeConference` | [...] |
| `awayTeam` | [...] |
| `awayConference` | [...] |
| `mediaType` | MediaType[...] |
| `outlet` | [...] |

### `GameWeather`
| Field | Notes |
|---|---|
| `id` | [...] |
| `season` | [...] |
| `week` | [...] |
| `seasonType` | SeasonType[...] |
| `startTime` | [...] |
| `gameIndoors` | [...] |
| `homeTeam` | [...] |
| `homeConference` | [...] |
| `awayTeam` | [...] |
| `awayConference` | [...] |
| `venueId` | [...] |
| `venue` | [...] |
| `temperature` | [...] |
| `dewPoint` | [...] |
| `humidity` | [...] |
| `precipitation` | [...] |
| `snowfall` | [...] |
| `windDirection` | [...] |
| `windSpeed` | [...] |
| `pressure` | [...] |
| `weatherConditionCode` | [...] |
| `weatherCondition` | [...] |

### `TeamRecord`
| Field | Notes |
|---|---|
| `games` | [...] |
| `wins` | [...] |
| `losses` | [...] |
| `ties` | [...] |

### `TeamRecords`
| Field | Notes |
|---|---|
| `year` | [...] |
| `teamId` | [...] |
| `team` | [...] |
| `classification` | [...] |
| `conference` | [...] |
| `division` | [...] |
| `expectedWins` | [...] |
| `total` | TeamRecord{... |

### `CalendarWeek`
| Field | Notes |
|---|---|
| `season` | [...] |
| `week` | [...] |
| `seasonType` | SeasonType[...] |
| `startDate` | [...] |
| `endDate` | [...] |
| `firstGameStart` | [...] |
| `lastGameStart` | [...] |

### `ScoreboardGame`
| Field | Notes |
|---|---|
| `id` | [...] |
| `startDate` | [...] |
| `startTimeTBD` | [...] |
| `tv` | [...] |
| `neutralSite` | [...] |
| `conferenceGame` | [...] |
| `status` | GameStatus[...] |
| `period` | [...] |
| `clock` | [...] |
| `situation` | [...] |
| `possession` | [...] |
| `lastPlay` | [...] |
| `venue` | {... |

### `Drive`
| Field | Notes |
|---|---|
| `offense` | [...] |
| `offenseConference` | [...] |
| `defense` | [...] |
| `defenseConference` | [...] |
| `gameId` | [...] |
| `id` | [...] |
| `driveNumber` | [...] |
| `scoring` | [...] |
| `startPeriod` | [...] |
| `startYardline` | [...] |
| `startYardsToGoal` | [...] |
| `startTime` | {... |

### `DraftTeam`
| Field | Notes |
|---|---|
| `location` | [...] |
| `nickname` | [...] |
| `displayName` | [...] |
| `logo` | [...] |

### `DraftPosition`
| Field | Notes |
|---|---|
| `name` | [...] |
| `abbreviation` | [...] |

### `DraftPick`
| Field | Notes |
|---|---|
| `collegeAthleteId` | [...] |
| `nflAthleteId` | [...] |
| `collegeId` | [...] |
| `collegeTeam` | [...] |
| `collegeConference` | [...] |
| `nflTeamId` | [...] |
| `nflTeam` | [...] |
| `year` | [...] |
| `overall` | [...] |
| `round` | [...] |
| `pick` | [...] |
| `name` | [...] |
| `position` | [...] |
| `height` | [...] |
| `weight` | [...] |
| `preDraftRanking` | [...] |
| `preDraftPositionRanking` | [...] |
| `preDraftGrade` | [...] |
| `hometownInfo` | {... |

### `CoachSeason`
| Field | Notes |
|---|---|
| `school` | [...] |
| `year` | [...] |
| `games` | [...] |
| `wins` | [...] |
| `losses` | [...] |
| `ties` | [...] |
| `preseasonRank` | [...] |
| `postseasonRank` | [...] |
| `srs` | [...] |
| `spOverall` | [...] |
| `spOffense` | [...] |
| `spDefense` | [...] |

### `Coach`
| Field | Notes |
|---|---|
| `firstName` | [...] |
| `lastName` | [...] |
| `hireDate` | [...] |
| `seasons` | [...] |

### `StatsByQuarter`
| Field | Notes |
|---|---|
| `total` | [...] |
| `quarter1` | [...] |
| `quarter2` | [...] |
| `quarter3` | [...] |
| `quarter4` | [...] |

### `TeamPPA`
| Field | Notes |
|---|---|
| `team` | [...] |
| `plays` | [...] |
| `overall` | StatsByQuarter{... |

### `TeamSuccessRates`
| Field | Notes |
|---|---|
| `team` | [...] |
| `overall` | StatsByQuarter{... |

### `TeamExplosiveness`
| Field | Notes |
|---|---|
| `team` | [...] |
| `overall` | StatsByQuarter{... |

### `TeamRushingStats`
| Field | Notes |
|---|---|
| `team` | [...] |
| `powerSuccess` | [...] |
| `stuffRate` | [...] |
| `lineYards` | [...] |
| `lineYardsAverage` | [...] |
| `secondLevelYards` | [...] |
| `secondLevelYardsAverage` | [...] |
| `openFieldYards` | [...] |
| `openFieldYardsAverage` | [...] |

### `TeamHavoc`
| Field | Notes |
|---|---|
| `team` | [...] |
| `total` | [...] |
| `frontSeven` | [...] |
| `db` | [...] |

### `TeamScoringOpportunities`
| Field | Notes |
|---|---|
| `team` | [...] |
| `opportunities` | [...] |
| `points` | [...] |
| `pointsPerOpportunity` | [...] |

### `TeamFieldPosition`
| Field | Notes |
|---|---|
| `team` | [...] |
| `averageStart` | [...] |
| `averageStartingPredictedPoints` | [...] |

### `PlayerGameUsage`
| Field | Notes |
|---|---|
| `total` | [...] |
| `quarter1` | [...] |
| `quarter2` | [...] |
| `quarter3` | [...] |
| `quarter4` | [...] |
| `rushing` | [...] |
| `passing` | [...] |
| `player` | [...] |
| `team` | [...] |
| `position` | [...] |

### `PlayerStatsByQuarter`
| Field | Notes |
|---|---|
| `total` | [...] |
| `quarter1` | [...] |
| `quarter2` | [...] |
| `quarter3` | [...] |
| `quarter4` | [...] |
| `rushing` | [...] |
| `passing` | [...] |

### `PlayerPPA`
| Field | Notes |
|---|---|
| `player` | [...] |
| `team` | [...] |
| `position` | [...] |
| `average` | PlayerStatsByQuarter{... |

### `AdvancedBoxScore`
| Field | Notes |
|---|---|
| `gameInfo` | {...

---

## Real Implementation Example: Clemson vs Syracuse Game Data

This section demonstrates a comprehensive real-world API implementation that fetches all available data for a specific game.

### Game: Syracuse @ Clemson (September 20, 2025)
- **Game ID**: 401754537
- **API Success Rate**: 92% (23/25 endpoints)
- **Total Data Retrieved**: 3.1MB JSON

### Successful Endpoints (23)

#### Core Game Data
```python
# Game basic information
GET /games?id=401754537
# Returns: Game details, Elo ratings, venue info

# Betting lines
GET /lines?gameId=401754537
# Returns: DraftKings lines (Clemson -17.5, O/U 54.5)

# Team box scores (ready for live data)
GET /games/teams?id=401754537

# Player box scores (ready for live data)
GET /games/players?id=401754537
```

#### Team Information
```python
# Complete team profiles
GET /teams?team=Clemson
GET /teams?team=Syracuse
# Returns: Colors, logos, venue details, Twitter handles

# Head-to-head history
GET /teams/matchup?team1=Clemson&team2=Syracuse
```

#### Advanced Metrics
```python
# SP+ Ratings (2025 season)
GET /ratings/sp?year=2025&team=Clemson
GET /ratings/sp?year=2025&team=Syracuse

# Elo Ratings (current: Clemson 1693, Syracuse 1484)
GET /ratings/elo?year=2025&team=Clemson
GET /ratings/elo?year=2025&team=Syracuse

# FPI Ratings
GET /ratings/fpi?year=2025&team=Clemson
GET /ratings/fpi?year=2025&team=Syracuse
```

#### Season Context
```python
# 2025 season records
GET /records?year=2025&team=Clemson
GET /records?year=2025&team=Syracuse

# Recruiting classes
GET /recruiting/teams?year=2025&team=Clemson
GET /recruiting/teams?year=2025&team=Syracuse

# Conference standings
GET /ratings/sp/conferences?year=2025&conference=ACC

# Week 4 ACC games
GET /games?year=2025&week=4&conference=ACC
```

#### Game Analytics
```python
# Win probability data
GET /metrics/wp?gameId=401754537

# Play-by-play tracking (ready for live)
GET /plays?year=2025&week=4&team=Clemson

# Drive data (ready for live)
GET /drives?year=2025&week=4&team=Clemson
```

#### Media Coverage
```python
# TV/streaming information
GET /games/media?year=2025&week=4&team=Clemson
# Returns: ESPN broadcast confirmed
```

### Failed Endpoints (2)
```python
# Advanced box score - HTTP 500 (server error)
GET /game/box/advanced?id=401754537

# Weather data - HTTP 401 (premium access required)
GET /games/weather?gameId=401754537
```

### Key Real Data Retrieved
- **Exact Betting Lines**: Clemson -17.5 (-800 ML), Syracuse +17.5 (+550 ML)
- **Precise Elo Ratings**: 209-point difference favoring Clemson
- **Complete Team Profiles**: Colors, venues, social media handles
- **SportsGameOdds Integration IDs**: CLEMSON_NCAAF, SYRACUSE_NCAAF
- **Venue Details**: Memorial Stadium, 81,500 capacity
- **Conference Context**: Full ACC Week 4 schedule

### Implementation Notes
- **Rate Limiting**: 1000 calls/month on free tier (used 25 for this comprehensive fetch)
- **Data Volume**: Single game comprehensive analysis = 3.1MB JSON
- **Success Rate**: 92% endpoint availability typical for pre-game data
- **Premium Features**: Weather requires Patreon subscription
- **Error Handling**: HTTP 500/401 errors expected for some endpoints

### File Output Structure
```
outputs/
├── clemson_syracuse_real_data.json     # Complete API response (3.1MB)
└── clemson_syracuse_analysis.md        # Human-readable analysis
```

This example demonstrates production-ready College Football Data API integration with comprehensive error handling, real betting data, and multi-endpoint aggregation suitable for Discord bot implementation. |

