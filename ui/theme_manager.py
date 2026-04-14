import json
import os

THEME_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "theme.json")

def load_theme(app, path):
    with open(path, "r") as f:
        app.setStyleSheet(f.read())

def set_theme(name):
    with open(THEME_PATH, "w") as f:
        json.dump({"theme": name}, f)

def get_theme():
    try:
        with open(THEME_PATH, "r") as f:
            return json.load(f)["theme"]
    except:
        return "dark"