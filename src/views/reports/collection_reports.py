import customtkinter as ctk
class CollectionReports(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Collection Reports", font=("Arial", 20, "bold")).pack(pady=20)