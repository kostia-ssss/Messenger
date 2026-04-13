import customtkinter as ctk
from data.funcs import *
from ui.select_user import SelectUserWindow

db = next(get_db())

class ChatsFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

        username = master.current_user.cget("text") if hasattr(master, "current_user") else "Unlogined"

        self.current_user = None

        if username != "Unlogined":
            self.current_user = get_user_by_username(db, username)

        self.chats_list = ctk.CTkLabel(self, text="Chats: ")
        self.chats_list.grid(row=0, column=0, padx=20, pady=20)

        self.chat_buttons = []
        self.update_chats_list()



    def update_chats_list(self):
        # Re-fetch current user from master widget
        username = self.master.current_user.cget("text") if hasattr(self.master, "current_user") else "Unlogined"
        if username != "Unlogined":
            self.current_user = get_user_by_username(db, username)
        else:
            self.current_user = None

        if not self.current_user:
            return

        chats = get_chats_of_user(db, self.current_user.id)

        for btn in self.chat_buttons:
            btn.destroy()

        self.chat_buttons = []

        for i, chat in enumerate(chats):
            other_user = get_user_by_id(
                db,
                chat.user2_id if chat.user1_id == self.current_user.id else chat.user1_id
            )

            btn = ctk.CTkButton(self, text=f"Chat with {other_user.username}")
            btn.grid(row=1 + i, column=0, padx=20, pady=5)

            self.chat_buttons.append(btn)
    
        next_row = 1 + len(chats)

        btn = ctk.CTkButton(
            self,
            text="+",
            command=self.add_chat
        )

        btn.grid(row=next_row, column=0, padx=20, pady=5)

        self.chat_buttons.append(btn)
        
    def add_chat(self):
        if not self.current_user:
            return

        SelectUserWindow(
            self,
            self.current_user,
            self.create_chat_with_user
        )
    
    def create_chat_with_user(self, user):
        create_chat(db, self.current_user.id, user.id)
        self.update_chats_list()