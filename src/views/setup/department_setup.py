import customtkinter as ctk
from src.controllers.department_controller import save_department

class DepartmentSetup(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Department Setup", font=("Arial", 20, "bold")).pack(pady=20)