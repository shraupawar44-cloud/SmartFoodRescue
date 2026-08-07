import sqlite3

conn = sqlite3.connect("food_rescue.db")
cur = conn.cursor()

# Users Table
cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    password TEXT,
    role TEXT
)
""")

# Donations Table
cur.execute("""
CREATE TABLE IF NOT EXISTS donations(
id INTEGER PRIMARY KEY AUTOINCREMENT,
food_name TEXT,
quantity TEXT,
location TEXT,
donor TEXT,
date_time TEXT,
status TEXT
)
""")

conn.commit()
conn.close()

print("Database Ready")