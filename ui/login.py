import customtkinter as ctk
from data.funcs import *

db = next(get_db())

class LoginWindow(ctk.CTkToplevel):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)
        
        self.geometry("400x300")
        self._set_appearance_mode("dark")
        self.title("Login")

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.grid(row=0, column=0, padx=20, pady=20)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="ꞏ")
        self.password_entry.grid(row=1, column=0, padx=20, pady=20)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login, bg_color="darkblue")
        self.login_button.grid(row=2, column=0, padx=20, pady=20)

        self.error_label = ctk.CTkLabel(self, text="Invalid username or password.", text_color="red")
        self.error_label.grid(row=3, column=0, padx=20, pady=20)
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = login_user(db, username, password)
        if user:
            print(f"User {username} logged in successfully!")
            self.master.refresh_users(user)
            self.destroy()
        else:
            self.error_label.configure(text="Invalid username or password.")