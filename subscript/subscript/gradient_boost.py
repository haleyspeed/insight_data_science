import config as cn
import pandas as pd
import numpy as np
import custom_funcs as cf
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn import preprocessing
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

df = pd.read_csv(os.path.join(cn.clean_dir,'random_forest_classifier',
        'final_time_stats.csv'),dtype = 'unicode')
df = df.drop_duplicates()
df = df.fillna(0)
train_set = pd.read_csv(os.path.join(cn.clean_dir,'random_forest_classifier',
        'time_stratified_train.csv'))
train_set = train_set.drop_duplicates()
train_set = train_set.fillna(0)
test_set = pd.read_csv(os.path.join(cn.clean_dir,'random_forest_classifier',
        'time_stratified_test.csv'))
test_set = test_set.drop_duplicates()
test_set = test_set.fillna(0)



#drop_cols = ['id']
#train_set = train_set.drop(drop_cols)

y_train = train_set.engagement
X_train = train_set.drop(['2020-05','engagement'],axis = 1)
y_test = test_set.engagement
X_test = test_set.drop(['2020-05','engagement'],axis = 1)
encoder = preprocessing.LabelEncoder() # get a type error if not encoded
y_train = encoder.fit_transform(y_train)
y_test = encoder.fit_transform(y_test)




# save the model to disk
pickle_name = 'final_time_model.sav'
os.chdir(os.path.join(cn.clean_dir,'random_forest_classifier'))
with open(pickle_name, 'wb') as file:
    pickle.dump(selected, file)
