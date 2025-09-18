Servers

https://api.collegefootballdata.com/

Authorize
games
Games scores and statistics



GET
/games


Retrieves historical game data

Parameters
Try it out
Name	Description
year
integer($int32)
(query)
Required year filter (except when id is specified)

year
week
integer($int32)
(query)
Optional week filter

week
seasonType
string
(query)
Optional season type filter

Available values : regular, postseason, both, allstar, spring_regular, spring_postseason


--
classification
string
(query)
Optional division classification filter

Available values : fbs, fcs, ii, iii


--
team
string
(query)
Optional team filter

team
home
string
(query)
Optional home team filter

home
away
string
(query)
Optional away team filter

away
conference
string
(query)
Optional conference filter

conference
id
integer($int32)
(query)
Game id filter to retrieve a single game

id
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "id": 0,
    "season": 0,
    "week": 0,
    "seasonType": "regular",
    "startDate": "2025-09-18T20:42:02.022Z",
    "startTimeTBD": true,
    "completed": true,
    "neutralSite": true,
    "conferenceGame": true,
    "attendance": 0,
    "venueId": 0,
    "venue": "string",
    "homeId": 0,
    "homeTeam": "string",
    "homeConference": "string",
    "homeClassification": "fbs",
    "homePoints": 0,
    "homeLineScores": [
      0
    ],
    "homePostgameWinProbability": 0,
    "homePregameElo": 0,
    "homePostgameElo": 0,
    "awayId": 0,
    "awayTeam": "string",
    "awayConference": "string",
    "awayClassification": "fbs",
    "awayPoints": 0,
    "awayLineScores": [
      0
    ],
    "awayPostgameWinProbability": 0,
    "awayPregameElo": 0,
    "awayPostgameElo": 0,
    "excitementIndex": 0,
    "highlights": "string",
    "notes": "string"
  }
]
No links

GET
/games/teams


Retrieves team box score statistics

Parameters
Try it out
Name	Description
year
integer($int32)
(query)
Required year filter (along with one of week, team, or conference), unless id is specified

year
week
integer($int32)
(query)
Optional week filter, required if team and conference not specified

week
team
string
(query)
Optional team filter, required if week and conference not specified

team
conference
string
(query)
Optional conference filter, required if week and team not specified

conference
classification
string
(query)
Optional division classification filter

Available values : fbs, fcs, ii, iii


--
seasonType
string
(query)
Optional season type filter

Available values : regular, postseason, both, allstar, spring_regular, spring_postseason


--
id
integer($int32)
(query)
Optional id filter to retrieve a single game

id
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "id": 0,
    "teams": [
      {
        "teamId": 0,
        "team": "string",
        "conference": "string",
        "homeAway": "home",
        "points": 0,
        "stats": [
          {
            "category": "string",
            "stat": "string"
          }
        ]
      }
    ]
  }
]
No links

GET
/games/players


Retrieves player box score statistics

Parameters
Try it out
Name	Description
year
integer($int32)
(query)
Required year filter (along with one of week, team, or conference), unless id is specified

year
week
integer($int32)
(query)
Optional week filter, required if team and conference not specified

week
team
string
(query)
Optional team filter, required if week and conference not specified

team
conference
string
(query)
Optional conference filter, required if week and team not specified

conference
classification
string
(query)
Optional division classification filter

Available values : fbs, fcs, ii, iii


--
seasonType
string
(query)
Optional season type filter

Available values : regular, postseason, both, allstar, spring_regular, spring_postseason


--
category
string
(query)
Optional player statistical category filter

category
id
integer($int32)
(query)
Optional id filter to retrieve a single game

id
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "id": 0,
    "teams": [
      {
        "team": "string",
        "conference": "string",
        "homeAway": "home",
        "points": 0,
        "categories": [
          {
            "name": "string",
            "types": [
              {
                "name": "string",
                "athletes": [
                  {
                    "id": "string",
                    "name": "string",
                    "stat": "string"
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
]
No links

GET
/games/media


Retrieves media information for games

Parameters
Try it out
Name	Description
year *
integer($int32)
(query)
Required year filter

year
seasonType
string
(query)
Optional season type filter

Available values : regular, postseason, both, allstar, spring_regular, spring_postseason


--
week
integer($int32)
(query)
Optional week filter

week
team
string
(query)
Optional team filter

team
conference
string
(query)
Optional conference filter

conference
mediaType
string
(query)
Optional media type filter

Available values : tv, radio, web, ppv, mobile


--
classification
string
(query)
Optional division classification filter

Available values : fbs, fcs, ii, iii


--
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "id": 0,
    "season": 0,
    "week": 0,
    "seasonType": "regular",
    "startTime": "2025-09-18T20:42:02.101Z",
    "isStartTimeTBD": true,
    "homeTeam": "string",
    "homeConference": "string",
    "awayTeam": "string",
    "awayConference": "string",
    "mediaType": "tv",
    "outlet": "string"
  }
]
No links

GET
/games/weather


Retrieve historical and future weather data (Patreon only)

Parameters
Try it out
Name	Description
year
integer($int32)
(query)
Year filter, required if game id not specified

year
seasonType
string
(query)
Optional season type filter

Available values : regular, postseason, both, allstar, spring_regular, spring_postseason


--
week
integer($int32)
(query)
Optional week filter

week
team
string
(query)
Optional team filter

team
conference
string
(query)
Optional conference filter

conference
classification
string
(query)
Optional division classification filter

Available values : fbs, fcs, ii, iii


--
gameId
integer($int32)
(query)
Filter for retrieving a single game

gameId
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "id": 0,
    "season": 0,
    "week": 0,
    "seasonType": "regular",
    "startTime": "2025-09-18T20:42:02.122Z",
    "gameIndoors": true,
    "homeTeam": "string",
    "homeConference": "string",
    "awayTeam": "string",
    "awayConference": "string",
    "venueId": 0,
    "venue": "string",
    "temperature": 0,
    "dewPoint": 0,
    "humidity": 0,
    "precipitation": 0,
    "snowfall": 0,
    "windDirection": 0,
    "windSpeed": 0,
    "pressure": 0,
    "weatherConditionCode": 0,
    "weatherCondition": "string"
  }
]
No links

GET
/records


Retrieves historical team records

Parameters
Try it out
Name	Description
year
integer($int32)
(query)
Year filter, required if team not specified

year
team
string
(query)
Team filter, required if year not specified

team
conference
string
(query)
Optional conference filter

conference
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "year": 0,
    "teamId": 0,
    "team": "string",
    "classification": "fbs",
    "conference": "string",
    "division": "string",
    "expectedWins": 0,
    "total": {
      "games": 0,
      "wins": 0,
      "losses": 0,
      "ties": 0
    },
    "conferenceGames": {
      "games": 0,
      "wins": 0,
      "losses": 0,
      "ties": 0
    },
    "homeGames": {
      "games": 0,
      "wins": 0,
      "losses": 0,
      "ties": 0
    },
    "awayGames": {
      "games": 0,
      "wins": 0,
      "losses": 0,
      "ties": 0
    },
    "neutralSiteGames": {
      "games": 0,
      "wins": 0,
      "losses": 0,
      "ties": 0
    },
    "regularSeason": {
      "games": 0,
      "wins": 0,
      "losses": 0,
      "ties": 0
    },
    "postseason": {
      "games": 0,
      "wins": 0,
      "losses": 0,
      "ties": 0
    }
  }
]
No links

GET
/calendar


Retrieves calendar information

Parameters
Try it out
Name	Description
year *
integer($int32)
(query)
Required year filter

year
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "season": 0,
    "week": 0,
    "seasonType": "regular",
    "startDate": "2025-09-18T20:42:02.143Z",
    "endDate": "2025-09-18T20:42:02.143Z"
  }
]
No links

GET
/scoreboard


Retrieves live scoreboard data

Parameters
Try it out
Name	Description
classification
string
(query)
Optional division classification filter, defaults to fbs

Available values : fbs, fcs, ii, iii


--
conference
string
(query)
Optional conference filter

conference
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "id": 0,
    "startDate": "2025-09-18T20:42:02.151Z",
    "startTimeTBD": true,
    "tv": "string",
    "neutralSite": true,
    "conferenceGame": true,
    "status": "scheduled",
    "period": 0,
    "clock": "string",
    "situation": "string",
    "possession": "string",
    "lastPlay": "string",
    "venue": {
      "state": "string",
      "city": "string",
      "name": "string"
    },
    "homeTeam": {
      "winProbability": 0,
      "lineScores": [
        0
      ],
      "points": 0,
      "classification": "fbs",
      "conference": "string",
      "name": "string",
      "id": 0
    },
    "awayTeam": {
      "winProbability": 0,
      "lineScores": [
        0
      ],
      "points": 0,
      "classification": "fbs",
      "conference": "string",
      "name": "string",
      "id": 0
    },
    "weather": {
      "windDirection": 0,
      "windSpeed": 0,
      "description": "string",
      "temperature": 0
    },
    "betting": {
      "awayMoneyline": 0,
      "homeMoneyline": 0,
      "overUnder": 0,
      "spread": 0
    }
  }
]
No links

