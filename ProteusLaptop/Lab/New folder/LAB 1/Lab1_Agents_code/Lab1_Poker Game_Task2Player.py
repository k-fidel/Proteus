import random
import itertools
import collections

LIST = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
LIST2 = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
SUIT_LIST = {'c', 'd', 'h', 's'}
Hand = {"High card": 1, "Pair": 2, "Flush": 3, "Straight": 4, "Three of a kind": 5, "Straight flush": 6}
Player1 = dict(Hand=["", "", ""], bet=0, TotalMoney=0)
Player2 = dict(Hand=["", "", ""], bet=0, TotalMoney=0)
CardDeal = []

def Deck():
    CardDeal.clear()
    for num, suit in itertools.product(LIST2, SUIT_LIST):
        CardDeal.append(num+suit)

def GetCard():
    card = random.choice(CardDeal)
    CardDeal.remove(card)
    return card

def AssignHand (Player1):
    Player1["Hand"] = [GetCard(), GetCard(), GetCard()]

def betting(Type_, my_Hand, opponentBid) :
    if(Type_ == "random"):
        bet = random.randint(0, 50)
    elif(Type_ == "fixed"):
        bet = 20
    elif(Type_ == "reflex"):
        bet = reflex_bet(my_Hand, opponentBid)
    else:
        bet = 0
    return bet

def Bet_randomly():
    return random.randint(0, 50)
def fixed_bet():
    return 20
def reflex_bet(my_Hand, opponentBid):
    global betting
    sa = next(Hand_Analyze(my_Hand))
    rank = Hand[sa["result"]]
    myBet = (rank-1)*10
    if(rank > 1):
        myBet = 50
    else:
        myBet = 1
    return myBet

def Hand_Analyze(Hand1):
    numeral_dict = collections.defaultdict(int)
    suit_dict = collections.defaultdict(int)
    rank = 0
    rank2 = 0
    rank3 = 0
    des = "High card"
    for my_card in Hand1:
        numeral_dict[my_card[0]] += 1
        suit_dict[my_card[1]] += 1
    if (len(numeral_dict) == 2):
        des = "Pair"
        for x in numeral_dict.keys():
            if(numeral_dict[x] == 2):
                rank = LIST2[x];

    elif (len(numeral_dict) == 1):
        des = "Three of a kind"
        x = numeral_dict.keys()
        for x in numeral_dict.keys():
            rank = LIST2[x]
    else:
        if (len(suit_dict) == 1):
            min_numeral = min([LIST2.get(x) for x in numeral_dict.keys()])
            max_numeral = max([LIST2.get(x) for x in numeral_dict.keys()])
            if ((max_numeral - min_numeral) == 2):
                des = "Straight flush"
                rank = max_numeral
            else:
                des = "Flush"
                rank = max_numeral
        else:
            min_numeral = min([LIST2.get(x) for x in numeral_dict.keys()])
            max_numeral = max([LIST2.get(x) for x in numeral_dict.keys()])
            low_straight = set(("A", "2", "3"))
            if ((max_numeral - min_numeral) == 2):
                des = "Straight"
                rank = max_numeral
            else:

                if(set(numeral_dict.keys()).difference(low_straight)):
                    des = "High card"
                    rank = max_numeral
                    a = [LIST2.get(x) for x in numeral_dict.keys()]
                    a.sort()

                    rank2 = a[1]
                    rank3 = a[2]
                else:
                    des ="Straight"
                    rank = 3
    yield dict(result=des, score=rank, score2=rank2, score3=rank3)

def IsPlayer1Winner(Player1_Hand,Player2_Hand):
    sa = next(Hand_Analyze(Player1_Hand))
    sb = next(Hand_Analyze(Player2_Hand))
    if (Hand[sa["result"]] == Hand[sb["result"]]):
        if(sa["score"]>sb["score"]):
           return 1
        elif(sa["score"]==sb["score"]):
            if(sa["score2"]==sb["score2"]):
                if(sa["score3"]>sb["score3"]):
                    return 1
                else:
                    return 0
            elif(sa["score2"]>sb["score2"]):
                return 1
            else:
                return 0


        else:

            return 0
    if( Hand[sa["result"]] > Hand[sb["result"]]):
        return 1
    else:
        return 0





Playe1NoOfWinning = 0
Playe2NoOfWinning = 0
for k in range(1000):
 Player1["TotalMoney"] = 0
 Player2["TotalMoney"] = 0
 for i in range(50):
    Deck()
    bidindex = 0
    pot = 0
    AssignHand(Player1)
    AssignHand(Player2)
    Player1["bet"] = betting("random", 0, 0)
    pot += Player1["bet"]
    Player2["bet"] = betting("reflex", Player2["Hand"], Player1["bet"])
    pot += Player2["bet"]

    Player1["bet"] = betting("random", 0, 0)
    pot += Player1["bet"]
    Player2["bet"] = betting("reflex", Player2["Hand"], Player1["bet"])
    pot += Player2["bet"]

    Player1["bet"] = betting("random", 0, 0)
    pot += Player1["bet"]
    Player2["bet"] = betting("reflex", Player2["Hand"], Player1["bet"])#relfx_bid(Player2["Hand"],Player1["bid"])#50#biding_phase()
    pot += Player2["bet"]

    sa = Hand_Analyze(Player1["Hand"])
    sb = Hand_Analyze(Player2["Hand"])
    check = IsPlayer1Winner(Player1["Hand"], Player2["Hand"])
    if(check==1):
        Player1["TotalMoney"] += pot
    elif(check == 0):
        Player2["TotalMoney"] += pot


 if (Player2["TotalMoney"] > Player1["TotalMoney"]):
    Playe2NoOfWinning += 1
 elif (Player2["TotalMoney"] < Player1["TotalMoney"]):
    Playe1NoOfWinning += 1
print("_______________ Player1 _________________")
print("Chips:", Playe1NoOfWinning)
print("money:", Player1["TotalMoney"], "$")
print("_______________ Player2 _________________")
print("Chips:" ,Playe2NoOfWinning)
print("money:", Player2["TotalMoney"], "$")
if (Player1["TotalMoney"] > Player2["TotalMoney"]):
    print("_________________________________________")
    print("Player 1 is winner")
else:
    print("_______________ RESULT __________________")
    print ("Player 2 is winner")