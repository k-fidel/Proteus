# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!
import random
import time
import Lab1_Agents_Task1_World as World

# connect to the server
robot = World.init()
# print important parts of the robot

print(sorted(robot.keys()))

while robot:
    simulationTime = World.getSimulationTime()
    NT = World.getSensorReading("energySensor")
    if ( NT.direction > 0.2 ):
        motorSpeed = dict(speedLeft=1, speedRight=0)
        World.collectNearestBlock()
    elif(NT.direction < -0.2 ):
        motorSpeed = dict(speedLeft=0, speedRight=1)
        World.collectNearestBlock()

    else:
        motorSpeed = dict(speedLeft=1, speedRight=1)
        World.collectNearestBlock()

    if (NT.distance <0.2 ):
        motorSpeed = dict(speedLeft=0, speedRight=0)
        World.collectNearestBlock()

        print("collect a block...", BlockCn)
    WSL = World.getSensorReading("ultraSonicSensorLeft")
    WSR = World.getSensorReading("ultraSonicSensorRight")
    if (WSL < 0.4 and WSR > 0.4):
        World.collectNearestBlock()
        motorSpeed = dict(speedLeft=0, speedRight=1)
    elif (WSR < 0.4 and WSL >0.4):
        World.collectNearestBlock()
        motorSpeed = dict(speedLeft=1, speedRight=0)
        World.collectNearestBlock()
    elif (WSL <0.4 and WSR < 0.4):
        count = 0
        while (count < 6):
            World.collectNearestBlock()
            motorSpeed = dict(speedLeft=random.randint(-100, 100), speedRight=random.randint(-100, 100))
            World.collectNearestBlock()
            count = count + 1
        count = 0
    World.setMotorSpeeds(motorSpeed)
    # try to collect energy block (will fail if not within range)
    if simulationTime % 10000 == 0:
      print("Trying to collect a block...", World.collectNearestBlock())

