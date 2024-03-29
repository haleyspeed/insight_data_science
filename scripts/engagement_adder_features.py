import os
import custom_funcs as cf
import csv
import config as cn
import numpy as np
import glob
import pandas as pd


dir_in = os.path.join(cn.processed_dir, '6-15_scrapes','processed', 'features')
file_in = os.path.join(dir_in, '*{}')
df = pd.DataFrame()
os.chdir (dir_in)
print(os.getcwd())
i = 1
for f in glob.glob('*{}'.format('csv')):
    print(i,f)
    df = pd.read_csv(f,dtype='unicode')

    #if 'engagement' not in df.columns.values:
    df['engagement'] = np.nan
    df['status'] = ''
    for index, row in df.iterrows():
        if int(row.time_since_login.split(' ')[0]) <= 30:
            df.at[index,'engagement'] = 0
            df.at[index,'status'] = 'active'
            continue
        elif int(row.time_since_login.split(' ')[0]) <= 240:
            df.at[index,'engagement'] = 1
            df.at[index,'status'] = 'risk'
            continue
        elif int(row.time_since_login.split(' ')[0]) >240:
            df.at[index,'engagement'] = 2
            df.at[index,'status'] = 'lapsed'
            continue
    df.to_csv(os.path.join(dir_in, 'engaged', f.replace('features', 'engaged')))
