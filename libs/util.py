import numpy as np
from sqlite3 import Cursor

root = {}

def root_tweet_id(t, tweet):
    id = tweet['id']
    if id in root:
        return root[id]

    ids = np.array([id])
    while tweet['in_reply_to_status_id'] is not None:
        parent_id = tweet['in_reply_to_status_id']
        print(parent_id)
        ids = np.append(ids, parent_id)
        tweet = t.statuses.show(_id=parent_id)

    root_id = tweet['id']
    for child_id in ids:
        root[child_id] = root_id

    return root_id

def show_dict(d: dict) -> None:
    for key in d:
        print(f'{key}: {d[key]}')

def insert_music(cur: Cursor, tbl_name: str, id: int, music_data: dict) -> None:
    date = music_data['date']
    title = music_data['title']
    artists = music_data['artists']
    url = music_data['url'].split('?')[0]

    # SQLに埋め込む際の文字列処理
    title = title.replace("'", "''")
    artists = (artist.replace("'", "''") for artist in artists)

    for artist in artists:
        try:
            cur.execute(f'''insert into {tbl_name} values ({id}, '{date}', '{title}', '{artist}', '{url}')''')
            print(f'{id}, {date}, {title}, {artist}, {url}')
        except Exception:
            print(date, title, 'でおかしい')
