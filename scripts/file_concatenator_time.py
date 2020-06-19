import os
import custom_funcs as cf
import csv
import config as cn
import numpy as np
import glob
import pandas as pd


#dir_in = os.path.join(cn.processed_dir, '6-10_scrapes',
#    'processed_6-10-20', 'concatenated', 'engaged')

dir_in = os.path.join(cn.processed_dir, '6-10_scrapes',
        'processed_6-10-20','time', 'engaged')

#file_in = os.path.join(dir_in, '*{}')
df = pd.DataFrame()
os.chdir (dir_in)
print(os.getcwd())
i = 1
for f in glob.glob('*{}'.format('csv')):
    print(i,f)
    df = df.append(pd.read_csv(f,dtype='unicode'))
    df = df.drop_duplicates()
df.to_csv(os.path.join(cn.clean_dir,'random_forest_classifier','final_time_stats.csv'))
