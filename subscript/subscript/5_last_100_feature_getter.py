import os
import custom_funcs as cf
import csv
import config as cn
import numpy as np
import pandas as pd
import glob


dir_in = os.path.join(cn.processed_dir,'6-10_scrapes', 'processed_6-10-20')
sub = 30
lapsed = 120

last_100 = [str(i) for i in list(np.arange(100,0, -1))]
base_cols = [ 'player', 'realm', 'engagement', 'status','last_login']
columns = ['player' 'realm' 'gear_score' 'last_login'
 'time_since_login' '2007-01' '2008-01' '2009-01' '2010-01' '2011-01'
 '2012-01' '2013-01' '2014-01' '2015-01' '2016-01' '2017-01' '2018-01'
 '2019-01' '2020-01' '2011-02' '2012-02' '2013-02' '2014-02' '2015-02'
 '2016-02' '2017-02' '2018-02' '2019-02' '2020-02' '2011-03' '2012-03'
 '2013-03' '2014-03' '2015-03' '2016-03' '2017-03' '2018-03' '2019-03'
 '2020-03' '2011-04' '2012-04' '2013-04' '2014-04' '2015-04' '2016-04'
 '2017-04' '2018-04' '2019-04' '2020-04' '2011-05' '2012-05' '2013-05'
 '2014-05' '2015-05' '2016-05' '2017-05' '2018-05' '2019-05' '2020-05'
 '2011-06' '2012-06' '2013-06' '2014-06' '2015-06' '2016-06' '2017-06'
 '2018-06' '2019-06' '2020-06' '2011-07' '2012-07' '2013-07' '2014-07'
 '2015-07' '2016-07' '2017-07' '2018-07' '2019-07' '2011-08' '2012-08'
 '2013-08' '2014-08' '2015-08' '2016-08' '2017-08' '2018-08' '2019-08'
 '2020-08' '2011-09' '2012-09' '2013-09' '2014-09' '2015-09' '2016-09'
 '2017-09' '2018-09' '2019-09' '2020-09' '2011-10' '2012-10' '2013-10'
 '2014-10' '2015-10' '2016-10' '2017-10' '2018-10' '2019-10' '2020-10'
 '2011-11' '2012-11' '2013-11' '2014-11' '2015-11' '2016-11' '2017-11'
 '2018-11' '2019-11' '2020-11' '2011-12' '2012-12' '2013-12' '2014-12'
 '2015-12' '2016-12' '2017-12' '2018-12' '2019-12' '2020-12']
os.chdir (dir_in)
for f in glob.glob('*{}'.format('csv')):
#for f in ['trimmed_6-8_dates_9000_16200.csv']:
    print(f)
    df = pd.read_csv(f, dtype = 'unicode')
    if 'id' not in df.columns.values:
        if len(df.index.values) > 5:
            df.columns = columns
            df['id'] = df.player + '_' + df.realm
            print("ok")
        else:
            print ('Error: Length of columns')
            continue



    out_cols = base_cols + last_100 + ['first_achievement_date','last_achievement', 'last_achievement_date']
    a_cols = [c for c in df.columns.values if c not in out_cols]
    del_cols = [c for c in df.columns.values if 'unnamed' in str(c).lower()]

    df = df.drop(del_cols, axis = 1)
    df = df.set_index ('id')
    dfo = pd.DataFrame(columns = out_cols)

    # Calculate engagement score and status
    df.engagement = np.nan
    df.status = ''
    for index, row in df.iterrows():
        if int(row.time_since_login.split(' ')[0]) <= sub:
            df.at[index,'engagement'] = 0
            df.at[index,'status'] = 'subscribed'
        elif int(row.time_since_login.split(' ')[0]) <= lapsed:
            df.at[index,'engagement'] = 1
            df.at[index,'status'] = 'lapsed'
        elif int(row.time_since_login.split(' ')[0]) > lapsed:
            df.at[index,'engagement'] = 2
            df.at[index,'status'] = 'unsubscribed'

    # Sort individual columns of dft and if '20' in col[index]
    i = 0
    dft = df.transpose()
    for col in dft.columns.values:

        new = pd.DataFrame(columns = out_cols)

        new.loc[i,base_cols] = df.loc[col,base_cols]
        l = dft[col]
        l = l.reset_index()
        l.columns = ['achievement', 'date']
        l = l[l.achievement != 'last_login']
        l = l[l.achievement != 'time_since_login']
        l = l.astype(str).apply(lambda x: x.str[:7])
        l = l[l.date.str.contains("-")]
        l = l[l.date.str.contains('NaN') == False]
        l = l[l.date.str.contains('none') == False]
        l = l.astype(str).sort_values('date', ascending = False)
        ach100 = list(l.achievement[:100])
        date100 = list(l.date[:100])
        for count, x in enumerate(last_100):
            try:
                new.loc[i, str(x)] = ach100[count]
            except:
                new.loc[i, str(x)] = ''
        new.loc[i,'last_achievement'] = ach100[0]
        new.loc[i,'last_achievement_date'] = date100[0]
        dfo = dfo.append(new, ignore_index = True)
        i = i + 1
    dfo.to_csv(os.path.join(cn.clean_dir, 'last_100', f.replace('trimmed','last100')))
