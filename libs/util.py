import numpy as np
from google.cloud.firestore_v1.client import Client

root = {}

def show_dict(d: dict) -> None:
    for key in d:
        print(f'{key}: {d[key]}')

def insert_music(db: Client, tbl_name: str|list, id: int, music_data: dict) -> None:
    date = music_data['date']
    title = music_data['title']
    artists = music_data['artists']
    url = music_data['music_url'].split('?')[0]

    try:
        doc_ref = db.collection(tbl_name).document(id)
        doc_ref.set({
            'id': id,
            'date': date,
            'title': title,
            'artist': artists,
            'url': url
        })
    except Exception:
        print(date, title, 'でおかしい')
