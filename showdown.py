from itertools import combinations
from functools import total_ordering, reduce
from collections import Counter
from operator import sub, eq, itemgetter


"""
#Here lies a reimplementation of something already in itertools.

def createChooseLookupTable(n,m):
  if m > n:
    raise ArithmeticError("Cannot choose for m > n")
  firstList = [[[]]]
  for i in range(n):
    firstList.append([])
    for elem in firstList[i]:
      elemTrues = sum(elem)
      elemFalses = len(elem) - elemTrues 
      if elemTrues < m:
        firstList[i+1].append(elem + [True])
      if elemFalses < n - m:
        firstList[i+1].append(elem + [False])
  return firstList[n]

print(createChooseLookupTable(7,5))   
"""


def best_hand(hand):
    hands = map(FiveCardHand, combinations(hand, 5))
    return max(hands)

@total_ordering
class FiveCardHand(object):
    def __init__(self, cards):
        self.cards = cards
        self.ranks = sorted([card.number for card in self.cards])
        self.suits = sorted([card.suit for card in self.cards])
        self.handValue = self.valueArray()
           
    def __eq__(self, other):
        return self.valueArray() == other.valueArray()

    def __lt__(self, other):
        return self.valueArray() < other.valueArray()
    
    def handName(self):
        if self.handValue[0] == 5:
            return "Straight Flush"
        if self.handValue[0] == 4:
            return "Four of a Kind"
        if self.handValue[0] == 3:
            if self.handValue[1] == 2:
                return "Full House"
            if self.handValue[2] == 4:
                return "Flush"
            if self.handValue[2] == 3 or self.handValue[2] == 2:
                return "Straight"
            else:
                return "Three of a Kind"
        if self.handValue[0] == 2:
            if self.handValue[1] == 2:
                return "Two Pair"
            else:
                return "Pair"
        return "High Card"

    def valueArray(self):
        rank, repeat = zip(*Counter(self.ranks).most_common())
        #rank, repeat = zip(*sorted(Counter(self.ranks).most_common(), key=itemgetter(1, 0), reverse=True))
        print(repeat + rank)
        return self.specialHands() + (repeat + rank)

    def specialHands(self):
        if self.isFlush():
            if self.isStraight():
                return 5, 2
            elif self.isBicycle():
                return 5, 1
            else:
                # Regular flush
                return 3, 1, 4
        if self.isStraight():
            return 3, 1, 3
        if self.isBicycle():
            return 3, 1, 2
        # TODO: Three of a kind?
        return ()

    def isStraight(self):
        steps = map(sub, self.ranks[1:5], self.ranks[0:4])
        return list(steps) == [1, 1, 1, 1]

    def isBicycle(self):
        return self.ranks == [2, 3, 4, 5, 14]

    def isFlush(self):
        return reduce(eq, self.suits)

#class 

if __name__ == '__main__':
    class Card(object):
        def __init__(self, rank, suit):
            self.number = rank
            self.suit = suit

    hand1 = FiveCardHand([Card(2, 1), Card(2, 3), Card(14, 1), Card(5, 3), Card(5, 4)])
    hand2 = FiveCardHand([Card(4, 1), Card(4, 1), Card(14, 1), Card(3, 3), Card(3, 4)])
    print(hand1 > hand2)

