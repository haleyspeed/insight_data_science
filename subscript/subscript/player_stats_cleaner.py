import config
import pandas as pd
import numpy as np
import os

dir_home = config.home_dir
dir_clean = config.clean_dir
dir_processed = config.processed_dir
dir_raw = config.raw_dir
f_in = 'leaderboard_stats.csv'
f_dfa = 'dataforazeroth_complete_dataset.csv'
path_in = os.path.join(dir_processed, f_in) # leaderboard_player_stats
path_in2 = os.path.join(dir_raw, f_dfa) # leaderboard_players

df_ps = pd.read_csv(path_in) # Load in the leaderboard_player_stats
df_dfa = pd.read_csv(path_in2) # load in the leaderboard_stats
df_ps['id'] = df_ps.player + '_' + df_ps.realm
df_dfa['id'] = ''
df_dfa['id'] = df_dfa.player + '_' + df_dfa.realm
df_ps = df_ps.fillna(0) # NA is equivalent to 0 for all columns (player has not attempted or completed)
for index,row in df_dfa.iterrows(): # Format player and realm with lowercase and no special chars
    if isinstance(row.player, str):
        df_dfa.at[index,'player'] = row.player.lower()
    if isinstance(row.realm, str):
        df_dfa.at[index,'realm'] = row.realm.replace('US-', '').replace("'", '').lower()
        df_dfa.at[index,'id'] = df_dfa.loc[index,'player'] + '_' + df_dfa.loc[index,'realm']

df_dfa = df_dfa.set_index('id')
df_ps['leaderboard'] = ''
for index, row in df_ps.iterrows(): # Add leaderboards to player stats
    df_ps.at[index, 'leaderboard'] = df_dfa[df_dfa.index == row.id].leaderboard.values


cols = [col for col in df_ps.columns if 'Unnamed' not in col] # Remove unnamed columns (former indexes)
df_ps = df_ps[cols]

df_ps.to_csv(os.path.join(dir_clean, 'cleaned_leaderboard_player_stats.csv'))
df_dfa.to_csv(os.path.join(dir_clean, 'cleaned_leaderboard_players.csv'))