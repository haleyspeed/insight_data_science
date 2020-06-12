import config as cn
import pandas as pd
import numpy as np
import custom_funcs as cf
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn import preprocessing
from sklearn.model_selection import ShuffleSplit
from sklearn import metrics
import pickle

# load the model from disk
def player_lapse_predictor(pickle_path, X_test, y_test):
    loaded_model = pickle.load(open(pickle_path, 'rb'))
    result = loaded_model.score(X_test, y_test)
    predictions = loaded_model.predict(X_test)
    df_pred = pd.DataFrame(X_test)
    df_pred['prediction'] = predictions
    return  df_pred

risk = 60
lapsed = 180

pickle_model = 'rf_time_model_60-180.sav'
pickle_path = os.path.join(cn.clean_dir, 'pickles', pickle_model)
df = pd.read_csv(os.path.join(cn.clean_dir, 'processed_6-10-20', 'processed_6-8_dates_100_100.csv'), dtype = 'unicode')
extra_cols = [c for c in df.columns.values if 'unnamed' in str(c).lower()]
df = df.drop(extra_cols, axis = 1)
if 'id' not in df.columns.values:
    df['id'] = df.player + '_' + df.realm
df = df.set_index('id')

#if 'engagement' not in df.columns.values:
df['engagement'] = np.nan
df['status'] = ''
for index, row in df.iterrows():
    if int(row.time_since_login.split(' ')[0]) <= 30:
        df.at[index,'engagement'] = 0
        df.at[index,'status'] = 'subscribed'
    elif int(row.time_since_login.split(' ')[0]) <= risk:
        df.at[index,'engagement'] = 1
        df.at[index,'status'] = 'risk'
    elif int(row.time_since_login.split(' ')[0]) <= lapsed:
        df.at[index,'engagement'] = 2
        df.at[index,'status'] = 'lapsed'
    elif int(row.time_since_login.split(' ')[0]) <= 365:
        df.at[index,'engagement'] = 3
        df.at[index,'status'] = 'unsubscribed'

print ("Making the tree dataset...")
df_tree = df.copy()
df_tree = df_tree.drop(['last_login','time_since_login', 'player','realm','status','gear_score'], axis = 1)
#df_tree = df_tree.set_index('id')


y_test = df_tree.engagement
X_test = df_tree.drop('engagement', axis = 1)
df_pred = player_lapse_predictor(pickle_path, X_test, y_test)
print(df_pred['actual', 'prediction', 'projection_1', 'projection2', 'projection3','projection4','projection5'])
df_pred['with_']
