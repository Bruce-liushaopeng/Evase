import sqlite3

conn = sqlite3.connect('sample.db')
print("Open db succesfullly")

conn.execute("""
    CREATE TABLE USER
         (FirstName           TEXT    PRIMARY KEY,
         LastName             TEXT    NOT NULL);
""")

print("db create success")

conn.close()