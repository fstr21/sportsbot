# SportsGameOdds Local Documentation

This directory holds the raw reference pages we scraped from sportsGameOdds.com so we can work offline. The material is reorganised here so the most useful bits are easy to find while we build a proper MCP/service layer.

## How to use this folder
- **Start with [`quickstart.md`](quickstart.md)** for auth requirements and a first-call walkthrough.
- **Check [`events.md`](events.md)** for schedule/odds retrieval, pagination, and filters such as `startsAfter`/`startsBefore`.
- **Use the data dictionaries** when you need identifiers:
  - [`sports.md`](sports.md) – list of `sportID` values
  - [`leagues.md`](leagues.md) – list of `leagueID` values grouped by sport
  - [`bookmakers.md`](bookmakers.md) – bookmaker identifiers from the API
  - [`bet_types.md`](bet_types.md) and [`stats.md`](stats.md) – supporting reference tables
- **Sport-specific snapshots** (`baseball.md`, `basketball.md`, `football.md`, `hockey.md`, `soccer.md`, `tennis.md`, `mma.md`) capture any unique endpoints or quirks noted for that sport.

Everything under `docs/sgo_docs/` is source material; feel free to replace these files as we firm up official docs. When you add new guidance, please cross-link it from this README.
