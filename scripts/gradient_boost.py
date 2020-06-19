import config as cn
import pandas as pd
import numpy as np
import custom_funcs as cf
import os
from sklearn.datasets import make_classification
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import metrics
import matplotlib.pyplot as plt
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



# Gradient Boost
clf = GradientBoostingClassifier(random_state = 17)
clf.fit(X_train, y_train)
GradientBoostingClassifier(random_state = 17)
predictions = clf.predict(X_test)
score = clf.score(X_test, y_test)

print (predictionz)
print(clf.score)

cnf_matrix = metrics.confusion_matrix(y_test,predictions)
print(cnf_matrix)

# Print the precision and recall, among other metrics
met = metrics.classification_report(y_test, predictions, digits=3)
folder = os.path.join(cn.clean_dir, 'random_forest_classifier',)
f_name = 'metrics_time_balanced_metrics.csv'
print(met)

# save the model to disk
#pickle_name = 'final_boost_model.sav'
#os.chdir(os.path.join(cn.clean_dir,'gradient_boost'))
#with open(pickle_name, 'wb') as file:
#    pickle.dump(clf, file)
