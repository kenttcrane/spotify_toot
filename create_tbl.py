import sqlite3
from config.config import DB_NAME

print(f'open {DB_NAME}')
print()

tbls = {
    'musics_xxx': 'id integer, date text, title text, artist text, url text, primary key (id, artist)',
    'playlist': 'id text primary key, title text, root_toot_id integer, spotify_url text'
}

conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

for tbl_name, columns in tbls.items():
    query = f'create table if not exists {tbl_name} ({columns})'
    print(query)
    cur.execute(query)

conn.close()
