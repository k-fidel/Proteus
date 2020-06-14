import random




# rank of the type
typeRank = {'HighCard': 1,
            'OnePair': 2,
            'TwoPairs': 3,
            '3ofakind': 4,
            'straight': 5,
            'flush': 6,
            'fullhouse': 7,
            '4ofakind': 8,
            'straightflush': 9}

# strength of each type
handRank = {'2': 1,
            '3': 2,
            '4': 3,
            '5': 4,
            '6': 5,
            '7': 6,
            '8': 7,
            '9': 8,
            'T': 9,
            'J': 10,
            'Q': 11,
            'K': 12,
            'A': 13}

handSuit = {'s','h','d','c'}
"""
deck = []

for e in handRank.keys(): #create deck
    for c in handSuit:
        deck.append(e+c)

random.shuffle(deck)      #shuffle

Hand1 = []
Hand2 = []
for i in range(5):        #pick cards
    Hand1.append(deck.pop())
    Hand2.append(deck.pop())

"""
def SortFunc(Rank):       #just for sorting
    return handRank[Rank[0]]


#Hand1 = ['2s', '3c', '5s', '6s', 'As'] #testing
#Hand2 = ['2c', '3c', '5d', '6c', 'Ac'] #testing


#Hand2sorted= sorted(Hand2,key=SortFunc)
#Hand1sorted= sorted(Hand1,key=SortFunc)
#print Hand1sorted
#print Hand2sorted

def groupHand(hand): #grouping cards by type
    sortedHand = sorted(hand,key=SortFunc)
    oldcard = 0
    theHand = []
    ap = 0
    for i in range(len(sortedHand)):
        if(len(theHand)==0):
            theHand.append([sortedHand[i]])
        else:
            if sortedHand[i][0] == oldcard:
               theHand[ap].append(sortedHand[i])
            else:
               ap += 1
               theHand.append([sortedHand[i]])

        oldcard = sortedHand[i][0]

    return sorted(theHand,key=len) #return the hand sorted by type

def identifyHand(theHand):
    rank = []
    type = ""
    theHand = groupHand(theHand)
    if len(theHand)==5:
       straight = True
       flush = True

       for c in range(len(theHand)-1):
           if handRank[theHand[c][0][0]]+1 != handRank[theHand[c+1][0][0]]: #checking if ranks are atleast sequential => straight
               straight = False
           if theHand[c][0][1] != theHand[c+1][0][1]: #checking if suit is the same on all cards => flush
               flush = False

       if straight:
           if(flush):
                  type = "straightflush"
           else:
                  type = "straight"
       elif(flush):
           type = "flush"
       else:
           type = "HighCard"
       rank = theHand[4][0][0]
    elif len(theHand)==4:
       for cardstacks in theHand:
           if len(cardstacks) == 2:
              rank = cardstacks[0][0]
              break
       type = "OnePair"

    elif len(theHand)==3:
        for cardstacks in theHand:
            if 1 < len(cardstacks) < 4:
                rank.append(cardstacks[0])

        if len(rank)>1:
            type = "TwoPairs"
        else:
            type = "3ofakind"

    elif len(theHand) == 2:
        for cardstacks in theHand:
            if 1 < len(cardstacks) < 5:
                rank.append(cardstacks[0])

        if len(rank)>1:
            type = "fullhouse"
        else:
            type = "4ofakind"

    return [type,rank,theHand]

def judgeHands(identHand1,identHand2):

    if typeRank[identHand1[0]]>typeRank[identHand2[0]]:
        return 1
    elif typeRank[identHand1[0]]<typeRank[identHand2[0]]:
        return -1
    else:
        Hand1_=identHand1[2]
        Hand2_=identHand2[2]
        for i in range(len(Hand1_)):#could also be len(identHand2) since if both types are equal, they have the same card structure
            if handRank[Hand1_[len(Hand1_)-(i+1)][0][0]]>handRank[Hand2_[len(Hand2_)-(i+1)][0][0]]:#comparing last(highest)cards first, then in decending order
                return 1
            elif handRank[Hand1_[len(Hand1_)-(i+1)][0][0]]<handRank[Hand2_[len(Hand2_)-(i+1)][0][0]]:#comparing last(highest)cards first, then in decending order
                return -1

    return 0


"""
identHand2 = groupHand(Hand2sorted)
identHand1 = groupHand(Hand1sorted)
out2 = identifyHand(identHand2)
out1 = identifyHand(identHand1)

print out1[2]
print out2[2]
result = judgeHands(out1,out2)
print "player 1 has:",out1[0],out1[1]
print "player 2 has:",out2[0],out2[1]

if result == 1: print "player 1 won"
elif result ==-1: print "player 2 won"
else: print "draw"
"""