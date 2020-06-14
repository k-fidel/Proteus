import math
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from operator import itemgetter
from collections import Counter
from sklearn.linear_model import SGDClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.datasets import load_iris
from sklearn import tree
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing
############################################################################
# Functions for K-NN   Part A
#---------------------------------------------------------------------------

# calculate the euclidean distance between instance1 and instance2 as inputs
def get_euclideanDistance(instance1, instance2):
    points = zip(instance1, instance2)
    squared_distance = [pow(a - b, 2) for (a, b) in points]
    sumSqDis = sum(squared_distance)
    return math.sqrt(sumSqDis)   # return the distance

# calculate the Manhattan distance between instance1 and instance2 as inputs
def get_manhattanDistance(instance1, instance2):
    points = zip(instance1, instance2)
    squared_distance = [abs(a - b) for (a, b) in points]
    sumSqDis = sum(squared_distance)
    return math.sqrt(sumSqDis)   # return the distance

#########  finding the k nearest distance
def get_neighbours(training_set,train_Target, test_instance, k , distance_method):  # return the k nearest distance

    # calculate distance between training_instance and test_instance and return distance and train_target that point for each distance
    distances = [_get_tuple_distance(train_Target[idx],training_instance, test_instance,distance_method) for idx,training_instance in enumerate(training_set)]

    sorted_distances = sorted(distances, key=itemgetter(1))  # sort the distance vector to find k nearest neighbour

    sorted_training_instances = [tuple[0] for tuple in sorted_distances]  # extract only training instances

    return sorted_training_instances[:k]      # select first k elements


def get_Regressorneighbours(training_set,train_Target, test_instance, k , distance_method):  # return the k nearest distance

    # calculate distance between training_instance and test_instance and return distance and train_target that point for each distance
    distances = [_get_tuple_distance(train_Target[idx],training_instance, test_instance,distance_method) for idx,training_instance in enumerate(training_set)]

    sorted_distances = sorted(distances, key=itemgetter(1))  # sort the distance vector to find k nearest neighbour

    sorted_training_instances = [tuple[1] for tuple in sorted_distances]  # extract only training instances

    return sorted_training_instances[:k]      # select first k elements


def _get_tuple_distance(Trainig_Target,training_instance, test_instance,distance_method):  # create a vector include of the training_target and distance between the test instance and the training point
    if distance_method == 'Eculidean':
        return (Trainig_Target, get_euclideanDistance(test_instance, training_instance))
    elif ( distance_method == 'Manhattan'):
        return (Trainig_Target, get_manhattanDistance(test_instance, training_instance))

def getRegressionPredict(neighbours):

    return  sum(neighbours)/len(neighbours)

###########  calculate the RMS of error
def getRMSE(Target_test, predictions):
    err = []
    for i in range(len(Target_test)):
        err.append(math.pow((Target_test[i]-predictions[i]),2))
    return math.sqrt(sum(err)/len(Target_test))

############ make decision and predict the target
def getResponse(neighbours):

    classes = [neighbour for neighbour in neighbours]
    count = Counter(classes)    # count each classes
    return count.most_common()[0][0]  # select the most and return the prediction

##########  calculate the accuracy of model  ##################
def getAccuracy(Target_test, predictions):
	correct = 0
	for x in range(len(Target_test)):
		if Target_test[x] == predictions[x]:    # checking the correctness of predictions
			correct += 1
	return (correct/float(len(Target_test))) * 100.0

##########################################################################
##############################Main########################################
Data = np.loadtxt(open("Lab5Data.csv", "rb"), delimiter=";", skiprows=1)
print ('*******************************************')
print('Length of Total Data:', len(Data))
Input_data = Data[:,:9]
Target_data = Data[:,9]
Input_data_Scaled = preprocessing.minmax_scale(Input_data)

Train_set, Test_set = train_test_split(Data, test_size=0.2)

Input_train = Train_set[:, :9]  # input features
Target_train = Train_set[:, 9]  # output labels
Input_train_Scaled = preprocessing.minmax_scale(Input_train) # scalee the inputs train



Input_test = Test_set[:, :9]
Target_test = Test_set[:, 9]
Input_test_Scaled = preprocessing.minmax_scale(Input_test)   # scale the inputs test



print ('*****************Part A*******************')
print('Length of Train Data:', len(Train_set))
print('Length of Test Data', len(Test_set))

# generate predictions list
predictions = []

k=5
for x in range(len(Target_test)):
    #print 'Classifying test instance number ' + str(x) + ":",
    distance_method = "Eculidean"
    neighbours = get_neighbours(Input_train_Scaled, Target_train, Input_test_Scaled[x, :], k,distance_method)
    majority_vote = getResponse(neighbours)
    predictions.append(majority_vote)
    #print 'Predicted label=' + str(majority_vote) + ', Actual label=' + str(Target_test[x])

    # summarize performance of the classification
