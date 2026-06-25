import customtkinter as ctk
class LoginView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Login", font=("Arial", 24, "bold")).pack(pady=20)