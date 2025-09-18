# Quickstart

Base URL: `https://api.collegefootballdata.com`

## Authentication
Set the `Authorization` header to `Bearer <API_KEY>`. Keys are issued from https://collegefootballdata.com/key and work across all endpoints.

```bash
curl -s \
  -H "Authorization: Bearer $CFBD_API_KEY" \
  https://api.collegefootballdata.com/status
```

A `200` response with service status indicates the key is valid.

## Helpful tooling
- Official Python client: [`cfbd`](https://github.com/CFBD/cfbd-python)
- Swagger reference: https://api.collegefootballdata.com/api/docs

Next stop: [`games.md`](games.md) for schedule retrieval and [`games_teams.md`](games_teams.md) for box scores.
