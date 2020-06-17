import pandas as pd
import os
import numpy as np
import config as cn
import custom_funcs as cf
import glob


# Setup IO
f_cat = os.path.join(cn.clean_dir,'6-13_achievement_list.csv')
folder = os.path.join(cn.processed_dir, '6-15_scrapes')

# Read in the list of categories with achievements
dfc = pd.read_csv(f_cat)
achievements = dfc.achievement_id.values.astype(int).astype(str)


# Define output file columns
player_cols = ['player', 'realm', 'gear_score', 'last_login', 'time_since_login']
months = np.arange(1, 13)
years = [2014, 2015, 2016, 2017, 2018, 2019, 2020]
timepoints = []

for month in months:
    if month < 10:
        month = str(0) + str(month)
    for year in years:
        if year == 2020 and month == '07':
            break
        if year < 2011 and month != '01':

            continue
        else:
            month = str(month)
            timepoints.append(str(year) + '-' + str(month))



os.chdir (folder)
for f in glob.glob('*{}'.format('csv')):

    print(f)

    # Create the output dataframe
    dfo = pd.DataFrame(columns=player_cols + timepoints)

    # Read in raw player achievement stats
    dfr = pd.read_csv(f)
    achievement_cols = [col for col in dfr.columns.values if col in achievements]

    # Build the processed_player_stats.csv dataset
    i = 0
    for index, row in dfr.iloc[:][:].iterrows():

        # Format output file
        f_out = os.path.join(cn.processed_dir, '6-15_scrapes', 'processed',
                'time', f.replace('wow', 'time'))

        # Convert date to month
        row[achievement_cols] = [str(d)[0:7] for d in row[achievement_cols]]

        # Set up df for achievements per month
        t = row[achievement_cols].transpose().reset_index()
        t = t.iloc[1:][:]
        t.columns = ['achievement', 'date']


        t = t.iloc[:][:].groupby('date').count().reset_index() # remove top row (formerly column names before transpose)
        t = t.transpose()
        t.columns = t.iloc[0][:].sort_values()
        t = t.iloc[1:][:]
        to_drop = [n for n in t.columns.values if n not in timepoints]
        t = t.drop(to_drop, axis = 1)


        # Create a new row to append to dfo
        tmp = dict()

        # Add player data to the output row
        for col in player_cols:
            tmp[col.lower()] = row[col.lower()]

        # Add achievements per month to the output row
        for col in t.columns.values:
            tmp[col.lower()] = t[col.lower()].achievement

        dfo = dfo.append(tmp, ignore_index=True)
        dfo = dfo.fillna(int(0))

        i = i + 1
        print(i)

    dfo.to_csv(f_out)
