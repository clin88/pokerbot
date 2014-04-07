from enum import Enum
from collections import OrderedDict
from itertools import chain, cycle, product
import random

"""
Player State tracked with OrderedDict <- this also describes turn info
round of betting?
dealer
whose turn is it?
"""

class Game:
    def __init__(self, players):
        deck = Card.shuffled_deck()

        self.community = [deck.pop() for _ in range(5)]
        self.players = []
        for player in players:
            self.players.append({
                'name': player,
                'hand': [deck.pop(), deck.pop()]
            })

        self.pot = 0

class Round:
    """Controls each round of betting.
    """
    def turns(self, players, start):
        """
            players :: List of playerinfos
            yields  :: player
        """
        # TODO: What are the edge cases for everyone folding/1 remaining?
        last_highbet = self.highbet
        last_raiser = players[start-1]
        round_ = cycle(players[start:] + players[:start])
        for player in round_:
            if self.highbet >
            if player['folded']:
                continue

            if self.highbet > last_highbet:


            if player == last_raiser:
                return

            yield player



        while True:
            prev_bet = self.highbet
            for player in cycle:
                if last_turn == player:
                    return
                if player['folded']:
                    continue

                # last raiser
                if all(folded or athighbet):
                    return
                last_turn = player
                yield player

            # completed one round of betting with no further raises, continue
            if self.highbet == prev_bet:
                return


    def __init__(self, players, blind, dealer):
        # TODO:
        #if len(players) < 3:
        #    raise Exception("Not enough players, dummy.")

        self.blind = blind
        self.highbet = blind

        # 3 players, a, b, c
        # dealer = 1
        # bb = 2 % 3 = 2
        # sb = a
        # start = b
        player_count = len(players)
        dealer = players.index(dealer)
        bigblind = (dealer + 1) % player_count
        smallblind = (dealer + 2) % player_count
        start = (dealer + 3) % player_count

        self.players = []
        for player in players:
            new_player = {
                'name': player,
                'bet': 0
            }
            if player == players[bigblind]:
                new_player['bet'] = blind
            elif player == players[smallblind]:
                new_player['bet'] = blind / 2

            self.players.append(new_player)

        self._turns = Round.turns(self.players, start=start)
        self.turn = next(self._turns)

    def bet(self, pname, decision, amount=None):
        curplayer = self.turn
        if pname != curplayer['name']:
            print("Stop betting out of turn!")
            #raise Exception("Stop betting out of turn!")



        if decision == Decision.fold:
            curplayer['folded'] = True
            self.turn = next(self._turns)
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
                return {'result': BetResult.invalid_bet}

            self.highbet = total
            curplayer['bet'] = total
            self.turn = next(self._turns, False)

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
        elif self.number == 14:
            n = "A"
        else:
            n = self.number

        return "{!s}{!s}".format(n, self.suit)

    def __repr__(self):
        return str(self)

    @classmethod
    def shuffled_deck(cls):
        deck = []
        for suit, number in product(Suits, range(1, 14)):
            deck.append(cls(suit, number))
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

test_round = Round(['a', 'b', 'c'], 10, 'b')
