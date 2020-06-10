import requests
import json
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
import httplib2
import numpy as np
import os
import wget
import glob
import csv
import config
import configparser
import gzip
import xlrd
import datetime


def unpack_json(txt):
    """Function to format a json page for parsing"""
    unpacked = json.loads(txt)
    return unpacked


def get_access_token (blizzard_key, blizzard_secret):
    """Get access token to access the blizzard API"""
    r = requests.post('https://us.battle.net/oauth/token', data={'grant_type': 'client_credentials'},
                  auth=(blizzard_key, blizzard_secret))
    unpacked = unpack_json(r.text)
    access_token = unpacked['access_token']
    return access_token


def dataforazeroth (dir_dataset):
    date_cols = []
    os.chdir(dir_dataset)
    files = os.listdir()
    csv_files = glob.glob('*.{}'.format('csv'))
    df = pd.DataFrame()
    for f in csv_files:
        temp = pd.read_csv(f)
        temp.columns = ['ranking','leaderboard','player','guild','realm','score']
        temp.leaderboard = f.split('wow_')[1].split('.csv')[0]
        df = df.append(temp[['ranking','leaderboard','player','guild','realm']], ignore_index=True)
    df.to_csv('../dataforazeroth_complete_dataset.csv')
    return df


def xlsx_to_csv (dir_xlsx):
    os.chdir(dir_xlsx)
    files = os.listdir()
    xlsx_files = glob.glob('*.{}'.format('xlsx'))
    for f in xlsx_files:
        wb = xlrd.open_workbook(f)
        sh = wb.sheet_by_name('Sheet1')
        csv_name = f.replace('xlsx','csv')
        f_csv = open(csv_name, 'w', encoding='utf8')
        wr = csv.writer(f_csv, quoting=csv.QUOTE_ALL)
        for rownum in range(sh.nrows):
            wr.writerow(sh.row_values(rownum))
        f_csv.close()


def get_wowprogress_rank_list(rank_list_name, locale, base_url,df):
    """Downloads guild rankings for each realm provided"""
    url = base_url + rank_list_name
    tar_file = wget.download(url)


def unpack_wowprogress_guild_ranks(locale):
    """Reads all the .gz files in the current working directory and extracts the
    data as JSON. Data is parsed and collated into a single dataframe."""
    files = os.listdir()
    df = pd.DataFrame()
    for tarfile in files:
        print("reading: " + tarfile)
        try:
            splits = tarfile.split('_tier')
            realm = splits[0]
            tier = splits[1].split('.json')[0]
            tmp = pd.DataFrame()
            with gzip.open(tarfile, 'rb') as f:
                json_text = f.read()
            unpacked = unpack_json(json_text)
            for guild in unpacked:
                tmp = tmp.append(guild, ignore_index=True)
                tmp['tier'] = tier
                tmp['region'] = locale
                tmp['realm'] = realm
                df = df.append(tmp, ignore_index=True)
        except:
            print('Could not read: ' + tarfile + '. Moving on...')
            continue
    df.to_csv('wow_guild_rankings.csv')
    #os.remove(tarfile)
    return df


def get_wowprogress_by_realm (locale, namespace,base_url):
    """Gets the realm list from the Blizzard API then scrapes the wowprogress.com website
    for guild rankings"""
    namespace = 'dynamic-us'
    realm_names, realm_ids, realm_slugs = bapi.get_wow_realms_list(namespace, locale)
    http = httplib2.Http()
    status, response = http.request(base_url)
    df = pd.DataFrame()
    for link in BeautifulSoup(response, parse_only=SoupStrainer('a'), features="lxml"):
        if link.has_attr('href'):
            link = str(link).split('="')[1].split('">')[0]
            for realm in realm_slugs:
                if realm in link and 'us_' in link[:3]:
                    print('Downloading: ' + link)
                    get_wowprogress_rank_list(link, locale, base_url,df)


def get_wow_achievements_category(namespace, locale):
    directory = 'data/wow/achievement-category/index'
    url = 'https://us.api.blizzard.com/'+ directory +'?namespace='+ namespace + \
      '&locale=' + locale + '&access_token='+ access_token
    r = requests.get (url)
    unpacked = unpack_json (r.text)
    df = pd.DataFrame()
    for keys, values in unpacked.items():
        tmp = pd.DataFrame()
        for category in values:
            if isinstance(category, dict):
                for keys, values in category.items():
                    tmp[keys] = values
                df = df.append(tmp)
    return df


