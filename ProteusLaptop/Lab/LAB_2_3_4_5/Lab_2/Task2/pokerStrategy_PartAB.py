import random
import itertools
import collections
from collections import defaultdict
from heapq import heappush, heappop # for priority queue

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

SUIT_LIST = {'c', 'd', 'h', 's'}

def pokerStrategyExample(playerAction, playerActionValue, playerStack, agentHand, agentHandRank, agentStack):#

    agentAction = None
    agentValue = None

    if typeRank[agentHand] == 1 and handRank[agentHandRank] < handRank['Q']: #Hand rank is lower than queen
        if playerActionValue < 0.02*playerStack:
            if agentStack < playerActionValue:
                agentAction = 'Bet'
                agentValue = agentStack
            else:
                agentAction = 'Call'
                agentValue = 5 if agentStack >= 5 else agentStack
        else:
            if playerActionValue < 0.05*agentStack:
                if agentStack > playerStack:
                    if agentStack < playerActionValue:
                        agentAction = 'Bet'
                        agentValue = agentStack
                    else:
                        agentAction = 'Call'
                        agentValue = 5 if agentStack >= 5 else agentStack
                else:
                    agentAction = 'Fold'
                    agentValue = 0

    if (typeRank[agentHand] == 1 and handRank[agentHandRank] >= handRank['Q']) \
