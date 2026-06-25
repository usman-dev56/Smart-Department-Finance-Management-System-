import customtkinter as ctk
class ReceiptSettings(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Receipt Settings", font=("Arial", 20, "bold")).pack(pady=20)