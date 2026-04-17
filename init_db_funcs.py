import sqlite3

db_name = "data.db"

def init_db():
    conn = sqlite3.connect(db_name, check_same_thread=False)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room TEXT,
        nickname TEXT,
        message TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nickname TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()