or (typeRank[agentHand] == 2 and handRank[agentHandRank] <= handRank['T']):
        #print(playerActionValue, type(agentStack))
        if playerActionValue < 0.02*agentStack:
            if agentStack < playerActionValue:
                agentAction = 'Bet'
                agentValue = agentStack
            else:
                agentAction = 'Call'
                agentValue = 5 if agentStack >= 5 else agentStack
        else:
            if playerActionValue < 0.05*agentStack:
                if agentStack < 2*playerActionValue:
                    agentAction = 'Bet'
                    agentValue = agentStack
                else:
                    agentAction = 'Bet'
                    agentValue = playerActionValue*2
            else:
                agentAction = 'Fold'
                agentValue = 0

    if typeRank[agentHand] == 2 and handRank[agentHandRank]> handRank['T'] and handRank[agentHandRank] < handRank['A']:
        if playerActionValue < 0.04*playerStack:
            if agentStack < playerStack:
                if playerActionValue < 0.06*agentStack:
                    if agentStack < 2*playerActionValue:
                        agentAction = 'Bet'
                        agentValue = agentStack
                    else:
                        agentAction = 'Bet'
                        agentValue = playerActionValue*2
                else:
                    if agentStack < playerActionValue:
                        agentAction = 'Bet'
                        agentValue = agentStack
                    else:
                        agentAction = 'Call'
                        agentValue = 5 if agentStack >= 5 else agentStack
            else:
                if agentStack < playerActionValue:
                    agentAction = 'Bet'
                    agentValue = agentStack
                else:
                    agentAction = 'Call'
                    agentValue = 5 if agentStack >= 5 else agentStack
        if handRank[agentHandRank] == handRank['A']:
            if agentStack < 2*playerActionValue:
                agentAction = 'Bet'
                agentValue = agentStack
            else:
                agentAction = 'Bet'
                agentValue = playerActionValue*2
        else:
            if agentStack < playerActionValue:
                agentAction = 'Bet'
                agentValue = agentStack
            else:
                agentAction = 'Call'
                agentValue = 5 if agentStack >= 5 else agentStack

    if typeRank[agentHand] == typeRank['TwoPairs']:
        if playerActionValue < 0.05*playerStack:
            if handRank[agentHandRank] > handRank['9']:
                if agentStack < 2*playerActionValue:
                    agentAction = 'Bet'
                    agentValue = agentStack
                else:
                    agentAction = 'Bet'
                    agentValue = playerActionValue*2
            else:
                if agentStack < playerActionValue:
                    agentAction = 'Bet'
                    agentValue = agentStack
                else:
                    agentAction = 'Call'
                    agentValue = 5 if agentStack >= 5 else agentStack
        else:
            if playerActionValue < 0.1*agentStack:
                if handRank[agentHandRank] > handRank['9'] and agentStack > playerStack:
                    if agentStack < 2*playerActionValue:
                        agentAction = 'Bet'
                        agentValue = agentStack
                    else:
                        agentAction = 'Bet'
                        agentValue = playerActionValue*2
                else:
                    if agentStack < playerActionValue:
                        agentAction = 'Bet'
                        agentValue = agentStack
                    else:
                        agentAction = 'Call'
                        agentValue = 5 if agentStack >= 5 else agentStack
                if handRank[agentHandRank] > handRank['J']:
                    if agentStack < playerActionValue:
                        agentAction = 'Bet'
                        agentValue = agentStack
                    else:
                        agentAction = 'Call'
                        agentValue = 5 if agentStack >= 5 else agentStack
                else:
                    agentAction = 'Fold'
                    agentValue = 0

    if typeRank[agentHand] == typeRank['3ofakind']:
        if agentStack > 1.5*playerStack:
            if playerActionValue < 0.05*agentStack:
                if playerActionValue > 0:
                    if agentStack < 2*playerActionValue:
                        agentAction = 'Bet'
                        agentValue = agentStack
                    else:
                        agentAction = 'Bet'
                        agentValue = playerActionValue*2
                else:
                    if agentStack < 10:
                        agentAction = 'Bet'
                        agentValue = agentStack
                    else:
                        agentAction = 'Bet'
                        agentValue = 10
            else:
                if agentStack < playerActionValue:
                    agentAction = 'Bet'
                    agentValue = agentStack
                else:
                    agentAction = 'Call'
                    agentValue = 5 if agentStack >= 5 else agentStack
        else:
            if agentStack < playerActionValue:
                agentAction = 'Bet'
                agentValue = agentStack
            else:
                agentAction = 'Call'
                agentValue = 5 if agentStack >= 5 else agentStack

    #additional strategy added > than 3ofakind
    if typeRank[agentHand] > typeRank['3ofakind']:
        if agentStack > 1.5*playerStack:
            if playerActionValue < 0.05*agentStack:
                if playerActionValue > 0:
                    if agentStack < 2*playerActionValue:
                        agentAction = 'Bet'
                        agentValue = agentStack
                    else:
                        agentAction = 'Bet'
                        agentValue = playerActionValue*2
                else:
                    if agentStack < 10:
                        agentAction = 'Bet'
                        agentValue = agentStack
                    else:
                        agentAction = 'Bet'
                        agentValue = 15
            else:
                if agentStack < playerActionValue:
                    agentAction = 'Bet'
                    agentValue = agentStack
                else:
                    agentAction = 'Call'
                    agentValue = 5 if agentStack >= 5 else agentStack
        else:
            if agentStack < playerActionValue:
                agentAction = 'Bet'
                agentValue = agentStack
            else:
                agentAction = 'Call'
                agentValue = 5 if agentStack >= 5 else agentStack

    if agentAction is None or agentValue is None:
        agentAction = 'Fold'
        agentValue = 0

    # You can extend this strategy as much as you want as long as you keep it fully deterministic (no random)
    return agentAction, agentValue


def dealing():
    Player1Hand = []
    Player2Hand = []
    Cards = []
    #Cards.clear();
    for num, suit in itertools.product(handRank, SUIT_LIST):
        Cards.append(num + suit);

    for i in range(5):
        ChosenCard = random.choice(Cards);
        Cards.remove(ChosenCard);
        Player1Hand.append(ChosenCard);         # assign a card to player1

        ChosenCard = random.choice(Cards);
        Cards.remove(ChosenCard);
        Player2Hand.append(ChosenCard);         # assign a card to player2

    return Player1Hand,Player2Hand


