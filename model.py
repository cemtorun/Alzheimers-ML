# =============================================================================
# Dementia classification / MMSE prediction using LR, RF, DT or SVM
# =============================================================================

import os

import warnings
warnings.filterwarnings("ignore")

import argparse
import numpy as np
import pandas as pd
from sklearn import tree
from sklearn.svm import SVC
from scipy.stats import pearsonr as pearson
from sklearn.metrics import precision_recall_curve
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import f1_score, accuracy_score, classification_report, roc_auc_score, confusion_matrix

seed = 212
def train(feature_set):
    # takes csv data from author and fits to knn model 
    data = pd.read_csv('feature_set_dem.csv')
    X = np.array([data['prp_count'], data['VP_count'], data['NP_count'], #data['DT_count'], 
                  data['prp_noun_ratio'], data['word_sentence_ratio'],
                  data['count_pauses'], data['count_unintelligible'], 
                  data['count_repetitions'], data['ttr'], data['R'],
                  data['ARI'], data['CLI']])
    
    X = X.resize(552, 8)
    
    Y = data['Category'].values
    
    
    X_train, X_test, y_train, y_test = train_test_split(X, Y, 
                                                        test_size=0, random_state=212)
    knn = KNeighborsClassifier()
    knn.fit(X_train, y_train)
    # takes attributes from experimental data and predicts result 
    inar = np.array(feature_set)
    prediction = knn.predict(inar)
    return prediction   # a percentage from 0 to 100
