import pandas as pd
import os
import config as cn

df = pd.read_csv(os.path.join(cn.processed_dir, '6-10_scrapes',
  'processed_6-10-20', 'concatenated', 'engaged',
  '500concat_trim_6-8_dates_100_22400.csv'), dtype = 'unicode')
#keep_cols = [c for c in df.columns.values if 'unnamed' not in str(c)]
#del_cols = ['status', 'gear_score','last_login', 'player',
#    'realm', 'time_since_login', 'total_achievement_points',
#    'total_achievements']

df = df.set_index('id')
print(df.head())
for c in df.columns.values:
  print(c)
#print(df.groupby('engagement').count())
