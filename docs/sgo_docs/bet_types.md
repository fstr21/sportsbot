Bet Types
All odds objects include a betTypeID and 2 corresponding sideIDs. There are 6 different betTypeIDs and 12 sideIDs. Below is a breakdown of each.

Moneyline
betTypeID: ml
description A wager on the winner of an event where a draw results in a push
Sides:
Home
sideID: home
description: The home team
Away
sideID: away
description: The away team
3-Way Moneyline
betTypeID: ml3way
description A 3-way wager on the winner of an event where a draw is a separate/non-push outcome
Sides:
Home
sideID: home
description: This side wins only if the home team wins
Away
sideID: away
description: This side wins only if the away team wins
Draw
sideID: home
description: This side wins only if the score results in a draw.
Away or Draw (Not Home)
sideID: away+draw
description: This side wins if the away team wins or if the score results in a draw. It’s the opponent/opposite side of a bet on the home team.
Home or Draw (Not Away)
sideID: home+draw
description: This side wins if the home team wins or if the score results in a draw. It’s the opponent/opposite side of a bet on the away team.
Not a Draw
sideID: not_draw
description: This side wins if the score does not result in a draw. In other words, this side wins if either the home or the away team wins. It’s the opponent/opposite side of a bet on a draw.
Spread
betTypeID: sp
description A wager on the winner of an event using a specified handicap
Sides:
Home
sideID: home
description: The home team
Away
sideID: away
description: The away team
Over/Under
betTypeID: ou
description A wager on whether the final value of a stat is over or under the given value
Sides:
Over
sideID: over
description: Final value is over the specified value
Under
sideID: under
description: Final value is under the specified value
Even/Odd
betTypeID: eo
description A wager on whether the final value of a stat is even or odd
Sides:
Even
sideID: even
description: Final value is even
Odd
sideID: odd
description: Final value is odd
Yes/No
betTypeID: yn
description A wager on a yes or no question
Sides:
Yes
sideID: yes
description: The answer to the question is yes
No
sideID: no
description: The answer to the question is no
Prop Bet
betTypeID: prop
description A wager on a sports prop
Sides:
Option 1
sideID: side1
description: One side of the prop
Option 2
sideID: side2
description: The opposing side of the prop


