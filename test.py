import unittest
from unittest.mock import patch
import sys

from blackjack import *

class TestDeck(unittest.TestCase):
    def setUp(self):
        self.deck   = DeckOfCards()
        self.player = Player()
        self.dealer = Dealer()
    
    def testDraw(self):
        # Tests whether the card count of the deck is decremented appropriately after a randomized draw
        drawn_1 = self.deck.drawRandomCard(self.player)
        drawn_2 = self.deck.drawRandomCard(self.dealer)

        if drawn_1 == drawn_2:
            self.assertEqual(self.deck.deck[drawn_1], 2)
        else:
            self.assertEqual(self.deck.deck[drawn_1], 3)
            self.assertEqual(self.deck.deck[drawn_2], 3) 

    def testOptimalAceScoringExample1(self):
        # Example #1 in Freenome Guide under section "The intricacies of Ace scoring" 
        self.player._hand = ['8']
        self.player.updateContestantStats('A', self.deck.points)
        self.assertEqual(self.player._score, 19)

    def testOptimalAceScoringExample2(self):
        # Example #2 in Freenome Guide under section "The intricacies of Ace scoring" 
        self.player._hand = ['8','A']
        self.player.updateContestantStats('7', self.deck.points)
        self.assertEqual(self.player._score, 16)

    def testOptimalAceScoringExample3(self):
        # Example #3 in Freenome Guide under section "The intricacies of Ace scoring" 
        self.player._hand = ['A']
        self.player.updateContestantStats('A', self.deck.points)
        self.assertEqual(self.player._score, 12)
    
    def testOptimalAceScoringExample4(self):
        # Example #4 in Freenome Guide under section "The intricacies of Ace scoring" 
        self.player._hand = ['A', 'A']
        self.player.updateContestantStats('A', self.deck.points)
        self.assertEqual(self.player._score, 13)

    def testOptimalAceScoring(self):
        # Tests scoring algorithm in scenario when a contestant draws all 4 Aces in a row 
        
        # If this scenario occurs, the score should update as shown in expectedScores
        # Each Ace should score optimally, meaning it must produce the greatest non-busting value
        # This also shows the scoring algorithm will never produce two Aces each worth 11 points
        expectedScores = [11,12,13,14]
        for i in range(4):
            self.player.updateContestantStats('A', self.deck.points)
            self.assertEqual(self.player._score, expectedScores[i])

    def testOptimalAceScoring2(self):
        # Set player hand, then simulate drawing an Ace
        self.player._hand = ['10']
        self.player.updateContestantStats('A', self.deck.points)

        # Tests if scoring algorithm will choose value of 11 for Ace to produce Blackjack!
        self.assertEqual(self.player._score, 21)
        
    def testOptimalAceScoring3(self):
        # Set player hand, then simulate drawing an Ace
        self.player._hand = ['A','A','A','A','Q']
        self.player.updateContestantStats('5', self.deck.points)
        self.assertEqual(self.player._score, 19)
    
    def testOptimalAceScoring4(self):
        # Set player hand, then simulate drawing an Ace
        self.player._hand = ['A','5']
        self.player.updateContestantStats('A', self.deck.points)
        self.assertEqual(self.player._score, 17)

    def testOptimalAceScoring5(self):
        # Set player hand, then simulate drawing an Ace
        self.player._hand = ['A','5','A']
        self.player.updateContestantStats('10', self.deck.points)
        self.assertEqual(self.player._score, 17)

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.deck   = DeckOfCards()
        self.player = Player()
        self.dealer = Dealer()
    
    inputs = ['H','S','ERRONEOUS', 4, 5.67, [2], (4)]
    @patch('builtins.input', side_effect=inputs)
    def testPrompt(self, mock_input):
        # Tests whether the prompt function handles erroneous input appropriately
        acceptable1   = self.player.prompt()
        acceptable2   = self.player.prompt()

        invalidString = self.player.prompt()
        invalidInt    = self.player.prompt()
        invalidFloat  = self.player.prompt()
        invalidList   = self.player.prompt()  

        self.assertEqual(acceptable1, 'H')
        self.assertEqual(acceptable2, 'S')

        self.assertEqual(invalidString, None)
        self.assertEqual(invalidInt, None)
        self.assertEqual(invalidFloat, None)
        self.assertEqual(invalidList, None)
    
    def testStatsUpdate(self):
        # Tests whether contestant stats such as hand and score are updated properly
        drawn_1 = self.deck.drawRandomCard(self.player)
        drawn_2 = self.deck.drawRandomCard(self.dealer)

        # Tests whether the hand property has been updated with one card
        self.assertEqual(len(self.player._hand), 1)
        self.assertEqual(len(self.dealer._hand), 1)

        # Tests whether the score property is updated appropriately
        if drawn_1 == 'A' and drawn_2 == 'A':
            self.assertEqual(self.player._score, 11)
            self.assertEqual(self.dealer._score, 11)
        elif drawn_1 == 'A':
            self.assertEqual(self.player._score, 11)
        elif drawn_2 == 'A':
            self.assertEqual(self.dealer._score, 11)
        else:
            self.assertEqual(self.player._score, self.deck.points[drawn_1])
            self.assertEqual(self.dealer._score, self.deck.points[drawn_2])

    def testBustOrWin(self):        
        # Tests whether the bustorwin flag is activated appropriately 

        # Greatest number of cards which sum to 21? [2]*4 + [3]*3 + [A]*4 = 21
        # After drawing 11 random cards, you would at least score 21 (but most likely score way over)
        for i in range(11):
            self.deck.drawRandomCard(self.player)

        self.player.contestantStatus()
        self.assertGreaterEqual(self.player._score, 21)
        self.assertEqual(self.player._bustorwin, True)

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def testInitializeObjects(self):
        # Tests whether the game object successfully initializes dealer, player and deck objects
        self.assertTrue(self.game.player)
        self.assertTrue(self.game.dealer)
        self.assertTrue(self.game.deck)

    def testInitializeHands(self):
        # Tests whether the hands and scores for both contestants are initialized properly
        self.game.initializeGame()

        # Tests whether exactly two cards are drawn for both player and dealer at start of game
        self.assertEqual(len(self.game.player._hand),2)
        self.assertEqual(len(self.game.dealer._hand),2)

        # Tests whether score has been updated to reflect initial cards drawn at start of game
        self.assertGreater(self.game.player._score, 0)
        self.assertGreater(self.game.dealer._score, 0)

if __name__ == '__main__':
    unittest.main()