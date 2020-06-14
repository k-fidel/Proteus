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

class node(object):
    xPos = 0    # x position
    yPos = 0    # y position
    cost = 0 # total cost already travelled to reach the node
    priority = 0 # priority = cost + remaining distance estimate
    def __init__(self, xPos, yPos, cost, priority):
        self.xPos = xPos
        self.yPos = yPos
        self.cost = cost
        self.priority = priority

    def __lt__(self, other):             # comparison method for priority queue
        return self.priority < other.priority

    def updatePriority(self, xDest, yDest,SwampPos,TopPath):
        self.priority = self.cost + self.estimate(xDest, yDest,SwampPos,TopPath) # A*
    # give higher priority to going straight instead of diagonally
    def nextMove(self,v):
        self.cost += v
    # Estimation function for the remaining distance to the goal.
    def estimate(self, xDest, yDest, SwampPos,TopPath):
        xd = xDest - self.xPos
        yd = yDest - self.yPos
        # Euclidian Distance
        yTop = SwampPos[0][1]+20
        yBot = SwampPos[1][1]-10


        xTop = SwampPos[0][0]+20
        xBot = SwampPos[1][0]-10

        if(TopPath > 0):
            Cr = self.yPos - yBot - ((yTop - yBot)/(xTop - xBot))*(self.xPos-xBot)

            if(Cr<0):
                d = abs(xd) + abs(yd)

            else:
                if(TopPath == 1):
                    d = abs(self.xPos - xTop) + abs(self.yPos - yTop) + abs(xTop - xDest) + abs(yTop - yDest)
                else:
                    d = abs(self.xPos - xBot)+abs(self.yPos-yBot) + abs(xBot - xDest)+abs(yBot-yDest)
        else:
            d = abs(xd) + abs(yd)
        return(d)

# A-star algorithm.
def pathFind(the_map, xA, yA, xB, yB, SwampPos,TopPath):
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    CountVisitedNode = 0
    n = the_map.shape[0]
    m = the_map.shape[1]
    visited_nodes = []   # visited nodes
    open_nodes_map = []     # the node is ready to open
    parents = [[ 0 for i in range(n)] for j in range(m)]
    solved_path = [[] for i in range(2)]
    row = [0] * n

    for i in range(m): # create 2d arrays
        visited_nodes.append(list(row))
        open_nodes_map.append(list(row))

    pq = [[], []] # priority queues of open (not-yet-tried) nodes
    pqi = 0 # priority queue index
    # create the start node and push into list of open nodes
    n0 = node(xA, yA, 0, 0)
    n0.updatePriority(xB, yB,SwampPos,TopPath)
    heappush(pq[pqi], n0)
    open_nodes_map[yA][xA] = n0.priority # mark it on the open nodes map
    CountVisitedNode +=1
    # A* search
    while len(pq[pqi]) > 0:
        # get the current node the highest priority
        # from the list of open nodes
        n1 = pq[pqi][0] # top node
        n0 = node(n1.xPos, n1.yPos, n1.cost, n1.priority)
        x = n0.xPos
        y = n0.yPos
        heappop(pq[pqi]) # remove the node from the open list
        open_nodes_map[y][x] = 0
        visited_nodes[y][x] = 1 # mark it on the closed nodes maps
        CountVisitedNode +=1

        # quit searching when the goal is reached
        # if n0.estimate(xB, yB) == 0:
        if x == xB and y == yB:
            # generate the path from finish to start
            # by following the dirs
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
            return solved_path , open_nodes_map, visited_nodes,the_map,PathLenght,CountVisitedNode

        # generate the child nodes
        for i in range(4):
            xdx = x + dx[i]
            ydy = y + dy[i]
            if not (xdx < 0 or xdx > n-1 or ydy < 0 or ydy > m - 1
                    or the_map[ydy][xdx] == -1 or visited_nodes[ydy][xdx] == 1):
                # generate a child node

                m0 = node(xdx, ydy, n0.cost, n0.priority)
                m0.nextMove(the_map[ydy][xdx])
                m0.updatePriority(xB, yB,SwampPos,TopPath)
                # if it is not in the open list then add into that
                if open_nodes_map[ydy][xdx] == 0:
                    open_nodes_map[ydy][xdx] = m0.priority
                    the_map[ydy][xdx] = (m0.priority)
                    heappush(pq[pqi], m0)
                    # mark its parent node direction
                    parents[ydy][xdx] = [y, x]
                elif open_nodes_map[ydy][xdx] > m0.priority:
                    # update the priority
                    open_nodes_map[ydy][xdx] = m0.priority
                    the_map[ydy][xdx] = (m0.priority)
                    # update the parent direction
                    parents[ydy][xdx] = [y, x]
                    # replace the node
                    # by emptying one pq to the other one
                    # except the node to be replaced will be ignored
                    # and the new node will be pushed in instead
                    while not (pq[pqi][0].xPos == xdx and pq[pqi][0].yPos == ydy):
                        heappush(pq[1 - pqi], pq[pqi][0])
                        heappop(pq[pqi])
                    heappop(pq[pqi]) # remove the target node
                    # empty the larger size priority queue to the smaller one
                    if len(pq[pqi]) > len(pq[1 - pqi]):
                        pqi = 1 - pqi
                    while len(pq[pqi]) > 0:
                        heappush(pq[1-pqi], pq[pqi][0])
                        heappop(pq[pqi])       
                    pqi = 1 - pqi
                    heappush(pq[pqi], m0) # add the better node instead
    return ''


#########################################################################
# MAIN
#########################################################################
n = 80 # horizontal size of the map
m = 80 # vertical size of the map

#thefile = open('map.txt', 'r')
#Map2 = pickle.load(thefile)
Map2 = m_path.generateMap2d_swamp([m,n])
Map = Map2[0]
CurMap = copy.copy(Map2[0])
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






BottomSwampPos = Map2[1][0]
TopSwampPos = Map2[1][1]
SwampPos = [BottomSwampPos,TopSwampPos]


################  Finding Path according to ordinary eculian heuristic function
path_ =[[0,1],[0,1]]
route = pathFind(CurMap, xA, yA, xB, yB, SwampPos,-1)


smap = route[3]
smap[smap==1]=0
smap[Ep[1]][Ep[0]]=-3

str = "The number of Visited nodes:",route[5]
str2 =  "The lenght of Path:", route[4]
m_path.plotMap(smap,route[0],str+str2)


################  Finding Path according to ordinary eculian new heuristic function for reducing search

##  chosing the path of moving
# first of all we measure the distance of start point to end point through two path (Top and Bottom), we consider two waypoints one in swamp Top position and the other in the
# swamp bottom position

disTop = abs(xA -TopSwampPos[0])+abs(yA-TopSwampPos[1])+abs(TopSwampPos[0]-xB)+abs(TopSwampPos[1]-yB)
disBot = abs(xA -BottomSwampPos[0])+abs(yA-BottomSwampPos[1])+abs(BottomSwampPos[0]-xB)+abs(BottomSwampPos[1]-yB)

if(disTop <= disBot):
    TopPath = 1
else:
    TopPath = 0

CurMap = copy.copy(Map2[0])
path_ =[[0,1],[0,1]]
route = pathFind(CurMap, xA, yA, xB, yB, SwampPos,TopPath)


smap = route[3]
smap[smap==1]=0
smap[Ep[1]][Ep[0]]=-3

str = "The number of Visited nodes:",route[5]
str2 =  "The lenght of Path:", route[4]
m_path.plotMap(smap,route[0],str+str2)

