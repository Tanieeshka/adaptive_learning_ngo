import sqlite3

# Create connection (this creates data.db automatically)
conn = sqlite3.connect("data.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        name TEXT PRIMARY KEY,
        role TEXT,
        grade TEXT,
        class INTEGER,
        time_slot TEXT,
        strong_subjects TEXT,
        weak_subjects TEXT,
        teaches TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ratings (
        mentor TEXT,
        rating INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
