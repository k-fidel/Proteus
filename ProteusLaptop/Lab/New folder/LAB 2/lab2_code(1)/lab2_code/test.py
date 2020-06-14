import Queue as queue
import numpy as np
import math
import PathPlanning as m_path
import matplotlib.pyplot as plt
import pickle

class Node(object):
    xPos =0
    yPos = 0
    cost =0
    f =0
    goTop = 0
    def __init__(self, xPos, yPos, cost , f,goTop):
        self.xPos = xPos
        self.yPos = yPos
        self.cost = cost
        self.f = f
        self.goTop = goTop
    def UpDatef(self,x,y):
        if (self.yPos > 30):
            k = 1
        else:
            k=1
        self.f = k*self.cost + self.heuristic(x,y)

    def Move(self):
        if(self.goTop==0):
            if(self.yPos > 30):
                self.cost += 1#(self.yPos-30)
            else:
                self.cost += 1
        else:
            self.cost +=1
    def heuristic(self,x,y):
        #d = math.sqrt(math.pow((self.xPos-x),2)+math.pow((self.yPos - y),2))
        d= abs(self.xPos-x) + abs(self.yPos - y)
        #d = max(abs(self.xPos - x) , abs(self.yPos - y))
        return  1*d

def Astart_PathFind(Map,PA,PB,GoTop):
    dirs = 4                               # number of possible directions to move on the map
    if dirs == 4:
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
    n= Map.shape[0]
    m= Map.shape[1]
    xGoal = PB[0]
    yGoal = PB[1]
    path = np.zeros((n, m))
    solved_path = [[] for i in range(2)]
    path.fill(1)
    parents = np.zeros((n, m))
    parents= x = [[0 for i in range(n)] for j in range(m)]
    Open_list = queue.PriorityQueue()
    xS = PA[0]
    yS = PA[1]
    n0 = Node(xS,yS,0,0,GoTop)
    n0.UpDatef(xGoal,yGoal)
    Open_list.put((n0.f,n0))

    #Map[xS][yS] = n0.f
    while not Open_list.empty():        # check the open list if there is any element for expanding
        temp = Open_list.get()       # read the low proirity element from the open list
        CurNode = temp[1]
        x = CurNode.xPos
        y = CurNode.yPos
        path[x][y] = 1
        if x == xGoal and y == yGoal:   # A* found the Goal

            solved_path[1].append(x)
            solved_path[0].append(y)
            #Map[x][y] = 20

            cur = parents[x][y]
            x = cur[0]
            y = cur[1]
            while not (x == xS and y == yS ):
                solved_path[1].append(x)
                solved_path[0].append(y)
                #Map[x][y] = 20
                cur = parents[x][y]
                x = cur[0]
                y= cur [1]
            solved_path[1].append(x)
            solved_path[0].append(y)
            #Map[x][y] = 20

            return Map ,solved_path
        for i in range(dirs):
            xn = x+dx[i]
            yn = y+dy[i]
            if ( xn >=0 and yn >=0 and xn<=n-1 and yn<=m-1 and path[xn][yn] == 1 and (Map[xn][yn] == 1 or Map[xn][yn]==-3)):
                n0 = Node(xn, yn, CurNode.cost, CurNode.f,GoTop)
                n0.Move()
                n0.UpDatef(xGoal,yGoal)
                Open_list.put((n0.f,n0))
                if(Map[xn][yn] <> -3):
                    Map[xn][yn] = n0.f
                parents[xn][yn]=[x,y]


##############  Main ########################################
thefile = open('map.txt', 'r')

Map2 = pickle.load(thefile)

#Map2 = m_path.generateMap2d_obstacle([60,60])
#Map = m_path.generateMap2d([60,60])
#Map = np.zeros((4,4))
#Map.fill(1)
print  Map2[1]
Map = Map2[0]

for i in range(60):
    for j in range(60):
        if (Map[i][j] == -2):
            s= [i,j]
        if(Map[i][j] == -3):
            f = [i,j]

yS = s[0]
yF = f[0]
yTop = Map2[1][0]
yBot = Map2[1][1]

DisFormTop = abs(yS-yTop) + abs(yF-yTop)
DisFormBot = abs(yS-yBot) + abs(yF-yBot)
GoTop = 1
if(DisFormTop > DisFormBot):
    GoTop = 0
p = Astart_PathFind(Map,s,f,GoTop)
path_ = p[1]
