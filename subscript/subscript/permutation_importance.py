import config as cn
import pandas as pd
import numpy as np
import custom_funcs as cf
import os
from sklearn.inspection import permutation_importance
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn import preprocessing
from sklearn.model_selection import ShuffleSplit
from sklearn import metrics
import pickle

risk = 60
lapsed = 180


print ("Reading in file...")
#df = pd.read_csv(os.path.join(cn.clean_dir, 'final_feature_stats.csv'), dtype = 'unicode')
df = pd.read_csv(os.path.join(cn.processed_dir,'6-10_scrapes','processed_6-10-20', 'concatenated', 'engaged', '2500concat_trim_6-8_dates_4000_39400.csv'), dtype = 'unicode')
dfa = pd.read_csv(os.path.join(cn.clean_dir, 'achievement_details_list.csv'))
print(df.info())
df_bfa = dfa.achievement_id[dfa.category_name == 'Battle for Azeroth'].astype(int).astype(str)
keep = [c for c in df_bfa]
keep = keep + ['last_login', 'engagement',
    'status', 'id', 'gear_score', 'player','realm','time_since_login',
    'total_achievement_points', 'total_achievements']
df = df[keep]
if 'id' not in df.columns.values:
    df['id'] = df.player + '_' + df.realm
print(df.info())
df = df.dropna(axis = 1)
print(df.info())
# Rank the achievements by order of completion
ranks = [c for c in df.columns.values if c not in ['last_login', 'engagement',
    'status', 'id', 'gear_score', 'player','realm','time_since_login',
    'total_achievement_points', 'total_achievements']]

#df[ranks] = np.where(df[ranks].isnull() == True, 0 , df[ranks])

df[ranks] = np.where(df[ranks] == 'none', np.nan , df[ranks])
df[ranks] = df[ranks].astype(str).apply(lambda x: x.str[:7])
df[ranks] = df[ranks].astype(str).apply(lambda x: [y.replace('-','.') for y in x])
df[ranks] = np.where('.' in df[ranks] == True, df[ranks].astype(float) , df[ranks])
df[ranks] = np.where(np.isnan(df[ranks].astype(float))== True, 0 , df[ranks])

#df[ranks] = np.where(df[ranks].astype(float) <= 2019.07, np.nan , df[ranks])
#df[ranks] = df[ranks].astype(float).rank(axis = 0, na_option = 'keep', ascending = True, numeric_only = True)


#df = df.fillna(0)
print(df.head())

print ("Making the tree dataset...")
df_tree = df.copy()
df_tree = df_tree.drop(['last_login', 'player','realm','status',
    'time_since_login','gear_score',], axis = 1)
df_tree = df_tree.set_index('id')

print("Start random forest...")
y_train = df_tree.engagement
X_train = df_tree.drop('engagement', axis=1)

selected = RandomForestClassifier(n_estimators = 100,n_jobs = -1,
                   oob_score = True,bootstrap = True,random_state = 17)
clf = selected.fit(X_train, y_train)

print("permutation time....")
result = permutation_importance(clf, X_train, y_train, n_repeats=10, random_state=17)
importances_mean = result.importances_mean
importances_std = result.importances_std
print(importances_mean,importances_std)
filename = 'finalized_model.sav'
pickle.dump(clf, open(os.path.join(cn.clean_dir, 'pickles', 'permutation_results.sav'), 'wb'))
