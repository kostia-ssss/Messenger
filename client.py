import sys
import asyncio
import threading
import websockets
import ssl

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QLabel, QScrollArea, QFrame,
    QDialog, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal


# =======================
# LOGIN WINDOW
# =======================
class Login(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setFixedSize(300, 150)

        self.room_input = QLineEdit()
        self.room_input.setPlaceholderText("Кімната (WW1, general...)")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Нік")

        self.btn = QPushButton("Join")
        self.btn.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.room_input)
        layout.addWidget(self.name_input)
        layout.addWidget(self.btn)

        self.setLayout(layout)

    def get_data(self):
        return self.room_input.text(), self.name_input.text()


# =======================
# Bubble widget
# =======================
class MessageBubble(QFrame):
    def __init__(self, text, is_me=False):
        super().__init__()

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {'#2b5278' if is_me else '#3a3a3a'};
                border-radius: 10px;
                padding: 8px;
                color: white;
            }}
        """)

        layout = QHBoxLayout()
        label = QLabel(text)
        label.setWordWrap(True)

        layout.addWidget(label)
        self.setLayout(layout)


# =======================
# MAIN CHAT
# =======================
class ChatApp(QWidget):

    message_signal = pyqtSignal(str)

    def __init__(self, room, nickname):
        super().__init__()

        self.room = room
        self.nickname = nickname

        self.setWindowTitle(f"Messenger - {room}")
        self.setGeometry(300, 150, 500, 700)

        # UI
        self.layout = QVBoxLayout()

        self.chat_layout = QVBoxLayout()

        self.scroll_widget = QWidget()
        self.scroll_widget.setLayout(self.chat_layout)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.scroll_widget)

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Напиши повідомлення...")
        self.input_box.returnPressed.connect(self.send_message)

        self.layout.addWidget(self.scroll)
        self.layout.addWidget(self.input_box)

        self.setLayout(self.layout)

        # signals
        self.message_signal.connect(self.handle_message)

        # websocket
        self.ws = None
        self.loop = asyncio.new_event_loop()

        threading.Thread(target=self.start_ws, daemon=True).start()

    # =======================
    # UI
    # =======================
    def add_message(self, text, is_me=False):
        bubble = MessageBubble(text, is_me)

        container = QHBoxLayout()

        if is_me:
            container.addStretch()
            container.addWidget(bubble)
        else:
            container.addWidget(bubble)
            container.addStretch()

        wrapper = QWidget()
        wrapper.setLayout(container)

        self.chat_layout.addWidget(wrapper)

        self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().maximum()
        )

    def handle_message(self, msg):
        is_me = f"{self.nickname}:" in msg
        self.add_message(msg, is_me)

    def send_message(self):
        msg = self.input_box.text()
        if msg and self.ws:
            asyncio.run_coroutine_threadsafe(self.ws.send(msg), self.loop)
            self.input_box.clear()

    # =======================
    # WS THREAD
    # =======================
    def start_ws(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.ws_main())

    

    async def ws_main(self):
        uri = f"wss://polarstar.onrender.com/ws/{self.room}/{self.nickname}"

        ssl_context = ssl._create_unverified_context()

        try:
            async with websockets.connect(uri, ssl=ssl_context) as ws:
                self.ws = ws

                self.message_signal.emit("✅ Connected")

                while True:
                    msg = await ws.recv()
                    self.message_signal.emit(msg)

        except Exception as e:
            print("WS ERROR:", e)
            self.message_signal.emit(f"❌ ERROR: {e}")


# =======================
# RUN
# =======================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    login = Login()
    if login.exec():
        room, nickname = login.get_data()

        window = ChatApp(room, nickname)
        window.show()

        sys.exit(app.exec())