def get_wow_achievement_category(cat_id):
    """Retrieves achievement catefory from the Blizzard API"""
    f_config = '/Users/haleyspeed/Docs/insight/api/config.ini'
    config = configparser.ConfigParser()
    config.read(f_config)
    blizzard_key = config.get('KEYS', 'blizzard')
    blizzard_secret = config.get('KEYS', 'blizzard_secret')
    access_token = get_access_token(blizzard_key, blizzard_secret)
    url = 'https://us.api.blizzard.com/data/wow/achievement-category/' + \
          str(cat_id)+'?namespace=static-us&locale=en_US&access_token=' + access_token
    try:
        r = requests.get(url)
        if r.status_code == 200:
            unpacked = unpack_json(r.text)
            achievement_category = unpacked['category']
            return achievement_category['name'], unpacked['points']
    except:
        return 'error'


def get_wow_achievement(achievement_id):
    f_config = '/Users/haleyspeed/Docs/insight/api/config.ini'
    config = configparser.ConfigParser()
    config.read(f_config)
    blizzard_key = config.get('KEYS', 'blizzard')
    blizzard_secret = config.get('KEYS', 'blizzard_secret')
    access_token = get_access_token(blizzard_key, blizzard_secret)
    """Retrieves achievement category from the Blizzard API"""
    url = 'https://us.api.blizzard.com/data/wow/achievement/' + \
          str(achievement_id)+'?namespace=static-us&locale=en_US&access_token=' + access_token
    try:
        r = requests.get(url)
    except:
        pass
    if r.status_code == 200:
        unpacked = unpack_json(r.text)
        results = {'achievement_name' : unpacked['name'],
                    'achievement_id': unpacked['id'],
                    'category_name': unpacked['category']['name'],
                    'category_id': unpacked['category']['id'],
                    'criteria_id': '',
                    'criteria_name': '',
                    'next_name': '',
                    'next_id': ''}
        try:
            results['criteria_id'] = unpacked['criteria']['id']
        except:
            print("unpacked['criteria']['id'] does not exist")
        try:
            results['criteria_name'] = unpacked['criteria']['name']
        except:
            print("unpacked['criteria']['name'] does not exist")
        try:
            results['next_id'] = unpacked['next_achievement']['id']
        except:
            print("unpacked['next_achievement']['id'] does not exist")
        try:
            results['next_name'] = unpacked['next_achievement']['name']
        except:
            print("unpacked['next_achievement']['name'] does not exist")
        return results



def get_wow_achievement_list (namespace, locale):
    """Retrieves the total achievement list from the Blizard API"""
    directory = 'data/wow/achievement/index'
    url = 'https://us.api.blizzard.com/'+ directory +'?namespace='+ namespace + \
      '&locale=' + locale + '&access_token='+ access_token
    try:
        r = requests.get(url)
    except:
        pass
    unpacked = unpack_json (r.text)
    df = pd.DataFrame()
    for i, achievement in enumerate(unpacked['achievements']):
        category, points = get_wow_achievement_category(achievement['id'], namespace, locale)
        row = dict(name = achievement['name'], id = achievement['id'], category = category, points = points)
        df = df.append(row, ignore_index = True)
        print(df.loc[i])
    return df


def get_wow_realms_list (namespace, locale):
    """Retrieves a list of reams and their ids using the Blizzard API"""
    directory = 'data/wow/realm/index'
    url = 'https://us.api.blizzard.com/' + directory + '?namespace=' + namespace + \
          '&locale=' + locale + '&access_token=' + access_token
    try:
        r = requests.get(url)
    except:
        pass
    unpacked = unpack_json(r.text)
    realm_names = []
    realm_ids = []
    realm_slugs = []
    for realm in unpacked ['realms']:
        realm_names.append(realm['name'])
        realm_ids.append(realm['id'])
        realm_slugs.append(realm['slug'])
    return realm_names, realm_ids, realm_slugs


def get_mythic_dungeon_leaderboard_instances (realm_id, namespace, locale, access_token):
    """Returns an index of Mythic Keystone Leaderboard dungeon instances for a connected realm"""
    directory = 'data/wow/connected-realm/' + str(realm_id) + '/mythic-leaderboard/index'
    url = 'https://us.api.blizzard.com/' + directory + '?namespace=' + namespace + \
          '&locale=' + locale + '&access_token=' + access_token
    try:
        r = requests.get(url)
    except:
        pass
    unpacked = unpack_json(r.text)
    current_leaderboards = unpacked['current_leaderboards']
    df = pd.DataFrame()
    for leaderboard in current_leaderboards:
        df = df.append(leaderboard, ignore_index=True)
    return df