GET
/game/box/advanced


Retrieves an advanced box score for a game

Parameters
Try it out
Name	Description
id *
integer($int32)
(query)
Required game id filter

id
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
{
  "gameInfo": {
    "excitement": 0,
    "homeWinner": true,
    "awayWinProb": 0,
    "awayPoints": 0,
    "awayTeam": "string",
    "homeWinProb": 0,
    "homePoints": 0,
    "homeTeam": "string"
  },
  "teams": {
    "fieldPosition": [
      {
        "team": "string",
        "averageStart": 0,
        "averageStartingPredictedPoints": 0
      }
    ],
    "scoringOpportunities": [
      {
        "team": "string",
        "opportunities": 0,
        "points": 0,
        "pointsPerOpportunity": 0
      }
    ],
    "havoc": [
      {
        "team": "string",
        "total": 0,
        "frontSeven": 0,
        "db": 0
      }
    ],
    "rushing": [
      {
        "team": "string",
        "powerSuccess": 0,
        "stuffRate": 0,
        "lineYards": 0,
        "lineYardsAverage": 0,
        "secondLevelYards": 0,
        "secondLevelYardsAverage": 0,
        "openFieldYards": 0,
        "openFieldYardsAverage": 0
      }
    ],
    "explosiveness": [
      {
        "team": "string",
        "overall": {
          "total": 0,
          "quarter1": 0,
          "quarter2": 0,
          "quarter3": 0,
          "quarter4": 0
        }
      }
    ],
    "successRates": [
      {
        "team": "string",
        "overall": {
          "total": 0,
          "quarter1": 0,
          "quarter2": 0,
          "quarter3": 0,
          "quarter4": 0
        },
        "standardDowns": {
          "total": 0,
          "quarter1": 0,
          "quarter2": 0,
          "quarter3": 0,
          "quarter4": 0
        },
        "passingDowns": {
          "total": 0,
          "quarter1": 0,
          "quarter2": 0,
          "quarter3": 0,
          "quarter4": 0
        }
      }
    ],
    "cumulativePpa": [
      {
        "team": "string",
        "plays": 0,
        "overall": {
          "total": 0,
          "quarter1": 0,
          "quarter2": 0,
          "quarter3": 0,
          "quarter4": 0
        },
        "passing": {
          "total": 0,
          "quarter1": 0,
          "quarter2": 0,
          "quarter3": 0,
          "quarter4": 0
        },
        "rushing": {
          "total": 0,
          "quarter1": 0,
          "quarter2": 0,
          "quarter3": 0,
          "quarter4": 0
        }
      }
    ],
    "ppa": [
      {
        "team": "string",
        "plays": 0,
        "overall": {
          "total": 0,
          "quarter1": 0,
          "quarter2": 0,
          "quarter3": 0,
          "quarter4": 0
        },
        "passing": {
          "total": 0,
          "quarter1": 0,
          "quarter2": 0,
          "quarter3": 0,
          "quarter4": 0
        },
        "rushing": {
          "total": 0,
          "quarter1": 0,
          "quarter2": 0,
          "quarter3": 0,
          "quarter4": 0
        }
      }
    ]
  },
  "players": {
    "ppa": [
      {
        "player": "string",
        "team": "string",
        "position": "string",
        "average": {
          "total": 0,
          "quarter1": 0,
          "quarter2": 0,
          "quarter3": 0,
          "quarter4": 0,
          "rushing": 0,
          "passing": 0
        },
        "cumulative": {
          "total": 0,
          "quarter1": 0,
          "quarter2": 0,
          "quarter3": 0,
          "quarter4": 0,
          "rushing": 0,
          "passing": 0
        }
      }
    ],
    "usage": [
      {
        "total": 0,
        "quarter1": 0,
        "quarter2": 0,
        "quarter3": 0,
        "quarter4": 0,
        "rushing": 0,
        "passing": 0,
        "player": "string",
        "team": "string",
        "position": "string"
      }
    ]
  }
}
No links
drives
Drive data



GET
/drives


plays
Play by play data



GET
/plays


Retrieves historical play data

Parameters
Try it out
Name	Description
year *
integer($int32)
(query)
Required year filter

year
week *
integer($int32)
(query)
Required week filter

week
team
string
(query)
Optional team filter

team
offense
string
(query)
Optional offensive team filter

offense
defense
string
(query)
Optional defensive team filter

defense
offenseConference
string
(query)
Optional offensive conference filter

offenseConference
defenseConference
string
(query)
Optional defensive conference filter

defenseConference
conference
string
(query)
Optional conference filter

conference
playType
string
(query)
Optoinal play type abbreviation filter

playType
seasonType
string
(query)
Optional season type filter

Available values : regular, postseason, both, allstar, spring_regular, spring_postseason


--
classification
string
(query)
Optional division classification filter

Available values : fbs, fcs, ii, iii


--
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "id": "string",
    "driveId": "string",
    "gameId": 0,
    "driveNumber": 0,
    "playNumber": 0,
    "offense": "string",
    "offenseConference": "string",
    "offenseScore": 0,
    "defense": "string",
    "home": "string",
    "away": "string",
    "defenseConference": "string",
    "defenseScore": 0,
    "period": 0,
    "clock": {
      "seconds": 0,
      "minutes": 0
    },
    "offenseTimeouts": 0,
    "defenseTimeouts": 0,
    "yardline": 0,
    "yardsToGoal": 0,
    "down": 0,
    "distance": 0,
    "yardsGained": 0,
    "scoring": true,
    "playType": "string",
    "playText": "string",
    "ppa": 0,
    "wallclock": "string"
  }
]
No links

GET
/plays/types


Retrieves available play types

Parameters
Try it out
No parameters

Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "id": 0,
    "text": "string",
    "abbreviation": "string"
  }
]
No links

GET
/plays/stats


Retrieve player-play associations (limit 2000)

Parameters
Try it out
Name	Description
year
integer($int32)
(query)
Optional year filter

year
week
integer($int32)
(query)
Optional week filter

week
team
string
(query)
Optional team filter

team
gameId
integer($int32)
(query)
Optional gameId filter

gameId
athleteId
integer($int32)
(query)
Optional athleteId filter

athleteId
statTypeId
integer($int32)
(query)
Optional statTypeId filter

statTypeId
seasonType
string
(query)
Optional season type filter

Available values : regular, postseason, both, allstar, spring_regular, spring_postseason


--
conference
string
(query)
Optional conference filter

conference
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "gameId": 0,
    "season": 0,
    "week": 0,
    "team": "string",
    "conference": "string",
    "opponent": "string",
    "teamScore": 0,
    "opponentScore": 0,
    "driveId": "string",
    "playId": "string",
    "period": 0,
    "clock": {
      "seconds": 0,
      "minutes": 0
    },
    "yardsToGoal": 0,
    "down": 0,
    "distance": 0,
    "athleteId": "string",
    "athleteName": "string",
    "statType": "string",
    "stat": 0
  }
]
No links

GET
/plays/stats/types


Retrieves available play stat types

Parameters
Try it out
No parameters

Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "id": 0,
    "name": "string"
  }
]
No links

GET
/live/plays


Queries live play-by-play data and advanced stats

Parameters
Try it out
Name	Description
gameId *
integer($int32)
(query)
Game Id filter

gameId
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
{
  "id": 0,
  "status": "string",
  "period": 0,
  "clock": "string",
  "possession": "string",
  "down": 0,
  "distance": 0,
  "yardsToGoal": 0,
  "teams": [
    {
      "teamId": 0,
      "team": "string",
      "homeAway": "home",
      "lineScores": [
        0
      ],
      "points": 0,
      "drives": 0,
      "scoringOpportunities": 0,
      "pointsPerOpportunity": 0,
      "averageStartYardLine": 0,
      "plays": 0,
      "lineYards": 0,
      "lineYardsPerRush": 0,
      "secondLevelYards": 0,
      "secondLevelYardsPerRush": 0,
      "openFieldYards": 0,
      "openFieldYardsPerRush": 0,
      "epaPerPlay": 0,
      "totalEpa": 0,
      "passingEpa": 0,
      "epaPerPass": 0,
      "rushingEpa": 0,
      "epaPerRush": 0,
      "successRate": 0,
      "standardDownSuccessRate": 0,
      "passingDownSuccessRate": 0,
      "explosiveness": 0,
      "deserveToWin": 0
    }
  ],
  "drives": [
    {
      "id": "string",
      "offenseId": 0,
      "offense": "string",
      "defenseId": 0,
      "defense": "string",
      "playCount": 0,
      "yards": 0,
      "startPeriod": 0,
      "startClock": "string",
      "startYardsToGoal": 0,
      "endPeriod": 0,
      "endClock": "string",
      "endYardsToGoal": 0,
      "duration": "string",
      "scoringOpportunity": true,
      "result": "string",
      "pointsGained": 0,
      "plays": [
        {
          "id": "string",
          "homeScore": 0,
          "awayScore": 0,
          "period": 0,
          "clock": "string",
          "wallClock": "2025-09-18T20:42:02.255Z",
          "teamId": 0,
          "team": "string",
          "down": 0,
          "distance": 0,
          "yardsToGoal": 0,
          "yardsGained": 0,
          "playTypeId": 0,
          "playType": "string",
          "epa": 0,
          "garbageTime": true,
          "success": true,
          "rushPass": "rush",
          "downType": "passing",
          "playText": "string"
        }
      ]
    }
  ]
}
No links
teams
Team information



