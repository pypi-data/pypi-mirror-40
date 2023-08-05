#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 18:37:20 2018

@author: gykovacs

This script contains all the functions and codes we used to produce the
data reported in the paper. Before using the script, update the "cache_path" variable
below to the path containing the cache file generated by the CacheAndValidate
object.
"""

import os, pickle, itertools

# import classifiers
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from smote_variants import MLPClassifierWrapper

# import SMOTE variants
import smote_variants as sv

# itertools to derive imbalanced databases
import imbalanced_databases as imbd

# global variables
folding_path= '/home/gykovacs/workspaces/smote_package/smote_results/'
max_sampler_parameter_combinations= 35
n_jobs= 5

# instantiate classifiers
sv_classifiers= [CalibratedClassifierCV(LinearSVC(C=1.0, penalty='l1', loss= 'squared_hinge', dual= False)),
                 CalibratedClassifierCV(LinearSVC(C=1.0, penalty='l2', loss= 'hinge', dual= True)),
                 CalibratedClassifierCV(LinearSVC(C=1.0, penalty='l2', loss= 'squared_hinge', dual= False)),
                 CalibratedClassifierCV(LinearSVC(C=10.0, penalty='l1', loss= 'squared_hinge', dual= False)),
                 CalibratedClassifierCV(LinearSVC(C=10.0, penalty='l2', loss= 'hinge', dual= True)),
                 CalibratedClassifierCV(LinearSVC(C=10.0, penalty='l2', loss= 'squared_hinge', dual= False))]

mlp_classifiers= []
for x in itertools.product(['relu', 'logistic'], [1.0, 0.5, 0.1]):
    mlp_classifiers.append(MLPClassifierWrapper(activation= x[0], hidden_layer_fraction= x[1]))

nn_classifiers= []
for x in itertools.product([3, 5, 7], ['uniform', 'distance']):
    nn_classifiers.append(KNeighborsClassifier(n_neighbors= x[0], weights= x[1]))

dt_classifiers= []
for x in itertools.product(['gini', 'entropy'], [None, 3, 5]):
    dt_classifiers.append(DecisionTreeClassifier(criterion= x[0], max_depth= x[1]))

classifiers= []
classifiers.extend(sv_classifiers)
classifiers.extend(mlp_classifiers)
classifiers.extend(nn_classifiers)
classifiers.extend(dt_classifiers)

datasets= imbd.get_data_loaders('study')

# instantiate the validation object
results= sv.evaluate_oversamplers(datasets,
                                  samplers= sv.get_all_oversamplers(),
                                  classifiers= classifiers,
                                  cache_path= folding_path,
                                  n_jobs= n_jobs,
                                  remove_sampling_cache= True,
                                  max_n_sampler_parameters= max_sampler_parameter_combinations)

pickle.dump(results, open('/home/gykovacs/workspaces/smote_package/smote_results/results.pickle', 'wb'))

#print(results)