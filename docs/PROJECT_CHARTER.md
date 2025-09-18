# Sports Intelligence Platform - Project Charter

## Purpose
Build a proof-of-concept sports data collection and analysis system that captures daily snapshots of NFL and NCAAF games, including schedules, odds, and team statistics.

## Project Phases

### Phase 1: POC Data Capture (Current)
- **Goal**: Validate data collection workflows for NFL and NCAAF
- **Scope**: Simple Python scripts that capture daily game data
- **Output**: JSON artifacts organized by sport and date
- **Success Criteria**:
  - Successful daily data capture for both leagues
  - Clean, structured output artifacts
  - Reliable team/player ID mapping

### Phase 2: API Layer (Future)
- **Goal**: Expose collected data through REST API
- **Scope**: FastAPI service with endpoint for querying historical data
- **Dependencies**: Successful Phase 1 completion

### Phase 3: Discord Integration (Future)
- **Goal**: User-friendly interface via Discord bot
- **Scope**: Slash commands for odds, player stats, and schedules
- **Dependencies**: Successful Phase 2 completion

## Target Sports

### NFL (Priority 1)
- **Schedule**: ESPN API
- **Odds**: SportsGameOdds API (1000 object monthly limit)
- **Team Stats**: ESPN API
- **Player Support**: Yes (individual player statistics)
- **Season**: Sept-Feb (regular season + playoffs)

### NCAAF (Priority 2)
- **Schedule**: CollegeFootballData API
- **Odds**: SportsGameOdds API
- **Team Stats**: ESPN API
- **Player Support**: No (team-level only for POC)
- **Season**: Aug-Jan (regular season + bowl games)

## Non-Goals (Out of Scope)
- ❌ Real-time data streaming
- ❌ Database persistence (file-based artifacts only)
- ❌ Advanced analytics or predictions
- ❌ Multiple betting providers (SportsGameOdds only)
- ❌ Historical data backfill (current season only)
- ❌ User authentication or permissions
- ❌ Mobile apps or web interfaces
- ❌ Other sports (NBA, MLB, NHL, Soccer)

## API Usage Constraints

### Critical: SportsGameOdds API
- **Monthly Limit**: 1000 objects maximum
- **Charging Model**: 1 search = ALL games that day
- **Example**: Monday search with 12 NFL games = 12 objects consumed
- **Strategy**: Minimize calls, maximize data per call
- **Monitoring**: Track usage to stay under 900 objects/month

### ESPN API
- **Limit**: Generous (no strict limits observed)
- **Strategy**: Use for schedules and team statistics
- **Backup**: Primary source for non-betting data

### CollegeFootballData API
- **Limit**: 200 calls per hour
- **Strategy**: Schedule NCAAF calls appropriately
- **Coverage**: Best source for college football data

## Success Metrics
1. **Data Quality**: 95%+ successful daily captures
2. **API Efficiency**: Stay under 900 SportsGameOdds objects/month
3. **Artifact Structure**: Consistent JSON schema across captures
4. **Team Mapping**: 100% successful team ID resolution
5. **Error Handling**: Graceful failure and retry logic

## Risk Mitigation
- **API Rate Limits**: Implement exponential backoff
- **Data Quality**: Schema validation on all outputs
- **Cost Control**: Daily SportsGameOdds usage monitoring
- **Reliability**: Multiple data sources where possible