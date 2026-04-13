from ui.app import App
from data.funcs import init_db

init_db()

app = App()
app.mainloop()