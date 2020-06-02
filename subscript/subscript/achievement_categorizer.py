import config
import pandas as pd
import numpy as np
import os

dir_clean = config.clean_dir
dir_processed = config.processed_dir
dir_raw = config.raw_dir

# Read in player stats and achievements to dataframes
print('Loading data...')
df_ps = pd.read_csv(os.path.join(dir_processed, 'player_stats.csv'))
df_cat = pd.read_csv(os.path.join(dir_raw, 'wow_achievement_categories.csv'))
df_ach = pd.read_csv(os.path.join(dir_clean, 'achievement_details_list.csv'))

# base_cols contains leaderboard player stats columns without achievements
base_cols = ['leaderboard','level', 'guild_rank','player', 'id', 'realm', 'realm_id',
        'playable_race', 'playable_class', 'faction', 'guild_name', 'completed_quests',
        'honor_level','mounts_collected','pets_collected','total_achievement_points',
        'total_achievements']
category_cols = list(df_cat.id.values.astype(int).astype(str))
engineered_cols = base_cols + category_cols
ach_ids = df_ps.columns.difference(base_cols) # Keeps only the numeric achievement_id Columns

# Make sure d columns are read in as strings
df_ach.category_id = df_ach.category_id.astype(int).astype(str)
df_ach.achievement_id = df_ach.achievement_id.astype(int).astype(str)

print('Checking unique ids....')
# Make sure there is a unique ID column in the player_stats data
if 'id' not in df_ps.columns.values:
    df_ps['id'] = df_ps.player + '_' + df_ps.realm

# Do this once. It takes ~7 hours for 1500 players
# Make a new, empty dataframe with player info and achievement categories
df_ps_cat = pd.DataFrame(columns=engineered_cols)
i = 0
start = 0
end = 10

print('Categorizing achievements....')
for index, row in df_ps[start:end,:].iterrows():
    print(i, end = ' ')
    tmp = dict.fromkeys(engineered_cols,0) # Achieve cols should be numbers, default value = 0
    for base_col in base_cols:
        tmp[base_col] = row[base_col]  # Copy basic player information from the df_ps dataset
    for col in ach_ids:  # Add category_id as columns instead of achievement_id
        if row[col] == 1:
            category_id = df_ach.loc[df_ach.achievement_id == col].category_id.values[0]
            tmp[category_id] = tmp[category_id] + 1  # Tallies the number of achievements completed in a category
    df_ps_cat = df_ps_cat.append(tmp, ignore_index = True)
    if i % 1000 == 0:
        df_ps_cat.to
        f_name = 'categorized_leaderboard_player_stats_' + i + '.csv'
        df_ps_cat.to_csv(os.path.join(dir_clean,f_name))
        df_ps_cat = pd.DataFrame()
    i = i + 1