GET
/teams


Retrieves team information

Parameters
Try it out
Name	Description
conference
string
(query)
Optional conference abbreviation filter

conference
year
integer($int32)
(query)
Optional year filter to get historical conference affiliations

year
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "id": 0,
    "school": "string",
    "mascot": "string",
    "abbreviation": "string",
    "alternateNames": [
      "string"
    ],
    "conference": "string",
    "division": "string",
    "classification": "string",
    "color": "string",
    "alternateColor": "string",
    "logos": [
      "string"
    ],
    "twitter": "string",
    "location": {
      "id": 0,
      "name": "string",
      "city": "string",
      "state": "string",
      "zip": "string",
      "countryCode": "string",
      "timezone": "string",
      "latitude": 0,
      "longitude": 0,
      "elevation": "string",
      "capacity": 0,
      "constructionYear": 0,
      "grass": true,
      "dome": true
    }
  }
]
No links

GET
/teams/fbs


Retrieves information on teams playing in the highest division of CFB

Parameters
Try it out
Name	Description
year
integer($int32)
(query)
Year or season

year
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "id": 0,
    "school": "string",
    "mascot": "string",
    "abbreviation": "string",
    "alternateNames": [
      "string"
    ],
    "conference": "string",
    "division": "string",
    "classification": "string",
    "color": "string",
    "alternateColor": "string",
    "logos": [
      "string"
    ],
    "twitter": "string",
    "location": {
      "id": 0,
      "name": "string",
      "city": "string",
      "state": "string",
      "zip": "string",
      "countryCode": "string",
      "timezone": "string",
      "latitude": 0,
      "longitude": 0,
      "elevation": "string",
      "capacity": 0,
      "constructionYear": 0,
      "grass": true,
      "dome": true
    }
  }
]
No links

GET
/teams/matchup


Retrieves historical matchup details for two given teams

Parameters
Try it out
Name	Description
team1 *
string
(query)
First team to compare

team1
team2 *
string
(query)
Second team to compare

team2
minYear
integer($int32)
(query)
Optional starting year

minYear
maxYear
integer($int32)
(query)
Optional ending year

maxYear
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
{
  "team1": "string",
  "team2": "string",
  "startYear": 0,
  "endYear": 0,
  "team1Wins": 0,
  "team2Wins": 0,
  "ties": 0,
  "games": [
    {
      "season": 0,
      "week": 0,
      "seasonType": "string",
      "date": "string",
      "neutralSite": true,
      "venue": "string",
      "homeTeam": "string",
      "homeScore": 0,
      "awayTeam": "string",
      "awayScore": 0,
      "winner": "string"
    }
  ]
}
No links

GET
/teams/ats


Retrieves against-the-spread (ATS) summary by team

Parameters
Try it out
Name	Description
year *
integer($int32)
(query)
Required year filter

year
conference
string
(query)
Optional conference filter

conference
team
string
(query)
Optional team filter

team
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "year": 0,
    "teamId": 0,
    "team": "string",
    "conference": "string",
    "games": 0,
    "atsWins": 0,
    "atsLosses": 0,
    "atsPushes": 0,
    "avgCoverMargin": 0
  }
]
No links

GET
/roster


Retrieves historical roster data

Parameters
Try it out
Name	Description
team
string
(query)
Optional team filter

team
year
integer($int32)
(query)
Optional year filter, defaults to 2025

year
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "id": "string",
    "firstName": "string",
    "lastName": "string",
    "team": "string",
    "height": 0,
    "weight": 0,
    "jersey": 0,
    "position": "string",
    "homeCity": "string",
    "homeState": "string",
    "homeCountry": "string",
    "homeLatitude": 0,
    "homeLongitude": 0,
    "homeCountyFIPS": "string",
    "recruitIds": [
      "string"
    ]
  }
]
No links

GET
/talent


Retrieve 247 Team Talent Composite for a given year

Parameters
Try it out
Name	Description
year *
integer($int32)
(query)
Year filter

year
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "year": 0,
    "team": "string",
    "talent": 0
  }
]
No links
conferences
Conference information



GET
/conferences


Retrieves list of conferences

Parameters
Try it out
No parameters

Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "id": 0,
    "name": "string",
    "shortName": "string",
    "abbreviation": "string",
    "classification": "fbs"
  }
]
No links
venues
Information about venues



GET
/venues


Retrieve list of venues

Parameters
Try it out
No parameters

Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "id": 0,
    "name": "string",
    "city": "string",
    "state": "string",
    "zip": "string",
    "countryCode": "string",
    "timezone": "string",
    "latitude": 0,
    "longitude": 0,
    "elevation": "string",
    "capacity": 0,
    "constructionYear": 0,
    "grass": true,
    "dome": true
  }
]
No links
coaches
Information about coaches



GET
/coaches


Retrieves historical head coach information and records

Parameters
Try it out
Name	Description
firstName
string
(query)
Optional first name filter

firstName
lastName
string
(query)
Optional last name filter

lastName
team
string
(query)
Optional team filter

team
year
integer($int32)
(query)
Optional year filter

year
minYear
integer($int32)
(query)
Optional start year range filter

minYear
maxYear
integer($int32)
(query)
Optional end year range filter

maxYear
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "firstName": "string",
    "lastName": "string",
    "hireDate": "2025-09-18T20:42:02.335Z",
    "seasons": [
      {
        "school": "string",
        "year": 0,
        "games": 0,
        "wins": 0,
        "losses": 0,
        "ties": 0,
        "preseasonRank": 0,
        "postseasonRank": 0,
        "srs": 0,
        "spOverall": 0,
        "spOffense": 0,
        "spDefense": 0
      }
    ]
  }
]
No links
players
Player information and data



GET
/player/search


Search for players (lists top 100 results)

Parameters
Try it out
Name	Description
searchTerm *
string
(query)
Search term for matching player name

searchTerm
year
integer($int32)
(query)
Optional year filter

year
team
string
(query)
Optional team filter

team
position
string
(query)
Optional position abbreviation filter

position
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "id": "string",
    "team": "string",
    "name": "string",
    "firstName": "string",
    "lastName": "string",
    "weight": 0,
    "height": 0,
    "jersey": 0,
    "position": "string",
    "hometown": "string",
    "teamColor": "string",
    "teamColorSecondary": "string"
  }
]
No links

GET
/player/usage


Retrieves player usage data for a given season

Parameters
Try it out
Name	Description
year *
integer($int32)
(query)
Required year filter

year
conference
string
(query)
Optional conference abbreviation filter

conference
position
string
(query)
Optional position abbreivation filter

position
team
string
(query)
Optional team filter

team
playerId
integer($int32)
(query)
Optional player id filter

playerId
excludeGarbageTime
boolean
(query)
Optional exclude garbage time flag, defaults to false


--
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "season": 0,
    "id": "string",
    "name": "string",
    "position": "string",
    "team": "string",
    "conference": "string",
    "usage": {
      "passingDowns": 0,
      "standardDowns": 0,
      "thirdDown": 0,
      "secondDown": 0,
      "firstDown": 0,
      "rush": 0,
      "pass": 0,
      "overall": 0
    }
  }
]
No links

GET
/player/returning


Retrieves returning production data. Either a year or team filter must be specified.

Parameters
Try it out
Name	Description
year
integer($int32)
(query)
Year filter, required if team not specified

year
team
string
(query)
Team filter, required if year not specified

team
conference
string
(query)
Optional conference filter

conference
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "season": 0,
    "team": "string",
    "conference": "string",
    "totalPPA": 0,
    "totalPassingPPA": 0,
    "totalReceivingPPA": 0,
    "totalRushingPPA": 0,
    "percentPPA": 0,
    "percentPassingPPA": 0,
    "percentReceivingPPA": 0,
    "percentRushingPPA": 0,
    "usage": 0,
    "passingUsage": 0,
    "receivingUsage": 0,
    "rushingUsage": 0
  }
]
No links

GET
/player/portal


Retrieves transfer portal data for a given year

Parameters
Try it out
Name	Description
year *
integer($int32)
(query)
Required year filter

year
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "season": 0,
    "firstName": "string",
    "lastName": "string",
    "position": "string",
    "origin": "string",
    "destination": "string",
    "transferDate": "2025-09-18T20:42:02.368Z",
    "rating": 0,
    "stars": 0,
    "eligibility": "Withdrawn"
  }
]
No links
rankings
Historical poll rankings



GET
/rankings


Retrieves historical poll data

Parameters
Try it out
Name	Description
year *
integer($int32)
(query)
Required year filter

year
seasonType
string
(query)
Optional season type filter

Available values : regular, postseason, both, allstar, spring_regular, spring_postseason


