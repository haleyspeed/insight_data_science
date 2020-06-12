import streamlit as st
import pandas as pd
import config as cn
import os.path
import requests
import numpy as np
import matplotlib.pyplot as plt

# Make a "database" of subscribers.SLOW!!!! Want a db unless using spark
# Need output with just engagment score
# Save a df with
#@st.cache

risk = 60
lapsed = 180
def get_data():
    df = pd.read_csv(os.path.join(cn.clean_dir,'processed_6-10-20', 'processed_6-8_dates_100_100.csv'), dtype = 'unicode')

    df_rec = pd.read_csv(os.path.join(cn.clean_dir, 'pickles','feature_selection_60-lapsed.csv'))
    df_rec = df_rec[df_rec.target_content_name.isnull() == False]
    features = ['gear_score', 'last_login', 'player', 'realm', 'time_since_login']
    return df[features], df_rec

df, df_rec = get_data()
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


st.markdown('# SubScript')
st.markdown('### Boosting subscription volume with targeted content')
st.markdown('\n')

server_name = st.text_input("Server ID \t", max_chars = 100,value='Optional')
player_name = st.text_input("User Name \t", max_chars = 100,value='Optional')
submit = st.button('Search')
st.write('')
users = ['anemonae_thrall', 'heyimpell_thrall', 'dyonian-thrall']
if submit:
    df_results = df[df.engagement ==1]
    #if server_name != 'Optional':
    #    df_results = df_results[df_results.realm == server_name]
    #if player_name != 'Optional':
    #    df_results = df_results[df_results.player == player_name]
    #if player_name != 'Optional' and server_name != 'Optional':
    #    df_results = df_results[df_results.realm == server_name][df_results.player == player_name]
    st.table(df_results)


    recs = df_rec.target_content_id[:5]
    rec_names = df_rec.target_content_name[:5]
    rec_names = [n for n in rec_names]
    rec_names.append('All Features')

    e = [250, 523, 623, 191, 800, 0] # Swap these to predicted gain

    data = pd.DataFrame(columns = ['Estimate'])
    data.Estimate = [1000,2000,4320,3200,5732,0]
    data.Estimate[5] = np.sum(data.Estimate[:5])


    fig, ax = plt.subplots()
    ax.bar (x = rec_names[0], height = data.Estimate[0], color = 'turquoise')
    ax.bar (x = rec_names[1], height = data.Estimate[1], color = 'skyblue')
    ax.bar (x = rec_names[2], height = data.Estimate[2], color = 'mediumpurple')
    ax.bar (x = rec_names[3], height = data.Estimate[3], color = 'plum')
    ax.bar (x = rec_names[4], height = data.Estimate[4], color = 'salmon')
    ax.bar (x = rec_names[5], height = data.Estimate[5], color = 'sandybrown')

    ax.annotate(data.Estimate[0], xy=(-0.2,data.Estimate[0] * 2))
    ax.annotate(data.Estimate[1], xy=(.8,data.Estimate[1] * 1.5))
    ax.annotate(data.Estimate[2], xy=(1.8,data.Estimate[2] * 1.25))
    ax.annotate(data.Estimate[3], xy=(2.8,data.Estimate[3] * 1.25))
    ax.annotate(data.Estimate[4], xy=(3.8,data.Estimate[4] * 1.25))
    ax.annotate(data.Estimate[5], xy=(4.8,data.Estimate[5] * 1.05))

    ax.tick_params(labelsize = 10)
    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(0, 20000)
    ax.set_xticklabels(rec_names, rotation = 90)
    ax.set_ylabel('Estimated Revenue Recovered (USD)', fontsize = 10)
    plt.tight_layout()
    st.pyplot()

#####
#risk = 60
#lapsed = 180
#pickle_model = 'rf_time_model_60-180.sav'
#pickle_path = os.path.join(cn.clean_dir, 'pickles', pickle_model)
#get_predictions (pickle_model, pickle_path, risk, lapsed, samples)
