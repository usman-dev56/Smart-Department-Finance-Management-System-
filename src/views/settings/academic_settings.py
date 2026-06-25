# src/views/settings/academic_settings.py
import customtkinter as ctk
from src.views.academics.session_manager import SessionManager
from src.views.academics.program_manager import ProgramManager
from src.views.academics.shift_manager import ShiftManager
from src.views.academics.section_manager import SectionManager


class AcademicSettings(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        ctk.CTkLabel(
            self, 
            text="📚 Academic Structure", 
            font=("Arial", 24, "bold")
        ).pack(pady=20)
        
        tabview = ctk.CTkTabview(self)
        tabview.pack(fill="both", expand=True, padx=20, pady=10)
        
        tabview.add("Sessions")
        tabview.add("Programs")
        tabview.add("Shifts")
        tabview.add("Sections")
        
        SessionManager(tabview.tab("Sessions")).pack(fill="both", expand=True)
        ProgramManager(tabview.tab("Programs")).pack(fill="both", expand=True)
        ShiftManager(tabview.tab("Shifts")).pack(fill="both", expand=True)
        SectionManager(tabview.tab("Sections")).pack(fill="both", expand=True)