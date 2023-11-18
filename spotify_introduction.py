import sys
import datetime
import sqlite3
import time

from mastodon import Mastodon
from spotipy import Spotify
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials
import firebase_admin
from firebase_admin import firestore

from libs.util import show_dict, insert_music
from libs.music_info import MusicInfo
from config.config import (
    SPOTIFY_ID,
    SPOTIFY_SECRET,
    MASTODON_ID,
    MASTODON_SECRET,
    MASTODON_ACCESS_TOKEN
)

mstdn = Mastodon(
    api_base_url = 'https://mstdn.jp',
    client_id = MASTODON_ID,
    client_secret = MASTODON_SECRET,
    access_token = MASTODON_ACCESS_TOKEN
)

# choose table
# 環境変数'GOOGLE_APPLICATION_CREDENTIALS'にFirebaseで取得したservice account（jsonファイル）のパスを入れる
firebase_admin.initialize_app()
db = firestore.client()

doc_ref = db.collection('playlist')
relationships = list(doc_ref.stream())

for i, relationship in enumerate(relationships):
    print(f'''{i + 1}: {relationship.get('id')}''')
while True:
    playlist_num = int(input('type the number of playlist: '))
    playlist_num -= 1
    if playlist_num < len(relationships):
        break
    print('type valid number')
relationship = relationships[playlist_num]

relationship_id_str = relationship.get('id')
root_toot_id = int(relationship.get('root_toot_id'))
playlist_url = relationship.get('spotify_url')

# get mastodon user id
mastodon_user_id = mstdn.me()["id"]

# search parent
parent = None
toots = mstdn.account_statuses(mastodon_user_id, limit=200)  # 新しい順

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

    multi_num = ''
    multi_today = input('multiple introduction today? (y/n): ') == 'y'
    if multi_today:
        num = input('input the toot number: ')
        multi_num = ' (' + num + ')'

    music_info = MusicInfo(
        {
            'date': date_str,
            'multi_num': multi_num,
            'title': title,
            'artists': artists,
            'music_url': url,
            'playlist_url': playlist_url
        }
    )

    # check toot text
    text = music_info.generate_message(f'data/template_{relationship_id_str}.txt')
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
tbl_name = f'musics_{relationship_id_str}'
insert_music(db, tbl_name, str(toot['id']), music_info.data)
