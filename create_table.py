import sqlite3

f = open('settings.txt', 'r')
splitted = f.read().splitlines()
f.close()
path_sql = splitted[3].split('-')[1].replace(' ', '')

conn = sqlite3.connect(path_sql)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE monitoring(
        TS timestamp not null,
        URL string not null,
        LABEL string not null,
        RESPONSE_TIME float,
        STATUS_CODE integer default null,
        CONTENT_LENGTH integer default null
    );
    """)

conn.commit()
conn.close()
