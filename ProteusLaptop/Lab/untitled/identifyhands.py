from collections import namedtuple



# rank of the type
typeRank = { 'HighCard':     1,
             'OnePair':      2,
             'TwoPairs':     3,
             '3ofakind':     4,
             'straight':     5,
             'flush':        6,
             'fullhouse':    7,
             '4ofakind':     8,
             'straightflush':9}

Type =     { 'HighCard':     1,
             'OnePair':      2,
             'TwoPairs':     3,
             '3ofakind':     4,
             'straight':     5,
             'flush':        6,
             'fullhouse':    7,
             '4ofakind':     8,
             'straightflush':9}


# strength of each type
handRank = { '2':1,
             '3':2,
             '4':3,
             '5':4,
             '6':5,
             '7':6,
             '8':7,
             '9':8,
             'T':9,
             'J':10,
             'Q':11,
             'K':12,
             'A':13}

Rank =     { '2':1,
             '3':2,
             '4':3,
             '5':4,
             '6':5,
             '7':6,
             '8':7,
             '9':8,
             'T':9,
             'J':10,
             'Q':11,
             'K':12,
             'A':13}


class Card(namedtuple('Card', 'face, suit')):
    def __repr__(self):
        return ''.join(self)
 
 
suit = 'h d c s'.split()
# ordered strings of faces
faces   = '2 3 4 5 6 7 8 9 T J Q K A'
lowaces = 'A 2 3 4 5 6 7 8 9 T J Q K'
# faces as lists
face   = faces.split()
lowace = lowaces.split()
 
 
def straightflush(hand):
    f,fs = ( (lowace, lowaces) if any(card.face == '2' for card in hand)
             else (face, faces) )
    ordered = sorted(hand, key=lambda card: (f.index(card.face), card.suit))
    first, rest = ordered[0], ordered[1:]
    if ( all(card.suit == first.suit for card in rest) and
         ' '.join(card.face for card in ordered) in fs ):
        return 'straightflush', ordered[-1].face
    return False
 
def fourofakind(hand):
    allfaces = [f for f,s in hand]
    allftypes = set(allfaces)
    if len(allftypes) != 2:
        return False
    for f in allftypes:
        if allfaces.count(f) == 4:
            allftypes.remove(f)
            return '4ofakind', [f, allftypes.pop()]
    else:
        return False
 
def fullhouse(hand):
    allfaces = [f for f,s in hand]
    allftypes = set(allfaces)
    if len(allftypes) != 2:
        return False
    for f in allftypes:
        if allfaces.count(f) == 3:
            allftypes.remove(f)
            return 'fullhouse', [f, allftypes.pop()]
    else:
        return False
 
def flush(hand):
    allstypes = {s for f, s in hand}
    if len(allstypes) == 1:
        allfaces = [f for f,s in hand]
        return 'flush', sorted(allfaces,
                               key=lambda f: face.index(f),
                               reverse=True)
    return False
 
def straight(hand):
    f,fs = ( (lowace, lowaces) if any(card.face == '2' for card in hand)
             else (face, faces) )
    ordered = sorted(hand, key=lambda card: (f.index(card.face), card.suit))
    first, rest = ordered[0], ordered[1:]
    if ' '.join(card.face for card in ordered) in fs:
        return 'straight', ordered[-1].face
    return False
 
def threeofakind(hand):
    allfaces = [f for f,s in hand]
    allftypes = set(allfaces)
    if len(allftypes) <= 2:
        return False
    for f in allftypes:
        if allfaces.count(f) == 3:
            allftypes.remove(f)
            return ('3ofakind', [f] +
                     sorted(allftypes,
                            key=lambda f: face.index(f),
                            reverse=True))
    else:
        return False
 
def twopair(hand):
    allfaces = [f for f,s in hand]
    allftypes = set(allfaces)
    pairs = [f for f in allftypes if allfaces.count(f) == 2]
    if len(pairs) != 2:
        return False
    p0, p1 = pairs
    other = [(allftypes - set(pairs)).pop()]
    return 'TwoPairs', pairs + other if face.index(p0) > face.index(p1) else pairs[::-1] + other
 
def onepair(hand):
    allfaces = [f for f,s in hand]
    allftypes = set(allfaces)
    pairs = [f for f in allftypes if allfaces.count(f) == 2]
    if len(pairs) != 1:
        return False
    allftypes.remove(pairs[0])
    return 'OnePair', pairs + sorted(allftypes,
                                      key=lambda f: face.index(f),
                                      reverse=True)
 
def highcard(hand):
    allfaces = [f for f,s in hand]
    return 'HighCard', sorted(allfaces,
                               key=lambda f: face.index(f),
                               reverse=True)
 
handrankorder =  (straightflush, fourofakind, fullhouse,
                  flush, straight, threeofakind,
                  twopair, onepair, highcard)
 
def rank(cards):
    hand = handy(cards)
    for ranker in handrankorder:
        rank = ranker(hand)
        if rank:
            break
    assert rank, "Invalid: Failed to rank cards: %r" % cards
    return rank
 
def handy(cards='2h 2d 2c Kc Qd'):
    hand = []
    for card in cards.split():
        f, s = card[:-1], card[-1]
        assert f in face, "Invalid: Don't understand card face %r" % f
        assert s in suit, "Invalid: Don't understand card suit %r" % s
        hand.append(Card(f, s))
    assert len(hand) == 5, "Invalid: Must be 5 cards in a hand, not %i" % len(hand)
    assert len(set(hand)) == 5, "Invalid: All cards in the hand must be unique %r" % cards
    return hand
 
 
if __name__ == '__main__':
    hands = ["2h 2d 2c Kc Qd",
     "2h 5h 7d 8c 9s",
     "Ah 2d 3c 4c 5d",
     "2h 3h 2d 3c 3d",
     "2h 7h 2d 3c 3d",
     "2h 7h 7d 7c 7s",
     "Th Jh Qh Kh Ah"] + [
     "4h 4s Ks 5d Ts",
     "Qc Tc 7c 6c 4c",
     ]
    print("%-18s %-15s %s %s" % ("HAND", "CATEGORY", "TIE-BREAKER","HAND-RANK"))
    for cards in hands:
        r = rank(cards)
        print("%-18r %-15s %r %r" % (cards, r[0], r[1],r[1][0]))