def HandAnalyzer(Hand):
    CardsRank = [0,0,0,0,0]
    max_numeral = 0
    min_numeral = 0
    HandRank = []
    numeral_dict = collections.defaultdict(int)
    suit_dict = collections.defaultdict(int)

    if (Hand != None):
        des = "HighCard"

        for i in range(5):
            CardsRank[i] = [handRank.get(Hand[i][0]),Hand[i][0]]
        CardsRank.sort();
        max_numeral = CardsRank[4][0]
        min_numeral = CardsRank[0][0]

        for my_card in Hand:
            numeral_dict[my_card[0]] += 1
            suit_dict[my_card[1]] += 1

        if (len(numeral_dict) == 2):
            keys = numeral_dict.keys();
            if(max(numeral_dict.values())==4):
                des = "4ofakind"

                if(numeral_dict[keys[0]] == 4):
                    HandRank.append(keys[0])
                else:
                    HandRank.append(keys[1])
            else:
                des = "fullhouse"
                if(numeral_dict[keys[0]] == 3):
                    HandRank.append(keys[0])
                    HandRank.append(keys[1])
                else:
                    HandRank.append(keys[1])
                    HandRank.append(keys[0])



        elif (len(numeral_dict) == 3):
            keys = numeral_dict.keys();
            if(max(numeral_dict.values())==3):
                des = "3ofakind"
                for num in numeral_dict:
                    if(numeral_dict[num] == 3):
                        HandRank.append(num)
                        break;

            else:
                des ="TwoPairs"
                for num in numeral_dict:
                    if(numeral_dict[num] == 2):
                        HandRank.append(num)

                if(numeral_dict[HandRank[1]] > numeral_dict[HandRank[0]]):
                    temp = HandRank[0]
                    HandRank[0] = HandRank[1]
                    HandRank[1] = temp

        elif (len(numeral_dict) == 4):
            des = "OnePair"
            rankt = []
            keys = numeral_dict.keys();
            for num in numeral_dict:
                if (numeral_dict[num] == 2):
                    HandRank.append(num)
                else:
                    rankt.append([handRank[num],num])
            rankt.sort(None,None,True);
            HandRank.append(rankt[0][1])
            HandRank.append(rankt[1][1])
            HandRank.append(rankt[2][1])
        else:
            if (len(suit_dict) == 1):
                if ((max_numeral - min_numeral) == 4):
                    des = "straightflush"
                    HandRank.append(CardsRank[4][1])
                else:
                    des = "flush"
                    HandRank.append(CardsRank[4][1])
            else:
                low_straight = set(("A", "2", "3", "4", "5"))      # lowest straight
                if ((max_numeral - min_numeral) == 4):
                    des = "straight"
                    HandRank.append(CardsRank[4][1])
                else:
                    if (set(numeral_dict.keys()).difference(low_straight)):
                        des = "HighCard"
                        for i in range(5):
                            HandRank.append(CardsRank[4-i][1])
                    else:
                        des = "straight"
                        HandRank.append('5')

    return des ,HandRank#, CardsRank=CardsRank)


class node(object):
    cost = 0 # total cost already travelled to reach the node
    priority = 0 # priority = cost + remaining distance estimate
    def __init__(self, act, cost, parent , index,Player1Stack, Player2Stack, pot):
        self.act = act
        self.parent = parent
        self.cost = cost
        self.index = index
        self.priority = self.cost
        self.pot = pot
        self.Player1Stack = Player1Stack
        self.Player2Stack = Player2Stack
    def __lt__(self, other):             # comparison method for priority queue
        return self.priority < other.priority

    def updatePriority(self):
        self.priority = self.cost + self.estimate() # A*
    # give higher priority to going straight instead of diagonally
    def nextMove(self,v):
        self.cost += v
    # Estimation function for the remaining distance to the goal.
    def estimate(self):

        return(0)


class agent(object):
      CurrentHand = None
      TotalMoney = 100
      CurAction = ""
      Value = 0
      def __init__(self,Hand,Money):
          self.CurrentHand = Hand
          self.TotalMoney = Money
      def HandStrength(self):
          return  HandAnalyzer(self.CurrentHand)
      def UpdateCoins(self,Pot):
          self.TotalMoney +=Pot
      def Action(self,Act,v):
          self.CurAction = Act
          self.Value = v
          if(Act == "Bet"):
            self.TotalMoney -=v
          elif(Act == "Call"):
            self.TotalMoney -=5


