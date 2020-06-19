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
X_train = train_set.drop('engagement',axis = 1)
y_test = test_set.engagement
X_test = test_set.drop('engagement',axis = 1)
encoder = preprocessing.LabelEncoder() # get a type error if not encoded
y_train = encoder.fit_transform(y_train)
y_test = encoder.fit_transform(y_test)

fig1, axes = plt.subplots( figsize=(10,10), dpi=100)
a = sns.distplot(df.engagement, color="darkcyan",  axlabel='status')
a.set_xticklabels(df.status, rotation = 45)
fig1.savefig(os.path.join(cn.clean_dir, 'random_forest_classifier',
            'histplot_time_balanced.png'), dpi=180)


print("Start random forest...")
from sklearn.ensemble import RandomForestClassifier
class_weight = dict({0:.9, 1:1.23, 2:5.46})
selected = RandomForestClassifier(bootstrap=True,
            class_weight=class_weight, n_estimators=300,
            oob_score=True,random_state=17)

#selected = RandomForestClassifier(n_estimators = 200,n_jobs = -1,
#            oob_score = True,bootstrap = True,random_state = 17)
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
df_pred.to_csv(os.path.join(cn.clean_dir, 'random_forest_classifier','final_test_predictions.csv'), index = False)


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
folder = os.path.join(cn.clean_dir, 'random_forest_classifier',)
f_name = 'metrics_time_balanced_metrics.csv'
print(met)
#print(cf.metrics_formatter(met, folder, f_name))


print("Plotting the confusion matrix...")
fig2, ax = plt.subplots(figsize = (8,8))
sns.heatmap(pd.DataFrame(cnf_matrix), annot = True, cmap = 'viridis', fmt = 'g', annot_kws={"size":16})
ax.set_xlabel ("Predicted Value", fontsize = 18)
ax.set_ylabel ("Actual Value", fontsize = 18)
ax.tick_params (labelsize = 14)
plt.tight_layout()
fig2.savefig(os.path.join(cn.clean_dir, 'random_forest_classifier','cnfmatrix_time_balanced.png'), dpi=180)

# save the model to disk
pickle_name = 'final_time_model.sav'
os.chdir(os.path.join(cn.clean_dir,'random_forest_classifier'))
with open(pickle_name, 'wb') as file:
    pickle.dump(selected, file)
plt.show()
