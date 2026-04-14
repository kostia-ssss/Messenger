import os
import json
from PyQt6.QtWidgets import *
from sql.funcs import *
from ui.theme_manager import *

db = next(get_db())

def load_styles(app):
    with open("styles.qss", "r") as f:
        app.setStyleSheet(f.read())

# ===== CURRENT USER =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(BASE_DIR, "..", "data", "current_user.json")

def get_current_user():
    try:
        with open(PATH, "r") as f:
            data = json.load(f)
            username = data["username"]
            return get_user_by_username(db, username)
    except:
        return None

def set_current_user(username):
    with open(PATH, "w") as f:
        json.dump({"username": username}, f)

# ===== MAIN APP =====
class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PolarStar")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)

        self.current_user = get_current_user()

        self.apply_theme()

        self.reload_ui()

    def apply_theme(self):
        theme = get_theme()

        if theme == "dark":
            load_theme(QApplication.instance(), "themes/dark.qss")
        else:
            load_theme(QApplication.instance(), "themes/light.qss")

    def toggle_theme(self):
        current = get_theme()

        if current == "dark":
            set_theme("light")
        else:
            set_theme("dark")

        self.apply_theme()

    def reload_ui(self):
        for i in reversed(range(self.main_layout.count())):
            w = self.main_layout.itemAt(i).widget()
            if w:
                w.deleteLater()

        if self.current_user is None:
            self.show_login_buttons()
        else:
            self.show_user_info()

    def show_login_buttons(self):
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.open_login_window)
        self.main_layout.addWidget(login_button)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self.open_register_window)
        self.main_layout.addWidget(register_button)

        theme_button = QPushButton("Toggle Theme")
        theme_button.clicked.connect(self.toggle_theme)
        self.main_layout.addWidget(theme_button)

    def show_user_info(self):
        label = QLabel(f"Welcome, {self.current_user.username}!")
        self.main_layout.addWidget(label)

        logout_button = QPushButton("Logout")
        logout_button.clicked.connect(self.logout)
        self.main_layout.addWidget(logout_button)

        theme_button = QPushButton("Toggle Theme")
        theme_button.clicked.connect(self.toggle_theme)
        self.main_layout.addWidget(theme_button)

    def logout(self):
        set_current_user("")
        self.current_user = None
        self.reload_ui()

# ===== REGISTER =====
class Register(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Register")
        self.setGeometry(200, 200, 300, 200)

        load_styles(self)

        self.parent_app = parent

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password)

        btn = QPushButton("Register")
        btn.clicked.connect(self.register)
        layout.addWidget(btn)

    def register(self):
        username = self.username.text()
        password = self.password.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Fill all fields")
            return

        user = create_user(db, username, password)
        if not user:
            QMessageBox.warning(self, "Error", "User exists")
            return

        set_current_user(username)

        self.parent_app.current_user = user
        self.parent_app.reload_ui()

        QMessageBox.information(self, "Success", "Registered!")
        self.close()

# ===== LOGIN =====
class Login(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.setGeometry(200, 200, 300, 200)

        load_styles(self)

        self.parent_app = parent

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password)

        btn = QPushButton("Login")
        btn.clicked.connect(self.login)
        layout.addWidget(btn)

    def login(self):
        username = self.username.text()
        password = self.password.text()

        user = get_user_by_username(db, username)

        if not user or not verify_password(password, user.password):
            QMessageBox.warning(self, "Error", "Invalid data")
            return

        set_current_user(username)

        self.parent_app.current_user = user
        self.parent_app.reload_ui()

        QMessageBox.information(self, "Success", "Logged in!")
        self.close()