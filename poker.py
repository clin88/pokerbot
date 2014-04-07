from enum import Enum
from collections import OrderedDict
import random

"""
Player State tracked with OrderedDict <- this also describes turn info
round of betting?
dealer
whose turn is it?
"""

class Round:
    """Controls each round of betting.
    """
    @staticmethod
    def turns(players, start):
        """
            players :: List of playerinfos
            yields  :: player
        """
        # TODO: What are the edge cases for everyone folding/1 remaining?
        while True:
            for player in players:
                if not player['folded']:
                    yield player


    def __init__(self, players, blind, dealer):
        # TODO:
        #if len(players) < 3:
        #    raise Exception("Not enough players, dummy.")

        #self.pot = 0
        self.blind = blind
        self.highbet = blind

        deck = Card.shuffled_deck()

        # draw community cards
        self.community = [deck.pop() for _ in range(5)]

        dealer_i = players.index(dealer)
        bigblind = players[dealer_i + 1]
        smallblind = players[dealer_i + 2]

        self.players = []
        for player in players:
            new_player = {
                'name': player,
                'hand': [deck.pop(), deck.pop()],
                'folded': False,
                'bet': 0
            }
            if player == bigblind:
                new_player['bet'] = blind
            elif player == smallblind:
                new_player['bet'] = blind / 2

            self.players.append(new_player)

        self._turns = Round.turns(self.players)
        self.turn = next(self._turns)

    def bet(self, pname, decision, amount=None):
        curplayer = self.turn
        if pname != curplayer['name']:
            raise Exception("Stop betting out of turn!")

        if decision == Decision.fold:
            curplayer['folded'] = True
        elif decision == Decision.check:
            # TODO: Some indicator that a turn has been passed, so we can tell
            # if everybody checks
            pass
        elif decision == Decision.bet:
            total = curplayer['bet'] + amount
            if total == self.highest:
                bet_type = BetResult.call
            elif total >= 2 * self.highbet:
                bet_type = BetResult.raisebet
            else:
                # TODO: Indicate unacceptable bet
                return {'result': BetResult.invalid_bet}

            self.highbet = total
            curplayer['bet'] = total
            #self.pot += amount

            self.turn = next(self._turns, False)
            if self.turn is False:
                # TODO: Indicate winner, since only one player remains unfolded.
                return {'result': BetResult.winner, 'winner': _}

            # TODO: Indicate call.
            # TODO: Indicate raise
            return {'result': bet_type}

class BetResult(Enum):
    call = "call"
    raisebet = "raise"
    invalid_bet = "invalid bet"
    winner = "winner"

class Decision(Enum):
    fold = 'fold'
    bet = 'bet'
    check = 'check'

class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number

    def __str__(self):
        if self.number == 11:
            n = "J"
        elif self.number == 12:
            n = "Q"
        elif self.number == 13:
            n = "K"
        elif self.number == 1:
            n = "A"
        else:
            n = self.number

        return "{!s}{!s}".format(n, self.suit)

    def __repr__(self):
        return str(self)

    @staticmethod
    def shuffled_deck():
        deck = []
        for suit in Suits:
            for number in range(1, 14):
                deck.append(Card(suit, number))
 
        random.shuffle(deck)
        return deck

class Suits(Enum):
    """
    Unicode hex numbers for

    spade: 2660, heart: 2665, diamond: 2666, club: 2663
    """
    heart = "\u2665"
    spade = "\u2660"
    diamond = "\u2666"
    club = "\u2663"

    def __str__(self):
        if self == Suits.heart:
            return "\u2665"
        elif self == Suits.spade:
            return "\u2660"
        elif self == Suits.diamond:
            return "\u2666"
        elif self == Suits.club:
            return "\u2663"

if __name__ == "__main__":
    print(hand.deck)
    print(hand.players)
    print(hand.community)

    players = {
        "sean": 150,
        "r0ml": 100,
        "fred": 999
    }

    hand = Game(len(players), 10)
