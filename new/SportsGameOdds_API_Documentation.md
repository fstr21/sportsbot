# SportsGameOdds API Documentation

## Overview
SportsGameOdds is a free alternative to The Odds API, providing comprehensive betting odds data through an MCP (Model Context Protocol) server. This documentation addresses critical data structure differences discovered during NFL integration.

## 🚨 CRITICAL: API Usage Constraints
- **Monthly Limit**: 1000 objects maximum
- **Charging Model**: 1 search query = ALL games visible that day
- **Example**: Search Monday MLB with 12 games = 12 objects consumed
- **Always ask before making API calls**

## MCP Server Configuration
- **URL**: `https://sports-production-b1af.up.railway.app`
- **Tool Name**: `get_sportsgameodds_events`
- **Authentication**: None required (handled by MCP server)

## Data Structure Overview

### 🔥 KEY DISCOVERY: Betting Data Location
**CRITICAL**: SportsGameOdds returns betting data in an `"odds"` object, NOT in a `"markets"` array as expected by our import scripts.

### API Response Structure
```json
{
  "success": true,
  "data": {
    "events": [
      {
        "eventID": "game_123",
        "homeTeam": "Las Vegas Raiders",
        "awayTeam": "Los Angeles Chargers",
        "markets": [],  // ❌ ALWAYS EMPTY - DO NOT USE
        "odds": {       // ✅ BETTING DATA IS HERE
          "moneyline-LAS_VEGAS_RAIDERS-game-ml": {
            "oddID": "moneyline-LAS_VEGAS_RAIDERS-game-ml",
            "marketName": "Las Vegas Raiders Moneyline",
            "bookOdds": "+155",
            "bookName": "DraftKings"
          },
          "rushing_yards-AUSTIN_EKELER_1_NFL-game-ou-over": {
            "oddID": "rushing_yards-AUSTIN_EKELER_1_NFL-game-ou-over",
            "marketName": "Austin Ekeler Rushing Yards Over/Under",
            "bookOdds": "-114",
            "bookOverUnder": "22.5",
            "bookName": "FanDuel"
          }
        }
      }
    ]
  }
}
```

## Data Conversion Requirements

### Converting Odds to Markets Format
Our import scripts expect betting data in a `markets` array. Here's the conversion pattern:

```python
def convert_odds_to_markets(game_data):
    """Convert SportsGameOdds 'odds' object to 'markets' array format"""
    odds = game_data.get("odds", {})
    markets = []
    
    for odd_id, odd_data in odds.items():
        market = {
            "id": odd_id,
            "type": odd_data.get("marketName", ""),
            "bookmaker": odd_data.get("bookName", ""),
            "odds": odd_data.get("bookOdds", ""),
            "participants": []
        }
        
        # Extract player ID from odd_id for player props
        if "_NFL-" in odd_id:
            parts = odd_id.split("-")
            if len(parts) >= 2:
                potential_player_id = parts[1]
                if potential_player_id.endswith("_1_NFL"):
                    market["participants"].append({
                        "playerID": potential_player_id,
                        "type": "player_prop"
                    })
        
        markets.append(market)
    
    # Replace empty markets array with converted data
    game_data["markets"] = markets
    return game_data
```

## Market Types & Player ID Extraction

### Player Prop ID Format
Player prop odds follow this pattern:
```
{stat_type}-{PLAYER_NAME}_{TEAM_ID}_NFL-game-{bet_type}-{over/under}
```

Examples:
- `rushing_yards-AUSTIN_EKELER_1_NFL-game-ou-over`
- `passing_attempts-all-game-ou-over`
- `receiving_yards-KEENAN_ALLEN_1_NFL-game-ou-under`

### Market Categories
1. **Game Lines**: Moneylines, spreads, totals
2. **Player Props**: Individual player statistics
3. **Team Props**: Team-specific betting markets

## MCP Call Template

