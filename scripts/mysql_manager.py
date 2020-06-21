import mysql.connector
from mysql.connector import errorcode
import configparser
import pandas as pd
import os

def create_database(cursor, DB_NMAE):
    try:
        cursor.execute(
            "CREATE DATABASE: {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Create database failed {}:".format(err))
        exit(1)


def locate_database(cursor, DB_NAME):
    """Change to the database indicated by DB_NAME"""
    try:
        cursor.execute("USE {}".format(DB_NAME))
        print("Data base {}".format(DB_NAME), " is active.")
    except mysql.connector.Error as err:
        print("Database {} does note exist.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            mysql_manager.create_database(cursor, DB_NMAE)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)


def create_table (cursor, table_name):
    """Iterate through the existing tables and check to see if the desired table already exists
    If not, it creates the database """
    table_description = table_name
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

# Import connection data from an external config.ini file (not in repository)
config = configparser.ConfigParser()
config.read('../../../api/config.ini')
DB_NAME = config.get('connections', 'DB_NAME')
USER_NAME = config.get('connections', 'DB_USER')
PWD = config.get('connections', 'DB_PWD')
HOST_NAME = config.get('connections','DB_HOST')
PORT = config.get('connections', 'DB_PORT')


# Establish Connection to Remote Database
cnx = mysql.connector.connect(user = USER_NAME,
    password = PWD, host = HOST_NAME, database = DB_NAME,
    port = PORT)
cursor = cnx.cursor(buffered = True)
locate_database(cursor, DB_NAME)


# Create Table for Leaderboard Top 500
csv = pd.read_csv('../../data/processed/dataforazeroth_complete_player_stats_500.csv')
fields = csv.columns
sizes = ['varchar(100)']*len(csv.columns)

sql = "CREATE TABLE leaderboards ("
i = 0
for field in fields:
    if i == 1:
        sql = sql + field + ' ' + sizes[i]
    elif i > 1 and i <= 16:
         sql = sql + ', ' + field + ' ' + sizes[i]
    elif i > 16:
        sql = sql + ', ' + 'a_' + field + ' ' + sizes[i]
    i = i + 1
sql = sql + ') engine=innodb default charset=utf8;'

print (len(csv.columns))

cursor.execute(sql)
cnx.commit()