print '\n\n********  KNN Classifier ******************************'
print '\nThe overall accuracy of the model with K='+str(k)+' is: ' + str(getAccuracy(Target_test, predictions)) + "%\n"
report = classification_report(Target_test, predictions)
print 'A detailed classification report: \n\n' + report


#########################################################################
####        PART B               ########################################
print ('****************************************************************')
print ('****  SGC Classifier *******************************************')

clf = SGDClassifier(loss="log", penalty="l2")
clf.fit(Input_train, Target_train)
PredictedOutcome = clf.predict(Input_test)
Number_of_Correct_Predictions = len([i for i, j in zip(PredictedOutcome, Target_test) if i == j])

print ('\n\n*************************************************************')
print('Number of Correct Predictions:', Number_of_Correct_Predictions, 'Out_of:', len(PredictedOutcome),
      'Number of Test Data')
print('Accuracy of Prediction in Percent:', (Number_of_Correct_Predictions/float(len(PredictedOutcome)))*100)
##
print ('\n\n*****************************************************************')
print ('****  LDA Classifier     ********************************************')
clf1 = LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto').fit(Input_train, Target_train)
PredictedOutcome = clf.predict(Input_test)
Number_of_Correct_Predictions = len([i for i, j in zip(PredictedOutcome, Target_test) if i == j])

print ('**********************************************************************')
print('Number of Correct Predictions:', Number_of_Correct_Predictions, 'Out_of:', len(PredictedOutcome),
      'Number of Test Data')
print('Accuracy of Prediction in Percent:', (Number_of_Correct_Predictions/float(len(PredictedOutcome)))*100)
##
print '\n\n************************************************************************'
print ('****  Decision Tree      **************************************************')
clf = tree.DecisionTreeClassifier()
clf = clf.fit(Input_train, Target_train)
PredictedOutcome = clf.predict(Input_test)
Number_of_Correct_Predictions = len([i for i, j in zip(PredictedOutcome, Target_test) if i == j])

print ('***************************************************************************')
print('Number of Correct Predictions:', Number_of_Correct_Predictions, 'Out_of:', len(PredictedOutcome),
      'Number of Test Data')
print('Accuracy of Prediction in Percent:', (Number_of_Correct_Predictions/float(len(PredictedOutcome)))*100)

print '\n\n*****************************************************************************'
print ('****  MLP  *********************************************************************')
clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2), random_state=1).fit(Input_train, Target_train)
PredictedOutcome = clf.predict(Input_test)
Number_of_Correct_Predictions = len([i for i, j in zip(PredictedOutcome, Target_test) if i == j])

print ('********************************************************************************')
print('Number of Correct Predictions:', Number_of_Correct_Predictions, 'Out_of:', len(PredictedOutcome),
      'Number of Test Data')
print('Accuracy of Prediction in Percent:', (Number_of_Correct_Predictions/float(len(PredictedOutcome)))*100)

print '\n\n*****************************************************************************'
print ('****  GradientBoostingClassifier  *********************************************')
clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0,max_depth=1, random_state=0).fit(Input_train, Target_train)
PredictedOutcome = clf.predict(Input_test)
Number_of_Correct_Predictions = len([i for i, j in zip(PredictedOutcome, Target_test) if i == j])

print ('*********************************************************************************')
print('Number of Correct Predictions:', Number_of_Correct_Predictions, 'Out_of:', len(PredictedOutcome),
      'Number of Test Data')
print('Accuracy of Prediction in Percent:', (Number_of_Correct_Predictions/float(len(PredictedOutcome)))*100)



##########################################################################################
#####        PART C

############   K = 5  and distance method: Eculidean



print '\n\n********** PART C : Cross validation ************************'

for i in [1,3,5,7,9,11,13]:
    Knn = KNeighborsClassifier(n_neighbors=i ,p=2,metric='minkowski')
    scores = cross_val_score(Knn, Input_data_Scaled, Target_data, cv=10)
    Accuracy = scores.mean()
    print 'KNN (K='+str(i)+' , Eculidean distance) Accuracy:'+str(Accuracy)

for i in [1,3,5,7,9,11,13]:
    Knn = KNeighborsClassifier(n_neighbors=i ,p=1,metric='minkowski')
    scores = cross_val_score(Knn, Input_data_Scaled, Target_data, cv=10)
    Accuracy = scores.mean()
    print 'KNN (k='+str(i)+' , Manhattan distance) Accuracy:'+str(Accuracy)

for i in [1,3,5,7,9,11,13]:
    Knn = KNeighborsClassifier(n_neighbors=i ,p=3,metric='minkowski')
    scores = cross_val_score(Knn, Input_data_Scaled, Target_data, cv=5)
    Accuracy = scores.mean()
    print 'KNN (k='+str(i)+' , minkowski distance(p=3)) Accuracy:'+str(Accuracy)
