import sqlite3

conn = sqlite3.connect("food_rescue.db")
cur = conn.cursor()

cur.execute("SELECT * FROM donations")

rows = cur.fetchall()

for row in rows:
    print(row)

conn.close()