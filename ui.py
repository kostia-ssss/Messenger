import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.geometry("800x600")
        self._set_appearance_mode("dark")
        self.title("Messenger")