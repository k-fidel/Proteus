__author__ = 'Mohammad Mirian'
from pyDatalog import pyDatalog
import numpy as np

data = np.load('SmartHomeData.npy')    # Load the recorded data of smart house

print "Task 1 part a:"

Sensor_List = ['EnterHome', 'OutHome', 'InBed', 'OutBed', 'OnChairBed', 'OutChairBed', 'OnChairKitchen', 'OutChairKitchen',
               'Hallway', 'Kitchen', 'Bathroom', 'Bedroom', 'OpenDrawer', 'CloseDrawer', 'WaterOn',
               'WaterOff', 'CabinetOn', 'CabinetOff']



pyDatalog.create_terms('X, Y, Z,K, sensor')


###################              Generate KB for the smart house
for d in range(0,1010):
    for t in range(60):
        for sn in range(18):                                # the number of sensor
            if( data[sn][t][d] == 1):                       # check which sensor in time t and in day d is active?
                + sensor(Sensor_List[sn],"%s" %d,"%s" %t)  # make the smart house KB

pyDatalog.create_terms('nextNr,dayNumber,greater,smaller')
for nr in range(60):
    + nextNr("%s" %nr, "%s" %(nr+1))

for dn in range(1010):
    + dayNumber("%s" %dn)

for nr1 in range(60):
    for nr2 in range(60):
        if nr1>nr2:
            + greater("%s" %nr1, "%s" %nr2)
        if nr1<nr2:
            + smaller("%s" %nr1, "%s" %nr2)



pyDatalog.create_terms('outofHome2,wakeUpAt, inBathroom,inBedroom, inKitchen, outofHome,sleep,intoHome')
inBedroom(Y,X) <=  sensor('Bedroom', Y,X)
wakeUpAt(Y,X) <=   sensor('OutBed',Y,X)
inKitchen(Y,X) <=  sensor('Kitchen', Y,X)
inBathroom(Y,X) <= sensor('Bathroom',Y,X)
outofHome(Y) <= sensor('OutHome',Y,X)
outofHome2(Y,X) <= sensor('OutHome',Y,X)
sleep(Y,X) <= sensor('InBed',Y,X)
intoHome(Y,X) <= sensor('EnterHome',Y,X)
pyDatalog.create_terms('kitchenToOutHome,kitchenToBathroom,intoHomeToBedroom,bathroomToBedroom,bedroomToSleep,outHomeToinHome,bedroomToOutHome,bedroomToKitchen,kitchenToBedroom,wakeupToBathroom,bathroomToKitchen,bathroomToBedroom,kitchenTooutofHome,wakeupToBathToKitchen,dailyRoutine')

bedroomToSleep(Y,Z)<= (inBedroom(Y,X) & sleep(Y,Z) & nextNr(X,Z))
outHomeToinHome(Y,Z) <= outofHome2(Y,X) & intoHome(Y,Z) & greater(Z,X)
bedroomToOutHome(Y,Z) <= (inBedroom(Y,X) & outofHome2(Y,Z) & nextNr(X,Z))
bedroomToKitchen(Y,Z) <= (inBedroom(Y,X) & inKitchen(Y,Z) & nextNr(X,Z))
wakeupToBathroom(Y,Z)  <= (inBedroom(Y,X) & inBathroom(Y,Z) & nextNr(X,Z))     # wake up first and then went to the Bathroom
bathroomToKitchen(Y,Z) <= (inBathroom(Y,X) & inKitchen(Y,Z) & nextNr(X,Z))     # left the bathroom and went to the kitchen
bathroomToBedroom(Y,Z) <= (inBathroom(Y,X) & inBedroom(Y,Z) & nextNr(X,Z))
kitchenToBedroom(Y,Z)   <= (inKitchen(Y,X) & inBedroom(Y,Z) & nextNr(X,Z))    # left the kitchen and went to the bedroom
kitchenToBathroom(Y,Z) <= inKitchen(Y,X) & inBathroom(Y,Z) & nextNr(X,Z)
intoHomeToBedroom(Y,Z)  <=  intoHome(Y,X) & inBedroom(Y,Z) & nextNr(X,Z)
kitchenToOutHome(Y,Z) <= inKitchen(Y,X) & outofHome2(Y,Z) & nextNr(X,Z)
wakeupToBathToKitchen(Y,Z) <= wakeupToBathroom(Y,X) & bathroomToKitchen(Y,Z) & greater(Z,X)  # Wake up -> bathroom -> kitchen


pyDatalog.create_terms('bedroomToKitchenToOutHome,bedroomToBathTokitchen,bedroomTokitchenToBathroom,bedRoomKitBedOutHome,dailyRoutine3,dailyRoutine4,dailyRoutine2,bedroomToKitchenToBedroom')
bedroomToKitchenToBedroom(Y,Z) <= bedroomToKitchen(Y,X) & kitchenToBedroom(Y,Z) & greater(Z,X)
bedroomTokitchenToBathroom(Y,Z) <= bedroomToKitchen(Y,X) & kitchenToBathroom(Y,Z)  & greater(Z,X)
bedroomToBathTokitchen(Y,Z) <= wakeupToBathroom(Y,X) & bathroomToKitchen(Y,Z) & greater(Z,X)
bedroomToKitchenToOutHome(Y,Z) <= bedroomToKitchen(Y,X) & kitchenToOutHome(Y,Z) & greater(Z,X)


