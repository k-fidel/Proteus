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

    motorSpeed = dict(speedLeft= random.randint(-1000, 1000), speedRight=random.randint(-1000, 1000))

    World.collectNearestBlock()


    #motorSpeed = dict(speedLeft=1, speedRight=2)
    World.setMotorSpeeds(motorSpeed)
    # try to collect energy block (will fail if not within range)
    if simulationTime % 10000 == 0:
        print("Trying to collect a block...", World.collectNearestBlock())
