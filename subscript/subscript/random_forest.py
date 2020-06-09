import config as cn
import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.feature_selection import SelectFromModel
from sklearn import preprocessing

df_tree = pd.read_csv(os.path.join(dir_clean,  'processed_player_concat_test_catcounts.csv'))
df_tree = df_tree.drop(['last_login','time_since_login','total_achievement_points'], axis = 1)
df_tree = df_tree.set_index('id')

#Normalizing the data
df_tree.completed_quests = df_tree.completed_quests.div(100)
df_tree.mounts_collected = df_tree.mounts_collected.div(10)
df_tree.pets_collected = df_tree.pets_collected.div(10)
df_tree.total_achievements = df_tree.total_achievements.div(100)
df_tree.engagement_score = df_tree.engagement_score.div(100)
df_tree.gear_score = df_tree.gear_score.div(10)
df_tree.honor_level = df_tree.honor_level.div(10)
df_tree = df_tree.dropna()
df_tree.describe()

from sklearn.model_selection import ShuffleSplit

rs = ShuffleSplit(n_splits=10, test_size=.25, random_state=17)
for train_index, test_index in rs.split(df_tree):
    train_set = df_tree.iloc[train_index].copy()
    test_set = df_tree.iloc[test_index].copy()

y_train = train_set.engagement_score
X_train = train_set.drop('engagement_score',axis = 1)
y_test = test_set.engagement_score
X_test = test_set.drop('engagement_score',axis = 1)

encoder = preprocessing.LabelEncoder() # get a type error if not encoded
y_train = encoder.fit_transform(y_train)
y_test = encoder.fit_transform(y_test)

# Don't do more than 50 estimators or it will crash
selected = RandomForestClassifier(n_estimators = 100,n_jobs = -1,
                           oob_score = True,bootstrap = True,random_state = 17)
selected.fit(X_train, y_train)