--
week
number($double)
(query)
Optional week filter

week
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "season": 0,
    "seasonType": "regular",
    "week": 0,
    "polls": [
      {
        "poll": "string",
        "ranks": [
          {
            "rank": 0,
            "teamId": 0,
            "school": "string",
            "conference": "string",
            "firstPlaceVotes": 0,
            "points": 0
          }
        ]
      }
    ]
  }
]
No links
betting
Betting lines and data



GET
/lines


Retrieves historical betting data

Parameters
Try it out
Name	Description
gameId
integer($int32)
(query)
Optional gameId filter

gameId
year
integer($int32)
(query)
Year filter, required if game id not specified

year
seasonType
string
(query)
Optional season type filter

Available values : regular, postseason, both, allstar, spring_regular, spring_postseason


--
week
integer($int32)
(query)
Optional week filter

week
team
string
(query)
Optional team filter

team
home
string
(query)
Optional home team filter

home
away
string
(query)
Optional away team filter

away
conference
string
(query)
Optional conference filter

conference
provider
string
(query)
Optional provider name filter

provider
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "id": 0,
    "season": 0,
    "seasonType": "regular",
    "week": 0,
    "startDate": "2025-09-18T20:42:02.393Z",
    "homeTeamId": 0,
    "homeTeam": "string",
    "homeConference": "string",
    "homeClassification": "fbs",
    "homeScore": 0,
    "awayTeamId": 0,
    "awayTeam": "string",
    "awayConference": "string",
    "awayClassification": "fbs",
    "awayScore": 0,
    "lines": [
      {
        "provider": "string",
        "spread": 0,
        "formattedSpread": "string",
        "spreadOpen": 0,
        "overUnder": 0,
        "overUnderOpen": 0,
        "homeMoneyline": 0,
        "awayMoneyline": 0
      }
    ]
  }
]
No links
recruiting
Recruiting rankings and data



GET
/recruiting/players


Retrieves player recruiting rankings

Parameters
Try it out
Name	Description
year
integer($int32)
(query)
Year filter, required when no team specified

year
team
string
(query)
Team filter, required when no team specified

team
position
string
(query)
Optional position categorization filter

position
state
string
(query)
Optional state/province filter

state
classification
string
(query)
Optional recruit type classification filter, defaults to HighSchool

Available values : JUCO, PrepSchool, HighSchool


--
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "id": "string",
    "athleteId": "string",
    "recruitType": "JUCO",
    "year": 0,
    "ranking": 0,
    "name": "string",
    "school": "string",
    "committedTo": "string",
    "position": "string",
    "height": 0,
    "weight": 0,
    "stars": 0,
    "rating": 0,
    "city": "string",
    "stateProvince": "string",
    "country": "string",
    "hometownInfo": {
      "fipsCode": "string",
      "longitude": 0,
      "latitude": 0
    }
  }
]
No links

GET
/recruiting/teams


Retrieves team recruiting rankings

Parameters
Try it out
Name	Description
year
integer($int32)
(query)
Optional year filter

year
team
string
(query)
Optional team filter

team
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "year": 0,
    "rank": 0,
    "team": "string",
    "points": 0
  }
]
No links

GET
/recruiting/groups


Retrieves aggregated recruiting statistics by team and position grouping

Parameters
Try it out
Name	Description
team
string
(query)
Optional team filter

team
conference
string
(query)
Optional conference filter

conference
recruitType
string
(query)
Optional recruit type filter, defaults to HighSchool

Available values : JUCO, PrepSchool, HighSchool


--
startYear
integer($int32)
(query)
Optional start year range, defaults to 2000

startYear
endYear
integer($int32)
(query)
Optional end year range, defaults to current year

endYear
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "team": "string",
    "conference": "string",
    "positionGroup": "string",
    "averageRating": 0,
    "totalRating": 0,
    "commits": 0,
    "averageStars": 0
  }
]
No links
ratings
Team rating data



GET
/ratings/sp


Retrieves SP+ ratings for a given year or school

Parameters
Try it out
Name	Description
year
integer($int32)
(query)
Year filter, required if team not specified

year
team
string
(query)
Team filter, required if year not specified

team
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "year": 0,
    "team": "string",
    "conference": "string",
    "rating": 0,
    "ranking": 0,
    "secondOrderWins": 0,
    "sos": 0,
    "offense": {
      "pace": 0,
      "runRate": 0,
      "passingDowns": 0,
      "standardDowns": 0,
      "passing": 0,
      "rushing": 0,
      "explosiveness": 0,
      "success": 0,
      "rating": 0,
      "ranking": 0
    },
    "defense": {
      "havoc": {
        "db": 0,
        "frontSeven": 0,
        "total": 0
      },
      "passingDowns": 0,
      "standardDowns": 0,
      "passing": 0,
      "rushing": 0,
      "explosiveness": 0,
      "success": 0,
      "rating": 0,
      "ranking": 0
    },
    "specialTeams": {
      "rating": 0
    }
  }
]
No links

GET
/ratings/sp/conferences


Retrieves aggregated historical conference SP+ data

Parameters
Try it out
Name	Description
year
integer($int32)
(query)
Optional year filter

year
conference
string
(query)
Optional conference filter

conference
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "year": 0,
    "conference": "string",
    "rating": 0,
    "secondOrderWins": 0,
    "sos": 0,
    "offense": {
      "pace": 0,
      "runRate": 0,
      "passingDowns": 0,
      "standardDowns": 0,
      "passing": 0,
      "rushing": 0,
      "explosiveness": 0,
      "success": 0,
      "rating": 0
    },
    "defense": {
      "havoc": {
        "db": 0,
        "frontSeven": 0,
        "total": 0
      },
      "passingDowns": 0,
      "standardDowns": 0,
      "passing": 0,
      "rushing": 0,
      "explosiveness": 0,
      "success": 0,
      "rating": 0
    },
    "specialTeams": {
      "rating": 0
    }
  }
]
No links

GET
/ratings/srs


Retrieves historical SRS for a year or team

Parameters
Try it out
Name	Description
year
integer($int32)
(query)
Year filter, required if team not specified

year
team
string
(query)
Team filter, required if year not specified

team
conference
string
(query)
Optional conference filter

conference
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "year": 0,
    "team": "string",
    "conference": "string",
    "division": "string",
    "rating": 0,
    "ranking": 0
  }
]
No links

GET
/ratings/elo


Retrieves historical Elo ratings

Parameters
Try it out
Name	Description
year
integer($int32)
(query)
Optional year filter

year
week
integer($int32)
(query)
Optional week filter, defaults to last available week in the season

week
seasonType
string
(query)
Optional season type filter

Available values : regular, postseason, both, allstar, spring_regular, spring_postseason


--
team
string
(query)
Optional team filter

team
conference
string
(query)
Optional conference filter

conference
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "year": 0,
    "team": "string",
    "conference": "string",
    "elo": 0
  }
]
No links

GET
/ratings/fpi


Retrieves historical Football Power Index (FPI) ratings

Parameters
Try it out
Name	Description
year
integer($int32)
(query)
year filter, required if team not specified

year
team
string
(query)
team filter, required if year not specified

team
conference
string
(query)
Optional conference filter

conference
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "year": 0,
    "team": "string",
    "conference": "string",
    "fpi": 0,
    "resumeRanks": {
      "gameControl": 0,
      "remainingStrengthOfSchedule": 0,
      "strengthOfSchedule": 0,
      "averageWinProbability": 0,
      "fpi": 0,
      "strengthOfRecord": 0
    },
    "efficiencies": {
      "specialTeams": 0,
      "defense": 0,
      "offense": 0,
      "overall": 0
    }
  }
]
No links
metrics
Data relating to Predicted Points and other metrics



GET
/ppa/predicted


Query Predicted Points values by down and distance

Parameters
Try it out
Name	Description
down *
integer($int32)
(query)
Down value

down
distance *
integer($int32)
(query)
Distance value

distance
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "yardLine": 0,
    "predictedPoints": 0
  }
]
No links

GET
/ppa/teams


Retrieves historical team PPA metrics by season

Parameters
Try it out
Name	Description
year
integer($int32)
(query)
Year filter, required if team not specified

year
team
string
(query)
Team filter, required if year not specified

team
conference
string
(query)
Conference abbreviation filter

conference
excludeGarbageTime
boolean
(query)
Exclude garbage time plays


--
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "season": 0,
    "conference": "string",
    "team": "string",
    "offense": {
      "cumulative": {
        "rushing": 0,
        "passing": 0,
        "total": 0
      },
      "thirdDown": 0,
      "secondDown": 0,
      "firstDown": 0,
      "rushing": 0,
      "passing": 0,
      "overall": 0
    },
    "defense": {
      "cumulative": {
        "rushing": 0,
        "passing": 0,
        "total": 0
      },
      "thirdDown": 0,
      "secondDown": 0,
      "firstDown": 0,
      "rushing": 0,
      "passing": 0,
      "overall": 0
    }
  }
]
No links

GET
/ppa/games


Retrieves historical team PPA metrics by game

