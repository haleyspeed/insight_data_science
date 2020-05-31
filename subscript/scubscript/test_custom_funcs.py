import os
import custom_funcs as cf
import csv
import config


#dir_out = config.processed_dir
#dir_in = os.path.join(config.home_dir.replace('git',''), 'datasets', 'leaderboard')
#big_csv = cf.csv_concatenator (dir_in)
#os.chdir(dir_out)
#big_csv.to_csv('leaderboard_stats.csv')

# Test concatenation of player stats csvs into one
# large csv
#dir_out = config.processed_dir
#dir_in = os.path.join(home_dir.replace('git',''), 'datasets', 'player_stats')
# #cf.super_big_csv_concatenator (dir_in, dir_out)


# Test data cleaning
f_name = 'player_stats.csv'
f_in = os.path.join(config.processed_dir, f_name)
f_out = os.path.join(config.clean_dir, f_name)
df = cf.dataset_cleaner(f_in)
df.to_csv(f_out)