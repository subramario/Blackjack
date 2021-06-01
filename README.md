# Blackjack
Simple OOP Blackjack game developed using Python 

## Brief
Blackjack is a card game. For our purposes, we'll use a single standard 52-card deck. This deck has:

* **"Number Cards"** with a face value of 2-10, worth the number on the card
* **"Face Cards"** (King, Queen, Jack), each worth 10 points
* **"Aces"** worth 1 or 11 points

## Definitions
* **Hand:** a collection of cards that a player owns for the duration of the game.
* **Hit:** add another card to a player's hand
* **Stand:** add no more cards to a player's hand; stop playing a turn; proceed to the next phase of the game.
* **Bust:** more than 21 points in a player's hand; the player's turn is instantly over; the player has lost.

## Winning
* Each player's objective is to get as close to 21 points as possible without going over.
* The human wants to outscore the dealer, despite not knowing the dealer's score.
* The dealer plays by a simple rule: hit until the hand's score is greater than or equal to 17 ("stand on 17").
* For our game there is no betting, no splitting, no doubling down. This is a simple game.

## Ace Scoring
* At any time, there is an optimal value for each Ace which can be worth either 1 or 11 points
* The value of Aces in a contestants hand must be confiugred to produce the greatest non-bustable value 
* _Note: any hand with more than one Ace as an 11 will be a bust_
```
Say you have the following hand: 
A 8 A = 11 + 8 + 1 = 20

When you draw another card, watch how the value of each Ace changes: 
A 8 A 10 = 1 + 8 + 1 + 10 = 20
```

## Gameplay Overview
* Deal initial cards (two cards to each player)
*  Display initial hands (hiding dealer's second card and score)
*  Prompt user (Hit or Stand?)
    * Hit: add card to hand (check if busted)
    * Stand: end turn
    * Show updated hand and value
    * Repeat until player has stood, won (score == 21), or busted (score > 21)
* Dealer plays (if player has neither busted nor won)
    * Print dealer's full hand, score
    * Dealer keeps hitting until score >= 17
* Decide and report the winner, including hands and scores where relevant

## Example Output
```
Dealer has: 9 ? = ?
Player has: K Q = 20
Would you like to (H)it or (S)tand? S

Player stands with: K Q = 20 

Dealer has: 9 4 = 13
Dealer hits
Dealer has: 9 4 2 = 15
Dealer hits
Dealer has: 9 4 2 K = 25

Dealer busts with 25
Player wins!
Player Hand: K Q = 20 | Dealer Hand: 9 4 2 K = 25
```

