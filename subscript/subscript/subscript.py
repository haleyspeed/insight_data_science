import streamlit as st
import pandas as pd
import config as cn
import os.path
import requests
import numpy as np
import matplotlib.pyplot as plt
import random as rn
import joblib

#@st.cache

def get_data():
    """ Loads in pre-processed data for fast loading """
    df = pd.read_csv(os.path.join(cn.clean_dir, 'random_forest_classifier',
            'test_predictions.csv'), dtype = 'unicode')
    df['id'] = df.player + '_' + df.realm
    df = df.set_index('id')
    df_rec = pd.read_csv(os.path.join(cn.clean_dir, 'selected_features.csv'),
            dtype = 'unicode')
    df_rec = df_rec[df_rec.id != 'engagment']
    return df, df_rec


def get_recommendations (df_feat):
    """ Uses a random number generator to select 5 of the most popular features
    from the achievement list csv"""
    features = list()
    for i in np.arange(0,20):
        n = rn.randrange(0,len(df_rec.name))
        rec = [df_rec.iloc[n]['id'], df_rec.iloc[n]['name'],
                df_rec.iloc[n]['description']]
        features.append(rec)
    return features[:5]


def update_plot(fig, ax, df_results):
    """ Plots the Maximum Estimated ROI"""
    retained = list()
    for i in np.arange(1,6):
        hyp = df_results[df_results['pred' + str(i)] == '0'].player.values
        retained.append(len(hyp))
    y1 = retained[0] * sub_cost / 1000
    y2 = retained[1] * sub_cost / 1000
    y3 = retained[2] * sub_cost / 1000
    y4 = retained[3] * sub_cost / 1000
    y5 = retained[4] * sub_cost / 1000
    ax.bar (x = 1, height = y1, color = 'turquoise', edgecolor = 'dimgray')
    ax.bar (x = 2, height = y2, color = 'skyblue', edgecolor = 'dimgray')
    ax.bar (x = 3, height = y3, color = 'mediumpurple', edgecolor = 'dimgray')
    ax.bar (x = 4, height = y4, color = 'plum', edgecolor = 'dimgray')
    ax.bar (x = 5, height = y5, color = 'salmon', edgecolor = 'dimgray')
    ax.annotate('$' + str(y1)[:4], xy=(0.75, y1 + y1 * 0.02), fontsize = 15)
    ax.annotate('$' + str(y2)[:4], xy=(1.75, y2 + y2 * 0.02), fontsize = 15)
    ax.annotate('$' + str(y3)[:4], xy=(2.75, y3 + y3 * 0.02), fontsize = 15)
    ax.annotate('$' + str(y4)[:4], xy=(3.75, y4 + y4 * 0.02), fontsize = 15)
    ax.annotate('$' + str(y5)[:4], xy=(4.75, y5 + y5 * 0.02), fontsize = 15)
    ax.tick_params(labelsize = 15)
    ax.set_xlim(0.5, 5.5)
    ax.set_ylim(0,y5 + y5 *0.5)
    ax.set_ylabel('Estimated Revenue Recovered \n (per $1000 USD) \n', fontsize = 18)
    ax.set_xlabel('\n Additional Achievements Completed', fontsize = 18)
    plt.tight_layout()
    st.sidebar.pyplot()


# Set default variables
df, df_rec = get_data()
get_recs = False
sub_cost = 15
df_results = pd.DataFrame(columns = df.columns.values)
x = 0
features = ['player', 'realm','last_login', 'time_since_login',
           'engagement', 'status','pred', 'pred1', 'pred2', 'pred3',
           'pred4', 'pred5']


# Setup main window
df_results = df[df.engagement == '1.0'].drop_duplicates()
st.title('SubScript')
st.subheader('Boosting subscription volume with targeted content')
st.markdown('\n')

# Refine the selected dataset by server
#st.sidebar.markdown('\n')
#st.sidebar.subheader('Refine By Server ID')
#server_name = st.sidebar.selectbox("", df_results.realm.unique())
#st.sidebar.markdown('\n')
#if server_name.lower() != '':
#    df_results = df_results[df_results.realm == server_name.lower()]
#    retained = list()
#    for i in np.arange(1,6):
#        hyp = df_results[df_results['pred' + str(i)] == '0'].player.values
#        retained.append(len(hyp))
#    y1 = retained[0] * sub_cost / 1000
#    y2 = retained[1] * sub_cost / 1000
#    y3 = retained[2] * sub_cost / 1000
#    y4 = retained[3] * sub_cost / 1000
#    y5 = retained[4] * sub_cost / 1000
#    st.sidebar.bar_chart([y1,y2,y3,y4,y5])




#start = st.button ('Get At-Risk Players')
#if start:
    # Puts the Maximum ROI on the sidebar
st.write ('\n')
st.sidebar.subheader('Estimated Return on Investment')
fig, ax = plt.subplots()
update_plot(fig, ax, df_results)
start = True

recs = get_recommendations(df_rec)
rec_list = st.sidebar.button('Get Curated Recommendations')
if rec_list:
    st.sidebar.subheader(recs[0][1])
    st.sidebar.markdown(recs[0][2])
    st.sidebar.subheader(recs[1][1])
    st.sidebar.markdown(recs[1][2])
    st.sidebar.subheader(recs[2][1])
    st.sidebar.markdown(recs[2][2])
    st.sidebar.subheader(recs[3][1])
    st.sidebar.markdown(recs[3][2])
    st.sidebar.subheader(recs[4][1])
    st.sidebar.markdown(recs[4][2])
    start = True
st.table(df_results[features])
start = True
