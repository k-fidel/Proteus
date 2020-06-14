# A* - Algorithm
# Mohammad Mirian 198203128775
from heapq import heappush, heappop # for priority queue
import math
import copy
import time
import random
import numpy as np
import matplotlib.pyplot as plt
import pickle
import PathPlanning as m_path

class node(object):    #initialize parameters
    xposition = 0    # x position
    yposition = 0    # y position
    cost = 0 # total cost already travelled to reach the node
    priority = 0 # priority = cost + remaining distance estimate
    HeuristicFuncType = "None"
    def __init__(self, xposition, yposition, cost, priority,HeuristicFuncType):
        self.xposition = xposition
        self.yposition = yposition
        self.cost = cost
        self.priority = priority
        self.HeuristicFuncType = HeuristicFuncType

    def __lt__(self, other):             # comparison method for priority queue
        return self.priority < other.priority

    def updatePriority(self, xDest, yDest):
        self.priority = self.cost + self.estimate(xDest, yDest) # A*
    # give higher priority to going straight instead of diagonally
    def nextMove(self):
        self.cost += 1
    # Estimation function for the remaining distance to the goal.
    def estimate(self, xDest, yDest):
        dx = xDest - self.xposition
        dy = yDest - self.yposition
        if( self.HeuristicFuncType == "Chebyshev" ):
            d = max(abs(dx), abs(dy))
        elif (self.HeuristicFuncType == "Euclidean"):
            d = math.sqrt(math.pow(dx,2)+ math.pow(dy,2))
        elif (self.HeuristicFuncType == "Manhatan"):
            d = abs(dx)+abs(dy)
        elif (self.HeuristicFuncType == "None"):
            d = 0;

        return(d)

# A-star algorithm.
def pathFind(the_map,xA, yA, xB, yB,HeuristicFuncType):
    dx = [1, 0, -1, 0]   #  we use them for finding the neighbours of each node
    dy = [0, 1, 0, -1]   #

    startTime = time.clock()
    CountVisitedNode = 0    # a counter that shows us the number of visited nodes it can be used as a criteria for algrithm effeciency

    n = the_map.shape[0]   # n , m are the dimension of map   n x m
    m = the_map.shape[1]

    visited_nodes = []      # visited nodes
    open_nodes_map = []     # the node is ready to open

    parents = [[ 0 for i in range(n)] for j in range(m)]
    solved_path = [[] for i in range(2)]
    row = [0] * n

    for i in range(m): # create 2d arrays
        visited_nodes.append(list(row))
        open_nodes_map.append(list(row))

    pq = [[], []] # priority queues of open (not-yet-tried) nodes
    pqi = 0       # priority queue index
    # create the start node and push into list of open nodes
    n0 = node(xA, yA, 0, 0,HeuristicFuncType)
    n0.updatePriority(xB, yB)
    heappush(pq[pqi], n0)
    open_nodes_map[yA][xA] = n0.priority # mark it on the open nodes map
    CountVisitedNode +=1
    # A* search
    while len(pq[pqi]) > 0:
        # get the current node the highest priority from the list of open nodes

        n1 = pq[pqi][0]         # top node
        n0 = node(n1.xposition, n1.yposition, n1.cost, n1.priority,HeuristicFuncType)
        x = n0.xposition
        y = n0.yposition
        heappop(pq[pqi])        # remove the node from the open list
        open_nodes_map[y][x] = 0
        visited_nodes[y][x] = 1 # mark it on the closed nodes maps
        CountVisitedNode +=1

        # quit searching when the goal is reached
        # if n0.estimate(xB, yB) == 0:
        if x == xB and y == yB:
            # generate the path from finish to start
            PathLenght = 0
            solved_path[1].append(y)
            solved_path[0].append(x)
            cur = parents[y][x]
            y = cur[0]
            x = cur[1]
            while not (x == xA and y == yA):
                solved_path[1].append(y)
                solved_path[0].append(x)
                cur = parents[y][x]
                y = cur[0]
                x = cur[1]
                PathLenght +=1
            solved_path[1].append(y)
            solved_path[0].append(x)
            endTime = time.clock()
            TakenTime =  endTime - startTime
            return solved_path , open_nodes_map, visited_nodes,the_map,PathLenght,CountVisitedNode,TakenTime
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # generate the child nodes
        for i in range(4):
            xdx = x + dx[i]
            ydy = y + dy[i]
            if not (xdx < 0 or xdx > n-1 or ydy < 0 or ydy > m - 1
                    or the_map[ydy][xdx] == -1 or visited_nodes[ydy][xdx] == 1):
                # generate a child node
                m0 = node(xdx, ydy, n0.cost, n0.priority,HeuristicFuncType)
                m0.nextMove()
                m0.updatePriority(xB, yB)
                # if it is not in the open list then add into that
                if open_nodes_map[ydy][xdx] == 0:
                    open_nodes_map[ydy][xdx] = m0.priority
                    the_map[ydy][xdx] = (m0.priority)
                    heappush(pq[pqi], m0)
                    # determine its parent node
                    parents[ydy][xdx] = [y, x]
                elif open_nodes_map[ydy][xdx] > m0.priority:
                    # update the priority
                    open_nodes_map[ydy][xdx] = m0.priority
                    the_map[ydy][xdx] = (m0.priority)
                    # update the parent
                    parents[ydy][xdx] = [y, x]
                    # replace the node by emptying one pq to the other one
                    # except the node to be replaced will be ignored
                    # and the new node will be pushed in instead
                    while not (pq[pqi][0].xposition == xdx and pq[pqi][0].yposition == ydy):
                        heappush(pq[1 - pqi], pq[pqi][0])
                        heappop(pq[pqi])
                    heappop(pq[pqi])      # remove the target node
                    # empty the larger size priority queue to the smaller one
                    if len(pq[pqi]) > len(pq[1 - pqi]):
                        pqi = 1 - pqi
                    while len(pq[pqi]) > 0:
                        heappush(pq[1-pqi], pq[pqi][0])
                        heappop(pq[pqi])       
                    pqi = 1 - pqi
                    heappush(pq[pqi], m0)       # add the better node instead
    return ''      # there isn't any path

#################################################
# MAIN
# The heuristic function for this task has been considered Chebyshev distance
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