Parameters
Try it out
Name	Description
year *
integer($int32)
(query)
Required year filter

year
week
integer($int32)
(query)
Optional week filter

week
seasonType
string
(query)
Optional season type filter

Available values : regular, postseason, both, allstar, spring_regular, spring_postseason


--
team
string
(query)
Optional team filter

team
conference
string
(query)
Optional conference abbreviation filter

conference
excludeGarbageTime
boolean
(query)
Optional flag to exclude garbage time plays


--
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "gameId": 0,
    "season": 0,
    "week": 0,
    "seasonType": "regular",
    "team": "string",
    "conference": "string",
    "opponent": "string",
    "offense": {
      "thirdDown": 0,
      "secondDown": 0,
      "firstDown": 0,
      "rushing": 0,
      "passing": 0,
      "overall": 0
    },
    "defense": {
      "thirdDown": 0,
      "secondDown": 0,
      "firstDown": 0,
      "rushing": 0,
      "passing": 0,
      "overall": 0
    }
  }
]
No links

GET
/ppa/players/games


Queries player PPA statistics by game

Parameters
Try it out
Name	Description
year *
integer($int32)
(query)
Required year filter

year
week
integer($int32)
(query)
Week filter, required if team not specified

week
seasonType
string
(query)
Optional season type filter

Available values : regular, postseason, both, allstar, spring_regular, spring_postseason


--
team
string
(query)
Team filter, required if week not specified

team
position
string
(query)
Optional player position abbreviation filter

position
playerId
string
(query)
Optional player ID filter

playerId
threshold
number($double)
(query)
Threshold value for minimum number of plays

threshold
excludeGarbageTime
boolean
(query)
Optional flag to exclude garbage time plays


--
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "season": 0,
    "week": 0,
    "seasonType": "regular",
    "id": "string",
    "name": "string",
    "position": "string",
    "team": "string",
    "opponent": "string",
    "averagePPA": {
      "rush": 0,
      "pass": 0,
      "all": 0
    }
  }
]
No links

GET
/ppa/players/season


Queries player PPA statistics by season

Parameters
Try it out
Name	Description
year
integer($int32)
(query)
Year filter, required if playerId not specified

year
conference
string
(query)
Optional conference abbreviation filter

conference
team
string
(query)
Optional team filter

team
position
string
(query)
Optional position abbreviation filter

position
playerId
string
(query)
Player ID filter, required if year not specified

playerId
threshold
number($double)
(query)
Threshold value for minimum number of plays

threshold
excludeGarbageTime
boolean
(query)
Optional flag to exclude garbage time plays


--
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "season": 0,
    "id": "string",
    "name": "string",
    "position": "string",
    "team": "string",
    "conference": "string",
    "averagePPA": {
      "passingDowns": 0,
      "standardDowns": 0,
      "thirdDown": 0,
      "secondDown": 0,
      "firstDown": 0,
      "rush": 0,
      "pass": 0,
      "all": 0
    },
    "totalPPA": {
      "passingDowns": 0,
      "standardDowns": 0,
      "thirdDown": 0,
      "secondDown": 0,
      "firstDown": 0,
      "rush": 0,
      "pass": 0,
      "all": 0
    }
  }
]
No links

GET
/metrics/wp


Query play win probabilities by game

Parameters
Try it out
Name	Description
gameId *
integer($int32)
(query)
Required game ID filter

gameId
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "gameId": 0,
    "playId": "string",
    "playText": "string",
    "homeId": 0,
    "home": "string",
    "awayId": 0,
    "away": "string",
    "spread": 0,
    "homeBall": true,
    "homeScore": 0,
    "awayScore": 0,
    "yardLine": 0,
    "down": 0,
    "distance": 0,
    "homeWinProbability": 0,
    "playNumber": 0
  }
]
No links

GET
/metrics/wp/pregame


Queries pregame win probabilities

Parameters
Try it out
Name	Description
year
integer($int32)
(query)
Optional year filter

year
week
integer($int32)
(query)
Optional week filter

week
seasonType
string
(query)
Optional season type filter

Available values : regular, postseason, both, allstar, spring_regular, spring_postseason


--
team
string
(query)
Optional team filter

team
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "season": 0,
    "seasonType": "regular",
    "week": 0,
    "gameId": 0,
    "homeTeam": "string",
    "awayTeam": "string",
    "spread": 0,
    "homeWinProbability": 0
  }
]
No links

GET
/metrics/fg/ep


Queries field goal expected points values

Parameters
Try it out
No parameters

Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "yardsToGoal": 0,
    "distance": 0,
    "expectedPoints": 0
  }
]
No links
stats
Statistical data



GET
/stats/player/season


Retrieves aggregated player statistics for a given season

Parameters
Try it out
Name	Description
year *
integer($int32)
(query)
Required year filter

year
conference
string
(query)
Optional conference filter

conference
team
string
(query)
Optional team filter

team
startWeek
integer($int32)
(query)
Optional starting week range

startWeek
endWeek
integer($int32)
(query)
Optional ending week range

endWeek
seasonType
string
(query)
Optional season type filter

Available values : regular, postseason, both, allstar, spring_regular, spring_postseason


--
category
string
(query)
Optional category filter

category
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "season": 0,
    "playerId": "string",
    "player": "string",
    "position": "string",
    "team": "string",
    "conference": "string",
    "category": "string",
    "statType": "string",
    "stat": "string"
  }
]
No links

GET
/stats/season


Retrieves aggregated team season statistics

Parameters
Try it out
Name	Description
year
integer($int32)
(query)
Year filter, required if team not specified

year
team
string
(query)
Team filter, required if year not specified

team
conference
string
(query)
Optional conference filter

conference
startWeek
integer($int32)
(query)
Optional week start range filter

startWeek
endWeek
integer($int32)
(query)
Optional week end range filter

endWeek
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "season": 0,
    "team": "string",
    "conference": "string",
    "statName": "string",
    "statValue": "string"
  }
]
No links

GET
/stats/categories


Gets team statistical categories

Parameters
Try it out
No parameters

Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  "string"
]
No links

GET
/stats/season/advanced


Retrieves advanced season statistics for teams

Parameters
Try it out
Name	Description
year
integer($int32)
(query)
Year filter, required if team not specified

year
team
string
(query)
Team filter, required if year not specified

team
excludeGarbageTime
boolean
(query)
Garbage time exclusion filter, defaults to false


--
startWeek
integer($int32)
(query)
Optional start week range filter

startWeek
endWeek
integer($int32)
(query)
Optional end week range filter

endWeek
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "season": 0,
    "team": "string",
    "conference": "string",
    "offense": {
      "passingPlays": {
        "explosiveness": 0,
        "successRate": 0,
        "totalPPA": 0,
        "ppa": 0,
        "rate": 0
      },
      "rushingPlays": {
        "explosiveness": 0,
        "successRate": 0,
        "totalPPA": 0,
        "ppa": 0,
        "rate": 0
      },
      "passingDowns": {
        "explosiveness": 0,
        "successRate": 0,
        "ppa": 0,
        "rate": 0
      },
      "standardDowns": {
        "explosiveness": 0,
        "successRate": 0,
        "ppa": 0,
        "rate": 0
      },
      "havoc": {
        "db": 0,
        "frontSeven": 0,
        "total": 0
      },
      "fieldPosition": {
        "averagePredictedPoints": 0,
        "averageStart": 0
      },
      "pointsPerOpportunity": 0,
      "totalOpportunies": 0,
      "openFieldYardsTotal": 0,
      "openFieldYards": 0,
      "secondLevelYardsTotal": 0,
      "secondLevelYards": 0,
      "lineYardsTotal": 0,
      "lineYards": 0,
      "stuffRate": 0,
      "powerSuccess": 0,
      "explosiveness": 0,
      "successRate": 0,
      "totalPPA": 0,
      "ppa": 0,
      "drives": 0,
      "plays": 0
    },
    "defense": {
      "passingPlays": {
        "explosiveness": 0,
        "successRate": 0,
        "totalPPA": 0,
        "ppa": 0,
        "rate": 0
      },
      "rushingPlays": {
        "explosiveness": 0,
        "successRate": 0,
        "totalPPA": 0,
        "ppa": 0,
        "rate": 0
      },
      "passingDowns": {
        "explosiveness": 0,
        "successRate": 0,
        "totalPPA": 0,
        "ppa": 0,
        "rate": 0
      },
      "standardDowns": {
        "explosiveness": 0,
        "successRate": 0,
        "ppa": 0,
        "rate": 0
      },
      "havoc": {
        "db": 0,
        "frontSeven": 0,
        "total": 0
      },
      "fieldPosition": {
        "averagePredictedPoints": 0,
        "averageStart": 0
      },
      "pointsPerOpportunity": 0,
      "totalOpportunies": 0,
      "openFieldYardsTotal": 0,
      "openFieldYards": 0,
      "secondLevelYardsTotal": 0,
      "secondLevelYards": 0,
      "lineYardsTotal": 0,
      "lineYards": 0,
      "stuffRate": 0,
      "powerSuccess": 0,
      "explosiveness": 0,
      "successRate": 0,
      "totalPPA": 0,
      "ppa": 0,
      "drives": 0,
      "plays": 0
    }
  }
]
No links

