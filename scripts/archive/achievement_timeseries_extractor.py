import config
import custom_funcs as cf
import pandas as pd
import os
import numpy as np

path_in = os.path.join(config.clean_dir, 'achievement_details_list.csv')
df = pd.read_csv(path_in)
df['patch'] = ''
df['release_date'] = ''
df['attained_by'] = ''
for index, row in df.iterrows():
    print(row.achievement_id, end = ' ')
    df.at[index,'patch'], df.at[index,'attained_by'] = cf.achievement_patch_scraper (row.achievement_id)
    df.at[index,'release_date'] = cf.patch_date_scraper (df.loc[index,'patch'])
    print(df.loc[index,'patch'],df.loc[index,'attained_by'],df.loc[index,'release_date'],)

df.to_csv(config.clean_dir, '')