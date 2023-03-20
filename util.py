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

def is_node(t, tweet):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    tweets = []

    while True:
        cur.execute(f'''select * from musics where id = {tweet['id']}''')
        result = cur.fetchone()
        if result:
            for tweet in tweets:
                insert_music_tweet(cur, tweet)
            conn.commit()
            conn.close()
            return True
        else:
            tweets.insert(0, tweet)
            if tweet['in_reply_to_status_id']:
                parent_id = tweet['in_reply_to_status_id']
                tweet = t.statuses.show(_id=parent_id)
            else:
                conn.close()
                return False

def show_dict(d):
    for key in d:
        print(f'{key}: {d[key]}')

def insert_music_tweet(cur, tweet):
    id = tweet['id']

    text = tweet['text']
    date, info, _ = text.splitlines()
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
    artists = (artist.replace("'", "''") for artist in artists )

    url = tweet['entities']['urls'][0]['expanded_url']

    for artist in artists:
        try:
            cur.execute(f'''insert into musics values ({id}, '{date}', '{title}', '{artist}', '{url}')''')
            print(f'{id}, {date}, {title}, {artist}, {url}')
        except:
            print(date, title, 'でおかしい')