GET
/stats/game/advanced


Retrieves advanced statistics aggregated by game

Parameters
Try it out
Name	Description
year
integer($int32)
(query)
Year filter, required if team not specified

year
team
string
(query)
Team filter, required if year not specified

team
week
number($double)
(query)
Optional week filter

week
opponent
string
(query)
Optional opponent filter

opponent
excludeGarbageTime
boolean
(query)
Garbage time exclusion filter, defaults to false


--
seasonType
string
(query)
Optional season type filter

Available values : regular, postseason, both, allstar, spring_regular, spring_postseason


--
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "gameId": 0,
    "season": 0,
    "week": 0,
    "team": "string",
    "opponent": "string",
    "offense": {
      "passingPlays": {
        "explosiveness": 0,
        "successRate": 0,
        "totalPPA": 0,
        "ppa": 0
      },
      "rushingPlays": {
        "explosiveness": 0,
        "successRate": 0,
        "totalPPA": 0,
        "ppa": 0
      },
      "passingDowns": {
        "explosiveness": 0,
        "successRate": 0,
        "ppa": 0
      },
      "standardDowns": {
        "explosiveness": 0,
        "successRate": 0,
        "ppa": 0
      },
      "openFieldYardsTotal": 0,
      "openFieldYards": 0,
      "secondLevelYardsTotal": 0,
      "secondLevelYards": 0,
      "lineYardsTotal": 0,
      "lineYards": 0,
      "stuffRate": 0,
      "powerSuccess": 0,
      "explosiveness": 0,
      "successRate": 0,
      "totalPPA": 0,
      "ppa": 0,
      "drives": 0,
      "plays": 0
    },
    "defense": {
      "passingPlays": {
        "explosiveness": 0,
        "successRate": 0,
        "totalPPA": 0,
        "ppa": 0
      },
      "rushingPlays": {
        "explosiveness": 0,
        "successRate": 0,
        "totalPPA": 0,
        "ppa": 0
      },
      "passingDowns": {
        "explosiveness": 0,
        "successRate": 0,
        "ppa": 0
      },
      "standardDowns": {
        "explosiveness": 0,
        "successRate": 0,
        "ppa": 0
      },
      "openFieldYardsTotal": 0,
      "openFieldYards": 0,
      "secondLevelYardsTotal": 0,
      "secondLevelYards": 0,
      "lineYardsTotal": 0,
      "lineYards": 0,
      "stuffRate": 0,
      "powerSuccess": 0,
      "explosiveness": 0,
      "successRate": 0,
      "totalPPA": 0,
      "ppa": 0,
      "drives": 0,
      "plays": 0
    }
  }
]
No links
draft
NFL Draft data



GET
/draft/teams


Retrieves list of NFL teams

Parameters
Try it out
No parameters

Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "location": "string",
    "nickname": "string",
    "displayName": "string",
    "logo": "string"
  }
]
No links

GET
/draft/positions


Retrieves list of player position categories for the NFL Draft

Parameters
Try it out
No parameters

Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "name": "string",
    "abbreviation": "string"
  }
]
No links

GET
/draft/picks


Retrieve historical NFL draft data

Parameters
Try it out
Name	Description
year
integer($int32)
(query)
Optional year filter

year
team
string
(query)
Optional NFL team filter

team
school
string
(query)
Optional college team filter

school
conference
string
(query)
Optional college conference filter

conference
position
string
(query)
Optional position classification filter

position
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "collegeAthleteId": 0,
    "nflAthleteId": 0,
    "collegeId": 0,
    "collegeTeam": "string",
    "collegeConference": "string",
    "nflTeamId": 0,
    "nflTeam": "string",
    "year": 0,
    "overall": 0,
    "round": 0,
    "pick": 0,
    "name": "string",
    "position": "string",
    "height": 0,
    "weight": 0,
    "preDraftRanking": 0,
    "preDraftPositionRanking": 0,
    "preDraftGrade": 0,
    "hometownInfo": {
      "countyFips": "string",
      "longitude": "string",
      "latitude": "string",
      "country": "string",
      "state": "string",
      "city": "string"
    }
  }
]
No links
adjustedMetrics
Metrics adjusted for opponent strength and other factors



GET
/wepa/team/season


Retrieve opponent-adjusted team season statistics

Parameters
Try it out
Name	Description
year
integer($int32)
(query)
Optional year filter

year
team
string
(query)
Optional team filter

team
conference
string
(query)
Optional conference filter

conference
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "year": 0,
    "teamId": 0,
    "team": "string",
    "conference": "string",
    "epa": {
      "rushing": 0,
      "passing": 0,
      "total": 0
    },
    "epaAllowed": {
      "rushing": 0,
      "passing": 0,
      "total": 0
    },
    "successRate": {
      "passingDowns": 0,
      "standardDowns": 0,
      "total": 0
    },
    "successRateAllowed": {
      "passingDowns": 0,
      "standardDowns": 0,
      "total": 0
    },
    "rushing": {
      "highlightYards": 0,
      "openFieldYards": 0,
      "secondLevelYards": 0,
      "lineYards": 0
    },
    "rushingAllowed": {
      "highlightYards": 0,
      "openFieldYards": 0,
      "secondLevelYards": 0,
      "lineYards": 0
    },
    "explosiveness": 0,
    "explosivenessAllowed": 0
  }
]
No links

GET
/wepa/players/passing


Retrieve opponent-adjusted player passing statistics

Parameters
Try it out
Name	Description
year
integer($int32)
(query)
Optional year filter

year
team
string
(query)
Optional team filter

team
conference
string
(query)
Optional conference abbreviation filter

conference
position
string
(query)
Optional position abbreviation filter

position
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "year": 0,
    "athleteId": "string",
    "athleteName": "string",
    "position": "string",
    "team": "string",
    "conference": "string",
    "wepa": 0,
    "plays": 0
  }
]
No links

GET
/wepa/players/rushing


Retrieve opponent-adjusted player rushing statistics

Parameters
Try it out
Name	Description
year
integer($int32)
(query)
Optional year filter

year
team
string
(query)
Optional team filter

team
conference
string
(query)
Optional conference abbreviation filter

conference
position
string
(query)
Optional position abbreviation filter

position
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "year": 0,
    "athleteId": "string",
    "athleteName": "string",
    "position": "string",
    "team": "string",
    "conference": "string",
    "wepa": 0,
    "plays": 0
  }
]
No links

GET
/wepa/players/kicking


Retrieve Points Added Above Replacement (PAAR) ratings for kickers

Parameters
Try it out
Name	Description
year
integer($int32)
(query)
Optional year filter

year
team
string
(query)
Optional team filter

team
conference
string
(query)
Optional conference abbreviation filter

conference
Responses
Code	Description	Links
200	
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "year": 0,
    "athleteId": "string",
    "athleteName": "string",
    "team": "string",
    "conference": "string",
    "paar": 0,
    "attempts": 0
  }
]
No links
info
General information about the API and user



GET
/info


Retrieves information about the user, including their Patreon level and remaining API calls.

Parameters
Try it out
No parameters

Responses
Code	Description	Links
200	
UserInfo object containing patron level and remaining calls, or null if not authenticated.

Media type

application/json
Controls Accept header.
Example Value
Schema
{
  "patronLevel": 0,
  "remainingCalls": 0
}
No links

