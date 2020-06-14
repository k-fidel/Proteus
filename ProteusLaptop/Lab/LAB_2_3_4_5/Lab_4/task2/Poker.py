import json
from libpgm.graphskeleton import GraphSkeleton
from libpgm.pgmlearner import PGMLearner
import pickle

###################  loading data samples  ##############################################
pkl_file = open('Lab4_poker_data.txt', 'rb')
lines = pkl_file.readlines()
index =0
mdata = []   # Player1 data set
mdata2= []   # Player2 data set

td = {'HandStrength':'','Rank':'','AverageRaise':0,'Call':'','Fold':'','Allin':'','Coin':''}   # the list of attributes of player1
td2 = {'HandStrength':'','Rank':'','AverageRaise':0,'Call':'','Fold':'','Allin':'','Coin':''} # the list of attributes of player2





#################  parsing data samples and making a dict list for player1 and player2
for i in lines:
    dt = i.split(',')
    Ave = 0
    Ave2 = 0
    index = 0
    agent1R = agent2R = 0
    td['Allin'] = td['Fold'] = td['Call'] = 'No'
    td2['Allin'] = td2['Fold'] = td2['Call'] = 'No'
    for j in dt:
        if (j != ' \n'):
            d = j.split(' ')
            index +=1

            if(index == 2):
                td['HandStrength'] = d[1]
                td['Rank'] = d[2]
                td['Coin'] = d[3]
            elif(index == 3):
                td2['HandStrength'] =d[1]
                td2['Rank'] = d[2]
                td2['Coin'] = d[3]
            elif(index != 1):
                if ( d[1] == 'Raise'):
                  agent1R +=1
                  Ave  += int(d[2])
                elif( d[1] != '\n'):
                    td[d[1]] = 'Yes'
                if( d[3] == 'Raise'):
                    agent2R +=1
                    Ave2 +=int(d[4])
                elif ( d[3] !='\n'):
                    td2[d[3]] = 'Yes'

    if(agent2R == 0 ):
        td2['AverageRaise'] = 0
    else:
        td2['AverageRaise'] = Ave2/agent2R
    if (agent1R == 0 ):
        td['AverageRaise'] = 0
    else:
        td['AverageRaise'] = Ave/agent1R
    mdata.append(td.copy())
    mdata2.append(td2.copy())

####    computing the value of each attributes
for da in mdata,mdata2:
 for di in da:
    if(int(di['AverageRaise']) < 20):
        di['AverageRaise'] = 'Low'
    elif (int(di['AverageRaise'])<40):
        di['AverageRaise'] = 'Med'
    else:
        di['AverageRaise'] = 'High'

    if(int(di['Coin'])<100):
        di['Coin'] = 'Low'
    elif(int(di['Coin'])<300):
        di['Coin'] = 'Med'
    else:
        di['Coin'] = 'High'

    if(di['HandStrength'] == 'straightflush' or di['HandStrength'] == '4ofakind'):
        di['HandStrength'] = 'VeryStrong'
    elif(di['HandStrength'] == 'fullhouse' or di['HandStrength'] == 'flush' or (di['HandStrength'] == 'straight' and (di['Rank']=='J' or di['Rank']=='K' or di['Rank']=='Q' or di['Rank']=='A'))):
        di['HandStrength'] = 'Strong'
    elif(di['HandStrength'] == 'straight' or di['HandStrength']=='3ofakind'):
        di['HandStrength'] = 'Medium'
    elif(di['HandStrength'] == 'TwoPairs' or (di['HandStrength'] == 'OnePair' and (di['Rank'] == 'A' or di['Rank'] == 'K' or di['Rank'] == 'Q' or di['Rank'] == 'J'))):
        di['HandStrength'] = 'Weak'
    else:
        di['HandStrength'] = 'VeryWeak'
print ('###################    PART A    ################################')
print ('*************** Network Parameters for BN agent1*****************')
for skeleton in ["Poker_Network.txt"]:    # loading skeleton of Network from given-file
    skel = GraphSkeleton()
    skel.load(skeleton)
    learner = PGMLearner()
    result = learner.discrete_mle_estimateparams(skel, mdata)
    print json.dumps(result.Vdata, indent=2)

print ('*************** Network Parameters for BN agent2*****************')
for skeleton in ["Poker_Network.txt"]:
    skel = GraphSkeleton()
    skel.load(skeleton)
    learner = PGMLearner()
    result = learner.discrete_mle_estimateparams(skel, mdata2)
    print json.dumps(result.Vdata, indent=2)

print ('########################## PART B    ################################')
print ('**************  NB1 parameters for agent 1  *************************')
for skeleton in ["Poker_Network1.txt"]:
    skel = GraphSkeleton()
    skel.load(skeleton)
    learner = PGMLearner()
    result = learner.discrete_mle_estimateparams(skel, mdata)   # estimate Bayesian network parameter
    print json.dumps(result.Vdata, indent=2)

print ('*************** NB1 parameters for agent2*****************')
for skeleton in ["Poker_Network1.txt"]:
    skel = GraphSkeleton()
    skel.load(skeleton)
    learner = PGMLearner()
    result = learner.discrete_mle_estimateparams(skel, mdata2)
    print json.dumps(result.Vdata, indent=2)
print ('**************  NB2 parameters for agent 1  *************************')
for skeleton in ["Poker_Network2.txt"]:
    skel = GraphSkeleton()
    skel.load(skeleton)
    learner = PGMLearner()
    result = learner.discrete_mle_estimateparams(skel, mdata)
    print json.dumps(result.Vdata, indent=2)

print ('*************** NB2 parameters for agent2*****************')
for skeleton in ["Poker_Network2.txt"]:
    skel = GraphSkeleton()
    skel.load(skeleton)
    learner = PGMLearner()
    result = learner.discrete_mle_estimateparams(skel, mdata2)
    print json.dumps(result.Vdata, indent=2)
