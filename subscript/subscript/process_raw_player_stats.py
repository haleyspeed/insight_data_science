import pandas as pd
import os
import numpy as np
import config as cn
import custom_funcs as cf
import glob


# Setup IO
f_cat = os.path.join(cn.clean_dir,'achievement_details_list.csv')
folder = os.path.join(cn.processed_dir)

# Read in the list of categories with achievements
dfc = pd.read_csv(f_cat)

# Define output file columns
player_cols = ['player', 'realm', 'gear_score', 'last_login', 'time_since_login']
categories = [name.lower() for name in np.unique(dfc.category_name)]
months = np.arange(1, 13)
years = [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
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
    dfo = pd.DataFrame(columns=player_cols + timepoints + categories)

    # Read in raw player achievement stats
    dfr = pd.read_csv(f)
    achievement_cols = [col for col in dfr.columns.values if col not in player_cols]


    # Build the processed_player_stats.csv dataset
    i = 0
    for index, row in dfr.iterrows():

        # Format output file
        f_out = os.path.join(cn.clean_dir, f.replace('wow', 'cat_counts'))

        # Convert date to month
        row[achievement_cols] = [str(d)[0:7] for d in row[achievement_cols]]

        # Set up df for achievements per month
        t = row[achievement_cols].transpose().reset_index()
        t = t.iloc[1:][:]
        t.columns = ['achievement', 'date']

        # Setup df dates by category
        c = t.copy()
        for indexes, rows in c.iterrows():
            try:
                c.at[indexes, 'category'] = list(dfc[dfc.achievement_id.astype(str) == rows.achievement].category_name)[0]
            except:
                continue
        b = c.copy()
        d = c.copy()

        # Get achievements per month
        t = t.iloc[:][:].groupby('date').count().reset_index() # remove top row (formerly column names before transpose)
        t = t.transpose()
        t.columns = t.iloc[0][:].sort_values()
        t = t.iloc[1:][:]
        to_drop = [n for n in t.columns.values if n not in timepoints]
        t = t.drop(to_drop, axis = 1)

        # Get total categories
        c = c.iloc[:][:].groupby('category').count().reset_index()  # remove top row (formerly column names before transpose)
        c = d.transpose()
        c.columns = c.iloc[0][:].sort_values()
        c.columns = c.iloc[2][:]
        c = c.drop(['achievement', 'category'])

        # Get dates per category
        #d = d.groupby('category')['date'].apply(list).reset_index().transpose()
        #d.columns = [col.lower() for col in d.iloc[0][:]]
        #d = d.iloc[1:][:]

        # Create a new row to append to dfo
        tmp = dict()

        # Add player data to the output row
        for col in player_cols:
            tmp[col.lower()] = row[col.lower()]

        # Add achievements per month to the output row
        for col in t.columns.values:
            tmp[col.lower()] = t[col.lower()].achievement

        # Add category per month data to the output row
        #for col in d.columns.values:
        #    tmp[col.lower()] = d[col.lower()].date

        add_categories = [add for add in dfo.columns.values if add not in tmp.keys()]
        for add in add_categories:
            tmp[add] = 0

        dfo = dfo.append(tmp, ignore_index=True)

        i = i + 1
        print(i)
    dfo.to_csv(f_out)