Schemas
AdjustedTeamMetrics{
year*	[...]
teamId*	[...]
team*	[...]
conference*	[...]
epa*	{...}
epaAllowed*	{...}
successRate*	{...}
successRateAllowed*	{...}
rushing*	{...}
rushingAllowed*	{...}
explosiveness*	[...]
explosivenessAllowed*	[...]
}
PlayerWeightedEPA{
year*	[...]
athleteId*	[...]
athleteName*	[...]
position*	[...]
team*	[...]
conference*	[...]
wepa*	[...]
plays*	[...]
}
KickerPAAR{
year*	[...]
athleteId*	[...]
athleteName*	[...]
team*	[...]
conference*	[...]
paar*	[...]
attempts*	[...]
}
Venue{
id*	[...]
name*	[...]
city*	[...]
state*	[...]
zip*	[...]
countryCode*	[...]
timezone*	[...]
latitude*	[...]
longitude*	[...]
elevation*	[...]
capacity*	[...]
constructionYear*	[...]
grass	[...]
dome	[...]
}
Team{
id*	[...]
school*	[...]
mascot*	[...]
abbreviation*	[...]
alternateNames*	[...]
conference*	[...]
division*	[...]
classification*	[...]
color*	[...]
alternateColor*	[...]
logos*	[...]
twitter*	[...]
location*	{...}
nullable: true
}
MatchupGame{
season*	[...]
week*	[...]
seasonType*	[...]
date*	[...]
neutralSite*	[...]
venue*	[...]
homeTeam*	[...]
homeScore*	[...]
awayTeam*	[...]
awayScore*	[...]
winner*	[...]
}
Matchup{
team1*	[...]
team2*	[...]
startYear	[...]
endYear	[...]
team1Wins*	[...]
team2Wins*	[...]
ties*	[...]
games*	[...]
}
TeamATS{
year*	[...]
teamId*	[...]
team*	[...]
conference*	[...]
games*	[...]
atsWins*	[...]
atsLosses*	[...]
atsPushes*	[...]
avgCoverMargin*	[...]
}
RosterPlayer{
id*	[...]
firstName*	[...]
lastName*	[...]
team*	[...]
height*	[...]
weight*	[...]
jersey*	[...]
year*	[...]
position*	[...]
homeCity*	[...]
homeState*	[...]
homeCountry*	[...]
homeLatitude*	[...]
homeLongitude*	[...]
homeCountyFIPS*	[...]
recruitIds*	[...]
}
DivisionClassificationstring
Enum:
Array [ 4 ]
Conference{
id*	[...]
name*	[...]
shortName*	[...]
abbreviation*	[...]
classification*	[...]
}
TeamTalent{
year*	[...]
team*	[...]
talent*	[...]
}
PlayerStat{
season*	[...]
playerId*	[...]
player*	[...]
position*	[...]
team*	[...]
conference*	[...]
category*	[...]
statType*	[...]
stat*	[...]
}
SeasonTypestring
Enum:
Array [ 6 ]
TeamStat{
season*	[...]
team*	[...]
conference*	[...]
statName*	[...]
statValue*	{...}
}
AdvancedSeasonStat{
season*	[...]
team*	[...]
conference*	[...]
offense*	{...}
defense*	{...}
}
AdvancedGameStat{
gameId*	[...]
season*	[...]
week*	[...]
team*	[...]
opponent*	[...]
offense*	{...}
defense*	{...}
}
RecruitClassificationstring
Enum:
Array [ 3 ]
Recruit{
id*	[...]
athleteId*	[...]
recruitType*	RecruitClassification[...]
year*	[...]
ranking*	[...]
name*	[...]
school*	[...]
committedTo*	[...]
position*	[...]
height*	[...]
weight*	[...]
stars*	[...]
rating*	[...]
city*	[...]
stateProvince*	[...]
country*	[...]
hometownInfo*	{...}
}
TeamRecruitingRanking{
year*	[...]
rank*	[...]
team*	[...]
points*	[...]
}
AggregatedTeamRecruiting{
team*	[...]
conference*	[...]
positionGroup*	[...]
averageRating*	[...]
totalRating*	[...]
commits*	[...]
averageStars*	[...]
}
TeamSP{
year*	[...]
team*	[...]
conference*	[...]
rating*	[...]
ranking*	[...]
secondOrderWins*	[...]
sos*	[...]
offense*	{...}
defense*	{...}
specialTeams*	{...}
}
ConferenceSP{
year*	[...]
conference*	[...]
rating*	[...]
secondOrderWins*	[...]
sos*	[...]
offense*	{...}
defense*	{...}
specialTeams*	{...}
}
TeamSRS{
year*	[...]
team*	[...]
conference*	[...]
division*	[...]
rating*	[...]
ranking*	[...]
}
TeamElo{
year*	[...]
team*	[...]
conference*	[...]
elo*	[...]
}
TeamFPI{
year*	[...]
team*	[...]
conference*	[...]
fpi*	[...]
resumeRanks*	{...}
efficiencies*	{...}
}
PollRank{
rank*	[...]
teamId*	[...]
school*	[...]
conference*	[...]
firstPlaceVotes*	[...]
points*	[...]
}
Poll{
poll*	[...]
ranks*	[...]
}
PollWeek{
season*	[...]
seasonType*	SeasonType[...]
week*	[...]
polls*	[...]
}
Play{
id*	[...]
driveId*	[...]
gameId*	[...]
driveNumber*	[...]
playNumber*	[...]
offense*	[...]
offenseConference*	[...]
offenseScore*	[...]
defense*	[...]
home*	[...]
away*	[...]
defenseConference*	[...]
defenseScore*	[...]
period*	[...]
clock*	{...}
offenseTimeouts*	[...]
defenseTimeouts*	[...]
yardline*	[...]
yardsToGoal*	[...]
down*	[...]
distance*	[...]
yardsGained*	[...]
scoring*	[...]
playType*	[...]
playText*	[...]
ppa*	[...]
wallclock*	[...]
}
PlayType{
id*	[...]
text*	[...]
abbreviation*	[...]
}
PlayStat{
gameId*	[...]
season*	[...]
week*	[...]
team*	[...]
conference*	[...]
opponent*	[...]
teamScore*	[...]
opponentScore*	[...]
driveId*	[...]
playId*	[...]
period*	[...]
clock*	{...}
yardsToGoal*	[...]
down*	[...]
distance*	[...]
athleteId*	[...]
athleteName*	[...]
statType*	[...]
stat*	[...]
}
PlayStatType{
id*	[...]
name*	[...]
}
PlayerSearchResult{
id*	[...]
team*	[...]
name*	[...]
firstName*	[...]
lastName*	[...]
weight*	[...]
height*	[...]
jersey*	[...]
position*	[...]
hometown*	[...]
teamColor*	[...]
teamColorSecondary*	[...]
}
PlayerPPAChartItem{
playNumber*	[...]
avgPPA*	[...]
}
PlayerUsage{
season*	[...]
id*	[...]
name*	[...]
position*	[...]
team*	[...]
conference*	[...]
usage*	{...}
}
ReturningProduction{
season*	[...]
team*	[...]
conference*	[...]
totalPPA*	[...]
totalPassingPPA*	[...]
totalReceivingPPA*	[...]
totalRushingPPA*	[...]
percentPPA*	[...]
percentPassingPPA*	[...]
percentReceivingPPA*	[...]
percentRushingPPA*	[...]
usage*	[...]
passingUsage*	[...]
receivingUsage*	[...]
rushingUsage*	[...]
}
TransferEligibilitystring
Enum:
Array [ 5 ]
PlayerTransfer{
season*	[...]
firstName*	[...]
lastName*	[...]
position*	[...]
origin*	[...]
destination*	[...]
transferDate*	[...]
rating*	[...]
stars*	[...]
eligibility*	[...]
}
PredictedPointsValue{
yardLine*	[...]
predictedPoints*	[...]
}
TeamSeasonPredictedPointsAdded{
season*	[...]
conference*	[...]
team*	[...]
offense*	{...}
defense*	{...}
}
TeamGamePredictedPointsAdded{
gameId*	[...]
season*	[...]
week*	[...]
seasonType*	SeasonType[...]
team*	[...]
conference*	[...]
opponent*	[...]
offense*	{...}
defense*	{...}
}
PlayerGamePredictedPointsAdded{
season*	[...]
week*	[...]
seasonType*	SeasonType[...]
id*	[...]
name*	[...]
position*	[...]
team*	[...]
opponent*	[...]
averagePPA*	{...}
}
PlayerSeasonPredictedPointsAdded{
season*	[...]
id*	[...]
name*	[...]
position*	[...]
team*	[...]
conference*	[...]
averagePPA*	{...}
totalPPA*	{...}
}
PlayWinProbability{
gameId*	[...]
playId*	[...]
playText*	[...]
homeId*	[...]
home*	[...]
awayId*	[...]
away*	[...]
spread*	[...]
homeBall*	[...]
homeScore*	[...]
awayScore*	[...]
yardLine*	[...]
down*	[...]
distance*	[...]
homeWinProbability*	[...]
playNumber*	[...]
}
PregameWinProbability{
season*	[...]
seasonType*	SeasonType[...]
week*	[...]
gameId*	[...]
homeTeam*	[...]
awayTeam*	[...]
spread*	[...]
homeWinProbability*	[...]
}
FieldGoalEP{
yardsToGoal*	[...]
distance*	[...]
expectedPoints*	[...]
}
LiveGameTeam{
teamId*	[...]
team*	[...]
homeAway*	[...]
lineScores*	[...]
points*	[...]
drives*	[...]
scoringOpportunities*	[...]
pointsPerOpportunity*	[...]
averageStartYardLine*	[...]
plays*	[...]
lineYards*	[...]
lineYardsPerRush*	[...]
secondLevelYards*	[...]
secondLevelYardsPerRush*	[...]
openFieldYards*	[...]
openFieldYardsPerRush*	[...]
epaPerPlay*	[...]
totalEpa*	[...]
passingEpa*	[...]
epaPerPass*	[...]
rushingEpa*	[...]
epaPerRush*	[...]
successRate*	[...]
standardDownSuccessRate*	[...]
passingDownSuccessRate*	[...]
explosiveness*	[...]
deserveToWin	[...]
}
LiveGamePlay{
id*	[...]
homeScore*	[...]
awayScore*	[...]
period*	[...]
clock*	[...]
wallClock*	[...]
teamId*	[...]
team*	[...]
down*	[...]
distance*	[...]
yardsToGoal*	[...]
yardsGained*	[...]
playTypeId*	[...]
playType*	[...]
epa*	[...]
garbageTime*	[...]
success*	[...]
rushPass*	[...]
downType*	[...]
playText*	[...]
}
LiveGameDrive{
id*	[...]
offenseId*	[...]
offense*	[...]
defenseId*	[...]
defense*	[...]
playCount*	[...]
yards*	[...]
startPeriod*	[...]
startClock*	[...]
startYardsToGoal*	[...]
endPeriod*	[...]
endClock*	[...]
endYardsToGoal*	[...]
duration*	[...]
scoringOpportunity*	[...]
result*	[...]
pointsGained*	[...]
plays*	[...]
}
LiveGame{
id*	[...]
status*	[...]
period*	[...]
clock*	[...]
possession*	[...]
down*	[...]
distance*	[...]
yardsToGoal*	[...]
teams*	[...]
drives*	[...]
}
GameLine{
provider*	[...]
spread*	[...]
formattedSpread*	[...]
spreadOpen*	[...]
overUnder*	[...]
overUnderOpen*	[...]
homeMoneyline*	[...]
awayMoneyline*	[...]
}
BettingGame{
id*	[...]
season*	[...]
seasonType*	SeasonType[...]
week*	[...]
startDate*	[...]
homeTeamId*	[...]
homeTeam*	[...]
homeConference*	[...]
homeClassification*	[...]
homeScore*	[...]
awayTeamId*	[...]
awayTeam*	[...]
awayConference*	[...]
awayClassification*	[...]
awayScore*	[...]
lines*	[...]
}
UserInfo{
patronLevel*	[...]
remainingCalls*	[...]
}
Game{
id*	[...]
season*	[...]
week*	[...]
seasonType*	SeasonType[...]
startDate*	[...]
startTimeTBD*	[...]
completed*	[...]
neutralSite*	[...]
conferenceGame*	[...]
attendance*	[...]
venueId*	[...]
venue*	[...]
homeId*	[...]
homeTeam*	[...]
homeConference*	[...]
homeClassification*	[...]
homePoints*	[...]
homeLineScores*	[...]
homePostgameWinProbability*	[...]
homePregameElo*	[...]
homePostgameElo*	[...]
awayId*	[...]
awayTeam*	[...]
awayConference*	[...]
awayClassification*	[...]
awayPoints*	[...]
awayLineScores*	[...]
awayPostgameWinProbability*	[...]
awayPregameElo*	[...]
awayPostgameElo*	[...]
excitementIndex*	[...]
highlights*	[...]
notes*	[...]
}
GameTeamStatsTeamStat{
category*	[...]
stat*	[...]
}
GameTeamStatsTeam{
teamId*	[...]
team*	[...]
conference*	[...]
homeAway*	[...]
points*	[...]
stats*	[...]
}
GameTeamStats{
id*	[...]
teams*	[...]
}
GamePlayerStatPlayer{
id*	[...]
name*	[...]
stat*	[...]
}
GamePlayerStatTypes{
name*	[...]
athletes*	[...]
}
GamePlayerStatCategories{
name*	[...]
types*	[...]
}
GamePlayerStatsTeam{
team*	[...]
conference*	[...]
homeAway*	[...]
points*	[...]
categories*	[...]
}
GamePlayerStats{
id*	[...]
teams*	[...]
}
MediaTypestring
Enum:
Array [ 5 ]
GameMedia{
id*	[...]
season*	[...]
week*	[...]
seasonType*	SeasonType[...]
startTime*	[...]
isStartTimeTBD*	[...]
homeTeam*	[...]
homeConference*	[...]
awayTeam*	[...]
awayConference*	[...]
mediaType*	MediaType[...]
outlet*	[...]
}
GameWeather{
id*	[...]
season*	[...]
week*	[...]
seasonType*	SeasonType[...]
startTime*	[...]
gameIndoors*	[...]
homeTeam*	[...]
homeConference*	[...]
awayTeam*	[...]
awayConference*	[...]
venueId*	[...]
venue*	[...]
temperature*	[...]
dewPoint*	[...]
humidity*	[...]
precipitation*	[...]
snowfall*	[...]
windDirection*	[...]
windSpeed*	[...]
pressure*	[...]
weatherConditionCode*	[...]
weatherCondition*	[...]
}
TeamRecord{
games*	[...]
wins*	[...]
losses*	[...]
ties*	[...]
}
TeamRecords{
year*	[...]
teamId*	[...]
team*	[...]
classification*	[...]
conference*	[...]
division*	[...]
expectedWins*	[...]
total*	TeamRecord{...}
conferenceGames*	TeamRecord{...}
homeGames*	TeamRecord{...}
awayGames*	TeamRecord{...}
neutralSiteGames*	TeamRecord{...}
regularSeason*	TeamRecord{...}
postseason*	TeamRecord{...}
}
CalendarWeek{
season*	[...]
week*	[...]
seasonType*	SeasonType[...]
startDate*	[...]
endDate*	[...]
firstGameStart*	[...]
lastGameStart*	[...]
}
GameStatusstring
Enum:
Array [ 3 ]
ScoreboardGame{
id*	[...]
startDate*	[...]
startTimeTBD*	[...]
tv*	[...]
neutralSite*	[...]
conferenceGame*	[...]
status*	GameStatus[...]
period*	[...]
clock*	[...]
situation*	[...]
possession*	[...]
lastPlay*	[...]
venue*	{...}
homeTeam*	{...}
awayTeam*	{...}
weather*	{...}
betting*	{...}
}
Drive{
offense*	[...]
offenseConference*	[...]
defense*	[...]
defenseConference*	[...]
gameId*	[...]
id*	[...]
driveNumber*	[...]
scoring*	[...]
startPeriod*	[...]
startYardline*	[...]
startYardsToGoal*	[...]
startTime*	{...}
endPeriod*	[...]
endYardline*	[...]
endYardsToGoal*	[...]
endTime*	{...}
elapsed*	{...}
plays*	[...]
yards*	[...]
driveResult*	[...]
isHomeOffense*	[...]
startOffenseScore*	[...]
startDefenseScore*	[...]
endOffenseScore*	[...]
endDefenseScore*	[...]
}
DraftTeam{
location*	[...]
nickname*	[...]
displayName*	[...]
logo*	[...]
}
DraftPosition{
name*	[...]
abbreviation*	[...]
}
DraftPick{
collegeAthleteId*	[...]
nflAthleteId*	[...]
collegeId*	[...]
collegeTeam*	[...]
collegeConference*	[...]
nflTeamId*	[...]
nflTeam*	[...]
year*	[...]
overall*	[...]
round*	[...]
pick*	[...]
name*	[...]
position*	[...]
height*	[...]
weight*	[...]
preDraftRanking*	[...]
preDraftPositionRanking*	[...]
preDraftGrade*	[...]
hometownInfo*	{...}
}
CoachSeason{
school*	[...]
year*	[...]
games*	[...]
wins*	[...]
losses*	[...]
ties*	[...]
preseasonRank*	[...]
postseasonRank*	[...]
srs*	[...]
spOverall*	[...]
spOffense*	[...]
spDefense*	[...]
}
Coach{
firstName*	[...]
lastName*	[...]
hireDate*	[...]
seasons*	[...]
}
StatsByQuarter{
total*	[...]
quarter1*	[...]
quarter2*	[...]
quarter3*	[...]
quarter4*	[...]
}
TeamPPA{
team*	[...]
plays*	[...]
overall*	StatsByQuarter{...}
passing*	StatsByQuarter{...}
rushing*	StatsByQuarter{...}
}
TeamSuccessRates{
team*	[...]
overall*	StatsByQuarter{...}
standardDowns*	StatsByQuarter{...}
passingDowns*	StatsByQuarter{...}
}
TeamExplosiveness{
team*	[...]
overall*	StatsByQuarter{...}
}
TeamRushingStats{
team*	[...]
powerSuccess*	[...]
stuffRate*	[...]
lineYards*	[...]
lineYardsAverage*	[...]
secondLevelYards*	[...]
secondLevelYardsAverage*	[...]
openFieldYards*	[...]
openFieldYardsAverage*	[...]
}
TeamHavoc{
team*	[...]
total*	[...]
frontSeven*	[...]
db*	[...]
}
TeamScoringOpportunities{
team*	[...]
opportunities*	[...]
points*	[...]
pointsPerOpportunity*	[...]
}
TeamFieldPosition{
team*	[...]
averageStart*	[...]
averageStartingPredictedPoints*	[...]
}
PlayerGameUsage{
total*	[...]
quarter1*	[...]
quarter2*	[...]
quarter3*	[...]
quarter4*	[...]
rushing*	[...]
passing*	[...]
player*	[...]
team*	[...]
position*	[...]
}
PlayerStatsByQuarter{
total*	[...]
quarter1*	[...]
quarter2*	[...]
quarter3*	[...]
quarter4*	[...]
rushing*	[...]
passing*	[...]
}
PlayerPPA{
player*	[...]
team*	[...]
position*	[...]
average*	PlayerStatsByQuarter{...}
cumulative*	PlayerStatsByQuarter{...}
}
AdvancedBoxScore{
gameInfo*	{...}
teams*	{...}
players*	{...}
}