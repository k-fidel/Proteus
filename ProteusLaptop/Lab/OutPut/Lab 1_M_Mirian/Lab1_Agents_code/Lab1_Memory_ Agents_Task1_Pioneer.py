
import random
import enum
import math
import Lab1_Agents_Task1_World as World

def Turn(Leftdis,Rightdis):
    global Rightspeed,Lspeed
    global motorSpeed;
    Rspeed = Leftspeed = 0
    motorSpeed = dict(speedLeft=Leftspeed, speedRight=Rightspeed)
    World.setMotorSpeeds(motorSpeed)
    if(Rightdis >= Leftdis):
        Leftspeed = 0
        Rightspeed = -1
    else:
        Leftspeed = -1
        Rightspeed = 0

    motorSpeed = dict(speedLeft=Leftspeed, speedRight=Rightspeed)
    World.execute(motorSpeed, 2000, -1)
    return;

def run(Ldis,Rdis,TP):
    global PLdis, PRdis
    global FindWall, FindingEnrgyCn
    global motorSpeed
    global Leftspeed, Rightspeed

    if (TP < 0.2 and TP > -0.2):
        Rightspeed = Leftspeed = 2
    if(TP>=0.2):
        Rightspeed = 0
        Leftspeed = 1
    if(TP<=-0.2):
        Leftspeed = 0
        Rightspeed = 1
    motorSpeed = dict(speedLeft=Leftspeed, speedRight=Rightspeed)

    return




def RandomStrategy():
    ESensor = World.getSensorReading("energySensor")
    LSensor = World.getSensorReading("ultraSonicSensorLeft")
    RSensor = World.getSensorReading("ultraSonicSensorRight")
    global motorSpeed,Leftspeed,Rightspeed
    if(LSensor > 0.3 and RSensor > 0.3):
       Leftspeed = random.uniform(2, 10)
       Rightspeed = Leftspeed # random.uniform(0, 10)

    elif(RSensor<0.3):
       Leftspeed = 0
       Rightspeed = -random.uniform(2, 10)

    elif(LSensor  <0.3):
        Leftspeed = -random.uniform(2, 10)
        Rightspeed = 0

    motorSpeed = dict(speedLeft=Leftspeed, speedRight=Rightspeed)
    World.setMotorSpeeds(motorSpeed)
    return

robot = World.init()
# print important parts of the robot
print(sorted(robot.keys()))

Counter = 0
Leftspeed = 1
Rightspeed = 1
PreTime = World.getSimulationTime()
CurrentState = 0
TCn = 0
FindingEnrgyCn = 0
FindWall = 0
while robot:
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

    if(CurrentState == 0):
        ESensor = World.getSensorReading("energySensor")
        LSensor = World.getSensorReading("ultraSonicSensorLeft")
        RSensor = World.getSensorReading("ultraSonicSensorRight")
        if(LSensor>0.3 and RSensor >0.3):
            run(LSensor, RSensor, ESensor.direction)
        else:
            CurrentState = 1
            World.STOP()
            Timer = 0
    elif(CurrentState == 1):
       Turn(LSensor, RSensor)

       if(LSensor > 0.4 and RSensor > 0.4):
          Timer = 0
          CurrentState = 2
    elif(CurrentState == 2):
       if (LSensor > 0.3 and RSensor > 0.3):
         run(LSensor, RSensor, 0)

         if(Timer >= 5):
             Timer = 0
             CurrentState = 0
       else:
             CurrentState = 1
             World.STOP()
             Timer = 0
    elif (CurrentState == 3):
        RandomStrategy()

    if(Counter >= 20):
        Counter = 0
        if(CurrentState == 3):
            CurrentState = 0
        else:
            CurrentState = 3


    print(LSensor,RSensor)
    World.setMotorSpeeds(motorSpeed)
    if (ESensor.distance < 0.3):
        World.collectNearestBlock()
        Counter = 0
        CurrentState = 0