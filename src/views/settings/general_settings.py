# src/views/settings/general_settings.py
import customtkinter as ctk
from src.views.settings.academic_settings import AcademicSettings


class GeneralSettings(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        # Main container
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(
            container, 
            text="⚙️ Settings", 
            font=("Arial", 24, "bold")
        ).pack(anchor="w", pady=10)
        
        # Tab view for settings categories
        tabview = ctk.CTkTabview(container)
        tabview.pack(fill="both", expand=True)
        
        # Add tabs
        tabview.add("General")
        tabview.add("Academics")    # ← IMPORTANT: This adds the Academics tab
        tabview.add("Receipt")
        tabview.add("Backup")
        
        # ─── General Tab ──────────────────────────────────────────────
        general_frame = tabview.tab("General")
        self.create_general_settings(general_frame)
        
        # ─── Academics Tab ────────────────────────────────────────────
        # This loads Session, Program, Shift, Section managers
        AcademicSettings(tabview.tab("Academics")).pack(fill="both", expand=True)
        
        # ─── Receipt Tab ──────────────────────────────────────────────
        receipt_frame = tabview.tab("Receipt")
        self.create_receipt_settings(receipt_frame)
        
        # ─── Backup Tab ───────────────────────────────────────────────
        backup_frame = tabview.tab("Backup")
        self.create_backup_settings(backup_frame)
    
    def create_general_settings(self, parent):
        ctk.CTkLabel(
            parent, 
            text="General Settings", 
            font=("Arial", 16, "bold")
        ).pack(anchor="w", pady=10)
        
        ctk.CTkLabel(parent, text="Department Name:").pack(anchor="w", pady=(10, 0))
        self.dept_entry = ctk.CTkEntry(parent, width=300)
        self.dept_entry.pack(anchor="w", pady=(0, 5))
        self.dept_entry.insert(0, "Computer Science")
        
        ctk.CTkLabel(parent, text="University Name:").pack(anchor="w", pady=(10, 0))
        self.uni_entry = ctk.CTkEntry(parent, width=300)
        self.uni_entry.pack(anchor="w", pady=(0, 5))
        self.uni_entry.insert(0, "GC University Faisalabad")
        
        ctk.CTkButton(
            parent, 
            text="💾 Save Settings",
            fg_color="#1a73e8"
        ).pack(anchor="w", pady=20)
    
    def create_receipt_settings(self, parent):
        ctk.CTkLabel(
            parent, 
            text="Receipt Settings", 
            font=("Arial", 16, "bold")
        ).pack(anchor="w", pady=10)
        
        ctk.CTkLabel(parent, text="Receipt Prefix:").pack(anchor="w", pady=(10, 0))
        self.prefix_entry = ctk.CTkEntry(parent, width=150)
        self.prefix_entry.pack(anchor="w", pady=(0, 5))
        self.prefix_entry.insert(0, "CS")
        
        ctk.CTkLabel(
            parent, 
            text="Current receipt number will be: CS-00001",
            text_color="gray",
            font=("Arial", 11)
        ).pack(anchor="w", pady=5)
        
        ctk.CTkButton(
            parent, 
            text="💾 Save Settings",
            fg_color="#1a73e8"
        ).pack(anchor="w", pady=20)
    
    def create_backup_settings(self, parent):
        ctk.CTkLabel(
            parent, 
            text="Backup Settings", 
            font=("Arial", 16, "bold")
        ).pack(anchor="w", pady=10)
        
        ctk.CTkLabel(
            parent,
            text="Create a backup of your database",
            text_color="gray"
        ).pack(anchor="w", pady=5)
        
        ctk.CTkButton(
            parent, 
            text="📦 Create Backup Now",
            fg_color="#0f9d58"
        ).pack(anchor="w", pady=10)