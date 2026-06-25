import customtkinter as ctk
class StudentSearch(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Search Students", font=("Arial", 20, "bold")).pack(pady=20)