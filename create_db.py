import sqlite3

dbname = 'music.db'
conn = sqlite3.connect(dbname)

tablename = 'musics'

cur = conn.cursor()

cur.execute(f'create table {tablename} (id integer primary key, date text, title text, artist text, url text)')

conn.close()