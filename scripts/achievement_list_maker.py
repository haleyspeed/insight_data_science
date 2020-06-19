import config as cn
import custom_funcs as cf
import pandas as pd
import os
import numpy as np
import configparser as cp


f_config = os.path.join(cn.home_dir, '../', 'api', 'config.ini')
conf = cp.ConfigParser()
conf.read(f_config)
blizzard_key = conf.get('KEYS', 'blizzard')
blizzard_secret = conf.get('KEYS', 'blizzard_secret')
locale = 'en_US'
namespace = 'static-us'
access_token = cf.get_access_token(blizzard_key, blizzard_secret)

dfa = pd.DataFrame()
for id in cf.get_wow_achievement_ids (access_token):
    ach = cf.get_wow_achievement(id, access_token)
    if ach['account_wide'] == False:
        dfa = dfa.append(ach, ignore_index = True)
        print (ach['achievement_id'])
dfa.to_csv(os.path.join(cn.clean_dir, '6-13_achievement_list.csv'))
