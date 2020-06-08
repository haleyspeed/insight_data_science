import os
import custom_funcs as cf
import csv
import config
import numpy as np

<<<<<<< HEAD
dir_in = os.path.join(config.clean_dir, 'processed_player_stats')
dir_out = config.clean_dir
file_in = os.path.join(dir_in, '*{}')
file_out = os.path.join(dir_out,'processed_player_concat_test.csv')
df = cf.csv_concatenator (dir_in)
df.to_csv(file_out)
=======
dir_in = os.path.join(config.clean_dir, 'time_tallied')
dir_out = config.clean_dir
file_in = os.path.join(dir_in, '*{}')
file_out = os.path.join(dir_out,'timed_player_stats_subset.csv')
df = cf.csv_concatenator (dir_in)
df.to_csv(file_out)
>>>>>>> c01bf7205576901f30adad57cb3c8e7686e44fb0