class game(object):
    Player1 = None
    Player2 = None
    NumberOfPlay = 0
    Pot = 0
    def __init__(self, Player1, Player2):
        self.Player1 = Player1
        self.Player2 = Player2
    def StartnewGame(self):
        Player1Hand, Player2Hand = dealing()
        Player1.CurrentHand = Player1Hand
        Player2.CurrentHand = Player2Hand
        self.NumberOfPlay +=1


def GenTree(index,Player1,Player2,pot):
    ActionSet = {"Fold", "Call", "Bet5", "Bet10", "Bet25"}
    agentHand = Player2.HandStrength()[0]
    agentRank = Player2.HandStrength()[1][0]
    VisitedNodes = []
    pot = pot
    pq = [[], []]  # priority queues of open (not-yet-tried) nodes
    pqi = 0  # priority queue index

    p2 = Player2
    for act in ActionSet:

        # create the start node and push into list of open nodes
        p1TotalMoney = Player1.TotalMoney
        p2TotalMoney = Player2.TotalMoney
        if act == "Fold":
            cost = 0
            pot = 0
        elif act == "Call":
            cost = 5
            pot = 5

        elif act == "Bet5":
            cost = 5
            pot =5

        elif act == "Bet10":
            cost = 10
            pot =10

        elif act == "Bet25":
            cost = 25
            pot = 25

        index += 1
        parent=0
        p1TotalMoney -=cost
        n0 = node(act,cost,parent,index,p1TotalMoney,p2TotalMoney,pot)
        heappush(pq[pqi], n0)

    while len(pq[pqi]) > 0:
        n1 = pq[pqi][0]  # top node
        heappop(pq[pqi])  # remove the node from the open list
        VisitedNodes.append(n1)
        pot = n1.pot
        p1TotalMoney = n1.Player1Stack
        p2TotalMoney = n1.Player2Stack

        if(n1.act == "Call"):
            index +=1

            if(ShowDown(Player1,Player2)==1):
                cost = n1.cost - pot
                p1TotalMoney += cost
            else:
                cost = n1.cost
                p2TotalMoney += cost
            n0 = node("SD",cost,n1.index,index,p1TotalMoney,p2TotalMoney,pot)
            heappush(pq[pqi],n0)
        elif(n1.act == "Bet5"):
            if (p2TotalMoney > 0):
                response = pokerStrategyExample("Bet",5,p1TotalMoney,agentHand,agentRank,p2TotalMoney)
                agentAct = response[0]
            else:
                agentAct = "Fold"

            #print (agentAct)
            if(agentAct == "Call"):
                pot = n1.pot+5
                p2TotalMoney -= 5
                if (ShowDown(Player1, Player2) == 1):
                    cost = n1.cost - pot
                    p1TotalMoney += pot
                else:
                    cost = n1.cost
                    p2TotalMoney +=cost
                index +=1
                n0 = node("SD",cost,n1.index,index,p1TotalMoney,p2TotalMoney,pot)
                heappush(pq[pqi],n0)
            elif(agentAct == "Fold"):
                index +=1
                cost = n1.cost - pot
                p1TotalMoney +=pot

                n0 = node("PlayerWon",cost,n1.index,index,p1TotalMoney,p2TotalMoney,pot)
                heappush(pq[pqi],n0)
            elif(agentAct=="Bet"):
                index +=1
                pot = n1.pot+response[1]
                p2TotalMoney -=response[1]
                n0 = node("Fold",n1.cost,n1.index,index, p1TotalMoney,p2TotalMoney,pot)
                heappush(pq[pqi],n0)
                index += 1
                pot = n1.pot+response[1]+5
                n0 = node("Call", n1.cost+5, n1.index, index,p1TotalMoney-5,p2TotalMoney, pot)
                heappush(pq[pqi], n0)
                index += 1
                pot = n1.pot + response[1] + 5
                n0 = node("Bet5", n1.cost + 5, n1.index, index,p1TotalMoney-5 ,p2TotalMoney ,pot)
                heappush(pq[pqi], n0)

                index += 1
                pot = n1.pot + response[1] + 10
                n0 = node("Bet10", n1.cost + 10, n1.index, index, p1TotalMoney-10 ,p2TotalMoney ,pot)
                heappush(pq[pqi], n0)
                index += 1
                pot = n1.pot + response[1] + 25
                n0 = node("Bet25", n1.cost + 25, n1.index, index,p1TotalMoney-25 ,p2TotalMoney ,pot)
                heappush(pq[pqi], n0)
        elif (n1.act == "Bet10"):
            if(p2TotalMoney >0):
                response = pokerStrategyExample("Bet", 10, p1TotalMoney, agentHand, agentRank, p2TotalMoney)
                agentAct = response[0]
            else:
                agentAct = "Fold"

            #print (agentAct ,"p1:",p1TotalMoney,"  P2:",p2TotalMoney)
            if (agentAct == "Call"):
                pot = n1.pot + 5
                p2TotalMoney -= 5
                if (ShowDown(Player1, Player2) == 1):
                    cost = n1.cost - pot
                    p1TotalMoney += pot
                else:
                    cost = n1.cost
                    p2TotalMoney += pot
                index += 1
                n0 = node("SD", cost, n1.index, index, p1TotalMoney, p2TotalMoney, pot)
                heappush(pq[pqi], n0)
            elif (agentAct == "Fold"):
                index += 1
                cost = n1.cost - pot
                p1TotalMoney += pot

                n0 = node("PlayerWon", cost, n1.index, index, p1TotalMoney, p2TotalMoney, pot)
                heappush(pq[pqi], n0)
            elif (agentAct == "Bet"):
                index += 1
                pot = n1.pot + response[1]
                p2TotalMoney -= response[1]
                n0 = node("Fold", n1.cost, n1.index, index, p1TotalMoney, p2TotalMoney, pot)
                heappush(pq[pqi], n0)
                index += 1
                pot = n1.pot + response[1] + 5
                n0 = node("Call", n1.cost + 5, n1.index, index, p1TotalMoney - 5, p2TotalMoney, pot)
                heappush(pq[pqi], n0)
                index += 1
                pot = n1.pot + response[1] + 5
                n0 = node("Bet5", n1.cost + 5, n1.index, index, p1TotalMoney - 5, p2TotalMoney, pot)
                heappush(pq[pqi], n0)

                index += 1
                pot = n1.pot + response[1] + 10
                n0 = node("Bet10", n1.cost + 10, n1.index, index, p1TotalMoney - 10, p2TotalMoney, pot)
                heappush(pq[pqi], n0)
                index += 1
                pot = n1.pot + response[1] + 25
                n0 = node("Bet25", n1.cost + 25, n1.index, index, p1TotalMoney - 25, p2TotalMoney, pot)
                heappush(pq[pqi], n0)

        elif(n1.act == "Bet25"):
            if(p2TotalMoney>0):
                response = pokerStrategyExample("Bet", 25, p1TotalMoney, agentHand, agentRank, p2TotalMoney)
                agentAct = response[0]
            else:
                agentAct = "Fold"
            #print (agentAct)
            if (agentAct == "Call"):
                pot = n1.pot + 5
                p2TotalMoney -=5
                if (ShowDown(Player1, Player2) == 1):
                    cost = n1.cost - pot
                    p1TotalMoney += pot
                else:
                    cost = n1.cost
                    p2TotalMoney += pot
                index += 1
                n0 = node("SD", cost, n1.index, index, p1TotalMoney, p2TotalMoney, pot)
                heappush(pq[pqi], n0)
            elif (agentAct == "Fold"):
                index += 1
                cost = n1.cost - pot
                p1TotalMoney += pot

                n0 = node("PlayerWon", cost, n1.index, index, p1TotalMoney, p2TotalMoney, pot)
                heappush(pq[pqi], n0)
            elif (agentAct == "Bet"):
                index += 1
                pot = n1.pot + response[1]
                p2TotalMoney -= response[1]
                n0 = node("Fold", n1.cost, n1.index, index, p1TotalMoney, p2TotalMoney, pot)
                heappush(pq[pqi], n0)
                index += 1
                pot = n1.pot + response[1] + 5
                n0 = node("Call", n1.cost + 5, n1.index, index, p1TotalMoney - 5, p2TotalMoney, pot)
                heappush(pq[pqi], n0)
                index += 1
                pot = n1.pot + response[1] + 5
                n0 = node("Bet5", n1.cost + 5, n1.index, index, p1TotalMoney - 5, p2TotalMoney, pot)
                heappush(pq[pqi], n0)

                index += 1
                pot = n1.pot + response[1] + 10
                n0 = node("Bet10", n1.cost + 10, n1.index, index, p1TotalMoney - 10, p2TotalMoney, pot)
                heappush(pq[pqi], n0)
                index += 1
                pot = n1.pot + response[1] + 25
                n0 = node("Bet25", n1.cost + 25, n1.index, index, p1TotalMoney - 25, p2TotalMoney, pot)
                heappush(pq[pqi], n0)

    Vnmax = len(VisitedNodes)
    path = []
    for i in range(Vnmax):
        vn = VisitedNodes[Vnmax-i-1]
        if(vn.act == "SD" or vn.act == "PlayerWon"):
            if(vn.cost<0):
             path.append("SD")
             index = Vnmax-i-1
             parent = vn.parent
             for j in  range(index-1,0,-1):
                 vn = VisitedNodes[j]
                 if(vn.index == parent):
                     path.append(vn.act)
                     parent = vn.parent
             break;

    if(path == []):
        path.append("Fold")
    else:
        Player1.TotalMoney = p1TotalMoney
        Player2.TotalMoney = p2TotalMoney
    print path

