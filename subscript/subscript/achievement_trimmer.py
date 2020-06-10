import config as cn
import custom_funcs as cf
import pandas as pd
import os
import numpy as np

# Read in the dataset and achievement details list
f_in = os.path.join(cn.processed_dir,'6-8_scrapes','wow_6-8_dates_100_100.csv')
dfa = pd.read_csv(os.path.join(cn.clean_dir,'achievement_details_list2.csv'))
df = pd.read_csv(os.path.join(f_in))

# Determine achievements with
account_wide = dfa[dfa.account_wide == True].achievement_name
account_wide = [a.lower() for a in account_wide]
category_cols = [c.lower() for c in dfa.category_name]
drop_cols = [c for c in account_wide + category_cols if c in df.columns.values]
df = df.drop(drop_cols, axis = 1)
df = df.to_csv(os.path.join(cn.clean_dir,'6-8_player_concat_test_trimmed.csv'))
