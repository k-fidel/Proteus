# A* - Algorithm
# Mohammad Mirian 198203128775

import math
import copy
import time
import random
import numpy as np
import matplotlib.pyplot as plt
import pickle
import PathPlanning as m_path
from heapq import heappush, heappop # for priority queue


class node(object):
    xposition=0
    yposition=0
    cost=0
    priority=0
    HeurFuncTyp="None"
    def __init__(self, xposition, yposition, cost, priority,HeurFuncTyp):
        self.xposition = xposition
        self.yposition = yposition
        self.cost = cost
        self.priority = priority
        self.HeurFuncTyp = HeurFuncTyp

    def __lt__(self, other):
        return self.priority < other.priority
    def NewPri(self,Xdestination,Ydestination):
        self.priority=self.cost+self.estimate(Xdestination,Ydestination)    #A*
    def nextMove(self):
        self.priority +=1
    def estimate(self,Xdestination,Ydestination):
            dx=Xdestination - self.xposition
            dy=Ydestination - self.yposition
            if(self.HeurFuncTyp == "Chebyshev"):
                dPath= max(abs(dx),abs(dy))
            elif (self.HeurFuncTyp == "Euclidean"):
                dPath = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
            elif (self.HeurFuncTyp == "Manhatan"):
                dPath = abs(dx) + abs(dy)
            elif (self.HeurFuncTyp == "None"):
                dPath = 0;

            return (dPath)
def pathFind(the_map,xA, yA, xB, yB,HeurFuncTyp):
    dx = [1, 0, -1, 0]   #  to finding the neighbours of each node
    dy = [0, 1, 0, -1]

    startTime=time.clock()
    CountNode =0

    n = the_map.shape[0]
    m = the_map.shape[1]

    VisNod = []   # viseted node
    NexnodMap = [] # Next node map

    Parents=[[0 for i in  range (n)] for j in range(m)]
    PrevPath=[[]for i in range(2)]
    row=[0]*n

    for i in range(m):
        VisNod.append(list(row))
        PrevPath.append(list(row))

    PriorQu=[[],[]] # Priority Queues
    PriorQuIndx=0   # priority Queue Index

    n0 = node(xA, yA, 0, 0,HeurFuncTyp)
    n0.NewPri(xB, yB)
    n0.NewPri(xB, yB)
    heappush(PriorQu[PriorQuIndx], n0)
    NexnodMap[yA][xA] = n0.priority  # mark Current position as a open nodes
    CountNode += 1
