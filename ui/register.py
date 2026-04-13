import customtkinter as ctk
from data.funcs import *

db = next(get_db())

class RegisterWindow(ctk.CTkToplevel):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)
        
        self.geometry("400x300")
        self._set_appearance_mode("dark")
        self.title("Register")

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.grid(row=0, column=0, padx=20, pady=20)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.grid(row=1, column=0, padx=20, pady=20)

        self.register_button = ctk.CTkButton(self, text="Register", command=self.register, bg_color="darkblue")
        self.register_button.grid(row=2, column=0, padx=20, pady=20)
    
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        create_user(db, username, password)
        print(f"User {username} registered successfully!")
        self.master.refresh_users(get_user_by_username(db, username))
        self.destroy()