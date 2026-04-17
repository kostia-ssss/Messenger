# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from jose import jwt
import sqlite3
import bcrypt

SECRET = "super_ultra_secret_key_123456"
ALGORITHM = "HS256"

app = FastAPI()

# =======================
# DB INIT
# =======================
def init_db():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT UNIQUE NOT NULL,
            password_hash BLOB NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def get_user(username):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()

    cur.execute("SELECT password_hash FROM users WHERE nickname = ?", (username,))
    row = cur.fetchone()
    conn.close()

    return row


# =======================
# AUTH
# =======================
@app.post("/register")
async def register(data: dict):
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Empty fields")

    conn = sqlite3.connect("data.db")
    cur = conn.cursor()

    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        cur.execute(
            "INSERT INTO users (nickname, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        conn.commit()
        return {"status": "ok"}
    except sqlite3.IntegrityError as e:
        print("DB ERROR:", e)
        raise HTTPException(status_code=400, detail="User exists")
    finally:
        conn.close()


@app.post("/login")
async def login(data: dict):
    username = data.get("username")
    password = data.get("password")

    row = get_user(username)

    if not row:
        raise HTTPException(status_code=401, detail="User not found")

    if not bcrypt.checkpw(password.encode(), row[0]):
        raise HTTPException(status_code=401, detail="Wrong password")

    token = jwt.encode({"username": username}, SECRET, algorithm=ALGORITHM)

    return {"token": token}


# =======================
# WS CHAT
# =======================
connections = []  # (ws, username)


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    token = ws.query_params.get("token")

    try:
        data = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username = data["username"]
    except:
        await ws.close()
        return

    await ws.accept()
    connections.append((ws, username))

    try:
        while True:
            msg = await ws.receive_text()

            for conn, user in connections:
                await conn.send_text(f"{username}: {msg}")

    except WebSocketDisconnect:
        connections.remove((ws, username))


# =======================
# RUN
# =======================
if __name__ == "__main__":
    import uvicorn

    init_db()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)