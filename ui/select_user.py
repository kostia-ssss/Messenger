import customtkinter as ctk
from data.funcs import *

db = next(get_db())

class SelectUserWindow(ctk.CTkToplevel):
    def __init__(self, master, current_user, on_select):
        super().__init__(master)

        self.title("New Chat")
        self.geometry("300x400")

        self.current_user = current_user
        self.on_select = on_select

        # 🔍 search box
        self.search_var = ctk.StringVar()

        self.search_entry = ctk.CTkEntry(
            self,
            textvariable=self.search_var,
            placeholder_text="Search user..."
        )
        self.search_entry.pack(fill="x", padx=10, pady=10)

        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh())

        # 📜 frame for users
        self.users_frame = ctk.CTkScrollableFrame(self)
        self.users_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh()

    def refresh(self):
        # clear old buttons
        for widget in self.users_frame.winfo_children():
            widget.destroy()

        query = self.search_var.get().lower()

        users = get_users(db)

        for user in users:
            if user.id == self.current_user.id:
                continue

            if query and query not in user.username.lower():
                continue

            btn = ctk.CTkButton(
                self.users_frame,
                text=user.username,
                command=lambda u=user: self.select_user(u)
            )
            btn.pack(fill="x", pady=5)

    def select_user(self, user):
        self.on_select(user)
        self.destroy()