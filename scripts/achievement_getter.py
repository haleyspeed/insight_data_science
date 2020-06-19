# Only do this once and save in another file to retrieve later. Takes a while.

import config as cn
import pandas as pd
import numpy as np
import os
from IPython.display import HTML

dir_home = cn.home_dir
dir_clean = cn.clean_dir
dir_processed = cn.processed_dir
dir_raw = cn.raw_dir

df = pd.read_csv(os.path.join(dir_clean,  'processed_player_concat_test.csv'))
df = df.drop_duplicates()
#del_cols = [c for c in df.columns.values if 'unnamed' in c.lower()]
#del_cols = del_cols + ['guild_rank', 'playable_class', 'playable_race', 'realm_id',
#                       'faction', 'guild_name', 'player', 'realm']

#df = df.drop(del_cols, axis = 1)
df = df.set_index('id')

f_cat = os.path.join(cn.clean_dir,'achievement_details_list.csv')
dfc = pd.read_csv(f_cat)
categories = [name.lower() for name in np.unique(dfc.category_name)]

df = df.dropna()

i = 0
for index, row in df.iterrows():
    print(i, end = ' ')
    for cat in np.unique(categories):
        if isinstance(row[cat], str):
            df.at[index,cat] = len(row[cat].split(","))
    i = i + 1

df.to_csv(os.path.join(dir_clean,  'processed_player_concat_test_catcounts.csv'))
