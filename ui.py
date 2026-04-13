import customtkinter as ctk
from data.funcs import *

db = next(get_db())

class App(ctk.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.geometry("800x600")
        self._set_appearance_mode("dark")
        self.title("Messenger")

        self.register_button = ctk.CTkButton(self, text="Register", command=self.register)
        self.register_button.grid(row=0, column=0, padx=20, pady=20)

        self.users = ctk.CTkLabel(self, text=f"Users: ")
        self.users.grid(row=1, column=0, padx=20, pady=20)

        self.users_list = []
        for user in get_users(db):
            self.users_list.append(ctk.CTkLabel(self, text=user.username))
            self.users_list[-1].grid(row=2+len(self.users_list), column=0, padx=20, pady=5)
    
    def refresh_users(self):
        self.users.configure(text=f"Users: ")
        # Clear existing user labels
        for label in self.users_list:
            label.destroy()
        self.users_list.clear()
        # Create new user labels
        for user in get_users(db):
            self.users_list.append(ctk.CTkLabel(self, text=user.username))
            self.users_list[-1].grid(row=2+len(self.users_list), column=0, padx=20, pady=5)

    def register(self):
        RegisterWindow(self)

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
        self.master.refresh_users()
        self.destroy()