# POC Plan - Artifacts and Run Flow

## What Artifacts Exist

### NFL Artifacts (`artifacts/nfl/`)
```
artifacts/nfl/YYYY-MM-DD/
├── schedule.json           # Daily NFL games from ESPN
├── odds.json              # Betting lines from SportsGameOdds
├── team_stats.json        # Team statistics from ESPN
├── player_stats.json      # Key player statistics from ESPN
└── summary.md             # Human-readable daily summary
```

### NCAAF Artifacts (`artifacts/ncaaf/`)
```
artifacts/ncaaf/YYYY-MM-DD/
├── schedule.json          # Daily NCAAF games from CollegeFootballData
├── odds.json             # Betting lines from SportsGameOdds
├── team_stats.json       # Team statistics from ESPN
└── summary.md            # Human-readable daily summary
```

## Daily Run Flow

### Morning Capture (Recommended: 8:00 AM ET)
1. **NFL Day Capture**:
   ```bash
   python scripts/nfl_day_capture.py
   ```
   - Prompts for date (default: today)
   - Fetches schedule from ESPN
   - Fetches odds from SportsGameOdds
   - Fetches team stats from ESPN
   - Fetches key player stats from ESPN
   - Writes artifacts to `artifacts/nfl/YYYY-MM-DD/`

2. **NCAAF Day Capture**:
   ```bash
   python scripts/ncaaf_day_capture.py
   ```
   - Prompts for date (default: today)
   - Fetches schedule from CollegeFootballData
   - Fetches odds from SportsGameOdds (teams only)
   - Fetches team stats from ESPN
   - Writes artifacts to `artifacts/ncaaf/YYYY-MM-DD/`

### Evening Update (Optional: 11:00 PM ET)
- Re-run same scripts to capture final scores and updated odds
- Artifacts will be updated in-place with final data

## QA Checklist

### Pre-Run Validation
- [ ] Check SportsGameOdds API usage (stay under 900 objects/month)
- [ ] Verify date format: YYYY-MM-DD
- [ ] Confirm target date has scheduled games
- [ ] Check API keys are valid and not expired

### Post-Run Validation
- [ ] All JSON files validate against expected schema
- [ ] Team IDs successfully mapped (no "UNKNOWN_TEAM" entries)
- [ ] Player IDs successfully mapped for NFL (if applicable)
- [ ] Odds data includes moneyline, spread, and total for each game
- [ ] Summary.md is human-readable and accurate
- [ ] No API errors or rate limit violations logged

### Data Quality Checks
- [ ] Schedule times are in Eastern Time
- [ ] Odds values are reasonable (not null or extreme outliers)
- [ ] Team abbreviations match mapping catalog
- [ ] Player names match mapping catalog (NFL only)
- [ ] All required fields present in each artifact

### File Structure Validation
```bash
# Expected structure after successful run
artifacts/
├── nfl/
│   └── 2024-09-18/
│       ├── schedule.json     ✓
│       ├── odds.json        ✓
│       ├── team_stats.json  ✓
│       ├── player_stats.json ✓
│       └── summary.md       ✓
└── ncaaf/
    └── 2024-09-18/
        ├── schedule.json    ✓
        ├── odds.json       ✓
        ├── team_stats.json ✓
        └── summary.md      ✓
```

## Error Handling Strategy

### API Failures
- **Retry Logic**: 3 attempts with exponential backoff
- **Fallback**: Continue with partial data, log missing components
- **Graceful Degradation**: Generate artifacts with available data

### Rate Limiting
- **Detection**: Monitor HTTP 429 responses
- **Response**: Wait and retry with increased delays
- **Prevention**: Track request counts and timing

### Data Quality Issues
- **Unknown Teams**: Log warning, continue with raw provider data
- **Missing Players**: NFL continues without player stats
- **Invalid Odds**: Log warning, mark as unavailable

## Monitoring and Logs

### Daily Metrics
- Total API calls made
- SportsGameOdds objects consumed
- Success/failure rates by data source
- Artifact generation time

### Weekly Review
- API usage trending toward monthly limits
- Data quality patterns and issues
- Team/player mapping coverage
- Script performance and reliability