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
from sklearn import svm
from sklearn import neighbors
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
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

    sorted_training_instances = [tuple[0] for tuple in sorted_distances]  # extract only training instances

    return sorted_training_instances[:k]      # select first k elements


def _get_tuple_distance(Trainig_Target,training_instance, test_instance,distance_method):  # create a vector include of the training_target and distance between the test instance and the training point
    if distance_method == 'Eculidean':
        return (Trainig_Target, get_euclideanDistance(test_instance, training_instance))
    elif ( distance_method == 'Manhattan'):
        return (Trainig_Target, get_manhattanDistance(test_instance, training_instance))

def getRegressionPredict(neighbours):

    return  sum(neighbours)/len(neighbours)

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

def getAccuracy(Target_test, predictions):
	correct = 0
	for x in range(len(Target_test)):
		if Target_test[x] == predictions[x]:
			correct += 1
	return (correct/float(len(Target_test))) * 100.0


##########################################################################
##############################Main########################################
Data = np.loadtxt(open("Lab5Data.csv", "rb"), delimiter=";", skiprows=1)
print ('*******************************************')
print('Length of Total Data:', len(Data))


Input_data = Data[:, :7]  # input features
Input_data = np.concatenate((Input_data,Data[:,8:10]),axis=1)
Target_data = Data[:, 7]  # output

Input_data_Scaled = preprocessing.minmax_scale(Input_data)

Train_set, Test_set = train_test_split(Data, test_size=0.2)
###################  PART E #####################################

Input_train = Train_set[:, :7]  # input features
Input_train = np.concatenate((Input_train,Train_set[:,8:10]),axis=1)
Target_train = Train_set[:, 7]  # output

Input_train_Scaled = preprocessing.minmax_scale(Input_train)

Input_test = Test_set[:, :7]
Input_test = np.concatenate((Input_test,Test_set[:,8:10]),axis=1)
Target_test = Test_set[:, 7]

Input_test_Scaled = preprocessing.minmax_scale(Input_test)

# generate predictions list
predictions = []

k=7
distance_method = "Eculidean"

for x in range(len(Target_test)):
    neighbours = get_neighbours(Input_train_Scaled, Target_train, Input_test_Scaled[x, :], k,distance_method)
    funcValue = getRegressionPredict(neighbours)
    predictions.append(funcValue)

# summarize performance of the classification
print '\nThe RMSE of the KNN model is: ' + str(getRMSE(Target_test, predictions))
print 'The mean squared error of the KNN model is: '+ str(mean_squared_error(Target_test, predictions))


####################  PART F  #########################################
###################### SVR

predictions = []
clf = svm.SVR().fit(Input_train_Scaled, Target_train)
predictions = clf.predict(Input_test_Scaled)
print '\n**************************************************************'
print '***   SVR Method:'
print 'The RMSE of the model is: ' + str(getRMSE(Target_test, predictions))
print 'The mean squared error of the SVR model is: '+ str(mean_squared_error(Target_test, predictions))

###################### Decision Tree

predictions = []
clf = tree.DecisionTreeRegressor().fit(Input_train_Scaled, Target_train)
predictions = clf.predict(Input_test_Scaled)
print '\n\nDecision Tree Method:'
print 'The RMSE of the model is: ' + str(getRMSE(Target_test, predictions))
print 'The mean squared error of the Decision Tree model is: '+ str(mean_squared_error(Target_test, predictions))




###################### Gradient Boosting

predictions = []
clf = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1,max_depth=1, random_state=0, loss='ls').fit(Input_train_Scaled, Target_train)
predictions = clf.predict(Input_test_Scaled)
print '\n\nGradient Boosting Method:'
print 'The RMSE of the model is: ' + str(getRMSE(Target_test, predictions))
print 'The mean squared error of the Gradient Boosting model is: '+ str(mean_squared_error(Target_test, predictions))


#############################################################################
############################ PART G #########################################
print '\n\n***************  Part G *******************************************'
for n_neighbors in [3,5,7,9,11,13]:
    clf = neighbors.KNeighborsRegressor(n_neighbors,p=2,metric='minkowski')
    scores = cross_val_score(clf, Input_data_Scaled, Target_data, cv=5)
    Accuracy = scores.mean()
    print 'KNN (k=' +str(n_neighbors)+' , Euclidean distance) Accuracy:'+str(Accuracy)

for n_neighbors in [3,5,7,9,11,13]:
    clf = neighbors.KNeighborsRegressor(n_neighbors,p=1,metric='minkowski')
    scores = cross_val_score(clf, Input_data_Scaled, Target_data, cv=5)
    Accuracy = scores.mean()
    print 'KNN (k=' +str(n_neighbors)+' , Manhattan distance) Accuracy:'+str(Accuracy)
