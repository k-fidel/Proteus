
import Lab1_Agents_Task1_World as World
import random
robot = World.init()
print(sorted(robot.keys()))
while robot:
    simulationTime = World.getSimulationTime()
    if simulationTime % 1000 == 0:
        # print some useful info, but not too often
        print('Time:', simulationTime, \
              'ultraSonicSensorLeft:', World.getSensorReading("ultraSonicSensorLeft"), \
              "ultraSonicSensorRight:", World.getSensorReading("ultraSonicSensorRight"))

    motorSpeed = dict(speedLeft= random.randint(-100, 100), speedRight=random.randint(-100, 100))

    World.collectNearestBlock()

    World.setMotorSpeeds(motorSpeed)
    # try to collect energy block (will fail if not within range)
    if simulationTime % 10000 == 0:
        print("Trying to collect a block...", World.collectNearestBlock())
