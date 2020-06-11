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
    loaded_model = pickle.load(open(pickled_model, 'rb'))
    result = fitted.score(X_test, Y_test)
    predictions = selected.predict(X_test)
    df_pred = pd.DataFrame(X_test)
    df_pred['prediction'] = predictions
return  df_pred

pickle_model = 'rf_time_model_60-180.sav'
pickle_path = os.path.join(cn.clean_dir, 'pickles', pickle_model)
X_test =
y_test = 
print(df_pred)
