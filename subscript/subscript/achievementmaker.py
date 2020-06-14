import config as cn
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

dfa = pd.DataFrame()
for id in get_wow_achievement_ids (access_token):
    ach = get_wow_achievement(achievement_id)
    if ach['account_wide'] == 'false':
        dfa = dfa.append()
        print ach
dfa.to_csv(os.path.join(cn.dir_clean, '6-13_achievement_list'))
