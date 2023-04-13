import numpy as np
import twitter
import sqlite3

dbname = 'music.db'
root = {}

def root_tweet_id(t, tweet):
    id = tweet['id']
    if id in root:
        return root[id]

    ids = np.array([id])
    while tweet['in_reply_to_status_id'] != None:
        parent_id = tweet['in_reply_to_status_id']
        print(parent_id)
        ids = np.append(ids, parent_id)
        tweet = t.statuses.show(_id=parent_id)
    
    root_id = tweet['id']
    for child_id in ids:
        root[child_id] = root_id

    return root_id

def show_dict(d):
    for key in d:
        print(f'{key}: {d[key]}')

def insert_music(cur, id, text):
    date, info, url = text.splitlines()
    date = date.split()[0]
    info = info.split(' - ')
    if len(info) == 2:
        title = info[0]
        artists = info[1]
    else:
        print('split error:', info)
        title = input('title: ')
        artists = input('artist(s): ')
    
    artists = artists.split(', ')

    title = title.replace("'", "''")
    artists = (artist.replace("'", "''") for artist in artists)

    for artist in artists:
        try:
            cur.execute(f'''insert into musics values ({id}, '{date}', '{title}', '{artist}', '{url}')''')
            print(f'{id}, {date}, {title}, {artist}, {url}')
        except:
            print(date, title, 'でおかしい')