import os
import custom_funcs as cf
import config as cn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Load in time dataset
dir_in = os.path.join(os.path.join(cn.processed_dir, '6-10_scrapes', 'processed_6-10-20',
    'time', 'engaged'))
f_in = 'engaged_time_6-8_dates_100_4500.csv'
dir_out = os.path.join(os.path.join(cn.clean_dir, 'eda'))


# Read in the time series dataset
df = pd.read_csv(os.path.join(dir_in, f_in))
df = df.drop_duplicates()
extra_cols = [c for c in df.columns.values if 'unnamed' in str(c).lower()]
df = df.drop(extra_cols, axis = 1)
#print(df)

# Get descriptive stats by engagement score
df_desc = df.groupby('engagement').describe()
df_desc.to_csv(os.path.join(dir_out, 'descriptive_stats_time.csv'))
#print(df_desc)


# Plot the time Series
time_cols = cf.get_dates()
time_cols.append('engagement')
drop_cols = [c for c in df.columns.values if c not in time_cols]
df_ts = df.drop(drop_cols, axis = 1)
df_ts.to_csv(os.path.join(dir_out, 'time_series.csv'))
#print(df_ts)

df_tsm = df_ts.groupby('engagement').describe()
df_tsm.to_csv(os.path.join(dir_out, 'time_series_desc.csv'))
#print(df_tsm)

df_tsp = df_ts.groupby('engagement').mean().T
print(df_tsp)
#print(df_tsp.columns.values)

fig, ax = plt.subplots(figsize=(20, 10))

a = ax.plot(sorted(df_tsp.mean().index.values),df_tsp.mean(),
    label = 'active',  color = 'green', alpha = 0.5)
a = ax.set_xlabel('\nTime (years)', fontsize = 20)
a = ax.set_ylabel('Achievements/Month \n', fontsize = 20)
a = ax.tick_params(labelsize = 16)
plt.tight_layout()
plt.show()