def ShowDown(Player1,Player2):

    PlayerHand = Player1.HandStrength()[0]
    PlayerRank = Player1.HandStrength()[1][0]

    agentHand = Player2.HandStrength()[0]
    agentRank = Player2.HandStrength()[1][0]

    if(typeRank[PlayerHand]>typeRank[agentHand]):
        return 1
    elif ( typeRank[PlayerHand] == typeRank[agentHand]):
        if(handRank[PlayerRank] > handRank[agentRank]):
            return  1
        else:
            return 0
    else:
        return 0
################### Main ####################
Player1Hand , Player2Hand = [None , None]
#Player1Hand =['Kd','Ks','2h','3s','7d']
Player1 = agent(Player1Hand,100)
#Player2Hand =['Qd','Qs','2h','3s','7d']
Player2 = agent(Player2Hand,100)
m_game = game(Player1,Player2)
while not (Player2.TotalMoney <= 0 or Player1.TotalMoney <= 0):
    m_game.StartnewGame()
    m_game.Pot =0
    Player1.Action("Bet",5)
    m_game.Pot += 5
    agentHand = Player2.HandStrength()[0]
    agentRank = Player2.HandStrength()[1][0]
    response = pokerStrategyExample("Bet", 5, Player1.TotalMoney, agentHand, agentRank, Player2.TotalMoney)
    if(response[0] == "Call"):
        Player2.Action("Call",5)
        m_game.Pot +=5
        if(ShowDown(Player1,Player2)==1):
            Player1.TotalMoney +=m_game.Pot
        else:
            Player2.TotalMoney +=m_game.Pot
    elif (response[0] == "Fold"):
        Player1.TotalMoney +=m_game.Pot
    elif (response[0] == "Bet"):
        m_game.Pot +=response[1]
        Player2.Action("Bet",response[1])
        Player1.Action("Call",5)
        m_game.Pot +=5
        if (ShowDown(Player1, Player2) == 1):
            Player1.TotalMoney += m_game.Pot
        else:
            Player2.TotalMoney += m_game.Pot
    print "Player1:" , Player1.TotalMoney
    print "Player2:" , Player2.TotalMoney

print "The Number of game hands:" , m_game.NumberOfPlay
print "Player1 Money:" , Player1.TotalMoney
print "Player2 Money:" , Player2.TotalMoney






