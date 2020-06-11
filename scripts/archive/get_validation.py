import config
import custom_funcs as cf
import pandas as pd
import os
import numpy as np
import configparser as cp
import glob


f_config = os.path.join(config.home_dir, '../', 'api', 'config.ini')
conf = cp.ConfigParser()
conf.read(f_config)
blizzard_key = conf.get('KEYS', 'blizzard')
blizzard_secret = conf.get('KEYS', 'blizzard_secret')
locale = 'en_US'
namespace = 'static-us'
access_token = cf.get_access_token(blizzard_key, blizzard_secret)


dir_in = os.path.join(config.clean_dir, 'time_tallied')
dir_out = config.clean_dir
file_in = os.path.join(dir_out,'timed_player_stats_subset.csv')
print('starting up...')

df = pd.read_csv(file_in, sep = ',')
df['gear_score'] = 0
df['last_login'] = ''
df = df.set_index('id')
i = 0
for index, row in df.iterrows():
     last_login, gear_score= cf.get_validation(row.player, row.realm, access_token)
     try:
          df.at[index, 'gear_score'] =  gear_score
          df.at[index, 'last_login'] = last_login
     except:
          print("error in " + index)
     print(index, i)
     if i % 2000 == 0:
          df.to_csv(os.path.join(dir_out, 'validated_achievements.csv'))
     i = i + 1
df.to_csv(os.path.join(dir_out, 'validated_achievements.csv'))