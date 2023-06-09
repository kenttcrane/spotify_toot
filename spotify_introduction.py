import sys
import datetime
import sqlite3
import time
import os
from mastodon import Mastodon
from spotipy import *
from spotipy.oauth2 import SpotifyClientCredentials

from config import *
from util import *

LIST_SELF = 14413 # 自分のみを入れたリストのID
ROOT_ID = 110186940072440364 # スレッドの一番上となるトゥートのID

spotify_id = os.environ['SPOTIFY_CLIENT_ID']
spotify_secret = os.environ['SPOTIFY_CLIENT_SECRET']

mastodon_id = os.environ['MASTODON_CLIENT_ID']
mastodon_secret = os.environ['MASTODON_CLIENT_SECRET']
mastodon_access_token = os.environ['MASTODON_ACCESS_TOKEN']

api = Mastodon(
    api_base_url = 'https://mstdn.jp',
    client_id = mastodon_id,
    client_secret = mastodon_secret,
    access_token = mastodon_access_token
)

# search parent
parent = None
toots = api.timeline_list(LIST_SELF, limit=500) # 新しい順

for toot in toots:
    if toot['id'] == ROOT_ID:
        parent = toot
        break
    if not toot['card']:
        continue
    if 'spotify' not in toot['card']['url']:
        continue
    ancestor_ids = [ancestor['id'] for ancestor in api.status_context(toot['id'])['ancestors']]
    if ROOT_ID in ancestor_ids:
        parent = toot
        break

if parent == None:
    print('No parent.')
    sys.exit(1)

print('parent: ')
show_dict(parent)

# spotify setup
ccm = SpotifyClientCredentials(client_id=spotify_id, client_secret=spotify_secret)
spotify = Spotify(client_credentials_manager=ccm, language='ja')

# get track info
while True:
    url = input('spotify track url: ')
    try:
        info = spotify.track(url)
        break
    except:
        print('invalid input')
        print()
        pass

# check track information
while True:
    print(f"title: {info['name']}")
    title = input('If the title is correct, press enter. If not, type the correct title.')
    if title == '':
        title = info['name']

    print(f"artist: {', '.join([info['artists'][i]['name'] for i in range(len(info['artists']))])}")
    artist = input('If the artist is correct, press enter. If not, type the correct artist.')
    if artist == '':
        artist = ', '.join([info['artists'][i]['name'] for i in range(len(info['artists']))])

    dt = datetime.datetime.now()
    month = dt.month
    day = dt.day - (1 if dt.hour < 5 else 0)
    date_str = str(month) + '/' + str(day)
    
    multi_today = (input('multiple introduction today? (y/n): ') == 'y')
    if multi_today:
        num = input('input the toot number: ')
        date_str += ' (' + num + ')'

    # check toot text
    text = date_str + '\n' + title + ' - ' + artist + '\n' + url
    while True:
        print(f'text: "{text}"')
        ans = input('OK? (y/n)')
        if ans in ('y', 'n'):
            break
        else:
            print('invalid answer')
    if ans == 'y':
        break
    else:
        print('input the information again.')

#tweet
print('-'*30)
print(text)
print('-'*30)
api.status_post(text, in_reply_to_id=parent['id'])

time.sleep(1)

# insert to database
conn = sqlite3.connect(dbname)
cur = conn.cursor()

toot = api.timeline_list(LIST_SELF, limit=1)[0]
insert_music(cur, toot['id'], text)
conn.commit()
conn.close()