# =============================================================================
# Dementia classification / MMSE prediction using LR, RF, DT or SVM
# =============================================================================

import os

import warnings
warnings.filterwarnings("ignore")

import argparse
import numpy as np
import pandas as pd
import data_process as dp
import feature_extract as fe
import sklearn
from sklearn import tree
from sklearn import model_selection
from sklearn.svm import SVC
from scipy.stats import pearsonr as pearson
from sklearn.metrics import precision_recall_curve
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
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
    
    X = X.T
    
    Y = data['Category'].values

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.20, random_state=212)
    train_samples, n_features = X.shape

    kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=212)
    cvscores = []

    # Spot Check Algorithms
    models = []
    models.append(('LR', LogisticRegression()))
    models.append(('LDA', LinearDiscriminantAnalysis()))
    models.append(('KNN', KNeighborsClassifier()))
    models.append(('CART', DecisionTreeClassifier()))
    models.append(('NB', GaussianNB()))
    models.append(('SVM', SVC()))
    # evaluate each model in turn
    results = []
    names = []
    for name, model in models:
	    kfold = model_selection.KFold(n_splits=10, random_state=seed)
	    cv_results = model_selection.cross_val_score(model, X_train, y_train, cv=kfold, scoring='accuracy')
	    results.append(cv_results)
	    names.append(name)
	    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
	    print(msg)

    lda = LinearDiscriminantAnalysis()
    lda.fit(X_train, y_train)
    # takes attributes from experimental data and predicts result 
    inar = [feature_set]
    prediction = lda.predict(inar)
    return prediction   # a percentage from 0 to 100 

a = dp.process_string('testfile.json')
b = fe.get_tag_info(a)
print(train(b))
