import customtkinter as ctk
from data.funcs import *
from ui.register import RegisterWindow
from ui.login import LoginWindow
from ui.chats import ChatsFrame

db = next(get_db())

class App(ctk.CTk):
    def __init__(self, **kwargs):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        super().__init__(**kwargs)

        self.geometry("800x600")
        self.title("Messenger")

        self.chats_frame = ChatsFrame(self)
        self.chats_frame.grid(row=0, column=2, padx=20, pady=20)

        self.register_button = ctk.CTkButton(self, text="Register", command=self.register)
        self.register_button.grid(row=0, column=0, padx=20, pady=20)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.grid(row=1, column=0, padx=20, pady=20)

        self.users = ctk.CTkLabel(self, text="Users: ")
        self.users.grid(row=2, column=0, padx=20, pady=20)

        self.current_user = ctk.CTkLabel(self, text="Unlogined")
        self.current_user.grid(row=0, column=1, padx=20, pady=20)

        self.users_list = []
        for user in get_users(db):
            lbl = ctk.CTkLabel(self, text=user.username)
            lbl.grid(row=2 + len(self.users_list), column=0, padx=20, pady=5)
            self.users_list.append(lbl)

    def refresh_users(self, current_user=None):
        self.users.configure(text="Users: ")

        for label in self.users_list:
            label.destroy()
        self.users_list.clear()

        for user in get_users(db):
            lbl = ctk.CTkLabel(self, text=user.username)
            lbl.grid(row=2 + len(self.users_list), column=0, padx=20, pady=5)
            self.users_list.append(lbl)

        if current_user:
            self.current_user.configure(text=current_user.username)
        else:
            self.current_user.configure(text="Unlogined")

        self.chats_frame.update_chats_list()

    def register(self):
        RegisterWindow(self)

    def login(self):
        LoginWindow(self)