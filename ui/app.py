import customtkinter as ctk
from data.funcs import *
from ui.register import RegisterWindow
from ui.login import LoginWindow

db = next(get_db())

class App(ctk.CTk):
    def __init__(self, **kwargs):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        super().__init__(**kwargs)
        
        self.geometry("800x600")
        self._set_appearance_mode("dark")
        self.title("Messenger")

        self.register_button = ctk.CTkButton(self, text="Register", command=self.register)
        self.register_button.grid(row=0, column=0, padx=20, pady=20)\
        
        self.register_button = ctk.CTkButton(self, text="Register", command=self.register)
        self.register_button.grid(row=0, column=0, padx=20, pady=20)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.grid(row=1, column=0, padx=20, pady=20)

        self.users = ctk.CTkLabel(self, text=f"Users: ")
        self.users.grid(row=2, column=0, padx=20, pady=20)

        self.current_user = ctk.CTkLabel(self, text=f"Unlogined")
        self.current_user.grid(row=0, column=1, padx=20, pady=20)

        self.users_list = []
        for user in get_users(db):
            self.users_list.append(ctk.CTkLabel(self, text=user.username))
            self.users_list[-1].grid(row=2+len(self.users_list), column=0, padx=20, pady=5)
    
    def refresh_users(self, current_user=None):
        self.users.configure(text=f"Users: ")
        # Clear existing user labels
        for label in self.users_list:
            label.destroy()
        self.users_list.clear()
        # Create new user labels
        for user in get_users(db):
            self.users_list.append(ctk.CTkLabel(self, text=user.username))
            self.users_list[-1].grid(row=2+len(self.users_list), column=0, padx=20, pady=5)

        if current_user:
            self.current_user.configure(text=f"Logged in as: {current_user.username}")
        else:
            self.current_user.configure(text=f"Unlogined")

    def register(self):
        RegisterWindow(self)

    def login(self):
        LoginWindow(self)