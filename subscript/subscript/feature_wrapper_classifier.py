#importing libraries
import pandas as pd
import os
import config as cn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

# Read in data and set p value Elimination
p_limit = 0.05
df = pd.read_csv(os.path.join(cn.clean_dir,'final_feature_stats.csv'), dtype = 'unicode')
dfa = pd.read_csv(os.path.join(cn.clean_dir, 'achievement_short_list.csv'))
keep = [str(int(c)) for c in dfa.achievement_id]
if 'id' not in df.columns.values:
    df['id'] = df.player + '_' + df.realm
keep = keep + ['engagement','id']
keep = [c for c in keep if c in df.columns.values]
df = df[keep]
df = df.set_index('id')

df = df.astype(str).apply(lambda x: x.str[:1]).replace('n','0')
dfp = pd.DataFrame()

y = df.engagement.astype(float)
X = sm.add_constant(df).astype(float)
feature_selector = ExhaustiveFeatureSelector(RandomForestClassifier(n_jobs=-1),
           min_features=2,
           max_features=4,
           scoring='roc_auc',
           print_progress=True,
           cv=2)
features = feature_selector.fit(np.array(X, y)
filtered_features= train_features.columns[list(features.k_feature_idx_)]
print(filtered_features)
