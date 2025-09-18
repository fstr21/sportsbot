# Naming & Format Conventions (LOCKED)

## Dates
- Input date format: **MM/DD/YYYY** (e.g., 09/21/2025)
- When written into filenames/paths, use **MM-DD-YYYY** (safe for folders)

## Timezone
- All *outputs* (times shown in JSON and .md) MUST be **Eastern Time (ET)**.
- If sources return UTC/Zulu, convert to ET for display.

## Snapshot tags
- **No snapshot tags** for now. (Do not invent MORNING/FINAL.)

## League keys
- NFL, NCAAF

## Artifact layout
- `artifacts/<league>/<MM-DD-YYYY>/`
  - JSON + a readable `.md`
  - The `.md` must be broken down **by game matchup** (one section per game).
