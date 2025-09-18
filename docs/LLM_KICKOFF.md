# LLM Kickoff Guide - What to Read First & How to "Finish"

## 🚀 Start Here: Essential Reading Order

### 1. **PROJECT_CHARTER.md** (2 min read)
- **Why**: Understand project scope, phases, and constraints
- **Key Focus**: API usage limits (especially SportsGameOdds 1000 object limit)
- **Critical**: Note what's IN scope vs OUT of scope

### 2. **POC_PLAN.md** (3 min read)
- **Why**: Understand current artifact structure and run flow
- **Key Focus**: Daily capture process and QA checklist
- **Critical**: File structure and validation requirements

### 3. **Repository Structure** (1 min scan)
```
sports-intel/
├── docs/           ← You are here
├── artifacts/      ← Output goes here (NFL, NCAAF)
├── scripts/        ← Main work area (day capture scripts)
└── mappings/       ← Team/player ID catalogs
```

## 🎯 How to "Finish" - Definition of Done

### Phase 1 POC Completion Criteria

#### ✅ **Scripts Working**
- [ ] `scripts/nfl_day_capture.py` successfully runs end-to-end
- [ ] `scripts/ncaaf_day_capture.py` successfully runs end-to-end
- [ ] Both scripts handle date prompting (today, specific date)
- [ ] Error handling and retry logic implemented
- [ ] API usage tracking (especially SportsGameOdds objects)

#### ✅ **Artifacts Generated**
- [ ] NFL: schedule.json, odds.json, team_stats.json, player_stats.json, summary.md
- [ ] NCAAF: schedule.json, odds.json, team_stats.json, summary.md
- [ ] All JSON validates against expected schema
- [ ] Summary.md is human-readable and informative

#### ✅ **Data Quality**
- [ ] Team IDs properly mapped using `mappings/teams.json`
- [ ] Player IDs properly mapped using `mappings/players.json` (NFL only)
- [ ] No "UNKNOWN_TEAM" or "UNKNOWN_PLAYER" entries
- [ ] Consistent timezone handling (Eastern Time)
- [ ] Reasonable odds values (not null or extreme)

#### ✅ **API Integration**
- [ ] ESPN API: Successfully fetches schedules and stats
- [ ] SportsGameOdds API: Successfully fetches odds (within limits)
- [ ] CollegeFootballData API: Successfully fetches NCAAF schedules
- [ ] Rate limiting respected for all APIs
- [ ] Usage monitoring in place

#### ✅ **Operational Readiness**
- [ ] Scripts can be run manually on any valid date
- [ ] Clear logging and error messages
- [ ] QA checklist validates all outputs
- [ ] Documentation updated with any discoveries

## 🛠️ Development Approach

### Start Small
1. **Focus on ONE script first** (recommend NFL)
2. **Get basic structure working** before adding complexity
3. **Test with a single game day** before handling edge cases

### Key Implementation Notes
- **SportsGameOdds API**: ONE call per day fetches ALL games that day
- **Team Mapping**: Must be bulletproof - scripts fail gracefully if mapping missing
- **File Structure**: Consistent YYYY-MM-DD dating across all artifacts
- **Error Handling**: Continue with partial data rather than complete failure

### Testing Strategy
```bash
# Test with recent game day
python scripts/nfl_day_capture.py
# Enter: 2024-09-15 (known NFL Sunday)

# Validate outputs
ls artifacts/nfl/2024-09-15/
# Expected: schedule.json, odds.json, team_stats.json, player_stats.json, summary.md
```

## 🔍 Common Gotchas

### API Limits
- **SportsGameOdds**: Don't test repeatedly! Each call counts toward 1000/month
- **Rate Limiting**: All APIs have different limits, implement backoff
- **API Keys**: Store in environment variables, never commit to git

### Data Consistency
- **Timezone**: ESPN times may be different from other sources
- **Team Names**: "Kansas City Chiefs" vs "KC" vs "Kansas City" - mapping critical
- **Date Formats**: Stick to YYYY-MM-DD everywhere

### File Operations
- **Directory Creation**: Scripts should create date directories if missing
- **Overwriting**: Re-running same date should update artifacts safely
- **JSON Formatting**: Use consistent indentation for human readability

## 🎯 Success Signals

### You Know You're Done When:
1. **Scripts run reliably** on any valid game date
2. **Artifacts are consistently generated** with quality data
3. **Team/player mapping works** without manual intervention
4. **API usage is monitored** and stays within limits
5. **QA checklist passes** for generated artifacts

### Bonus Points:
- Scripts handle "no games today" gracefully
- Summary.md includes betting insights or interesting stats
- Error logs are clear and actionable
- Code is clean and well-commented

## 📞 Getting Help

### When Stuck:
1. **Check API documentation** for data format changes
2. **Validate API keys** and rate limiting
3. **Test with known good dates** (recent game days)
4. **Focus on one API at a time** to isolate issues

### Ready for Next Phase When:
- POC runs reliably for 1+ week
- Data quality consistently meets standards
- API usage well within monthly limits
- Ready to discuss Phase 2 API layer design