import sqlite3
from config.config import DB_NAME

conn = sqlite3.connect(DB_NAME)

while True:
    tbl_name = input('name of table to create: ')
    ans = input(f'OK? (y/n)')
    if ans == 'y':
        break

while True:
    columns = input('columns (ex. "id integer primary key, name text"): ')
    ans = input(f'OK? (y/n)')
    if ans == 'y':
        break

cur = conn.cursor()
cur.execute(f'create table {tbl_name} ({columns})')
conn.close()
