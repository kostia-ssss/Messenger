import sqlite3
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

rooms = {}

# --- DB SETUP ---
conn = sqlite3.connect("chat.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room TEXT,
    nickname TEXT,
    message TEXT
)
""")
conn.commit()


def save_message(room, nickname, message):
    cur.execute(
        "INSERT INTO messages (room, nickname, message) VALUES (?, ?, ?)",
        (room, nickname, message)
    )
    conn.commit()


def load_history(room, limit=20):
    cur.execute(
        "SELECT nickname, message FROM messages WHERE room=? ORDER BY id DESC LIMIT ?",
        (room, limit)
    )
    return cur.fetchall()[::-1]


# --- WEBSOCKET ---
@app.websocket("/ws/{room}/{nickname}")
async def websocket_endpoint(ws: WebSocket, room: str, nickname: str):
    await ws.accept()

    if room not in rooms:
        rooms[room] = set()

    rooms[room].add(ws)

    print(f"🔌 {nickname} зайшов у {room}")

    # 📜 відправка історії при вході
    history = load_history(room)
    for nick, msg in history:
        await ws.send_text(f"[HISTORY] {nick}: {msg}")

    try:
        while True:
            msg = await ws.receive_text()

            formatted = f"[{room}] {nickname}: {msg}"
            print("📩", formatted)

            # 💾 save to DB
            save_message(room, nickname, msg)

            # 📤 broadcast
            for client in list(rooms[room]):
                try:
                    await client.send_text(formatted)
                except:
                    rooms[room].remove(client)

    except WebSocketDisconnect:
        rooms[room].remove(ws)
        print(f"❌ {nickname} вийшов з {room}")