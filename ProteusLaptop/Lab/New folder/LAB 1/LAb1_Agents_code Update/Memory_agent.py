# Make sure to have the server side running in V-REP:
# in a child script of a V-REP scene, add following command
# to be executed just once, at simulation start:
#
# simExtRemoteApiStart(19999)
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!
import random
import enum
import math
import Lab1_Agents_Task1_World as World

def Turn(Ldis,Rdis):
    global Rspeed,Lspeed;
    global motorSpeed;
    Rspeed = Lspeed = 0;
    motorSpeed = dict(speedLeft=Lspeed, speedRight=Rspeed)
    World.setMotorSpeeds(motorSpeed);
    if(Rdis>=Ldis):
        Lspeed = 0
        Rspeed = -1
    else:
        Lspeed = -1
        Rspeed = 0

    motorSpeed = dict(speedLeft=Lspeed, speedRight=Rspeed)
    World.execute(motorSpeed,2000,-1)
    return;

def run(Ldis,Rdis,TP):
    global PLdis,PRdis
    global FindWall,FindingEnrgyCn
    global  motorSpeed
    global Lspeed,Rspeed

    if (TP < 0.2 and TP > -0.2):
        Rspeed = Lspeed = 2;
    if(TP>=0.2):
        Rspeed = 0
        Lspeed = 1
    if(TP<=-0.2):
        Lspeed = 0
        Rspeed = 1
    motorSpeed = dict(speedLeft=Lspeed, speedRight=Rspeed)

    return


def RandomStrategy():
   global motorSpeed,Lspeed,Rspeed
   WR = World.getSensorReading("ultraSonicSensorRight")
   WL = World.getSensorReading("ultraSonicSensorLeft")

   if(WL >0.3 and WR>0.3):
       Lspeed = random.uniform(2, 10)
       Rspeed = Lspeed # random.uniform(0, 10)

   elif(WR<0.3):
       Lspeed = 0
       Rspeed = -random.uniform(2, 10)

   elif(WL<0.3):
        Lspeed = -random.uniform(2, 10)
        Rspeed = 0

   motorSpeed = dict(speedLeft=Lspeed, speedRight=Rspeed)
   World.setMotorSpeeds(motorSpeed)
   WR = World.getSensorReading("ultraSonicSensorRight")
   WL = World.getSensorReading("ultraSonicSensorLeft")


   return;

# connect to the server
robot = World.init()
# print important parts of the robot
print(sorted(robot.keys()))

Counter = 0
Lspeed = 1;
Rspeed = 1;
PreTime = World.getSimulationTime()
CurrentState = 0
TCn = 0
FindingEnrgyCn = 0
FindWall = 0
while robot: # main Control loop
    #######################################################
    # Perception Phase: Get information about environment #
    #######################################################
    simulationTime = World.getSimulationTime()
    ElapsedTime = simulationTime - PreTime;

    if ElapsedTime > 1000:
        PreTime = simulationTime
        FindingEnrgyCn = FindingEnrgyCn +1
        TCn = TCn + 1
        Counter = Counter + 1






    if (FindingEnrgyCn > 10):
        FindingEnrgyCn = 0
        if(CurrentState == 0):
            #CurrentState = 1
            print("Random agent")
        else:
            #CurrentState = 0
            print("Memory agent")

    Bt = World.getSensorReading("energySensor")
    WL = World.getSensorReading("ultraSonicSensorLeft")
    WR = World.getSensorReading("ultraSonicSensorRight")

   # CurrentState = 3
    #Counter = 0
    if(CurrentState == 0):
        if(WL>0.3 and WR >0.3):
            run(WL, WR, Bt.direction)
        else:
            CurrentState = 1
            World.STOP()
            Tcn = 0
    elif(CurrentState == 1):
       Turn(WL,WR);
       WL = World.getSensorReading("ultraSonicSensorLeft")
       WR = World.getSensorReading("ultraSonicSensorRight")
       if(WL > 0.4 and WR > 0.4):
            TCn = 0
            CurrentState = 2
    elif(CurrentState == 2):
       if (WL > 0.3 and WR > 0.3):
         run(WL,WR,0)

         if(TCn >= 5):
             TCn = 0
             CurrentState = 0
       else:
             CurrentState = 1
             World.STOP()
             Tcn = 0
    elif (CurrentState == 3):
        RandomStrategy()

    if(Counter >= 20):
        Counter = 0
        if(CurrentState == 3):
            CurrentState = 0
        else:
            CurrentState = 3


    print(WL,WR)
    World.setMotorSpeeds(motorSpeed);
    if (Bt.distance < 0.3):
        World.collectNearestBlock()
        Counter = 0
        CurrentState = 0