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


print('starting up...')
final_cols = ['faction', 'guild_name', 'guild_rank', 'id', 'level', 'playable_class',
              'playable_race','player', 'realm', 'realm_id', 'total_achievements',
              'total_achievement_points', 'mounts_collected', 'pets_collected','completed_quests',
              'honor_level']
achievement_list = pd.read_csv(os.path.join(config.raw_dir,'wow_achievements.csv'))
achievement_list.columns = ['unnamed0', 'unnamed1', 'player', 'guild', 'realm', 'id']
achievement_list = achievement_list.drop(['unnamed0', 'unnamed1'], axis = 1)
print(achievement_list.columns)
for id in achievement_list.id:
    final_cols.append(str(int(id)))
empty_row = dict.fromkeys(final_cols)
i = 1
for group_num in np.arange(100, 1000, 100):
    print("sifting through players...")
    f = 'wow_roster' + str(group_num) + '.csv'
    player_roster = pd.read_csv(os.path.join(config.home_dir, '../', 'api', f))
    df = pd.DataFrame()
    for m in player_roster.itertuples():
        print("Here's One: " + m.player)
        if m.level == 120:
            print(i, end=' ')
            player = m.player.lower()
            realm = m.realm
            row = cf.get_player_achievements(player, realm, empty_row, access_token)
            if not isinstance(row, str):
                row['player'] = player
                row['realm'] = realm
                row['level'] = m.level
                row['playable_class'] = m.playable_class
                row['faction'] = m.faction
                row['guild_name'] = m.guild_name
                row['guild_rank'] = m.id
                row['playable_race'] = m.playable_race
                row['realm_id'] = m.realm_id
                row['id']  = player + '_' + realm
                row['mounts_collected'] = cf.get_wow_mounts(player, realm, access_token)
                row['pets_collected'] = cf.get_wow_pets(player, realm, access_token)
                row['completed_quests'] = cf.get_wow_quests(player, realm, access_token)
                row['honor_level'] = cf.get_wow_honor(player, realm, access_token)
                df = df.append(row, ignore_index=True)
                #print(row)
        if i % 100 == 0:
            f_name = f.split('roster')[0] + 'achievement_dates_' + str(group_num) + '_' + str(i) + '.csv'
            df.to_csv(os.path.join(config.processed_dir, f_name))
            df = pd.DataFrame()
            print(f_name + ' saved')
        i = i + 1