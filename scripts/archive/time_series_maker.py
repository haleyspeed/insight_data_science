import config
import pandas as pd
import numpy as np
import os
import datetime
import glob


dir_clean = config.clean_dir
dir_processed = config.processed_dir
dir_raw = config.raw_dir
file_in = os.path.join(dir_processed, 'wow_ach_time', '*{}')

# Read in player stats and achievements to dataframes
count = 0
for f in glob.glob(file_in.format('csv')):
    print(f)
    print('Loading data...')
    df_ps = pd.read_csv(f)
    df_ps = df_ps.fillna(0)


    # Make sure there is a unique ID column in the player_stats data
    print('Checking unique ids....')
    if 'id' not in df_ps.columns.values:
        df_ps['id'] = df_ps.player + '_' + df_ps.realm

    # Drop unnamed  and duplicate rows
    print('Cleaning data')
    df_ps = df_ps.drop_duplicates()
    cols = [col for col in df_ps.columns if 'Unnamed' not in col]
    df_ps = df_ps[cols]


    # Load in reference data (achievement and category ids)
    df_cat = pd.read_csv(os.path.join(dir_raw, 'wow_achievement_categories.csv'))
    df_ach = pd.read_csv(os.path.join(dir_clean, 'achievement_details_list.csv'))


    # base_cols contains leaderboard player stats columns without achievements
    base_cols = ['level', 'guild_rank','player', 'id', 'realm', 'realm_id',
        'playable_race', 'playable_class', 'faction', 'guild_name', 'completed_quests',
        'honor_level','mounts_collected','pets_collected','total_achievement_points',
        'total_achievements']
    category_cols = list(df_cat.id.values.astype(int).astype(str))
    engineered_cols = base_cols + category_cols
    ach_ids = df_ps.columns.difference(base_cols) # Keeps only the numeric achievement_id Columns

    # Make sure d columns are read in as strings
    df_ach.category_id = df_ach.category_id.astype(int).astype(str)
    df_ach.achievement_id = df_ach.achievement_id.astype(int).astype(str)
    df_ps[ach_ids] = df_ps[ach_ids].astype(str)
    # Do this once. It takes ~7 hours for 1500 players
    # Make a new, empty dataframe with player info and achievement categories
    df_ps_cat = pd.DataFrame()

    #print(df_ps['10'])
    i = 0
    print('Formatting achievement timestamps....')
    for index, row in df_ps.iterrows():
        tmp = dict.fromkeys(engineered_cols,0) # Achieve cols should be numbers, default value = 0
        for base_col in base_cols:
            tmp[base_col] = row[base_col]  # Copy basic player information from the df_ps dataset
        for col in ach_ids:  # Add category_id as columns instead of achievement_id
            if 'none' not in row[col] and '.' not in row[col] and row[col != 0]:
                month = datetime.datetime.utcfromtimestamp((int(row[col])/1000)).strftime("%Y-%m")
                print(month)
                tmp[col+'_date'] = month  # swaps the value of the cell and the column name
        df_ps_cat = df_ps_cat.append(tmp, ignore_index = True)
        print(i, end = ' ')
        i = i + 1

    df_ps_cat.to_csv(os.path.join(dir_clean,'time_formatted',f.split('wow_ach_time/')[1].replace('.csv', '_utc.csv')))
    print(df_ps_cat.shape)
    count = count + 1