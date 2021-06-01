from abc import ABC, abstractmethod
import random
import sys

class Contestant(ABC):
    @abstractmethod
    def __init__(self):
        self._hand      = []
        self._score     = 0
        self._stand     = False
        self._bustorwin = False

    @abstractmethod
    def contestantStatus(self):
        pass

    @abstractmethod
    def displayHand(self):
        pass

    def updateContestantStats(self, cardDrawn, pointsDict):
        # add recently drawn card to contestant hand property
        self._hand.append(cardDrawn)

        # calculate total score assuming all Aces are worth 1, and find number of Aces in hand
        numAces      = 0
        updatedScore = 0

        for i in range(len(self._hand)):
            if self._hand[i] == 'A':
                numAces      += 1
                updatedScore += 1
            else:
                updatedScore += pointsDict[self._hand[i]] 
        
        # if no Aces, simply update contestant score. Else, see if it is feasible to make one Ace worth 11 points
        if numAces == 0:
            self._score = updatedScore
        else:
            # this determines if there are enough points available to convert a single Ace value from 1 to 11
            makeOneAceWorthEleven = True if (21 - updatedScore) >= 10 else False

            # if enough points are available, adds 10 to total score (this simulates converting an Aces' value from 1 to 11)
            if makeOneAceWorthEleven:
                updatedScore += 10

            self._score = updatedScore

class Player(Contestant):
    def __init__(self):
        super().__init__()
    
    def contestantStatus(self):
        # player gets score > 21 (Bust) or == 21 (Blackjack!)
        if self._score >= 21:
            self._bustorwin = True
    
    def displayHand(self):
        # simply displays the players hand
        print("Player has:", *self._hand, "=", self._score)

    def prompt(self):
        # returns None for any other input besides H or S
        prompt = "Would you like to (H)it or (S)tand? "
        command = input(prompt)
        
        if command == 'H':
            return 'H'
        elif command == 'S':
            return 'S'
        else:
            return None

class Dealer(Contestant):
    def __init__(self):
        super().__init__()
    
    def contestantStatus(self):
        # this condition states when the automated dealer has achieved its objective (decides to stand)
        if self._score >= 17 and self._score < 21:
            self._stand = True

        # dealer gets score > 21 (Bust) or == 21 (Blackjack!)
        if self._score >= 21:
            self._bustorwin = True

    def displayHand(self, player):
        # if the player did not stand, the dealers hand is not fully shown. 
        # if it is the dealers turn, the player must have stood
        if player._stand == False:
            print("\nDealer has:", self._hand[0], "? = ?")
        else:
            print("Dealer has:", *self._hand, "=", self._score)

class DeckOfCards:
    # creates one dictionary for the card counts and another for each cards value
    def __init__(self):
        self.deck = {
            '2':4, '3':4, '4':4, 
            '5':4, '6':4, '7':4, 
            '8':4, '9':4, '10':4, 
            'J':4, 'Q':4, 'K':4,
            'A':4
        }
        self.points = {
            '2':2, '3':3, '4':4, 
            '5':5, '6':6, '7':7, 
            '8':8, '9':9, '10':10, 
            'J':10, 'Q':10, 'K':10,
            'A':[1,11]
        }
    
    def drawRandomCard(self, contestant):
        cardDrawn = None
        
        while cardDrawn == None:
            draw = random.choice(list(self.deck.items()))
            if draw[1] == 0:
                # if randomizer generates card with 0 instances in deck, draw again
                continue
            else:
                cardDrawn = draw[0] 

                # update deck statistics
                self.deck[cardDrawn] -= 1

        # once valid card is drawn, update contestant hand and score properties appropriately
        contestant.updateContestantStats(cardDrawn, self.points)
        return cardDrawn
    
class Game:
    def __init__(self):
        self.player      = Player()
        self.dealer      = Dealer()
        self.deck        = DeckOfCards()

    def startGame(self):
        # this method is used to start the entire game
        # notice how the functions called within govern the general flow of the game

        self.initializeGame()
        self.playersTurn()
        self.dealersTurn()
        self.evaluateWinner()

    def initializeGame(self):
        # initialize hand for player by drawing 2 random cards
        playerCard1 = self.deck.drawRandomCard(self.player)
        playerCard2 = self.deck.drawRandomCard(self.player)

        # initialize hand for dealer by drawing 2 random cards
        dealerCard1 = self.deck.drawRandomCard(self.dealer)
        dealerCard2 = self.deck.drawRandomCard(self.dealer)

    def playersTurn(self):

        # this loop will always assess whether the player has stood
        while self.player._stand == False:
            
            # displays hands of both dealer and player
            # (remember: dealer must know whether player has stood)
            self.dealer.displayHand(self.player) 
            self.player.displayHand()
            
            # evaluates whether player has bust or blackjacked
            self.player.contestantStatus()
            
            # if the player status has changed to bust or blackjack, this flow routes to game end
            if self.player._bustorwin == True:
                self.evaluateWinner()

            # if the player has not bust or blackjacked, this prompts the user for the next move
            self.userAction()
            
    def dealersTurn(self):

        # this loop will always assess whether the dealer has stood
        while self.dealer._stand == False:
            # (remember: dealer must know whether player has stood)
            self.dealer.displayHand(self.player)

            # evaluates whether dealer has bust, blackjacked, or achieved its target score [17,21]
            # activates appropriate property flag as necessary
            self.dealer.contestantStatus()

            # based on the property flags, this piece of logic governs the games next move
            if self.dealer._bustorwin == True:
                self.evaluateWinner()
            elif self.dealer._stand == True:
                print("\nDealer stands with:", *self.dealer._hand, "=", self.dealer._score)
                self.evaluateWinner()
            else:
                print("Dealer hits")
                self.deck.drawRandomCard(self.dealer)

    def userAction(self):

        command = self.player.prompt()
        if command == 'H':
            drawn = self.deck.drawRandomCard(self.player)
        elif command == 'S':
            self.player._stand = True
            print("\nPlayer stands with:", *self.player._hand, "=", self.player._score, "\n")
        else:
            print("Invalid command, please try again!")

    def finalScore(self):
        # just a function to produce the final scores and hands of both contestants
        finalScore = ["Player Hand:", *self.player._hand, "=", self.player._score, "| Dealer Hand:", *self.dealer._hand, "=", self.dealer._score]
        print(*finalScore)

    def evaluateWinner(self):
        # both contestants achieve same score (includes dual blackjack)
        if self.player._score == self.dealer._score:
            print("\nTie Game!")
        
        # player busts
        elif self.player._score > 21:
            print("\nPlayer busts with {}\nDealer wins!".format(self.player._score))
        
        # dealer busts
        elif self.dealer._score > 21:
            print("\nDealer busts with {}\nPlayer wins!".format(self.dealer._score))

        # player blackjack
        elif self.player._score == 21:
            print("\nPlayer wins!\nBlackjack!")
        
        # dealer blackjack
        elif self.dealer._score == 21:
            print("\nDealer wins!\nBlackjack!")
        
        # player wins
        elif self.player._score > self.dealer._score:
            print("\nPlayer Wins!")

        # dealer wins
        elif self.player._score < self.dealer._score:
            print("\nDealer Wins!")
        
        # print contestants' hands with scores
        self.finalScore()
        sys.exit()

if __name__ == '__main__':
    Game().startGame()