```python
import httpx
import json

SPORTSGAMEODDS_MCP_URL = "https://sports-production-b1af.up.railway.app"

async def call_sportsgameodds_mcp(tool_name: str, arguments: dict):
    """Call the SportsGameOdds MCP server"""
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{SPORTSGAMEODDS_MCP_URL}/tools/call",
            json={
                "name": tool_name,
                "arguments": arguments
            },
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        result = response.json()
        return json.loads(result["content"][0]["text"])

# Usage example
async def get_nfl_games():
    result = await call_sportsgameodds_mcp("get_sportsgameodds_events", {
        "league_id": "NFL",
        "limit": 1,  # ALWAYS use limit=1 to minimize object consumption
        "include_opposing_odds": True,
        "event_type": "match"
    })
    
    # Convert odds to markets for each game
    for event in result["data"]["events"]:
        event = convert_odds_to_markets(event)
    
    return result
```

## Standard Parameters
- `league_id`: "MLB", "NFL", "NBA", "NHL"
- `limit`: 1 (ALWAYS set to minimize object consumption)
- `include_opposing_odds`: True
- `include_alt_lines`: False (exclude to reduce complexity)
- `event_type`: "match"

## Timezone Handling
- **Standard**: All operations use Eastern Time (ET/EST)
- **Game Windows**: 12:01 AM to 11:59 PM Eastern Time
- **Date Calculations**: Account for Eastern timezone conversion

## Testing Workflow
1. **Check Usage**: Verify remaining object count before testing
2. **Single Test**: Use limit=1 for comprehensive single-day tests
3. **Document**: Track object consumption for each test session
4. **Convert**: Apply odds-to-markets conversion in extraction scripts
5. **Validate**: Ensure betting markets are populated after conversion

## Common Issues & Solutions

### Issue: Empty Markets Array
**Problem**: All games show `"markets": []` despite SportsGameOdds claiming 708+ markets per NFL game
**Solution**: Betting data is in the `"odds"` object, not `"markets"` array. Use conversion function above.

### Issue: Player ID Extraction
**Problem**: Need to map SportsGameOdds player IDs to database player records
**Solution**: Extract player IDs from odd_id strings using the pattern matching shown above.

### Issue: API Parameter Errors
**Problem**: Attempting to use unsupported parameters like `"odds_present"`, `"include_markets"`
**Solution**: Use only documented parameters listed in Standard Parameters section.

## Migration Strategy
1. **Test with limit=1**: Minimize object consumption during validation
2. **Convert data structure**: Always apply odds-to-markets conversion
3. **Validate critical markets**: Ensure player props and game lines are present
4. **Compare with The Odds API**: Verify data quality before full migration
5. **Document usage**: Track all API calls against 1000 object monthly limit

# NFL Import Workflow - COMPLETE PROCESS

## Production-Ready Scripts

### 1. Data Extraction: `nfl_game_mapper.py` 
**Location**: `mapping/sportsgameodds/nfl/players/temp_output/`
**Purpose**: Fetch NFL games from SportsGameOdds MCP and convert to import-ready JSON
**Status**: ✅ **PRODUCTION READY**

```bash
cd C:\Users\fstr2\Desktop\sports\mapping\sportsgameodds\nfl\players\temp_output
python nfl_game_mapper.py
```

**Key Features:**
- Extracts betting data from SportsGameOdds "odds" object
- Converts to "markets" array format for import compatibility  
- Filters players with active betting lines (100% accuracy)
- Generates individual game JSON files + summary
- **API Usage**: ~2 objects per execution (1 per game found)

### 2. Database Import: `test_single_real_import.py`
**Purpose**: Import SportsGameOdds player IDs to database
**Status**: ✅ **PRODUCTION READY** 

```bash
python test_single_real_import.py
```

**Processing Options:**
- **Option 1**: Single file (interactive selection)
- **Option 2**: Batch mode (all JSON files)
- **Option 3**: Quit

**Smart Features:**
- ✅ **Skip Logic**: Players with existing SGO IDs are automatically skipped
- ✅ **Re-run Safe**: Running same data multiple times won't duplicate
- ✅ **Betting Market Filter**: Only processes players with active betting lines
- ✅ **New Player Detection**: Flags players not in database who have betting markets

