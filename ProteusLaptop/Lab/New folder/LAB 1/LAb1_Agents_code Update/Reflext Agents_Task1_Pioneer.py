# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!
import random
import time
import Lab1_Agents_Task1_World as World

# connect to the server
robot = World.init()
# print important parts of the robot

print(sorted(robot.keys()))

while robot:  # main Control loop
    #######################################################
    # Perception Phase: Get information about environment #
    #######################################################
    simulationTime = World.getSimulationTime()
    if simulationTime % 1000 == 0:
        # print some useful info, but not too often
        print('Time:', simulationTime, \
              'ultraSonicSensorLeft:', World.getSensorReading("ultraSonicSensorLeft"), \
              "ultraSonicSensorRight:", World.getSensorReading("ultraSonicSensorRight"))

    # NT = NearestTarget
    NT = World.getSensorReading("energySensor")
    if ( NT.direction > 0.2 ):
        World.collectNearestBlock()
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
    WSL = World.getSensorReading("ultraSonicSensorLeft")
    WSR = World.getSensorReading("ultraSonicSensorRight")
    if (WSL < 0.4 and WSR > 0.4):
        motorSpeed = dict(speedLeft=0, speedRight=1)
    elif (WSR < 0.4 and WSL >0.4):
        motorSpeed = dict(speedLeft=1, speedRight=0)
    #elif (WSR == WSL):
     #   motorSpeed = dict(speedLeft=-2, speedRight=-2)
    elif (WSL <0.4 and WSR < 0.4):

        count = 0
        while (count < 3):
            World.collectNearestBlock()
            motorSpeed = dict(speedLeft=random.randint(-1000, 1000), speedRight=random.randint(-1000, 1000))
            count = count + 1
        count = 0
    World.setMotorSpeeds(motorSpeed)
    # try to collect energy block (will fail if not within range)
    if simulationTime % 10000 == 0:
        print("Trying to collect a block...", World.collectNearestBlock())
