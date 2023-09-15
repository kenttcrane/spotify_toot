import sys
import datetime
import sqlite3
import time

from mastodon import Mastodon
from spotipy import Spotify
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials

from libs.util import show_dict, insert_music
from config.config import (
    SPOTIFY_ID,
    SPOTIFY_SECRET,
    MASTODON_ID,
    MASTODON_SECRET,
    MASTODON_ACCESS_TOKEN,
    LIST_SELF,
    DB_NAME
)

mstdn = Mastodon(
    api_base_url = 'https://mstdn.jp',
    client_id = MASTODON_ID,
    client_secret = MASTODON_SECRET,
    access_token = MASTODON_ACCESS_TOKEN
)

# choose table
conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

cur.execute('select * from playlist')
relationships = cur.fetchall()

for i, relationship in enumerate(relationships):
    print(f'{i + 1}: {relationship[0]}')
while True:
    playlist_num = int(input('type the number of playlist: '))
    playlist_num -= 1
    if playlist_num < len(relationships):
        break
    print('type valid number')
relationship = relationships[playlist_num]
root_toot_id = relationship[1]
tbl_name = relationship[2]
playlist_url = relationship[3]

# search parent
parent = None
toots = mstdn.timeline_list(LIST_SELF, limit=200) # 新しい順

for toot in toots:
    if toot['id'] == root_toot_id:
        parent = toot
        break
    if not toot['card']:
        continue
    if 'spotify' not in toot['card']['url']:
        continue
    ancestor_ids = [ancestor['id'] for ancestor in mstdn.status_context(toot['id'])['ancestors']]
    if root_toot_id in ancestor_ids:
        parent = toot
        break

if parent is None:
    print('No parent.')
    sys.exit(1)

print('parent: ')
show_dict(parent)

# spotify setup
ccm = SpotifyClientCredentials(client_id=SPOTIFY_ID, client_secret=SPOTIFY_SECRET)
spotify = Spotify(client_credentials_manager=ccm, language='ja')

# get track info
while True:
    url = input('spotify track url: ')
    url = url.split('?')[0]
    try:
        info = spotify.track(url)
        break
    except SpotifyException:
        print('invalid input')
        print()

# check track information
while True:
    print(f"title: {info['name']}")
    title = input('If the title is correct, press enter. If not, type the correct title.')
    if title == '':
        title = info['name']

    artists = [info['artists'][i]['name'] for i in range(len(info['artists']))]
    print(f"artist: {', '.join([info['artists'][i]['name'] for i in range(len(info['artists']))])}")
    artist = input('If the artist is correct, press enter. If not, type the correct artist.')
    if artist == '':
        artist = ', '.join(artists)

    dt = datetime.datetime.now()
    month = dt.month
    day = dt.day - (1 if dt.hour < 5 else 0)
    date_str = str(month) + '/' + str(day)

    multi_today = input('multiple introduction today? (y/n): ') == 'y'
    if multi_today:
        num = input('input the toot number: ')
        date_str += ' (' + num + ')'

    # check toot text
    text = ''
    if playlist_num == 0:
        text += date_str + '\n'
    text += title + ' - ' + artist + '\n' + url + '\n\n'\
           + 'プレイリストはこちら↓' + '\n' + playlist_url
    while True:
        print(f'text: "{text}"')
        ans = input('OK? (y/n)')
        if ans in ('y', 'n'):
            break
        print('invalid answer')
    if ans == 'y':
        break
    print('input the information again.')

#toot
print('-'*30)
print(text)
print('-'*30)
toot = mstdn.status_post(text, in_reply_to_id=parent['id'])

time.sleep(1)

# insert to database
music_data = {'date': date_str, 'title': title, 'artists': artists, 'url': url}

insert_music(cur, tbl_name, toot['id'], music_data)
conn.commit()
conn.close()
