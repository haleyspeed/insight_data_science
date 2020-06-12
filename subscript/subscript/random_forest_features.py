import config as cn
import pandas as pd
import numpy as np
import custom_funcs as cf
import os

risk = 60
lapsed = 180


print ("Reading in file...")
#df = pd.read_csv(os.path.join(cn.clean_dir, 'final_feature_stats.csv'), dtype = 'unicode')
df = pd.read_csv(os.path.join(cn.processed_dir,'6-10_scrapes','processed_6-10-20', 'trimmed_6-8_dates_100_100.csv'), dtype = 'unicode')
extra_cols = [c for c in df.columns.values if 'unnamed' in str(c).lower()]
df = df.drop(extra_cols, axis = 1)
if 'id' not in df.columns.values:
    df['id'] = df.player + '_' + df.realm


# Calculate engagement score and status
df['engagement'] = np.nan
df['status'] = ''
for index, row in df.iterrows():
    if int(row.time_since_login.split(' ')[0]) <= 30:
        df.at[index,'engagement'] = 0
        df.at[index,'status'] = 'subscribed'
    elif int(row.time_since_login.split(' ')[0]) <= risk:
        df.at[index,'engagement'] = 1
        df.at[index,'status'] = 'risk'
    elif int(row.time_since_login.split(' ')[0]) <= lapsed:
        df.at[index,'engagement'] = 2
        df.at[index,'status'] = 'lapsed'
    elif int(row.time_since_login.split(' ')[0]) <= 365:
        df.at[index,'engagement'] = 3
        df.at[index,'status'] = 'unsubscribed'

# Rank the achievements by order of completion
ranks = [c for c in df.columns.values if c not in ['last_login', 'engagement',
    'status', 'id', 'gear_score', 'player','realm','time_since_login',
    'total_achievement_points', 'total_achievements']]

#df[ranks] = np.where(df[ranks].isnull() == True, 0 , df[ranks])

df[ranks] = np.where(df[ranks] == 'none', np.nan , df[ranks])

df[ranks] = df[ranks].astype(str).apply(lambda x: x.str[:7])
df[ranks] = df[ranks].astype(str).apply(lambda x: [y.replace('-','.') for y in x])
df[ranks] = np.where('.' in df[ranks] == True, df[ranks].astype(float) , df[ranks])
df[ranks] = np.where(df[ranks].astype(float) <= 2019.07, np.nan , df[ranks])
df[ranks] = df[ranks].astype(float).rank(axis = 0, na_option = 'bottom', ascending = True, numeric_only = True)


print ("Making the tree dataset...")
df_tree = df.copy()
df_tree = df_tree.drop(['last_login', 'player','realm','status',
    'time_since_login','gear_score',], axis = 1)
df_tree = df_tree.set_index('id')

#print(df.head())
# Set up lapsed and current
print('Making subscribed dataset...')
current = df_tree[df_tree.engagement.astype(int) == 0]
sub_achievement_ids, sub_achievements = cf.random_forest_feature_selection (current, 'subscribed')

print("Making lapsed dataset...")
lapsed = df_tree[df_tree.engagement.astype(int) != 0][df_tree.engagement.astype(int) !=1]
lapsed_acheivement_ids,lapsed_achievements = cf.random_forest_feature_selection (lapsed, 'lapsed')


dfo = pd.DataFrame([sub_achievement_ids, sub_achievements, lapsed_acheivement_ids, lapsed_achievements]).T
dfo.columns = ['current_id', 'current_name', 'lapsed_id', 'lapsed_name']
dfo['completed_in_lapsed'] = np.nan
dfo['target_content_id'] = ''
dfo['target_content_name'] = ''
for index, row in dfo.iterrows():
    if row.current_id not in dfo.lapsed_id.values:
        dfo.at[index,'target_content_id'] = row.current_id
        dfo.at[index,'target_content_name'] = row.current_name
        dfo.at[index,'completed_in_lapsed'] = 0
    elif row.current_id in dfo.lapsed_id.values:
        dfo.at[index, 'target_content_id'] = ''
        dfo.at[index,'target_content_name'] =''
        dfo.at[index,'completed_in_lapsed'] = 1
dfo.to_csv(os.path.join(cn.clean_dir, 'pickles', 'feature_selection_' + str(risk) + '-' + 'lapsed.csv'))
print('Target Content: ')
recommendations = dfo.current_id[dfo.completed_in_lapsed == 0]


## Initial results were heavily skewed toward old content. Will only look at recent expansion next
