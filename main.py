from ui.app import App
from sql.funcs import init_db
from PyQt6.QtWidgets import QApplication
import sys

def main():
    init_db()

    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()