# for searching A*

    while len(PriorQu[PriorQuIndx]) > 0:
        n1 = PriorQu[PriorQuIndx][0]  # top node
        n0 = node(n1.xposition, n1.yposition, n1.cost, n1.priority, HeurFuncTyp)
        x = n0.xposition
        y = n0.yposition
        heappop(PriorQu[PriorQuIndx])  # remove the node from the open list
        NexnodMap[y][x] = 0
        VisNod[y][x] = 1  # mark it on the closed nodes maps
        CountNode += 1


        if x == xB and y == yB:
            # generate the path from finish to start
            PathLenght = 0
            PrevPath[1].append(y)
            PrevPath[0].append(x)
            cur = Parents[y][x]
            y = cur[0]
            x = cur[1]
            while not (x == xA and y == yA):
                PrevPath[1].append(y)
                PrevPath[0].append(x)
                cur = Parents[y][x]
                y = cur[0]
                x = cur[1]
                PathLenght +=1
            PrevPath[1].append(y)
            PrevPath[0].append(x)
            endTime = time.clock()
            TakenTime = endTime - startTime
            return PrevPath, NexnodMap, VisNod,the_map,PathLenght,CountNode,TakenTime
    for i in range(4):
        xdx = x + dx[i]
        ydy = y + dy[i]
        if not (xdx < 0 or xdx > n - 1 or ydy < 0 or ydy > m - 1
                or the_map[ydy][xdx] == -1 or VisNod[ydy][xdx] == 1):
            # generate a child node
            m0 = node(xdx, ydy, n0.cost, n0.priority, HeurFuncTyp)
            m0.nextMove()
            m0.NewPri(xB, yB)
            # if it is not in the open list then add into that
            if NexnodMap[ydy][xdx] == 0:
                NexnodMap[ydy][xdx] = m0.priority
                the_map[ydy][xdx] = (m0.priority)
                heappush(PriorQu[PriorQuIndx], m0)
                # determine its parent node
                Parents[ydy][xdx] = [y, x]
            elif NexnodMap[ydy][xdx] > m0.priority:
                # update the priority
                NexnodMap[ydy][xdx] = m0.priority
                the_map[ydy][xdx] = (m0.priority)
                # update the parent
                Parents[ydy][xdx] = [y, x]
                # replace the node by emptying one pq to the other one
                # except the node to be replaced will be ignored
                # and the new node will be pushed in instead
                while not (PriorQu[PriorQuIndx][0].xposition == xdx and PriorQu[PriorQuIndx][0].yposition == ydy):
                    heappush(PriorQu[1 - PriorQuIndx], PriorQu[PriorQuIndx][0])
                    heappop(PriorQu[PriorQuIndx])
                heappop(PriorQu[PriorQuIndx])  # remove the target node
                # empty the larger size priority queue to the smaller one
                if len(PriorQu[PriorQuIndx]) > len(PriorQu[1 - PriorQuIndx]):
                    PriorQuIndx = 1 - PriorQuIndx
                while len(PriorQu[PriorQuIndx]) > 0:
                    heappush(PriorQu[1 - PriorQuIndx], PriorQu[PriorQuIndx][0])
                    heappop(PriorQu[PriorQuIndx])
                PriorQuIndx = 1 - PriorQuIndx
                heappush(PriorQu[PriorQu], m0)  # add the better node instead

                return ''  # there isn't any path
#################################################

n = 60 # vertical size of the map
m = 60 # horizontal size of the map

Map = m_path.generateMap2d([m,n])
print Map
CurMap = copy.copy(Map)
for i in range(n):
    for j in range(m):
        if (CurMap[i][j] == -2):  #find the start point
            Sp= [j,i]
        if(CurMap[i][j] == -3):  # find the end point
            Ep = [j,i]
xA = Sp[0]
yA = Sp[1]

xB = Ep[0]
yB = Ep[1]

path_ =[[0,1],[0,1]]
route = pathFind(CurMap, xA, yA, xB, yB,"Chebyshev")
smap = route[3]
smap[smap==1]=0
smap[Ep[1]][Ep[0]]=-3

str = "Visited nodes:",route[5]
str2 =  "LPath:", route[4]
str3 = "Time:",'{:0.4f}'.format(route[6])
m_path.plotMap(smap,route[0],str+str2+str3)

CurMap = copy.copy(Map)
route = pathFind(CurMap, xA, yA, xB, yB,"Manhatan")
smap = route[3]
smap[smap==1]=0
smap[Ep[1]][Ep[0]]=-3

str = "Visited nodes:",route[5]
str2 =  "LPath:", route[4]
str3 = "Time:",'{:0.4f}'.format(route[6])
m_path.plotMap(smap,route[0],str+str2+str3)

CurMap = copy.copy(Map)
route = pathFind(CurMap, xA, yA, xB, yB,"Euclidean")
smap = route[3]
smap[smap==1]=0
smap[Ep[1]][Ep[0]]=-3

str = "Visited nodes:",route[5]
str2 =  "LPath:", route[4]
str3 = "Time:",'{:0.4f}'.format(route[6])
m_path.plotMap(smap,route[0],str+str2+str3)

CurMap = copy.copy(Map)

route = pathFind(CurMap, xA, yA, xB, yB,"None")

smap = route[3]
smap[smap==1]=0
smap[Ep[1]][Ep[0]]=-3

str = "Visited nodes:",route[5]
str2 =  "LPath:", route[4]
str3 = "Time:",'{:0.4f}'.format(route[6])
m_path.plotMap(smap,route[0],str+str2+str3)












