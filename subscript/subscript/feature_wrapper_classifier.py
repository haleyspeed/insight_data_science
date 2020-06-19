#importing libraries
import pandas as pd
import os
import config as cn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from mlxtend.feature_selection import SequentialFeatureSelector
from sklearn.model_selection import StratifiedShuffleSplit
import numpy as np

# Read in data and set p value Elimination
df = pd.read_csv(os.path.join(cn.clean_dir,'final_aggregated_categories.csv'), dtype = 'unicode')
player_cols =  ['Unnamed: 0','Unnamed: 0.1','player','realm','gear_score','last_login',
            'time_since_login','status']
df = df.drop(player_cols, axis = 1)
print(df.head())
dfp = pd.DataFrame()

df = df[df.engagement.astype(float) != 1]
split = StratifiedShuffleSplit(n_splits = 10, test_size = 0.25, random_state = 17)
for train_index, test_index in split.split(df, df.engagement):
    strat_train = df.iloc[train_index][:]
    strat_test = df.iloc[test_index][:]

y_train = strat_train.engagement
X_train = strat_train.drop('engagement', axis = 1)
y_test = strat_train.engagement
X_test = strat_test.drop('engagement', axis = 1)

feature_selector = SequentialFeatureSelector(RandomForestClassifier(n_jobs=1),
           k_features=15,
           forward=True,
           verbose=2,
           scoring='roc_auc',
           cv=4)
features = feature_selector.fit(np.array(X_train.fillna(0)), y_train)
filtered_features = train_features.columns[list(features.k_feature_idx_)]
print(filtered_features)

clf = RandomForestClassifier(n_estimators=100, random_state=17, max_depth=3)
clf.fit(X_train[filtered_features], y_train)

train_pred = clf.predict_proba(X_train[filtered_features])
print('Accuracy on training set: {}'.format(roc_auc_score(X_train, train_pred[:,1])))

test_pred = clf.predict_proba(X_test[filtered_features].fillna(0))
print('Accuracy on test set: {}'.format(roc_auc_score(y_test, test_pred [:,1])))
