import os
import custom_funcs as cf
import csv
import config
import numpy as np


dir_in = os.path.join(config.processed_dir)
dir_out = config.clean_dir
file_in = os.path.join(dir_in, '*{}')
file_out = os.path.join(dir_out,'raw_player_stats.csv')
cf.super_big_csv_concatenator (file_in, file_out)

