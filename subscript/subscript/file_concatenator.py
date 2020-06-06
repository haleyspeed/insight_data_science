import os
import custom_funcs as cf
import csv
import config
import numpy as np

dir_in = os.path.join(config.clean_dir, 'time_tallied')
dir_out = config.clean_dir
file_in = os.path.join(dir_in, '*{}')
file_out = os.path.join(dir_out,'timed_player_stats_subset.csv')
df = cf.csv_concatenator (dir_in)
df.to_csv(file_out)