### 3. Status Verification: `check_player_sgo_ids.py`
**Purpose**: Query database to verify SGO ID population status

## Proven Results

### Current NFL Coverage
- **Total Teams Tested**: 3 (Chargers, Raiders, Texans) 
- **Players Processed**: 70 players across 2 games
- **Success Rate**: 100% accurate betting market detection
- **Database Updates**: Successfully added SGO IDs to existing players

### Import Success Statistics
```
✅ Updated Players: Players who received new SGO IDs
⏭️  Skipped Players: Players who already had SGO IDs  
🆕 New Players: Players with betting markets not in database
🚫 Filtered Players: Players without betting markets (excluded)
```

## Critical Player ID Issues Resolved

### Name Matching Discoveries
- **KeAndre Lambert-Smith** (DB) = **KEANDRE_LAMBERTSMITH_1_NFL** (SGO)
- **Tre' Harris** (DB) = **TRE_HARRIS_1_NFL** (SGO)

### ✅ High Priority Players - RESOLVED (2025-09-13)
- **Joe Mixon** (Texans RB) - ✅ ESPN ID: 3116385 ADDED
- **Tank Dell** (Texans WR) - ✅ ESPN ID: 4366031 ADDED  
- **Keenan Allen** (Chargers WR) - ✅ ESPN ID: 15818 ADDED
- **Najee Harris** (Chargers RB) - ✅ ESPN ID: 4241457 ADDED

### 🎯 Full Database Coverage Achieved
- **Total NFL Players**: 739
- **ESPN IDs**: 739/739 (100% COMPLETE)
- **SGO IDs**: 363/739 (49% complete, 376 ready for import)

## Troubleshooting Guide

### Issue: Empty Markets Array
**Symptom**: JSON shows `"markets": []`
**Cause**: Looking in wrong data location
**Solution**: Betting data is in `"odds"` object, conversion handles this automatically

### Issue: Players Not Updating  
**Symptom**: Script shows "SKIP" for players who should update
**Cause**: Players already have SGO IDs
**Solution**: This is correct behavior - re-run safety working as intended

### Issue: "NEW player needed" Messages
**Symptom**: Players with betting markets not found in database
**Cause**: Legitimate players not yet in your database
**Action Required**: Manually review and add high-priority players

### Issue: Unicode Encoding Errors (Windows)
**Symptom**: `UnicodeEncodeError: 'charmap' codec can't encode character`
**Solution**: Scripts updated to remove problematic Unicode characters

## ✅ PRODUCTION DEPLOYMENT PHASE

### **Immediate Actions** 
1. ✅ **Star Players Added**: All high-priority missing players now in database
2. 🎯 **Scale Up**: Execute full-league SGO import across multiple game dates
3. 📊 **Monitor Usage**: Track API consumption against 1000 object limit
4. 🎮 **Optimize Coverage**: Focus on high-value games (primetime, divisional matchups)

### **Strategic Game Selection**
**Recommended Priority Order:**
1. **Prime Time Games** (SNF, MNF, TNF) - Maximum betting volume
2. **Divisional Matchups** - High-stakes games with more player props  
3. **Playoff-Implication Games** - Increased betting interest
4. **Star Player Games** - Teams with fantasy-relevant players

### **API Usage Strategy**
- **Target**: 10-15 games per month (within 1000 object limit)
- **Expected Coverage**: ~300-500 players per month
- **Full League Timeline**: 2-3 months to reach 80%+ SGO coverage
- **Monitoring**: Track objects consumed per extraction

## File Locations
```
mapping/sportsgameodds/nfl/players/temp_output/
├── nfl_game_mapper.py          # Data extraction
├── test_single_real_import.py  # Database import  
├── test_automated_import.py    # Analysis/verification
├── check_player_sgo_ids.py     # Status queries
├── *.json                      # Extracted game data
└── *_summary.json              # Batch summaries
```

---
*Last Updated: 2025-09-13*
*Remember: Every API call counts against our 1000 object monthly limit!*
*STATUS: NFL Pipeline PRODUCTION READY ✅*