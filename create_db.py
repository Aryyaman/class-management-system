import sqlite3

conn = sqlite3.connect('cms.db')

conn.execute('''
create table if not exists students(
id integer primary key autoincrement,
name text,
roll text,
dept text
)
''')

conn.commit()
conn.close()

print("Database created")