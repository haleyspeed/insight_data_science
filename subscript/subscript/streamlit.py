import streamlit as st
import pandas as pd
import config
import os.path
import requests
import numpy as np

# Make a "database" of subscribers.SLOW!!!! Want a db unless using spark
@st.cache
def get_data():
    csv = os.path.join(config.processed_dir, 'wow_achievement_dates_16000_11100.csv')
    df = pd.read_csv(csv)
    df['engagement score'] = np.random.randint(0,1000)
    return df

df = get_data()

st.markdown('# SubScript')
st.markdown('### Guaging subscriber engagement to reduce churn')
st.markdown('\n')

server_name = st.text_input("Server ID \t", max_chars = 100,value='Optional')
player_name = st.text_input("User Name \t", max_chars = 100,value='Optional')
submit = st.button('Search')

if submit:
    df_results = df[df.engagement_score < 100]
    if server_name != 'Optional':
        df_results = df_results[df_results.realm == server_name]
    if player_name != 'Optional':
        df_results = [df_results.player == server_name]
    if player_name != 'Optional' and server_name != 'Optional':
        df_results = df.results[df_results.realm == server_name][df_results.player == player_name]
    st.table(df_results)

# streamlit.slider(label, min_value=None, max_value=None, value=None, step=None, format=None)
#x = st.slider ('x')
#st.write(x, 'squared is', x * x)