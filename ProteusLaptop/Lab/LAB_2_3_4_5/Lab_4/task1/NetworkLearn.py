import json
from libpgm.graphskeleton import GraphSkeleton
from libpgm.pgmlearner import PGMLearner
import pickle

pkl_file = open('Data_Sample.pkl', 'rb')
datafile = pickle.load(pkl_file)
pkl_file.close()
data = datafile

# instantiate my learner
learner = PGMLearner()

# estimate parameters
result = learner.discrete_estimatebn(data)

print ('*************** Network Parameters for BN1 *****************')
for skeleton in ["Network_skeleton_1.txt"]:
    skel = GraphSkeleton()
    skel.load(skeleton)
    learner = PGMLearner()
    result = learner.discrete_mle_estimateparams(skel, data)
    print json.dumps(result.Vdata, indent=2)

print ('*************** Network Edges *****************')
print json.dumps(result.E, indent=2)

print ('*************** Overload conditional probability *****************')
print result.Vdata["Outage_Duration"]["cprob"]

print ('*************** Network Parameters for BN2*****************')
for skeleton in ["Network_skeleton_2.txt"]:
    skel = GraphSkeleton()
    skel.load(skeleton)
    learner = PGMLearner()
    result = learner.discrete_mle_estimateparams(skel, data)
    print json.dumps(result.Vdata, indent=2)

print ('*************** Network Edges *****************')
print json.dumps(result.E, indent=2)

print ('*************** Overload conditional probability *****************')
print result.Vdata["Outage_Duration"]["cprob"]


############## Task2 Part B ############## The optimal BN  ################################

net = learner.discrete_constraint_estimatestruct(data)
print net.E

result = learner.discrete_mle_estimateparams(net, data)
print ('*************** Network Edges *****************')
print json.dumps(result.Vdata, indent=2)