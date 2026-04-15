# ui/theme_manager.py
import json
import os
import sys

# ===== PATH RESOLUTION =====
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
    RESOURCE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RESOURCE_DIR = BASE_DIR
    
THEME_PATH = os.path.join(BASE_DIR, "data", "theme.json")

def load_theme(app, theme_name):
    theme_path = os.path.join(BASE_DIR, "themes", f"{theme_name}.qss")
    if os.path.exists(theme_path):
        try:
            with open(theme_path, "r", encoding="utf-8") as f:
                app.setStyleSheet(f.read())
        except Exception as e:
            print(f"Error loading theme: {e}")
    else:
        print(f"Warning: Theme file not found at {theme_path}")

def set_theme(name):
    try:
        os.makedirs(os.path.dirname(THEME_PATH), exist_ok=True)
        with open(THEME_PATH, "w", encoding="utf-8") as f:
            json.dump({"theme": name}, f)
    except Exception as e:
        print(f"Error setting theme: {e}")

def get_theme():
    try:
        if os.path.exists(THEME_PATH):
            with open(THEME_PATH, "r", encoding="utf-8") as f:
                return json.load(f)["theme"]
        return "dark"
    except Exception as e:
        print(f"Error reading theme: {e}")
        return "dark"