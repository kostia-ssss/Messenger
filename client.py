# client.py
import sys
import asyncio
import threading
import websockets
import requests

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QLabel, QScrollArea, QFrame,
    QDialog, QPushButton
)
from PyQt6.QtCore import pyqtSignal


API_URL = "http://localhost:8000"


# =======================
# API
# =======================
def login_request(username, password):
    try:
        r = requests.post(f"{API_URL}/login", json={
            "username": username,
            "password": password
        })
        return r.json().get("token")
    except:
        return None


def register_request(username, password):
    try:
        r = requests.post(f"{API_URL}/register", json={
            "username": username,
            "password": password
        })

        if r.status_code != 200:
            print("SERVER:", r.text)

        return r.status_code == 200

    except Exception as e:
        print("REQUEST ERROR:", e)
        return False


# =======================
# LOGIN UI
# =======================
class Login(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setFixedSize(300, 170)

        self.token = None
        self.username = None

        self.name_input = QLineEdit()
        self.password_input = QLineEdit()

        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_btn = QPushButton("Login")
        self.register_btn = QPushButton("Register")

        self.login_btn.clicked.connect(self.try_login)
        self.register_btn.clicked.connect(self.try_register)

        layout = QVBoxLayout()
        layout.addWidget(self.name_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.register_btn)

        self.setLayout(layout)

    def try_login(self):
        username = self.name_input.text()
        password = self.password_input.text()

        token = login_request(username, password)

        if token:
            self.token = token
            self.username = username
            self.accept()
        else:
            self.setWindowTitle("❌ Wrong login")

    def try_register(self):
        username = self.name_input.text()
        password = self.password_input.text()

        if register_request(username, password):
            self.setWindowTitle("✅ Registered")
        else:
            self.setWindowTitle("❌ Error")


# =======================
# CHAT
# =======================
class ChatApp(QWidget):

    message_signal = pyqtSignal(str)

    def __init__(self, username, token):
        super().__init__()

        self.username = username
        self.token = token

        self.setWindowTitle(f"Chat - {username}")
        self.resize(500, 700)

        layout = QVBoxLayout()

        self.chat_layout = QVBoxLayout()
        self.chat_widget = QWidget()
        self.chat_widget.setLayout(self.chat_layout)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.chat_widget)

        self.input = QLineEdit()
        self.input.returnPressed.connect(self.send_message)

        layout.addWidget(self.scroll)
        layout.addWidget(self.input)

        self.setLayout(layout)

        self.message_signal.connect(self.add_message)

        self.ws = None
        self.loop = asyncio.new_event_loop()

        threading.Thread(target=self.start_ws, daemon=True).start()

    def add_message(self, msg):
        label = QLabel(msg)
        self.chat_layout.addWidget(label)

    def send_message(self):
        msg = self.input.text()
        if self.ws and msg:
            asyncio.run_coroutine_threadsafe(self.ws.send(msg), self.loop)
            self.input.clear()

    def start_ws(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.ws_main())

    async def ws_main(self):
        uri = f"ws://localhost:8000/ws?token={self.token}"

        while True:
            try:
                async with websockets.connect(uri) as ws:
                    self.ws = ws
                    self.message_signal.emit("✅ Connected")

                    while True:
                        msg = await ws.recv()
                        self.message_signal.emit(msg)

            except Exception as e:
                print("WS ERROR:", e)
                self.message_signal.emit("❌ Reconnecting...")
                await asyncio.sleep(3)


# =======================
# RUN
# =======================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    login = Login()
    if login.exec():
        window = ChatApp(login.username, login.token)
        window.show()
        sys.exit(app.exec())