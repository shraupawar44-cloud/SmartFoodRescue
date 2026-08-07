import sqlite3

conn = sqlite3.connect("food_rescue.db")
cur = conn.cursor()

cur.execute("""
UPDATE donations
SET created_at = datetime('now','localtime')
WHERE created_at IS NULL
""")

conn.commit()
conn.close()

print("Date and time updated")