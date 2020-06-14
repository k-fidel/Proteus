import math
import numpy as np
from numpy import loadtxt
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
# #---------------------------------------------------------------------------
##############################Main########################################
Call_Agent1 = 1.0
Call_Agent2 = 2.0
Fold_Agent1 = 3.0
Fold_Agent2 = 4.0
AllIn_Agent1 = 5.0
AllIn_Agent2 = 6.0

HandStrength = {'HighCard':1.0,'OnePair':2.0, 'TwoPairs':3.0, '3ofakind':4.0,'straight':5.0,'flush':6.0, 'fullhouse':7.0,'4ofakind':8.0, 'straightflush':9.0}
ASH1 =[]
ASH2= []
FinalAct = []
AV1 =[]
AV2 =[]
AC1 = []
AC2 = []
text_file = open("Lab5PokerData.txt", "r");
lines = text_file.readlines()
####################   Reading the log data and create the input vector
for i in lines:
    SumRaiseAg1 = []
    SumRaiseAg2 = []
    if( i == '\n'):
        break;
    data = i.split(',')
    player1Hand = data[1].split(' ')
    ASH1.append(HandStrength[player1Hand[1]])
    AC1.append(float(player1Hand[3]))
    player2Hand = data[2].split(' ')
    ASH2.append(HandStrength[player2Hand[1]])
    AC2.append(float(player2Hand[3]))
    for dt in range(3,len(data)):
        temp = data[dt].split(' ')
        if( temp[1] != '\n'):
            if( temp[1]=='Raise'):
                SumRaiseAg1.append(float(temp[2]))
            elif ( temp[1]=='Call'):
                FinalAct.append(Call_Agent1)
                break;
            elif ( temp[1] == 'Fold'):
                FinalAct.append(Fold_Agent1)
                break;
            elif ( temp[1] == 'AllIn'):
                FinalAct.append(AllIn_Agent1)
                break;
            if (temp[3] == 'Raise'):
                SumRaiseAg2.append(float(temp[4]))
            elif (temp[3] == 'Call'):
                FinalAct.append(Call_Agent2)
                break;
            elif (temp[3] == 'Fold'):
                FinalAct.append(Fold_Agent2)
                break;
            elif (temp[3] == 'AllIn'):
                FinalAct.append(AllIn_Agent2)
                break;

    AV1.append(np.mean(SumRaiseAg1))
    AV2.append(np.mean(SumRaiseAg2))



d1 = np.array(ASH1)
d2 = np.array(ASH2)
d3 = np.array(AC2)
d4 = np.array(AC1)
d5 = np.array(AV1)
d6 = np.array(AV2)
d7 = np.array(FinalAct)

Data = np.stack((d1,d2,d3,d4,d5,d6,d7),axis=-1)

print ('*******************************************')
print('Length of Total Data:', len(Data))
Input_data = Data[:,:6]
Target_data = Data[:,6]

Train_set, Test_set = train_test_split(Data, test_size=0.2)

Input_train = Train_set[:, :6]  # input features
Target_train = Train_set[:, 6]  # output
Input_train_Scaled = preprocessing.minmax_scale(Input_train)        # scale the input train data

Input_test = Test_set[:, :6]
Target_test = Test_set[:, 6]
Input_test_Scaled = preprocessing.minmax_scale(Input_test)         # scale the input test data


##################################################
####        PART B
print ('*******************************************')
print ('****  Knn Classifier **********************')
Knn = KNeighborsClassifier(n_neighbors=7 ,p=1,metric='minkowski')
Knn.fit(Input_train_Scaled, Target_train)
PredictedOutcome = Knn.predict(Input_test_Scaled)
Number_of_Correct_Predictions = len([i for i, j in zip(PredictedOutcome, Target_test) if i == j])

print ('*******************************************')
print('Number of Correct Predictions:', Number_of_Correct_Predictions, 'Out_of:', len(PredictedOutcome),
      'Number of Test Data')
print('Accuracy of Prediction in Percent:', (Number_of_Correct_Predictions/float(len(PredictedOutcome)))*100)




print ('\n\n*******************************************')
print ('****  SGC Classifier **********************')

clf = SGDClassifier(loss="log", penalty="l2")
clf.fit(Input_train_Scaled, Target_train)
PredictedOutcome = clf.predict(Input_test_Scaled)
Number_of_Correct_Predictions = len([i for i, j in zip(PredictedOutcome, Target_test) if i == j])

print ('*******************************************')
print('Number of Correct Predictions:', Number_of_Correct_Predictions, 'Out_of:', len(PredictedOutcome),
      'Number of Test Data')
print('Accuracy of Prediction in Percent:', (Number_of_Correct_Predictions/float(len(PredictedOutcome)))*100)
##
print ('\n\n*******************************************')
print ('****  LDA Classifier **********************')
clf1 = LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto').fit(Input_train_Scaled, Target_train)
PredictedOutcome = clf.predict(Input_test_Scaled)
Number_of_Correct_Predictions = len([i for i, j in zip(PredictedOutcome, Target_test) if i == j])

print ('*******************************************')
print('Number of Correct Predictions:', Number_of_Correct_Predictions, 'Out_of:', len(PredictedOutcome),
      'Number of Test Data')
print('Accuracy of Prediction in Percent:', (Number_of_Correct_Predictions/float(len(PredictedOutcome)))*100)
##
print ('\n\n****        Decision Tree      *********************')
#iris = load_iris()
clf = tree.DecisionTreeClassifier()
clf = clf.fit(Input_train, Target_train)
PredictedOutcome = clf.predict(Input_test)
Number_of_Correct_Predictions = len([i for i, j in zip(PredictedOutcome, Target_test) if i == j])

print ('*******************************************')
print('Number of Correct Predictions:', Number_of_Correct_Predictions, 'Out_of:', len(PredictedOutcome),
      'Number of Test Data')
print('Accuracy of Prediction in Percent:', (Number_of_Correct_Predictions/float(len(PredictedOutcome)))*100)

################################################################################
###################   Part C ###################################################
print '\n\n*****************  Part C **************************************'
Input = Data[:,:6]
Input_Scaled = preprocessing.minmax_scale(Input)
Target = Data[:,6]




for n_neighbors in [3,5,7,9,11,13]:
    clf = neighbors.KNeighborsClassifier(n_neighbors,p=2,metric='minkowski')
    scores = cross_val_score(clf, Input_Scaled, Target, cv=5)
    Accuracy = scores.mean()
    print 'KNN (k=' +str(n_neighbors)+' , Eculidean distance) Accuracy:'+str(Accuracy)

for n_neighbors in [3,5,7,9,11,13]:
    clf = neighbors.KNeighborsClassifier(n_neighbors,p=1,metric='minkowski')
    scores = cross_val_score(clf, Input_Scaled, Target, cv=5)
    Accuracy = scores.mean()
    print 'KNN (k=' +str(n_neighbors)+' , Manhattan distance) Accuracy:'+str(Accuracy)


