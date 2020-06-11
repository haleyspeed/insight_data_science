import pandas as pd
import numpy as np
import os
import requests
import configparser
import json

config = configparser.ConfigParser()
config.read('config.ini')
blizzard_key = config.get("KEYS", 'blizzard')
blizzard_secret = config.get("KEYS", 'blizzard_secret')


def get_access_token (blizzard_key, blizzard_secret):
    r = requests.post('https://us.battle.net/oauth/token', data={'grant_type': 'client_credentials'},
                  auth=(blizzard_key, blizzard_secret))
    unpacked = json.loads (r.text)
    access_token = unpacked['access_token']
    return access_token


def get_wow_mounts (player, realm, access_token):
    url = 'https://us.api.blizzard.com/profile/wow/character/' + realm + '/' + \
          player + '/collections/mounts?namespace=profile-us&locale=en_US&access_token=' + access_token
    r = requests.get(url)
    if r.status_code == 200:
        try:
            unpacked = json.loads(r.text)
            mounts = len(unpacked['mounts'])
            return mounts
        except:
            return np.nan
    else:
        return np.nan

def get_wow_pets (player, realm, access_token):
    url = 'https://us.api.blizzard.com/profile/wow/character/' + realm + '/' + player + \
          '/collections/pets?namespace=profile-us&locale=en_US&access_token=' + access_token
    r = requests.get(url)
    if r.status_code == 200:
        try:
            unpacked = json.loads(r.text)
            pets = len (unpacked['pets'])
            return pets
        except:
            return np.nan
    else:
        return np.nan


def get_wow_quests (player, realm, access_token):
    url = 'https://us.api.blizzard.com/profile/wow/character/' + realm + '/' + player \
            + '/titles?namespace=profile-us&locale=en_US&access_token=' + access_token
    r = requests.get(url)
    if r.status_code == 200:
        try:
            unpacked = json.loads(r.text)
            titles = len(unpacked['titles'])
            return titles
        except:
            return np.nan
    else:
        return np.nan


def get_wow_honor (player, realm, access_token):
    url = 'https://us.api.blizzard.com/profile/wow/character/' + realm + '/' + player + \
          '/pvp-summary?namespace=profile-us&locale=en_US&access_token=' + access_token
    r = requests.get(url)
    if r.status_code == 200:
        try:
            unpacked = json.loads(r.text)
            honor_level = unpacked['honor_level']
            return honor_level
        except:
            return np.nan
    else:
        return np.nan


f = '~/Docs/insight/api/wow_roster200.csv'
df = pd.read_csv(f)
df['mounts_collected'] = np.nan
df['pets_collected'] = np.nan
df['completed_quests'] = np.nan
df['honor_level'] = np.nan
access_token = get_access_token (blizzard_key, blizzard_secret)
i = 1
for m in df.itertuples():
    print(i)
    row = dict()
    row['mounts_collected'] = get_wow_mounts(m.player, m.realm, access_token)
    row['m.pets_collected = get_wow_pets(m.player, m.realm, access_token)
    m.completed_quests = get_wow_quests(m.player, m.realm, access_token)
    m.honor_level = get_wow_honor(m.player, m.realm, access_token)
    print(m)
    df.at[i, 'ifor'] = ifor_val
    i = i + 1