def get_mythic_keystone_dungeon_leaderboard(realm_id,namespace,locale, instance, period):
    """Retrieves the leaderboard information for a mythic using the Blizzard API.
    Player information not included in recent data. Leads to an error."""
    directory = 'data/wow/connected-realm/'
    url = 'https://us.api.blizzard.com/' + directory + str(realm_id) + '/mythic-leaderboard/' + str(instance) + \
          '/period/' + str(period) + '?namespace=' + namespace + \
          '&locale=' + locale + '&access_token=' + access_token
    try:
        r = requests.get(url)
    except:
        pass
    unpacked = unpack_json(r.text)
    features = ['period', 'period_start_timestamp', 'period_end_timestamp', 'map_challenge_mode_id',
               'map_challenge_mode_name', 'map_name', 'map_id', 'connected_realm', 'keystone_affix_names',
               'keystone_affix_ids', 'keystone_affix_starting_level', 'leading_groups_ranking',
               'leading_groups_duration', 'leading_groups_completed_timestamp', 'leading_groups_keystone_level',
               'member_name, member_id', 'member_realm_id', 'member_realm_slug', 'member_faction',
               'member_specialization']
    df = pd.DataFrame()
    values = list(unpacked.values())
    map = values[1]
    period = values[2]
    period_start_timestamp  = values[3]
    period_end_timestamp  = values[4]
    map_challenge_mode_id  = values[8]
    map_challenge_mode_name = values[9]
    map_name = map['name']
    map_id = map['id']

    connected_realm = values[5]
    connected_realm = connected_realm['href']

    keystone_affixes = values[7]
    keystone_affix_names = []
    keystone_affix_ids = []
    keystone_affix_starting_level = []
    for affix in keystone_affixes:
        keystone_affix_names.append(affix['keystone_affix']['name'])
        keystone_affix_ids.append(affix['keystone_affix']['id'])
        keystone_affix_starting_level.append(affix['starting_level'])

    leading_groups = values[6]
    for leading_group in leading_groups:
        leading_groups_ranking = leading_group['ranking']
        leading_groups_duration = leading_group['duration']
        leading_groups_completed_timestamp = leading_group['completed_timestamp']
        leading_groups_keystone_level = leading_group['keystone_level']
        members = leading_group['members']
        for member in members:
            member_name = member['profile']['name']
            member_id = member['profile']['id']
            member_realm_id = member['profile']['realm']['id']
            member_realm_slug =  member['profile']['realm']['slug']
            member_faction = member['faction']['type']
            member_specialization = member['specialization']['id']
            tmp = {'period':period,
                    'period_start_timestamp':period_start_timestamp,
                   'period_end_timestamp':period_end_timestamp,
                   'map_challenge_mode_id':map_challenge_mode_id,
                   'map_challenge_mode_name':map_challenge_mode_name,
                   'map_name':map_name,
                   'map_id':map_id,
                   'connected_realm':connected_realm,
                   'keystone_affix_names':keystone_affix_names,
                   'keystone_affix_ids':keystone_affix_ids,
                   'keystone_affix_starting_level':keystone_affix_starting_level,
                   'leading_groups_ranking':leading_groups_ranking,
                   'leading_groups_duration':leading_groups_duration,
                   'leading_groups_completed_timestamp':leading_groups_completed_timestamp,
                   'leading_groups_keystone_level':leading_groups_keystone_level,
                   'member_name':member_name,
                   'member_id':member_id,
                   'member_realm_id':member_realm_id,
                   'member_realm_slug':member_realm_slug,
                   'member_faction':member_faction,
                   'member_specialization':member_specialization}
        df = df.append(tmp, ignore_index=True)
    return (df)


def get_wow_profile (realm, player, token):
    """Retrievesthe public profile for a player using the Blizzard API"""
    url = 'https://us.api.blizzard.com/profile/wow/character/' + realm \
          + '/' + player + '?namespace=profile-us&locale=en_US&access_token=' + access_token
    try:
        r = requests.get(url)
    except:
        pass
    unpacked = unpack_json(r.text)
    row = dict(id = unpacked['id'], name = unpacked['name'], gender = unpacked['gender']['name'],
          faction = unpacked['faction']['name'], race = unpacked['race']['name'],
          character_class = unpacked['character_class']['name'],
          active_spec = unpacked['active_spec']['name'], realm = unpacked['realm']['slug'],
          guild = unpacked['guild']['name'], level = unpacked['level'],
          achievement_points = unpacked['achievement_points'],
          last_login = unpacked['last_login_timestamp'],
          average_item_level = unpacked['average_item_level'],
          equipped_item_level = unpacked['equipped_item_level'])
    return row

