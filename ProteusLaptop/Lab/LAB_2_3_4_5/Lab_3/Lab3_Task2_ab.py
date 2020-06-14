__author__ = 'Mohammad Mirian'

from pyDatalog import pyDatalog
import numpy as np

print "Task2 part a:"

List_agentHand = ['HighCard','OnePair', 'TwoPairs', 'ThreeOfKind','straight','flush', 'FullHouse','4ofakind', 'StraightFlush']

pyDatalog.create_terms('X,Y,playerStack,agentHand')

for i in range(len(List_agentHand)):
    + agentHand(List_agentHand[i])

###################      Create a KB  ########################################################
pyDatalog.create_terms('veryweakHand,weakHand, mediumHand, strongHand,verystrongHand,ultrastrongHand')
pyDatalog.create_terms('agentAction')

+ veryweakHand('HighCard')
+ weakHand('OnePair')
+ mediumHand('TwoPairs')
+ strongHand('ThreeOfKind')
+ strongHand('straight')
+ verystrongHand('flush')
+ verystrongHand('FullHouse')
+ ultrastrongHand('4ofakind')
+ ultrastrongHand('StraightFlush')



Stack_list = [100,50,30]              # define a list of stack for testing the strategy

for val in Stack_list:
    Stack = val

    if Stack>70:                    # define some different Stack levels
        playerStack[Stack] = 'Large'
    elif(Stack>35):
        playerStack[Stack] = 'Medium'
    else:
        playerStack[Stack] = 'Small'


    #######################  the Rules ##########################################################
    agentAction('Raise',X) <= (agentHand(X) & ultrastrongHand(X))
    agentAction('Raise',X) <= (agentHand(X) & verystrongHand(X))
    agentAction('Raise',X) <= (agentHand(X) & strongHand(X) & ~(playerStack[Stack] == 'Large'))

    agentAction('Call',X) <= (agentHand(X) & mediumHand(X) & (playerStack[Stack] == 'Small'))
    agentAction('Call',X) <= (agentHand(X) & strongHand(X) & (playerStack[Stack] == 'Large'))
    agentAction('Call',X) <= (agentHand(X) & mediumHand(X) & (playerStack[Stack] == 'Medium'))
    agentAction('Call',X) <=  (agentHand(X) & weakHand(X) &  (playerStack[Stack] == 'Small'))

    agentAction('Fold',X) <= (agentHand(X) & mediumHand(X) & (playerStack[Stack] == 'Large'))
    agentAction('Fold',X) <=  (agentHand(X) & weakHand(X) & ~(playerStack[Stack] == 'Small'))
    agentAction('Fold',X) <=  (agentHand(X) & weakHand(X))
    agentAction('Fold',X) <=  (agentHand(X) & veryweakHand(X))

    print '-----------------Stack-----------------'
    print Stack
    print('-----------------Raise-----------------')
    print(agentAction('Raise',X))
    print('-----------------Call (large stack)-----------------')
    print(agentAction('Call',X))
    print('-----------------Fold (large stack)-----------------')
    print(agentAction('Fold',X))

###################################################
print '--------------------------------------------'
print "Task2 part b:"

pyDatalog.create_terms('OppnentStack,oppenentHand,OppnentStack')
for i in range(len(List_agentHand)):
    + oppenentHand(List_agentHand[i])

OppStack = 100

if OppStack > 50:  # define some different Stack levels
    OppnentStack[OppStack] = 'Large'
else:
    OppnentStack[OppStack] = 'Small'

pyDatalog.create_terms('opponentAction')

opponentAction('Raise',Y,X) <= (agentAction('Raise',X) & (OppnentStack[OppStack] == 'Small')& oppenentHand(Y) & ultrastrongHand(Y))
opponentAction('Raise',Y,X) <= (agentAction('Raise',X) & (OppnentStack[OppStack] == 'Large')& oppenentHand(Y) & ultrastrongHand(Y))

opponentAction('Raise',Y,X) <= (agentAction('Raise',X) & (OppnentStack[OppStack] == 'Large')& oppenentHand(Y) & verystrongHand(Y))
opponentAction('Raise',Y,X) <= (agentAction('Raise',X) & (OppnentStack[OppStack] == 'Small')& oppenentHand(Y) & verystrongHand(Y))
opponentAction('Raise',Y,X) <= (agentAction('Raise',X) &   (OppnentStack[OppStack] == 'Small')& oppenentHand(Y) & strongHand(Y) & ~(playerStack[Stack] == 'Small'))

opponentAction('Call',Y,X) <= (agentAction('Raise',X) &   (OppnentStack[OppStack] == 'Small')& oppenentHand(Y) & strongHand(Y) & (playerStack[Stack] == 'Small'))
opponentAction('Call',Y,X) <= (agentAction('Raise',X) & (OppnentStack[OppStack] == 'Large')& oppenentHand(Y) & strongHand(Y) & (playerStack[Stack] == 'Large'))
opponentAction('Call',Y,X) <= (agentAction('Raise',X) & (OppnentStack[OppStack] == 'Large')& oppenentHand(Y) & mediumHand(Y) & (playerStack[Stack] == 'Large'))

opponentAction('Raise',Y) <= (agentAction('Raise',X) & (OppnentStack[OppStack] == 'Small')& oppenentHand(Y) & mediumHand(Y) & ~(playerStack[Stack] == 'Large'))
opponentAction('Fold',Y,X) <= (agentAction('Raise',X) & (OppnentStack[OppStack] == 'Large')& oppenentHand(Y) & mediumHand(Y) & ~(playerStack[Stack] == 'Large'))
opponentAction('Call',Y,X) <= (agentAction('Raise',X) & (OppnentStack[OppStack] == 'Small')& oppenentHand(Y) & mediumHand(Y) & (playerStack[Stack] == 'Large'))
opponentAction('Fold',Y) <= (agentAction('Raise',X) & (OppnentStack[OppStack] == 'Large')& oppenentHand(Y) & mediumHand(Y))
opponentAction('Fold',Y) <= (agentAction('Raise',X) & (OppnentStack[OppStack] == 'Small')& oppenentHand(Y) & mediumHand(Y) & (playerStack[Stack] == 'Large'))


opponentAction('Fold',Y) <= (agentAction('Raise',X) & (OppnentStack[OppStack] == 'Large')& oppenentHand(Y) & weakHand(Y))
opponentAction('Fold',Y) <= (agentAction('Raise',X) & (OppnentStack[OppStack] == 'Large')& oppenentHand(Y) & veryweakHand(Y))
opponentAction('Fold',Y) <= (agentAction('Raise',X) & (OppnentStack[OppStack] == 'Small')& oppenentHand(Y) & weakHand(Y))
opponentAction('Fold',Y) <= (agentAction('Raise',X) & (OppnentStack[OppStack] == 'Small')& oppenentHand(Y) & veryweakHand(Y))

print('---------- Raise --------------')
print  (opponentAction('Raise',Y,X))
print('---------- Call --------------')
print  (opponentAction('Call',Y,X))
print('---------- Fold --------------')
print  (opponentAction('Fold',Y,X))