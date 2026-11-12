import sqlite3

conn = sqlite3.connect("schedule.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time TEXT NOT NULL, 
    activity TEXT
)
""")
conn.commit()