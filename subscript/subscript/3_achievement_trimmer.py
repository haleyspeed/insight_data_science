import config as cn
import custom_funcs as cf
import pandas as pd
import os
import numpy as np
import glob

# Read in the dataset and achievement details list
dfa = pd.read_csv(os.path.join(cn.clean_dir,'achievement_details_list2.csv'), dtype = 'unicode')

# Determine achievements with
account_wide = dfa[dfa.account_wide == True].achievement_name
account_wide = [a.lower() for a in account_wide]
category_cols = [c.lower() for c in dfa.category_name]

os.chdir (os.path.join(cn.processed_dir,'6-10_scrapes'))
for f in glob.glob('*{}'.format('csv')):


    df = pd.read_csv(f, dtype = 'unicode')
    drop_cols = [c for c in account_wide + category_cols if c in df.columns.values]
    df = df.drop(drop_cols, axis = 1)
    f_out = os.path.join(cn.processed_dir,'6-10_scrapes', 'processed_6-10-20',f.replace('wow','trimmed'))
    df = df.to_csv(f_out)
    print(f_out)
