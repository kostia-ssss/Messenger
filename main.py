# main.py
import sys
import traceback
from PyQt6.QtWidgets import QApplication
from ui.app import App
from sql.funcs import init_db

def main():
    try:
        print("START")
        init_db()
        print("DB OK")

        app = QApplication(sys.argv)
        window = App()
        window.show()

        sys.exit(app.exec())

    except Exception:
        traceback.print_exc()
        input("ERROR (press Enter)")

if __name__ == "__main__":
    main()