def get_guild_roster (realm, guild, access_token):
    "Retrieves the list of players in a guild using the Blizzard API"
    url = 'https://us.api.blizzard.com/data/wow/guild/'+ realm \
          + '/' + guild + '/roster?namespace=profile-us&locale=en_US&access_token=' + access_token
    r = requests.get(url)
    unpacked = unpack_json(r.text)
    guild_faction = unpacked['guild']['faction']['name']
    for member in unpacked['members']:
        row = dict(player = member['character']['name'], id = member['character']['id'],
              realm = member['character']['realm']['slug'], realm_id = member['character']['realm']['id'],
              level = member['character']['level'], playable_class = member['character']['playable_class']['id'],
              playable_race = member['character']['playable_race']['id'], guild_rank = member['rank'],
              guild_name = guild, faction = guild_faction)
    return row

def get_player_achievements(player,realm, row, access_token):
    "Retrieves achievements for a player using the Blizzard API"
    url = 'https://us.api.blizzard.com/profile/wow/character/' + realm \
          + '/' + player + '/achievements?namespace=profile-us&locale=en_US&access_token=' + access_token
    try:
        r = requests.get(url)
    except:
        return 'error'
    if r.status_code == 200:
        try:
            unpacked = unpack_json(r.text)
            row['total_achievements'] = unpacked['total_quantity']
            row['total_achievement_points'] = unpacked['total_points']
            for achievement in unpacked['achievements']:
                try:
                    if achievement['criteria']['is_completed'] == True:
                        row[str(achievement['id'])] = datetime.datetime.utcfromtimestamp((int(achievement['completed_timestamp'])/1000)).strftime('%Y-%m-%d')
                    else:
                        row[str(achievement['id'])] = 'none'
                except:
                    row[str(achievement['id'])] = 'none'
            return row
        except:
            return 'error'
    else:
        return 'error'


def get_wow_mounts (player, realm, access_token):
    "Retrieves number of mounts collected for a player using the Blizzard API"
    url = 'https://us.api.blizzard.com/profile/wow/character/' + realm + '/' + \
          player + '/collections/mounts?namespace=profile-us&locale=en_US&access_token=' + access_token
    try:
        r = requests.get(url)
    except:
        return np.nan
    if r.status_code == 200:
        try:
            unpacked = json.loads(r.text)
            return len(unpacked['mounts'])
        except:
            return np.nan
    else:
        return np.nan

def get_wow_pets (player, realm, access_token):
    "Retrieves number of pets collected for a player using the Blizzard API"
    url = 'https://us.api.blizzard.com/profile/wow/character/' + realm + '/' + player + \
          '/collections/pets?namespace=profile-us&locale=en_US&access_token=' + access_token
    try:
        r = requests.get(url)
    except:
        return np.nan
    if r.status_code == 200:
        try:
            unpacked = json.loads(r.text)
            return len (unpacked['pets'])
        except:
            return np.nan
    else:
        return np.nan


def get_wow_quests (player, realm, access_token):
    "Retrieves quest completion for a player using the Blizzard API"
    url = 'https://us.api.blizzard.com/profile/wow/character/' + realm + '/' + player \
            + '/quests/completed?namespace=profile-us&locale=en_US&access_token=' + access_token
    try:
        r = requests.get(url)
    except:
        return np.nan
    if r.status_code == 200:
        try:
            unpacked = json.loads(r.text)
            return len(unpacked['quests'])
        except:
            return np.nan
    else:
        return np.nan


def get_wow_honor (player, realm, access_token):
    "Retrieves honor level for a player using the Blizzard API"
    url = 'https://us.api.blizzard.com/profile/wow/character/' + realm + '/' + player + \
          '/pvp-summary?namespace=profile-us&locale=en_US&access_token=' + access_token
    try:
        r = requests.get(url)
    except:
        return np.nan

    if r.status_code == 200:
        try:
            unpacked = json.loads(r.text)
            return unpacked['honor_level']
        except:
            return np.nan
    else:
        return np.nan


