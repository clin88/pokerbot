from itertools import combinations
from functools import total_ordering
from collections import Counter
from operator import itemgetter, sub
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
@total_ordering
class CombinedHand(object):
  def __init__(self, holeCards, communityCards = []):
    self.communityCards = communityCards
    self.holeCards = holeCards
    
  def winHand(self):
    self.combinedCards = holeCards + communityCards  
    return max(map(FiveCardHand, combinations(combinedCards, 5)))
  
  def __eq__(self, other):
    return self.winHand() == other.winHand()
  def __lt__(self, other): 
    return self.winHand() < other.winHand()


    

@total_ordering
class FiveCardHand(object):
  def __init__(self,cards):
    self.cards = cards
  def __eq__(self, other):
    return self.valueArray() == other.valueArray()
  def __lt__(self, other): 
    return self.valueArray() < other.valueArray()

  def SuitIterator(self):
    def SuitGeneratorClosure():
      for card in self.cards:
        yield card.suit
    return SuitGeneratorClosure()

  def RankIterator(self):
    def RankGeneratorClosure():
      for card in self.cards:
        yield card.number
    return RankGeneratorClosure()

  def cardValueTuples(self):
    rank, repeat = zip(*sorted(Counter(self.RankIterator()).most_common(), key=itemgetter(1,0), reverse = True))
    return list(repeat + rank)
  
  def valueArray(self):
    return self.specialHands() + self.cardValueTuples()
  
  def specialHands(self):
    if self.isFlush():
      if self.isStraight():
        return [5,2]
      elif self.isBicycle():
        return [5,1]
      else:
        return [3,1,4]
    if self.isStraight():
      return [3,1,3]
    if self.isBicycle():
      return [3,1,2]
    return []

  def isStraight(self):
    sortedCards = sorted(self.RankIterator())
    return(list(map(sub,sortedCards[1:5], sortedCards[0:4]))) == [1,1,1,1]
 
  def isBicycle(self):
    sortedCards = sorted(self.RankIterator())
    return sortedCards == [2, 3, 4, 5, 14]

  def isFlush(self):
    
    #all(map(self.cards[0].suit.__eq__,self.cards.suits # as an iterable))
    
    aSuit = self.cards[0].suit
    for card in self.cards:
      if card.suit != aSuit:
        return False
    return True

#class 

if __name__ == '__main__':
  class Card(object):
    def __init__(self,rank,suit):
      self.number = rank
      self.suit = suit

  hand1 = FiveCardHand([Card(3,1), Card(2, 1), Card(14, 1), Card(4, 3), Card(5, 4)])
  hand2 = FiveCardHand([Card(3,1), Card(7, 1), Card(14, 1), Card(4, 3), Card(5, 4)])
  print(hand1>hand2)
