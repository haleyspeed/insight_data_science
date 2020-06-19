import os
import pandas as pd
import config as cn
from IPython.display import HTML
import numpy as np


# Read in the feature files
df = pd.read_csv(os.path.join(cn.clean_dir, 'final_feature_categories.csv'),
                 dtype = 'unicode')
dfa = pd.read_csv(os.path.join(cn.clean_dir, '6-13_achievement_list.csv'))

categories = list(np.unique(dfa.category_name))
print(categories, end = ' ')
from IPython.display import HTML
df = df.set_index ('id')
player_cols = ['player','realm','gear_score','last_login',
            'time_since_login', 'engagement','status']
out_cols = player_cols + categories
dfo = pd.DataFrame(columns = out_cols)
i = 0
for index, row in df.iterrows():

    tmp = pd.DataFrame(columns = out_cols)
    grp = row.T.reset_index()
    grp.columns = ['label', 'category']
    grp = grp.groupby('category').count()
    grp = grp.T
    tmp.at[index,player_cols] = row[player_cols]
    for col in categories:
        try:
            tmp.at[index,col] = grp[col].label
        except:
            tmp[col] = 0
            continue
    dfo = dfo.append(tmp)
    if i % 250 == 0:
        dfo.to_csv(os.path.join(cn.clean_dir, str(i) + '_categorized_feature_stats.csv'))
        dfo = pd.DataFrame(columns = out_cols)
        print(i, end = ' ')
    i = i + 1
dfo.to_csv(os.path.join(cn.clean_dir, str(i) + '_categorized_feature_stats.csv'))
