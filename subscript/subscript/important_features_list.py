import config as cn
import pandas as pd
import numpy as np
import custom_funcs as cf
import os

df = pd.read_csv(os.path.join(cn.clean_dir, 'feature_wrapper', 'selected_features.csv'))
dfc = pd.read_csv(os.path.join(cn.clean_dir, 'achievement_short_list.csv'))
drop_cols = [c for c in df.columns.values if 'Unnamed' in c]
df = df.drop(drop_cols, axis = 1)
df.columns = ['id']

ach_list = [c for c in df.id if 'engagement' not in c]
for index, row in df.iterrows():
    df.at[index,'name'] = dfc[dfc.achievement_id.astype(int).astype(str) == row.id].achievement_name.to_string(index=False)
    df.at[index,'description'] = dfc[dfc.achievement_id.astype(int).astype(str) == row.id].description.to_string(index=False)
df.to_csv(os.path.join(cn.clean_dir, 'selected_features.csv'))
print(df.head())
