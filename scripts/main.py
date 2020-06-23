import sys
import streamlit as st
import pandas as pd
import config as cn
import os.path
import numpy as np
import matplotlib.pyplot as plt
import random as rn
import time
import configparser
import mysql.connector
from mysql.connector import errorcode
from custom_funcs import create_database, create_table, locate_database


# Connection details for the SQL database
config = configparser.ConfigParser()
config.read('../config.ini')
DB_NAME = config.get('connections', 'db_name')
USER_NAME = config.get('connections', 'db_user')
PWD = config.get('connections', 'db_pwd')
HOST_NAME = config.get('connections','db_host')
PORT = config.get('connections', 'db_port')


def connect():
    """ Establishes connection to the mySQL database """
    cnx = mysql.connector.connect(user = USER_NAME,
    password = PWD, host = HOST_NAME, database = DB_NAME,
    port = PORT)
    cursor = cnx.cursor(buffered = True)
    locate_database(cursor, DB_NAME)
    return cnx, cursor


def get_realm_sql(realm, fields):
    """ Filters at-risk players by realm"""
    cnx, cursor = connect()
    sql = "SELECT * FROM final_time_stats WHERE realm = realm AND status = 'risk'"
    cursor.execute(sql)
    search = cursor.fetchall()
    df_search = pd.DataFrame(columns = fields)
    for item in search:
        tmp = pd.DataFrame(item)
        tmp = tmp.T
        tmp.columns = fields
        tmp.time_since_login = tmp.time_since_login.str.split('days')[0][0]
        df_search = df_search.append(tmp, ignore_index = True)
    return df_search


def get_data_sql(fields):
    """ Gets all at-risk players in the entire database"""
    cnx, cursor = connect()
    sql = "SELECT * FROM final_time_stats WHERE status = 'risk'"
    cursor.execute(sql)
    search = cursor.fetchall()
    df_search = pd.DataFrame(columns = fields)
    for item in search:
        tmp = pd.DataFrame(item)
        tmp = tmp.T
        tmp.columns = fields
        tmp.time_since_login = tmp.time_since_login.str.split('days')[0][0]
        df_search = df_search.append(tmp, ignore_index = True)
    return df_search


def get_data_csv():
    """ Loads in pre-processed data for fast loading """
    df = pd.read_csv(os.path.join(cn.clean_dir, 'random_forest_time',
            'test_predictions.csv'), dtype = 'unicode')
    df['id'] = df.player + '_' + df.realm
    df = df.set_index('id')
    df = df[df.status == 'risk']
    return df


def get_recommendations_sql ():
    cnx, cursor = connect()
    sql = "SELECT name, category FROM features " + \
            "LIMIT " + str(np.random.randint(0,498)) + ',1'
    cursor.execute(sql)
    search = cursor.fetchall()
    df_search = pd.DataFrame(columns = ['name', 'category'])
    for item in search:
        tmp = pd.DataFrame(item)
        tmp = tmp.T
        tmp.columns = ['name', 'category']
        df_search = df_search.append(tmp, ignore_index = True)
    return df_search


def update_plot(fig, ax, df_results):
    """ Plots the Maximum Estimated ROI"""
    retained = list()
    for i in np.arange(1,6):
        hyp = df_results[df_results['pred' + str(i)] == '0.0'].player.values
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



# Set default variables
fields = ['time_since_login', 'status', 'realm', 'player',
        'last_login', 'id', 'gear_score', 'engagement', '2020-12',
        '2020-11', '2020-10', '2020-09', '2020-08', '2020-06',
        '2020-05', '2020-04', '2020-03', '2020-02', '2020-01',
        '2019-12', '2019-11', '2019-10', '2019-09', '2019-08',
        '2019-07', '2019-06', '2019-05', '2019-04', '2019-03',
        '2019-02', '2019-01', '2018-12', '2018-11', '2018-10',
        '2018-09', '2018-08', '2018-07', '2018-06', '2018-05',
        '2018-04', '2018-03', '2018-02', '2018-01', '2017-12',
        '2017-11', '2017-10', '2017-09', '2017-08', '2017-07',
        '2017-06', '2017-05', '2017-04', '2017-03', '2017-02',
        '2017-01', '2016-12', '2016-11', '2016-10', '2016-09',
        '2016-08', '2016-07', '2016-06', '2016-05', '2016-04',
        '2016-03', '2016-02', '2016-01', '2015-12', '2015-11',
        '2015-10', '2015-09', '2015-08', '2015-07', '2015-06',
        '2015-05', '2015-04', '2015-03', '2015-02', '2015-01',
        '2014-12', '2014-11', '2014-10', '2014-09', '2014-08',
        '2014-07', '2014-06', '2014-05', '2014-04', '2014-03',
        '2014-02', '2014-01']

#df_results = get_data_sql(fields) #For full dataset loads slow
df_results = get_data_csv()


sub_cost = 15
x = 0
features = ['player', 'realm','gear_score','last_login','status']

# Setup main window at start
df_results = df_results.drop_duplicates()
main_top = st.image('logo_full.jpg')


#st.title('SubScript')
st.subheader('Boosting subscription volume with targeted content')
st.markdown('\n')
fig, ax = plt.subplots()
main_bottom = st.empty()


# Setup sidebar at start
side1 = st.sidebar.empty()
side2 = st.sidebar.empty()
side3 = st.sidebar.empty()
side4 = st.sidebar.empty()
side5 = st.sidebar.empty()
side6 = st.sidebar.empty()
side7 = st.sidebar.empty()
side8 = st.sidebar.empty()

# Action to get At-Risk Players
st.sidebar.markdown(' ')
side1.subheader('Subscript Analysis Menu \n')
start = side2.button('Get  At-Risk  Players')
if start:
    main_top.image('logo.jpg')
    main_bottom.table(df_results[features])


# Action for Get Recommendations button

#side4.subheader('Curated Content Recommendations')
recs = side3.button('Get Recommendations')
if recs:
    main_top.empty()
    main_top.image('logo.jpg')
    main_bottom.empty()
    for i in np.arange(0,5):
        dfs = get_recommendations_sql()
        st.subheader(dfs.category.to_string(index = False))
        st.write(dfs.name.to_string(index = False))


# Action for "Calculate ROI"


#side6.subheader('Estimated Return on Investment')
calc = side4.button('Calculate ROI')
if calc:
    main_top.empty()
    main_bottom.empty()
    main_top.image('logo.jpg')

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
