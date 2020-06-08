import os
import custom_funcs as cf
import csv
import config
import numpy as np

#dir_out = config.processed_dir
#dir_in = os.path.join(config.home_dir.replace('git',''), 'datasets', 'leaderboard')
#big_csv = cf.csv_concatenator (dir_in)
#os.chdir(dir_out)
#big_csv.to_csv('leaderboard_stats.csv')

# Test concatenation of player stats csvs into one
# large csv
#home_dir = config.home_dir
<<<<<<< HEAD
dir_in = os.path.join(config.processed_dir)
dir_out = config.clean_dir
file_in = os.path.join(dir_in, '*{}')
file_out = os.path.join(dir_out,'raw_player_stats.csv')
=======
dir_in = os.path.join(config.processed_dir, 'wow_ach_time')
dir_out = config.clean_dir
file_in = os.path.join(dir_in, '*{}')
file_out = os.path.join(dir_out,'player_stats_subset.csv')
>>>>>>> 652b680204ce2295cbd00167ac9e169d137d8113
cf.super_big_csv_concatenator (file_in, file_out)


# Test data cleaning
#f_name = 'player_stats.csv'
#f_in = os.path.join(config.processed_dir, f_name)
#f_out = os.path.join(config.clean_dir, f_name)
#df = cf.dataset_cleaner(f_in)
#df.to_csv(f_out)


#print(cf.achievement_patch_scraper (11546))
#print(cf.patch_date_scraper ('7.2.0'))