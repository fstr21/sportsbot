# ⚾ MLB SportsGameOdds - Complete Workflow Guide

## 🎯 **Quick Start**

```bash
# Navigate to MLB players directory
cd mapping/sportsgameodds/mlb/players

# Step 1: Extract players from API
python fetch_mlb_players_by_date.py
# Enter date when prompted: 2025-09-13

# Step 2: Import to database (no duplicates)
node import_mlb_players_to_db.js 2025-09-13
```

## 📋 **Complete Workflow**

### **Step 1: Extract Players from SportsGameOdds API**
- **Script**: `fetch_mlb_players_by_date.py`
- **Location**: `mapping/sportsgameodds/mlb/players/`
- **Function**: Calls SportsGameOdds MCP server via Railway
- **Input**: Date in YYYY-MM-DD format
- **Output**: `mlb_players_YYYY_MM_DD.json`

**Features:**
- ✅ **Eastern Time conversion** - captures all ET games properly
- ✅ **15 games found** instead of previous 9 (timezone fix)
- ✅ **API cost tracking** - ~1 object per game
- ✅ **Error handling** - validates date format and API response

### **Step 2: Import to Railway Database**
- **Script**: `import_mlb_players_to_db.js`
- **Location**: `mapping/sportsgameodds/mlb/players/`
- **Function**: Smart import preventing duplicates
- **Input**: Date argument (optional)
- **Output**: Updated database with SportsGameOdds IDs

**V2 Logic (No Duplicates):**
1. **Find existing player** by name + team + sport
2. **If found**: Update with SportsGameOdds ID (preserves positions, jerseys)
3. **If not found**: Create new player entry
4. **Result**: Clean database, zero duplicates

## 📊 **Expected Results**

**Typical Single-Day Import:**
- **179 players processed** (from 15 games)
- **170+ existing players updated** with SportsGameOdds IDs
- **5-10 new players created** (call-ups, recent trades)
- **0 duplicates created** (smart matching prevents this)
- **All data preserved** (positions, jersey numbers, ESPN IDs)

## 🔧 **Directory Structure**

```
mapping/sportsgameodds/mlb/players/
├── fetch_mlb_players_by_date.py    # Extract from API
├── import_mlb_players_to_db.js     # Import to DB (V2)
├── mlb_players_2025_09_12.json     # Extracted data
└── README.md                       # This documentation
```

## ⚠️ **Important Considerations**

**API Limits:**
- **SportsGameOdds**: 1000 objects/month
- **Cost per day**: 8-15 objects (varies by games scheduled)
- **Strategy**: Extract multiple dates, then batch import

**Data Quality:**
- **Coverage**: ~10-15% of total MLB players per day
- **Focus**: Players in betting markets (stars, starters, key matchups)
- **Missing**: Bench warmers, injured players, non-active roster

**Error Prevention:**
- Always run from correct directory
- Verify JSON file exists before import
- Check database connection before large imports
- Use date arguments to avoid hardcoded paths

## 🎉 **Success Metrics**

**Perfect Import Results:**
- ✅ **0 duplicates** in database
- ✅ **170+ players updated** with both position data AND SportsGameOdds IDs
- ✅ **Aaron Judge example**: RF, #99, AARON_JUDGE_1_MLB (all data present)
- ✅ **Team coverage**: 30/30 MLB teams mapped successfully
- ✅ **Transaction safety**: Rollback on any errors

This workflow eliminates the duplicate player issue and provides clean data for betting market integrations.