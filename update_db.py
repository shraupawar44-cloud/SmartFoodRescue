import sqlite3

conn = sqlite3.connect("food_rescue.db")
cur = conn.cursor()

# Check if created_at column exists
cur.execute("PRAGMA table_info(donations)")
columns = [column[1] for column in cur.fetchall()]

if "created_at" not in columns:
    cur.execute("ALTER TABLE donations ADD COLUMN created_at TEXT")
    print("created_at column added.")
else:
    print("created_at column already exists.")

cur.execute("""
UPDATE donations
SET created_at = datetime('now')
WHERE created_at IS NULL
""")

conn.commit()
conn.close()

print("Database Updated Successfully")