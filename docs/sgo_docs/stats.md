Stats
NOTE

The data on this page may be outdated. For the most up-to-date list of statID values for each sport, please call the /stats endpoint

A statID corresponds to a specific statistic or value. Each sport has its own set of supported statIDs.

When looking at the results object of an Event, the statID allows you to find a specific stat value for a team or player.

When looking at odds data, each item (betting option) will contain a statID corresponding to the stat which will determine the outcome of the bet.

All sports contain the statID points. This will always correspond to the stat which determines the winner of a game/match. The points statID is applied even in sports where the word “points” isn’t used to describe that stat. For example, we commonly use the term runs for baseball but the statID for Runs is still points. Different types or prop bets also all have their own statIDs. Below you’ll find a list of supported statID values for each sport.

Baseball
Runs
statID: points
description: Runs scored
Doubles
statID: batting_doubles
description: Doubles
Home Runs
statID: batting_triples
description: Triples
Home Runs
statID: batting_homeRuns
description: Home runs
Strikeouts
statID: batting_strikeouts
description: Strike outs
Walks
statID: batting_basesOnBalls
description: Base on balls
Hits
statID: batting_hits
description: Hits
Batting Average
statID: batting_battingAvg
description: Batting average
On-Base %
statID: batting_onBasePercent
description: On-base percentage
Slugging %
statID: batting_sluggingPercent
description: Slugging percentage
On-Base + Slugging %
statID: batting_OPS
description: On-base plus slugging
Runs Batted In
statID: batting_RBI
description: Runs batted in
At Bats
statID: batting_atBats
description: At bats
Left on Base
statID: batting_leftOnBase
description: Left on base
Fly Outs
statID: batting_flyOuts
description: Fly outs
Ground Outs
statID: batting_groundOuts
description: Ground outs
Hit by Pitch
statID: batting_hitByPitch
description: Hit by pitch
Caught Stealing
statID: batting_caughtStealing
description: Caught stealing
Stolen Bases
statID: batting_stolenBases
description: Stolen bases
Sacrifice Bunts
statID: batting_sacrificeBunts
description: Sacrifice bunts
Sacrifice Flies
statID: batting_sacrificeFlies
description: Sacrifice flies
Runs Allowed
statID: pitching_runsAllowed
description: Runs allowed
Home Runs Allowed
statID: pitching_homeRunsAllowed
description: Home runs allowed
Strikeouts
statID: pitching_strikeouts
description: Strikeouts
Walks
statID: pitching_basesOnBalls
description: Walks allowed
Hits Allowed
statID: pitching_hits
description: Hits allowed
ERA
statID: pitching_ERA
description: Earned run average
Innings Pitched
statID: pitching_inningsPitched
description: Innings pitched
Earned Runs
statID: pitching_earnedRuns
description: Earned runs allowed
Batters Faced
statID: pitching_battersFaced
description: Batters faced
Outs
statID: pitching_outs
description: Outs recorded
Pitches Thrown
statID: pitching_pitchesThrown
description: Pitches thrown
Strikes Thrown
statID: pitching_strikesThrown
description: Strikes thrown
Errors
statID: fielding_errors
description: Errors
Assists
statID: fielding_assists
description: Assists
Put Outs
statID: fielding_putOuts
description: Put outs
Largest Lead
statID: largestLead
description: Largest lead held during the game
Innings in Lead
statID: inningsInLead
description: Number of innings the team was in the lead
Times Tied
statID: timesTied
description: Number of times the game was tied (excluding the start)
Lead Changes
statID: leadChanges
description: Number of times the winning team changed
Football
Points
statID: points
description: Points scored
Touchdowns
statID: touchdowns
description: Total Touchdowns
Yards
statID: yards
description: Total Yards (net)
First Downs
statID: firstDowns
description: Total First Downs
Turnovers
statID: turnovers
description: Total Turnovers
Fumbles
statID: fumbles
description: Number of fumbles committed by the offense and special teams
Fumbles Lost
statID: fumblesLost
description: Fumbles lost
Num. Penalties
statID: penalty_count
description: Number of penalties incurred
Penalty Yards
statID: penalty_yards
description: Number of yards penalized
Penalty First Downs
statID: penalty_firstDowns
description: Number of first downs achieved by penalty
Field Goal Blocks
statID: fieldGoalBlocks
description: Number of field goal attempts successfully blocked
Punt Blocks
statID: puntBlocks
description: Number of punt attempts successfully blocked
Red Zone Trips
statID: offense_redZoneTrips
description: Number of times the offense has entered the red zone
Red Zone Touchdowns
statID: offense_redZoneTouchdowns
description: Number of times the offense has scored a touchdown in the red zone
Drives
statID: offense_drives
description: Number of offensive drives
Plays
statID: offense_plays
description: Number of offensive plays ran
Yards Per Play
statID: offense_yardsPerPlay
description: Average net yards gained per offensive play
Time of Possession (Sec.)
statID: offense_secondsOfPossession
description: Time of possession (seconds)
Time of Possession (Min.)
statID: offense_minutesOfPossession
description: Time of possession (minutes)
Third Down Attempts
statID: offense_thirdDownAttempts
description: Number of third down attempts
Third Down Conversions
statID: offense_thirdDownConversions
description: Number of third down conversions
Third Down Efficiency
statID: offense_thirdDownEfficiency
description: Third down efficiency
Fourth Down Attempts
statID: offense_fourthDownAttempts
description: Number of fourth down attempts
Fourth Down Conversions
statID: offense_fourthDownConversions
description: Number of fourth down conversions
Fourth Down Efficiency
statID: offense_fourthDownEfficiency
description: Fourth down efficiency
Receiving Touchdowns
statID: receiving_touchdowns
description: Receiving touchdowns
Receiving Yards
statID: receiving_yards
description: Receiving yards
Receptions
statID: receiving_receptions
description: Receptions
Targets
statID: receiving_targets
description: Targets
Yards After Catch
statID: receiving_yardsAfterCatch
description: Yards after catch
Receiving First Downs
statID: receiving_firstDowns
description: Receiving first downs
Longest Reception
statID: receiving_longestReception
description: Longest reception
Yards Per Reception
statID: receiving_yardsPerReception
description: Yards per reception
Two Point Conversions
statID: receiving_twoPointConversions
description: Two point conversions
Rushing Touchdowns
statID: rushing_touchdowns
description: Rushing touchdowns
Rushing Yards
statID: rushing_yards
description: Rushing yards
Rushing Attempts
statID: rushing_attempts
description: Rushing attempts
Rushing First Downs
statID: rushing_firstDowns
description: Rushing first downs
Longest Rush
statID: rushing_longestRush
description: Longest rush
Rush Yards Per Attempt
statID: rushing_yardsPerAttempt
description: Yards per attempt
Rush Yards After Contact
statID: rushing_yardsAfterContact
description: Yards after contact
Rush Two Point Conversions
statID: rushing_twoPointConversions
description: Two point conversions (rushing)
Passing Attempts
statID: passing_attempts
description: Passing attempts
Passing Completions
statID: passing_completions
description: Passing completions
Passing Yards
statID: passing_yards
description: Passing yards
Passing First Downs
statID: passing_firstDowns
description: Passing first downs
Sack Yards Lost
statID: passing_sackYards
description: Yards lost due to sacks
Net Yards
statID: passing_netYards
description: Net passing yards (yards - sack yards)
Interceptions
statID: passing_interceptions
description: Number of interceptions thrown
Longest Completion
statID: passing_longestCompletion
description: Longest completion
Sacks Taken
statID: passing_sacksTaken
description: Sacks taken
Passing Touchdowns
statID: passing_touchdowns
description: Touchdowns thrown
Yards Per Attempt
statID: passing_yardsPerAttempt
description: Yards per attempt
Yards Per Completion
statID: passing_yardsPerCompletion
description: Yards per completion
Passer Rating
statID: passing_passerRating
description: Passer rating
Pass Two Point Conversions
statID: passing_twoPointConversions
description: Two point conversions (passing)
Tackles
statID: defense_tackles
description: Tackles (half point for assisted)
Combined Tackles
statID: defense_combinedTackles
description: Number of combined (solo + assisted) tackles
Solo Tackles
statID: defense_soloTackles
description: Number of solo (unassisted) tackles
Assisted Tackles
statID: defense_assistedTackles
description: Number of assisted tackles
Sacks
statID: defense_sacks
description: Sacks
Tackles for Loss
statID: defense_tacklesForLoss
description: Tackles for loss
Passes Defended
statID: defense_passesDefended
description: Passes defended
QB Hits
statID: defense_qbHits
description: Quarterback hits
Interceptions
statID: defense_interceptions
description: Interceptions recovered
Pick Sixes
statID: defense_pickSixes
description: Interceptions returned for touchdowns
Fumbles Forced
statID: defense_fumblesForced
description: Fumbles forced
Fumbles Recovered
statID: defense_fumblesRecovered
description: Fumbles recovered
Scoop and Scores
statID: defense_scoopAndScores
description: Fumbles returned for touchdowns
Defensive Safeties
statID: defense_safeties
description: Safeties
Kickoff Returns
statID: kickoffReturn_numReturns
description: Kickoffs returned
Kickoff Return Yards
statID: kickoffReturn_yards
description: Kickoff return yards
Kickoff Return Touchdowns
statID: kickoffReturn_touchdowns
description: Kickoff return touchdowns
Longest Kickoff Return
statID: kickoffReturn_longestReturn
description: Longest kickoff return
Kickoff Return Yards Per Return
statID: kickOffReturn_yardsPerReturn
description: Yards per kickoff return
Punt Returns
statID: puntReturn_numReturns
description: Punts returned
Punt Return Yards
statID: puntReturn_yards
description: Punt return yards
Punt Return Touchdowns
statID: puntReturn_touchdowns
description: Punt return touchdowns
Longest Punt Return
statID: puntReturn_longestReturn
description: Longest punt return
Punt Return Yards Per Return
statID: puntReturn_yardsPerReturn
description: Yards per punt return
Punts
statID: punting_numPunts
description: Number of punts
Punting Yards
statID: punting_yards
description: Total punting yards (gross)
Net Punting Yards
statID: punting_netYards
description: Net punting yards (after returns)
Punting Yards Per Punt
statID: punting_yardsPerPunt
description: Average yards per punt
Longest Punt
statID: punting_longestPunt
description: Longest punt
Punts Inside 20
statID: punting_puntsInside20
description: Punts inside the 20 yard line
Punts for Touchback
statID: punting_puntsForTouchback
description: Punts for touchback
Punts for Fair Catch
statID: punting_puntsForFairCatch
description: Punts for fair catch
Blocked Punts
statID: punting_puntsBlocked
description: Number of punt attempts blocked by the other team
Field Goal Attempts
statID: fieldGoals_attempts
description: Field goal attempts
Field Goals Made
statID: fieldGoals_made
description: Field goals made
Field Goal Percentage
statID: fieldGoals_percentMade
description: Field goal percentage
Longest Field Goal Made
statID: fieldGoals_longestMade
description: Longest field goal made
Longest Field Goal Attempt
statID: fieldGoals_longestAttempt
description: Longest field goal attempt
1-19 Yard FGs Made
statID: fieldGoals_1to19YardsMade
description: Number of 1-19 yard field goals made
20-29 Yard FGs Made
statID: fieldGoals_20to29YardsMade
description: Number of 20-29 yard field goals made
30-39 Yard FGs Made
statID: fieldGoals_30to39YardsMade
description: Number of 30-39 yard field goals made
undefined
statID: fieldGoals_40to49YardsMade
description: Number of 40-49 yard field goals made
50+ Yard FGs Made
statID: fieldGoals_50PlusYardsMade
description: Number of 50+ yard field goals made
Field Goal Attempts Blocked
statID: fieldGoals_attemptsBlocked
description: Number of field goal attempts blocked by the other team
Extra Points Made
statID: extraPoints_kicksMade
description: Extra points made
Extra Point Attempts
statID: extraPoints_kickAttempts
description: Extra point attempts
Largest Lead
statID: largestLead
description: Largest lead held during the game
Seconds In Lead
statID: secondsInLead
description: Number of game clock seconds team was winning
Minutes In Lead
statID: minutesInLead
description: Number of game clock minutes team was winning
Longest Scoring Run
statID: longestScoringRun
description: Longest run of unanswered points
Times Tied
statID: timesTied
description: Number of times the game was tied (excluding the start)
Lead Changes
statID: leadChanges
description: Number of times the winning team changed
Basketball
Points
statID: points
description: Points
Blocks
statID: blocks
description: Blocks
Steals
statID: steals
description: Steals
Assists
statID: assists
description: Assists
Rebounds
statID: rebounds
description: Rebounds
Offensive Rebounds
statID: offensiveRebounds
description: Offensive rebounds
Defensive Rebounds
statID: defensiveRebounds
description: Defensive rebounds
Turnovers
statID: turnovers
description: Turnovers committed
Fouls
statID: fouls
description: Fouls committed
Field Goals Made
statID: fieldGoalsMade
description: Field goals made
Field Goals Attempted
statID: fieldGoalsAttempted
description: Field goals attempted
Field Goal Percentage
statID: fieldGoalPercent
description: Field goal shooting percentage
Three Pointers Made
statID: threePointersMade
description: Three pointers made
Three Pointers Attempted
statID: threePointersAttempted
description: Three pointers attempted
Three Pointer Percentage
statID: threePointerPercent
description: Three pointer shooting percentage
Two Pointers Attempted
statID: twoPointersAttempted
description: Two pointers attempted
Two Pointers Made
statID: twoPointersMade
description: Two pointers made
Two Pointer Percentage
statID: twoPointerPercent
description: Two pointer percentage
Free Throws Made
statID: freeThrowsMade
description: Free throws made
Free Throws Attempted
statID: freeThrowsAttempted
description: Free throws attempted
Free Throw Percentage
statID: freeThrowPercent
description: Free throw percentage
Points In The Paint
statID: pointsInPaint
description: Points in the paint
Points Off Turnovers
statID: pointsOffTurnovers
description: Points off of turnovers
Second Chance Points
statID: secondChancePoints
description: Points scored after an offensive rebound
Fast Break Points
statID: fastBreakPoints
description: Fast break points
Seconds Played
statID: secondsPlayed
description: Seconds played
Minutes Played
statID: minutesPlayed
description: Minutes played
Plus/Minus
statID: plusMinus
description: Net score change while on the court
Largest Lead
statID: largestLead
description: Largest lead held during the game
Seconds In Lead
statID: secondsInLead
description: Number of game clock seconds team was winning
Minutes In Lead
statID: minutesInLead
description: Number of game clock minutes team was winning
Longest Scoring Run
statID: longestScoringRun
description: Longest run of unanswered points
Times Tied
statID: timesTied
description: Number of times the game was tied (excluding the start)
Lead Changes
statID: leadChanges
description: Number of times the winning team changed
Hockey
Goals
statID: points
description: Goals scored
Assists
statID: assists
description: Assists
Shots
statID: shots
description: Shots taken
Shots On Goal
statID: shots_onGoal
description: Shots on goal
Hits
statID: hits
description: Hits
Blocked Shots
statID: blockedShots
description: Blocked shots
Penalty Seconds
statID: penaltySeconds
description: Number of seconds spent in the penalty box
Penalty Minutes
statID: penaltyMinutes
description: Number of minutes spent in the penalty box
Giveaways
statID: giveaways
description: Giveaways
Takeaways
statID: takeaways
description: Takeaways
Power Play Count
statID: powerPlay_count
description: Power play count
Short Handed Count
statID: shortHanded_count
description: Short handed count
Power Play Goals
statID: powerPlay_goals
description: Power play goals
Power Play Assists
statID: powerPlay_assists
description: Power play assists
Short Handed Goals
statID: shortHanded_goals
description: Short handed goals
Short Handed Assists
statID: shortHanded_assists
description: Short handed assists
Even Strength Goals
statID: evenStrength_goals
description: Even strength goals
Even Strength Assists
statID: evenStrength_assists
description: Even strength assists
Faceoffs Won
statID: faceOffs_won
description: Faceoffs won
Faceoffs Lost
statID: faceOffs_lost
description: Faceoffs lost
Faceoffs Taken
statID: faceOffs_taken
description: Faceoffs taken
Goals Against
statID: goalie_goalsAgainst
description: Goals against
Saves
statID: goalie_saves
description: Saves
Short Handed Saves
statID: goalie_shortHanded_saves
description: Short handed saves
Even Strength Saves
statID: goalie_evenStrength_saves
description: Even strength saves
Power Play Saves
statID: goalie_powerPlay_saves
description: Power play saves
Shots Against
statID: goalie_shotsAgainst
description: Shots against
Short Handed Shots Against
statID: goalie_shortHanded_shotsAgainst
description: Short handed shots against
Even Strength Shots Against
statID: goalie_evenStrength_shotsAgainst
description: Even strength shots against
Power Play Shots Against
statID: goalie_powerPlay_shotsAgainst
description: Power play shots against
Save Percentage
statID: goalie_savePercent
description: Save percentage
Seconds Played
statID: secondsPlayed
description: Seconds played
Minutes Played
statID: minutesPlayed
description: Minutes played
Plus/Minus
statID: plusMinus
description: Net score change while player was playing
Largest Lead
statID: largestLead
description: Largest lead held during the game
Seconds In Lead
statID: secondsInLead
description: Number of game clock seconds team was winning
Minutes In Lead
statID: minutesInLead
description: Number of game clock minutes team was winning
Longest Scoring Run
statID: longestScoringRun
description: Longest run of unanswered goals
Times Tied
statID: timesTied
description: Number of times the game was tied (excluding the start)
Lead Changes
statID: leadChanges
description: Number of times the winning team changed
Soccer
Goals
statID: points
description: Goals scored
Assists
statID: assists
description: Assists
Shots
statID: shots
description: Shots
Shots On Goal
statID: shots_onGoal
description: Shots on goal
Shots Off Goal
statID: shots_offGoal
description: Shots off goal
Shots Hit Crossbar
statID: shots_hitCrossbar
description: Shots that hit the crossbar
Shots Inside Box
statID: shots_insideBox
description: Shots inside box
Shots Outside Box
statID: shots_outsideBox
description: Shots outside box
Shots Blocked
statID: shots_blocked
description: Shots that were blocked by the opposing team
Touches
statID: touches
description: Touches
Clearances
statID: clearances
description: Clearances
Corner Kicks
statID: cornerKicks
description: Corner kicks
Throw Ins
statID: throwIns
description: Throw-ins
Passes Attempted
statID: passes_attempted
description: Passes attempted
Passes Accurate
statID: passes_accurate
description: Passes accurate
Passes Inaccurate
statID: passes_inaccurate
description: Passes inaccurate
Pass Accuracy
statID: passes_percent
description: Pass accuracy percentage
Long Balls Attempted
statID: longBalls_attempted
description: Long balls attempted
Accurate Long Balls
statID: longBalls_accurate
description: Number of accurate long balls
Inaccurate Long Balls
statID: longBalls_inaccurate
description: Number of inaccurate long balls
Long Ball Accuracy
statID: longBalls_percent
description: Long ball accuracy percentage
Crosses Attempted
statID: crosses_attempted
description: Crosses attempted
Accurate Crosses
statID: crosses_accurate
description: Number of accurate crosses
Inaccurate Crosses
statID: crosses_inaccurate
description: Number of inaccurate crosses
Cross Accuracy
statID: crosses_percent
description: Cross accuracy percentage
Duels Attempted
statID: duels_attempted
description: Number of duels attempted
Duels Won
statID: duels_won
description: Number of duels won
Duels Lost
statID: duels_lost
description: Number of duels lost
Duel Win Percentage
statID: duels_percent
description: Duel win percentage
Aerials Attempted
statID: aerials_attempted
description: Number of aerials attempted
Aerials Won
statID: aerials_won
description: Number of aerials won
Aerials Lost
statID: aerials_lost
description: Number of aerials lost
Aerial Win Percentage
statID: aerials_percent
description: Aerial win percentage
Dribbles Attempted
statID: dribbles_attempted
description: Number of dribbles/take-ons attempted (offense)
Dribbles Won
statID: dribbles_won
description: Number of dribbles/take-ons won (offense)
Dribbles Lost
statID: dribbles_lost
description: Number of dribbles/take-ons lost (offense)
Dribble Win Percentage
statID: dribbles_percent
description: Dribble/take-on win percentage (offense)
Defensive Dribbles Contested
statID: defense_dribbles_contested
description: Number of dribbles/take-ons contested (defense)
Defensive Dribbles Won
statID: defense_dribbles_won
description: Number of dribbles/take-ons won (defense)
Defensive Dribbles Lost
statID: defense_dribbles_lost
description: Number of dribbles/take-ons lost (defense)
Defensive Dribble Win Percentage (Defense)
statID: defense_dribbles_percent
description: Dribble/take-on win percentage (defense)
Tackles
statID: tackles
description: Number of tackles
Interceptions
statID: interceptions
description: Number of interceptions
Blocks
statID: blocks
description: Number of blocked shots
Dispossessed
statID: disposessed
description: Number of times dispossessed
Fouls Drawn
statID: foulsDrawn
description: Number of fouls drawn
Fouls Committed
statID: fouls
description: Number of fouls committed
Offsides
statID: offsides
description: Number of times called for offsides
Free Kicks
statID: freeKicks
description: Number of free kicks
Yellow Cards
statID: yellowCards
description: Number of yellow cards received
Red Cards
statID: redCards
description: Number of red cards received
Penalties Committed
statID: penaltiesCommitted
description: Number of penalties committed (for penalty kicks)
Penalty Kicks Taken
statID: penaltyKicks_taken
description: Number of penalty kicks taken
Penalty Kicks Made
statID: penaltyKicks_made
description: Number of penalty kicks made
Penalty Kicks Missed
statID: penaltyKicks_missed
description: Number of penalty kicks missed
Penalty Kick Accuracy
statID: penaltyKicks_percent
description: Penalty kick accuracy percentage
Goals Against
statID: goalie_goalsAgainst
description: Number of goals allowed
Saves
statID: goalie_saves
description: Number of saves
Shots Against
statID: goalie_shotsAgainst
description: Number of shots against
Save Percentage
statID: goalie_savePercent
description: Goalie save percentage
Penalty Kicks Saved
statID: goalie_penaltyKicksSaved
description: Number of penalty kicks saved
Inside Box Saves
statID: goalie_insideBox_saves
description: Number of saves inside the box
Goal Kicks
statID: goalie_goalKicks
description: Number of goal kicks
Seconds Played
statID: secondsPlayed
description: Seconds played
Minutes Played
statID: minutesPlayed
description: Minutes played
Plus/Minus
statID: plusMinus
description: Net score change while player was playing
Player Rating
statID: playerRating
description: Player rating
Largest Lead
statID: largestLead
description: Largest lead held during the game
Seconds In Lead
statID: secondsInLead
description: Number of game clock seconds team was winning
Minutes In Lead
statID: minutesInLead
description: Number of game clock minutes team was winning
Possession Percentage
statID: possessionPercent
description: Percentage of time the team had possession of the ball
Longest Scoring Run
statID: longestScoringRun
description: Longest run of unanswered goals
Times Tied
statID: timesTied
description: Number of times the game was tied (excluding the start)
Lead Changes
statID: leadChanges
description: Number of times the winning team changed
Handball
Goals
statID: points
description: Goals scored
Tennis
Sets
statID: points
description: Goals scored
Games
statID: games
description: Games won
Golf
To Par
statID: points
description: To Par Score