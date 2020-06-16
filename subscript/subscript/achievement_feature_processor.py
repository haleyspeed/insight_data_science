import config as cn
import custom_funcs as cf
import pandas as pd
import os
import numpy as np
import glob

# Read in the dataset and achievement details list
dfa = pd.read_csv(os.path.join(cn.clean_dir,'6-13_achievement_list.csv'))
achievements = list(dfa.achievement_id.values.astype(int).astype(str))
print(type(achievements))

os.chdir (os.path.join(cn.processed_dir,'6-10_scrapes'))
for f in glob.glob('*{}'.format('csv')):
    player_cols = ['player', 'realm', 'gear_score', 'last_login', 'time_since_login']
    keep_cols = player_cols + achievements

    df = pd.read_csv(f, dtype = 'unicode')
    keep_cols = [c for c in keep_cols if c in df.columns.values]

    df = df[keep_cols]
    f_out = os.path.join(cn.processed_dir,'6-10_scrapes','processed_6-10-20',
            'bfa_features', f.replace('wow','bfa_features'))
    df = df.to_csv(f_out)
    print(f_out)
