import sqlite3, bcrypt

db_name = "data.db"

def register(username, password):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    # хеш пароля
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        cur.execute(
            "INSERT INTO users (nickname, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # юзер вже існує
        return False
    finally:
        conn.close()

def login(username, password):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.execute(
        "SELECT password_hash FROM users WHERE nickname = ?",
        (username,)
    )
    row = cur.fetchone()

    conn.close()

    if row is None:
        return False

    stored_hash = row[0]

    return bcrypt.checkpw(password.encode(), stored_hash)