import subscript.config as cn
import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn import preprocessing
from sklearn.model_selection import ShuffleSplit
from sklearn import metrics
import pickle
import joblib
import matplotlib.pyplot as plt

print('Reading in File...')
df = pd.read_csv(os.path.join(cn.clean_dir, 'random_forest_time',
        'whole_test_set.csv'))
dfo = df.copy()
model = joblib.load(os.path.join(cn.clean_dir,'random_forest_time',
        'final_time_model.sav'))
features = ['player', 'realm','last_login', 'time_since_login',
           'engagement', 'status']

print('Preparing test set...')
y = df.engagement
X = df.fillna(0).drop(features, axis = 1)
print(X)

print('Predicting engagement status... ')
pred = model.predict(X)
dfo['pred'] = pred
dfo['actual'] = y

print('Printing predictions....')
print_cols = features + ['pred']
#print(dfo)

# Add 1-5 achievements in the next month
i = 1
for i in np.arange(1,6):
    df['2020-05'] = df['2020-05'].values.astype(float) + 1
    new_pred = model.predict(df.drop(features, axis = 1))
    dfo['pred' + str(i)] = new_pred
dfo.to_csv(os.path.join(cn.clean_dir, 'random_forest_time',
        'test_predictions.csv'), index = False)
