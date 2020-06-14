# Make sure to have the server side running in V-REP:
# in a child script of a V-REP scene, add following command
# to be executed just once, at simulation start:
#
# simExtRemoteApiStart(19999)
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!
import Lab1_Agents_Task1_World as World
import time

# connect to the server
robot = World.init()
# print important parts of the robot
print(sorted(robot.keys()))

while robot: # main Control loop
    #######################################################
    # Perception Phase: Get information about environment #
    #######################################################
    simulationTime = World.getSimulationTime()
    if simulationTime%1000==0:
        # print some useful info, but not too often
        print 'Time:',simulationTime,\
              'ultraSonicSensorLeft:',World.getSensorReading("ultraSonicSensorLeft"),\
              "ultraSonicSensorRight:", World.getSensorReading("ultraSonicSensorRight")

        World.collectNearestBlock()
        # ========================================================================
        #                     =>>> turn moving forward
        tim = 0
        while (tim < 3):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=1, speedRight=1), 2000, -1)
            World.collectNearestBlock()

            tim = tim + 1

        # =>>> turn Right (1)
        tim = 0
        while (tim < 2):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=0, speedRight=1), 2350, -1)
            World.collectNearestBlock()

            tim = tim + 1

        # >>>>> move forward
        tim = 0
        while (tim < 5):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=1, speedRight=1), 3100, -1)
            World.collectNearestBlock()
            tim = tim + 1
        # >>>>> move backward

        tim = 0
        while (tim < 5):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=-1, speedRight=-1), 3100, -1)
            World.collectNearestBlock()
            tim = tim + 1

        # =>>> turn left (1)
        tim = 0
        while (tim < 2):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=0, speedRight=-1), 2370, -1)
            World.collectNearestBlock()
            tim = tim + 1

        # >>>>> move forward
        tim = 0
        while (tim < 5):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=1, speedRight=1), 3500, -1)  # move forward
            World.collectNearestBlock()
            tim = tim + 1
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #                     =>>> turn Right (1)
        tim = 0
        while (tim < 2):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=0, speedRight=1), 2380, -1)
            World.collectNearestBlock()

            tim = tim + 1

        # >>>>> move forward
        tim = 0
        while (tim < 4):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=1, speedRight=1), 3200, -1)
            World.collectNearestBlock()
            tim = tim + 1

        # =>>> turn Left (1)
        tim = 0
        while (tim < 2):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=1, speedRight=0), 2400, -1)
            World.collectNearestBlock()

            tim = tim + 1

        # >>>>> move forward
        tim = 0
        while (tim < 4):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=1, speedRight=1), 3200, -1)
            World.collectNearestBlock()
            tim = tim + 1

        # =>>> turn Right (1)
        tim = 0
        while (tim < 2):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=0, speedRight=1), 2650, -1)
            World.collectNearestBlock()

            tim = tim + 1

        # >>>>> move forward
        tim = 0
        while (tim < 4):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=1, speedRight=1), 3300, -1)
            World.collectNearestBlock()
            tim = tim + 1

        # =>>> turn Right (1)
        tim = 0
        while (tim < 2):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=0, speedRight=1), 2550, -1)
            World.collectNearestBlock()

            tim = tim + 1

        # >>>>> move forward
        tim = 0
        while (tim < 5):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=1, speedRight=1), 3100, -1)
            World.collectNearestBlock()
            tim = tim + 1
            # ---------------------------------------------------------------
        #                   >>>>> move backward
        tim = 0
        while (tim < 4):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=-1, speedRight=-1), 3100, -1)
            World.collectNearestBlock()
            tim = tim + 1

        # =>>> turn left (1)
        tim = 0
        while (tim < 2):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=0, speedRight=-1), 2600, -1)
            World.collectNearestBlock()

            tim = tim + 1

        # >>>>> move backward
        tim = 0
        while (tim < 3):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=-1, speedRight=-1), 3100, -1)
            World.collectNearestBlock()
            tim = tim + 1

        # =>>> turn left (1)
        tim = 0
        while (tim < 2):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=0, speedRight=-1), 2600, -1)
            World.collectNearestBlock()

            tim = tim + 1

        # >>>>> move backward
        tim = 0
        while (tim < 3):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=-1, speedRight=-1), 3000, -1)
            World.collectNearestBlock()
            tim = tim + 1

        # =>>> turn Right (1)
        tim = 0
        while (tim < 2):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=-1, speedRight=0), 2550, -1)
            World.collectNearestBlock()

            tim = tim + 1

        # >>>>> move backward
        tim = 0
        while (tim < 4):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=-1, speedRight=-1), 3400, -1)
            World.collectNearestBlock()
            tim = tim + 1
        # =>>> turn left (1)
        tim = 0
        while (tim < 2):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=0, speedRight=-1), 2690, -1)
            World.collectNearestBlock()

            tim = tim + 1

        # ----------------

        #                   >>>>> move forward
        tim = 0
        while (tim < 7):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=1, speedRight=1), 4000, -1)
            World.collectNearestBlock()
            tim = tim + 1
        # =>>> Turn right
        tim = 0
        while (tim < 2):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=0, speedRight=1), 2700, -1)
            World.collectNearestBlock()
            tim = tim + 1
        # >>>>> move forward
        tim = 0
        while (tim < 16):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=1, speedRight=1), 3300, -1)
            World.collectNearestBlock()
            tim = tim + 1

        # =>>> Turn right
        tim = 0
        while (tim < 2):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=0, speedRight=1), 2650, -1)
            World.collectNearestBlock()

            tim = tim + 1

        # >>>>> move forward
        tim = 0
        while (tim < 8):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=1, speedRight=1), 3450, -1)
            World.collectNearestBlock()
            tim = tim + 1
        # =>>> Turn left
        tim = 0
        while (tim < 2):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=0, speedRight=1), 2700, -1)
            World.collectNearestBlock()
            tim = tim + 1

        # >>>>> move forward
        tim = 0
        while (tim < 3):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=1, speedRight=1), 2000, -1)
            World.collectNearestBlock()
            tim = tim + 1
        # <<<= Turn left
        tim = 0
        while (tim < 2):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=1, speedRight=0), 2700, -1)  # turn Right (4)
            World.collectNearestBlock()
            tim = tim + 1
        # >>>>> move forward
        tim = 0
        while (tim < 4):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=1, speedRight=1), 3000, -1)
            World.collectNearestBlock()
            tim = tim + 1
        # =>>> Turn left
        tim = 0
        while (tim < 2):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=0, speedRight=1), 2700, -1)
            World.collectNearestBlock()
            tim = tim + 1
        # >>>>> move forward
        tim = 0
        while (tim < 4):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=1, speedRight=1), 4000, -1)
            World.collectNearestBlock()
            tim = tim + 1
        # >>>>> move backward
        tim = 0
        while (tim < 4):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=-1, speedRight=-1), 4000, -1)
            World.collectNearestBlock()
            tim = tim + 1

        # =>>> Turn left
        tim = 0
        while (tim < 2):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=1, speedRight=0), 2700, -1)
            World.collectNearestBlock()
            tim = tim + 1

        # >>>>> move Forward
        tim = 0
        while (tim < 5):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=1, speedRight=1), 2000, -1)
            World.collectNearestBlock()
            tim = tim + 1
        # =>>> Turn left
        tim = 0
        while (tim < 2):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=0, speedRight=1), 2700, -1)
            World.collectNearestBlock()
            tim = tim + 1

        # >>>>> move Forward
        tim = 0
        while (tim < 12):
            World.collectNearestBlock()
            World.execute(dict(speedLeft=1, speedRight=1), 3000, -1)
            World.collectNearestBlock()
            tim = tim + 1

        World.STOP()














    '''##############################################
    # Reasoning: figure out which action to take #
    ##############################################
    if simulationTime<5000:
        motorSpeed = dict(speedLeft=1, speedRight=1.5)
    elif simulationTime<10000:
        motorSpeed = dict(speedLeft=-1.5, speedRight=-1.0)
    elif simulationTime<15000:
        print "Turning for a bit...",
        World.execute(dict(speedLeft=2, speedRight=-2),15000,-1)
        print "... got dizzy, stopping!"
        print "BTW, nearest energy block is at:",World.getSensorReading("energySensor")
    else:
        motorSpeed = dict(speedLeft=0, speedRight=0)
        
    ########################################
    # Action Phase: Assign speed to wheels #
    ########################################
    # assign speed to the wheels
    World.setMotorSpeeds(motorSpeed)'''''
    # try to collect energy block (will fail if not within range)
    if simulationTime%10000==0:
        print "Trying to collect a block...",World.collectNearestBlock()