########################   4 daily routines  #####################################################
dailyRoutine(Y) <= wakeupToBathToKitchen(Y,X) &  kitchenToBedroom(Y,Z) & ~outofHome(Y) & greater(Z,X) # Wake up -> bathroom -> kitchen -> bedroom  and stay at home
dailyRoutine2(Y) <= bedroomToKitchenToOutHome(Y,X) & intoHomeToBedroom(Y,Z) & greater(Z,X)
dailyRoutine3(Y)<= bedroomToOutHome(Y,X) & intoHomeToBedroom(Y,Z) & sleep(Y,K) & greater(Z,X)& greater(K,Z)#
dailyRoutine4(Y)<= wakeupToBathroom(Y,X) & bathroomToBedroom(Y,Z) & sleep(Y,K) & greater(Z,X) & greater(K,Z) & ~outofHome(Y) & ~inKitchen(Y,K)#
#################################################################################################

print 'kitchen -> outHome'+str(len(kitchenToOutHome(Y,Z)))
print 'bedRoom -> Sleep : '+ str(len(bedroomToSleep(Y,Z)))
print 'outHome -> inHome : '+ str(len(outHomeToinHome(Y,Z)))
print 'BedRoom -> outHome : '+ str(len(bedroomToOutHome(Y,Z)))
print 'BedRoom -> Kitchen : '+ str(len(bedroomToKitchen(Y,Z)))

print 'Wakeup -> Bathroom : '+ str(len(wakeupToBathroom(Y,Z)))
print 'Bathroom -> Kitchen : '+str(len(bathroomToKitchen(Y,Z)))
print 'Kitchen -> Bedroom : '+str(len(kitchenToBedroom(Y,Z)))
print 'Wakeup -> Bathroom -> Kitchen : '+str(len(wakeupToBathToKitchen(Y,Z)))
print "The number of this daily routine(wakeup-> bath -> kitchen-> bedroom) :" +str(len(dailyRoutine(Y)))
print 'The number of this daily routine2(Bedroom->Kitchen->goout->goIn->bedroom) :'+str(len(dailyRoutine2(Y)))
print 'The number of this daily routine3(Bedroom->goOut->goIn->bedroom->goToBed) :'+str(len(dailyRoutine3(Y)))
print 'The number of this daily routine4(Bedroom->Bath->Beedroom->sleep) :'+str(len(dailyRoutine4(Y)))

#####################   Part B ###################################
print "####################################################"
print "Task1 Part b :"

### Rule 1 ###############  HallWay Sensor doesn't work
pyDatalog.create_terms('inHallway,wentOutThroughHall')
inHallway(Y) <= sensor('Hallway',Y,X)
wentOutThroughHall (Y) <= dayNumber(Y) & ~inHallway(Y) & outofHome(Y)    # went out without activation the hallway sensor
print "He has gone out " + str(len(wentOutThroughHall (Y))) +" times but the Hall Sensor has never activated."
print "The Hall way sensor has been activated " + str(len(inHallway(Y))) +" times."

### Rule 2 ############  The kitchen chair has never been used #########
pyDatalog.create_terms('onKitChair,outKitChair,usingKitChair')
onKitChair(Y,X) <= sensor('OnChairKitchen',Y,X)
outKitChair(Y,X) <= sensor('OutChairKitchen',Y,X)

usingKitChair(Y) <= dayNumber(Y) & onKitChair(Y,X) & outKitChair(Y,Z) & nextNr(Z,X)
print "The kitchen chair has been used "+str(len(usingKitChair(Y))) + " times."
print len(onKitChair(Y,X))
print len(outKitChair(Y,X))

### Rule 3 ###########  The bed chair has never been used ##############
pyDatalog.create_terms('onBedChair,outBedChair,usingBedChair')
onBedChair(Y,X) <= sensor('OnChairBed',Y,X)
outBedChair(Y,X) <= sensor('OutChairBed',Y,X)

usingBedChair(Y) <= dayNumber(Y) & onBedChair(Y,X) & outBedChair(Y,Z) & nextNr(Z,X)
print "The bed chair has been used "+str(len(usingKitChair(Y))) + " times."
print len(onKitChair(Y,X))
print len(outKitChair(Y,X))

### Rule 4 ############ The cabinet's door has been opened but has never been closed ######
pyDatalog.create_terms('onCabinet,offCabinet,cabinetOnButneverOFF')
onCabinet(Y,X) <= sensor('CabinetOn',Y,X)
offCabinet(Y,X) <= sensor('CabinetOff',Y,X)


cabinetOnButneverOFF(Y) <=  dayNumber(Y) & onCabinet(Y,X) & ~offCabinet(Y,Z)

print cabinetOnButneverOFF(Y)
print "The cabinet's door has been opened in the day "+str(Y.data)

### Rule 5 ############ The kettle has never been used

pyDatalog.create_terms('onWater,offWater,usingKettle')
onWater(Y,X) <= sensor('WaterOn',Y,X)
offWater(Y,X) <= sensor('WaterOff',Y,X)


usingKettle(Y) <=  dayNumber(Y) & onWater(Y,X) & offWater(Y,Z)

print usingKettle(Y)
print "The kettle has been used "+str(len(usingKettle(Y)))+" times."


### Rule 6 ############
pyDatalog.create_terms('closeDrawer,openDrawer,openDrawerClose')
openDrawer(Y,X) <= sensor('OpenDrawer',Y,X)
closeDrawer(Y,X) <= sensor('CloseDrawer',Y,X)


openDrawerClose(Y) <=  dayNumber(Y) & openDrawer(Y,X) & ~closeDrawer(Y,Z)

print openDrawerClose(Y)
print "The drawer has been opened in the day "+str(Y.data)+" but has never been closed!"






