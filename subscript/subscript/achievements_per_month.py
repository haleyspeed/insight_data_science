import config
import pandas as pd
import numpy as np
import os
import datetime
import glob


dir_clean = config.clean_dir
dir_processed = config.processed_dir
dir_raw = config.raw_dir
file_in = os.path.join(dir_clean, 'time_formatted', '*{}')

# Read in player stats and achievements to dataframes
count = 0
for f in glob.glob(file_in.format('csv')):
    print(f)
    df_ps_cat = pd.read_csv(f)
    # df_ps_cat = df_ps_cat.set_index('id')

    base_cols = ['level', 'guild_rank', 'player', 'id', 'realm', 'realm_id',
                 'playable_race', 'playable_class', 'faction', 'guild_name', 'completed_quests',
                 'honor_level', 'mounts_collected', 'pets_collected', 'total_achievement_points',
                 'total_achievements']
    months = np.arange(1,13)
    years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
    timepoints = []

    for month in months:
        if month < 10:
            month = str(0)+str(month)
        for year in years:
            if year == 2020 and month == '05':
                break
            else:
                month = str(month)
                timepoints.append(str(year) + '-' + str(month))


    df_date = pd.DataFrame(columns=base_cols + timepoints)
    i = 0
    for index, row in df_ps_cat.iterrows():
        #print(i, end=' ')
        t = pd.DataFrame(row.transpose())
        t = t.reset_index()
        print(t)
        t.columns = ['ach', 'date']
        tg = t.groupby('date').count()
        rows = [rows for rows in tg.index.values if '-' in str(rows) and '20' in str(rows)]
        tg = tg.loc[rows]
        tg = tg.transpose()
        for col in base_cols:
            df_date.at[index, col] = row[col]
        for col in tg.columns.values:
            df_date.at[index, col] = tg[col][0]
        i = i + 1

    cols = []
    for col in df_date.columns.values:
        cols.append(col.replace(' ', '-'))
    df_date.columns = cols
    df_date.to_csv(os.path.join(dir_clean, 'time_tallied', f.split('time_formatted/')[1].replace('utc', 'datetime')))
    count = count + 1


