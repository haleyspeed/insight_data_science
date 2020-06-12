import streamlit as st
import pandas as pd
import config as cn
import os.path
import requests
import numpy as np

# Make a "database" of subscribers.SLOW!!!! Want a db unless using spark
# Need output with just engagment score
# Save a df with
@st.cache
def get_data():
    df = pd.read_csv(os.path.join(cn.clean_dir, 'final_player_stats_test2.csv'), dtype = 'unicode')
    df_rec = pd.read_csv(os.path.join(cn.clean_dir, 'pickles','feature_selection_60-lapsed.csv'))
    df_rec = df_rec[df_rec.target_content_name.isnull() == False]
    return df, df_rec

df, df_rec = get_data()

st.markdown('# SubScript')
st.markdown('### Guaging subscriber engagement to reduce churn')
st.markdown('\n')

server_name = st.text_input("Server ID \t", max_chars = 100,value='Optional')
player_name = st.text_input("User Name \t", max_chars = 100,value='Optional')
submit = st.button('Search')

if submit:
    df_results = df[1:3]
    if server_name != 'Optional':
        df_results = df_results[df_results.realm == server_name]
    if player_name != 'Optional':
        df_results = [df_results.player == server_name]
    if player_name != 'Optional' and server_name != 'Optional':
        df_results = df.results[df_results.realm == server_name][df_results.player == player_name]
    st.table(df_results)


recs = df_rec.target_content_id[:5]
rec_names = df_rec.target_content_name[:5]

    #
feat1 = st.checkbox(rec_names.iloc[0])
feat2 = st.checkbox(rec_names.iloc[1])
feat3 = st.checkbox(rec_names.iloc[2])
feat4 = st.checkbox(rec_names.iloc[3])
feat5 = st.checkbox(rec_names.iloc[4])


data = pd.DataFrame(columns = ['y'])
data.y = [0,0,0,0,0]
if feat1:
    data.y = [1+(15*245),0,0,0,0]
if feat2:
    data.y = [0,2 +(15*265),0,0,0]
if feat1 and feat2:
    data.y = [1+(15*245),2 +(15*265),0,0,0]
if feat3:
    data.y = [0,0,3 + (429 * 15),0,0]
if feat2 and feat3:
    data.y = [0,2 +(15*265),3 + (429 * 15),0,0]
if feat1 and feat2 and feat3:
    data.y = [1+(15*245),2 +(15*265),3 + (429 * 15),0,0]
if feat1 and feat3:
    data.y = [1+(15*245),0,3 + (429 * 15),0,0]


st.bar_chart(data)


# streamlit.slider(label, min_value=None, max_value=None, value=None, step=None, format=None)
#x = st.slider ('x')
#st.write(x, 'squared is', x * x)
