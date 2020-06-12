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
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

risk = 60
lapsed = 180

print ("Reading in file...")
df = pd.read_csv(os.path.join(cn.clean_dir,  'final_player_stats_test.csv'))
extra_cols = [c for c in df.columns.values if 'unnamed' in str(c).lower()]
df = df.drop(extra_cols, axis = 1)
if 'id' not in df.columns.values:
    df['id'] = df.player + '_' + df.realm


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
    df.to_csv(os.path.join(cn.clean_dir, 'final_player_stats_test2.csv'))
exit()
print ("Making the tree dataset...")
df_tree = df.copy()
df_tree = df_tree.drop(['last_login','time_since_login', 'player','realm','status','last_login','gear_score'], axis = 1)
df_tree = df_tree.set_index('id')
print(df_tree.head())

print("Making training and test sets....")
rs = ShuffleSplit(n_splits=10, test_size=.25, random_state=17)

for train_index, test_index in rs.split(df_tree):
    train_set = df_tree.iloc[train_index].copy()
    test_set = df_tree.iloc[test_index].copy()
print(train_set.head())

y_train = train_set.engagement
X_train = train_set.drop('engagement',axis = 1)
y_test = test_set.engagement
X_test = test_set.drop('engagement',axis = 1)
encoder = preprocessing.LabelEncoder() # get a type error if not encoded
y_train = encoder.fit_transform(y_train)
y_test = encoder.fit_transform(y_test)

fig1, axes = plt.subplots( figsize=(10,10), dpi=100)
a = sns.distplot(df.engagement, color="darkcyan",  axlabel='status')
a.set_xticklabels(df.status, rotation = 45)
fig1.savefig(os.path.join(cn.clean_dir, 'pickles','histplot_time_model_60-180.png'), dpi=180)


print("Start random forest...")
selected = RandomForestClassifier(n_estimators = 100,n_jobs = -1,
                           oob_score = True,bootstrap = True,random_state = 17)
selected.fit(X_train, y_train)


print("Important Features...")
importances = selected.feature_importances_
indices = np.argsort(importances)
important_features = X_train.columns.values[indices]
for i, v in enumerate(important_features[:25]):
    print(i,v)


print("Making predictions...")
predictions = selected.predict(X_test)
df_pred = pd.DataFrame(X_test)
df_pred['prediction'] = predictions
df_pred['actual'] = y_test


print('Getting accuracy score...')
print(selected.score(X_train,y_train))


print('Oob score...')
print(selected.oob_score_)

print ("Making confusion matrix...")
# Print the confusion matrix
cnf_matrix = metrics.confusion_matrix(y_test,predictions)
print(cnf_matrix)

# Print the precision and recall, among other metrics
met = metrics.classification_report(y_test, predictions, digits=3)
folder = os.path.join(cn.clean_dir, 'pickles')
f_name = 'metrics_time_model_60-180.csv'
print(cf.metrics_formatter(met, folder, f_name))



print("Plotting the confusing matrix...")
fig2, ax = plt.subplots(figsize = (8,8))
sns.heatmap(pd.DataFrame(cnf_matrix), annot = True, cmap = 'viridis', fmt = 'g', annot_kws={"size":16})
ax.set_xlabel ("Predicted Value", fontsize = 18)
ax.set_ylabel ("Actual Value", fontsize = 18)
ax.tick_params (labelsize = 14)
plt.tight_layout()
fig2.savefig(os.path.join(cn.clean_dir, 'pickles','cnfmatrix_time_model_60-180.png'), dpi=180)

# save the model to disk
pickle_name = 'rf_time_model_60-180.sav'
os.chdir(os.path.join(cn.clean_dir, 'pickles'))
with open(pickle_name, 'wb') as file:
    pickle.dump(selected, file)
plt.show()