def csv_concatenator (folder):
    """Reads in a directory then sequentially adds the concatenates the
    csv files in that directory"""
    df = pd.DataFrame()
    os.chdir (folder)
    for f in glob.glob('*{}'.format('csv')):
        print(f)
        df = df.append(pd.read_csv(f))
    return df, f

def super_big_csv_concatenator (file_in, file_out):
    """Reads in a directory then sequentially adds the concatenates the
    csv files in that directory"""
    f_out = open(file_out, "w")
    writer = csv.writer(f_out)
    i = 0
    for f in glob.glob(file_in.format('csv')):
        df = pd.read_csv(f)
        if i == 0:
            writer.writerow(df.columns)
        print(f)
        for row in df.itertuples():
            writer.writerow(row)
        i = i + 1
    f_out.close()


def dataset_cleaner (f):
    """Removes empty rows and duplicate rows from a csv file"""
    df = pd.read_csv(f)
    df = df.drop_duplicates()
    return df


def achievement_patch_scraper (achievement_id):
    url = 'https://www.wowhead.com/achievement=' + str(achievement_id)
    http = httplib2.Http()
    patch = ''
    attained_by = ''
    status, response = http.request(url)
    for scripts in BeautifulSoup(response, parse_only=SoupStrainer('script'), features="lxml"):
        if '[li]Added in patch' in str(scripts):
            patch = str(scripts).split("patch ")[1].split("[\\")[0]
            try:
                attained_by = str(scripts).split("Attained by ")[1].split("%")[0]
            except:
                continue
    return patch, attained_by


def patch_date_scraper (patch_id):
    patch = 'Patch_'+ patch_id[:5]
    release_date = ''
    url = 'https://wow.gamepedia.com/' + patch
    http = httplib2.Http()
    status, response = http.request(url)
    for scripts in BeautifulSoup(response, parse_only=SoupStrainer('td'), features="lxml"):
        if 'Release date' in str(scripts):
            release_date = str(scripts.next_sibling).split("<p>")[1].split("\n")[0]
    return release_date

def get_validation(player, realm, access_token):
    "Retrieves quest completion for a player using the Blizzard API"
    url = 'https://us.api.blizzard.com/profile/wow/character/' + realm + '/' + player \
          + '?namespace=profile-us&locale=en_US&access_token=' + access_token
    r = requests.get(url)
    if r.status_code == 200:
        try:
            unpacked = json.loads(r.text)
            last_login = datetime.datetime.utcfromtimestamp((int(unpacked['last_login_timestamp'])/1000)).strftime('%Y-%m-%d')
            gear_score = unpacked['equipped_item_level']
            return last_login, gear_score
        except:
            return ['','']
    else:
        return ['','']

def get_account_wide_achievement(achievement_id, access_token):
    f_config = '/Users/haleyspeed/Docs/insight/api/config.ini'
    config = configparser.ConfigParser()
    config.read(f_config)
    blizzard_key = config.get('KEYS', 'blizzard')
    blizzard_secret = config.get('KEYS', 'blizzard_secret')
    access_token = get_access_token(blizzard_key, blizzard_secret)
    """Retrieves achievement category from the Blizzard API"""
    url = 'https://us.api.blizzard.com/data/wow/achievement/' + \
          str(achievement_id)+'?namespace=static-us&locale=en_US&access_token=' + access_token
    try:
        r = requests.get(url)
    except:
        pass
    if r.status_code == 200:
        unpacked = unpack_json(r.text)
        results = {'achievement_name' : unpacked['name'],
                    'achievement_id': unpacked['id'],
                    'category_name': unpacked['category']['name'],
                    'category_id': unpacked['category']['id'],
                    'account_wide': unpacked['is_account_wide'],
                    'criteria_id': '',
                    'criteria_name': '',
                    'next_name': '',
                    'next_id': ''}
        try:
            results['criteria_id'] = unpacked['criteria']['id']
        except:
            print("unpacked['criteria']['id'] does not exist")
        try:
            results['criteria_name'] = unpacked['criteria']['name']
        except:
            print("unpacked['criteria']['name'] does not exist")
        try:
            results['next_id'] = unpacked['next_achievement']['id']
        except:
            print("unpacked['next_achievement']['id'] does not exist")
        try:
            results['next_name'] = unpacked['next_achievement']['name']
        except:
            print("unpacked['next_achievement']['name'] does not exist")
        return results
