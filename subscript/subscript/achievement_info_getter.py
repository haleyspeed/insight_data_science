import config
import custom_funcs as cf
import pandas as pd
import os
import numpy as np
import configparser as cp


f_config = os.path.join(config.home_dir, '../', 'api', 'config.ini')
conf = cp.ConfigParser()
conf.read(f_config)
blizzard_key = conf.get('KEYS', 'blizzard')
blizzard_secret = conf.get('KEYS', 'blizzard_secret')
locale = 'en_US'
namespace = 'static-us'
access_token = cf.get_access_token(blizzard_key, blizzard_secret)

achievement_list = pd.read_csv(os.path.join(config.clean_dir,'achievement_details_list.csv'))

#achievement_list.columns = ['unnamed0', 'unnamed1', 'player', 'guild', 'realm', 'id']
#achievement_list = achievement_list.drop(['unnamed0', 'unnamed1'], axis = 1)
dfo = pd.DataFrame()
for id in achievement_list.achievement_id:
    results = cf.get_account_wide_achievement(int(id), access_token)
    print(results)
    dfo = dfo.append(results, ignore_index = True)
dfo.to_csv(os.path.join(config.clean_dir,'achievement_details_list2.csv'))
