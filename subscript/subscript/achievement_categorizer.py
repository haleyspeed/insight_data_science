import config as cn
import pandas as pd
import numpy as np
import os



# Read in player stats and achievements to dataframes
print('Loading data...')
#df = pd.read_csv(os.path.join(cn.clean_dir, 'final_feature_stats.csv'),
        #dtype = 'unicode')
df = pd.read_csv(os.path.join(cn.processed_dir,'6-15_scrapes',
        'processed', 'features', 'engaged',
        'engaged_6-8_dates_9000_22300.csv'),dtype = 'unicode')

# Make sure there is a unique ID column in the player_stats data
print('Checking unique ids....')
if 'id' not in df.columns.values:
    df['id'] = df.player + '_' + df.realm

# Drop unnamed  and duplicate rows
print('Cleaning data')
df = df.drop_duplicates()
cols = [str(col).lower() for col in df.columns.values if 'unnamed' not in str(col).lower()]
df = df[cols]
df = df.fillna('none')


# Load in reference data (achievement and category ids)
print('Categorizing achievements....')
dfa = pd.read_csv(os.path.join(cn.clean_dir, '6-13_achievement_list.csv'))

cols = [c for c in dfa.columns.values if 'unnamed' not in str(c).lower()]
dfa[cols]
ach = [str(c) for c in dfa.achievement_id if str(c) in df.columns.values]

i = 1
for a in ach:
    category = dfa.category_name[dfa.achievement_id.astype(str) == a]
    df[a] = np.where(df[a].str.contains("20"), category, df[a])
    print(i)
    i = i + 1
df.to_csv(os.path.join(cn.clean_dir, 'final_feature_categories.csv'))
