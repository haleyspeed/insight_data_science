import sys
import streamlit as st
import pandas as pd
import config as cn
import os.path
import numpy as np
import matplotlib.pyplot as plt
import random as rn
import time



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
    ax.set_xlabel('\n Additional Content Completed', fontsize = 18)
    plt.tight_layout()
    main_bottom.pyplot()
    return retained
#@st.cache
# Set default variables
df, df_rec = get_data()
get_recs = False
sub_cost = 15
df_results = pd.DataFrame(columns = df.columns.values)
x = 0
features = ['player', 'realm','gear_score','last_login','status']


# Setup main window at start
df_results = df[df.engagement == '1.0'].drop_duplicates()
main_top = st.image('subscript_full.jpg')

#st.title('SubScript')
st.subheader('Boosting subscription volume with targeted content')
st.markdown('\n')
fig, ax = plt.subplots()
main_bottom = st.empty()

# Action to get At-Risk Players
st.sidebar.markdown(' ')
st.sidebar.subheader('Predict Player Engagement')
start = st.sidebar.button('Get At-Risk Players')
if start:
    main_top.image('subscript.jpg')
    main_bottom.table(df_results[features])

# Setup sidebar at start
side1 = st.sidebar.empty()
side2 = st.sidebar.empty()
side3 = st.sidebar.empty()
side4 = st.sidebar.empty()

# Action for Get Recommendations button
st.sidebar.markdown(' ')
recs = get_recommendations(df_rec)
rec_list = side1.subheader('Content Recommendations')
rec_list = side2.button('Get Curated Recommendations')
if rec_list:
    main_top.empty()
    main_top.image('subscript.jpg')
    main_bottom.empty()
    st.subheader(recs[0][1])
    st.write(recs[0][2])
    st.subheader(recs[1][1])
    st.write(recs[1][2])
    st.subheader(recs[2][1])
    st.write(recs[2][2])
    st.subheader(recs[3][1])
    st.write(recs[3][2])
    st.subheader(recs[4][1])
    st.write(recs[4][2])

# Action for "Calculate ROI"
st.write ('\n')
side3.subheader('Estimated Return on Investment')
calc = side4.button('Calculate ROI')
if calc:
    main_top.empty()
    main_bottom.empty()
    main_top.image('subscript.jpg')

    retained = update_plot(fig, ax, df_results)
    sample_size = len(df_results.player)
    #st.sidebar.markdown(sample_size)
    percent_recovery = []
    for i in np.arange(0,5):
        percent_recovery.append(round(100*(retained[i])/sample_size,1))
    st.sidebar.subheader('Estimated Conversion from At-Risk to Active Status: ')
    st.sidebar.markdown('1 additional activity: ' + str(percent_recovery[0]) + '%')
    st.sidebar.markdown('2 additional activities: ' + str(percent_recovery[1])+ '%')
    st.sidebar.markdown('3 additional activities: ' + str(percent_recovery[2])+ '%')
    st.sidebar.markdown('4 additional activities: '+ str(percent_recovery[3])+ '%')
    st.sidebar.markdown('5 additional activities: '+ str(percent_recovery[4])+ '%')
