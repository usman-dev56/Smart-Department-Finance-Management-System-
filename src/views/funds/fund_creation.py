# src/views/funds/fund_creation.py
import customtkinter as ctk
from tkinter import messagebox
from src.controllers.fund_controller import create_fund, get_all_funds


class FundCreation(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.create_header()
        self.create_form()
    
    def create_header(self):
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            header, 
            text="💰 Create New Fund", 
            font=("Arial", 24, "bold")
        ).pack(side="left")
        
        ctk.CTkLabel(
            header, 
            text="Create funds for different department activities", 
            font=("Arial", 12),
            text_color="gray"
        ).pack(side="left", padx=20)
    
    def create_form(self):
        # Main form frame
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # ─── Row 1: Fund Name ──────────────────────────────────────────
        ctk.CTkLabel(form_frame, text="Fund Name *", font=("Arial", 13)).grid(
            row=0, column=0, padx=10, pady=15, sticky="w")
        self.name_entry = ctk.CTkEntry(
            form_frame, 
            width=400, 
            placeholder_text="e.g., Study Tour Fund, Lab Fund, Sports Fund"
        )
        self.name_entry.grid(row=0, column=1, padx=10, pady=15, sticky="w")
        
        # ─── Row 2: Fund Description ──────────────────────────────────
        ctk.CTkLabel(form_frame, text="Description", font=("Arial", 13)).grid(
            row=1, column=0, padx=10, pady=15, sticky="w")
        self.desc_entry = ctk.CTkEntry(
            form_frame, 
            width=400, 
            placeholder_text="Brief description of the fund (optional)"
        )
        self.desc_entry.grid(row=1, column=1, padx=10, pady=15, sticky="w")
        
        # ─── Row 3: Fund Type ──────────────────────────────────────────
        ctk.CTkLabel(form_frame, text="Fund Type", font=("Arial", 13)).grid(
            row=2, column=0, padx=10, pady=15, sticky="w")
        
        fund_types = [
            "General",
            "Academic",
            "Event", 
            "Tour",
            "Lab",
            "Sports",
            "Workshop",
            "Industrial Visit",
            "Farewell",
            "Other"
        ]
        self.type_combo = ctk.CTkComboBox(
            form_frame, 
            width=400, 
            values=fund_types
        )
        self.type_combo.set("General")
        self.type_combo.grid(row=2, column=1, padx=10, pady=15, sticky="w")
        
        # ─── Submit Button ─────────────────────────────────────────────
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=3, column=0, columnspan=2, pady=30)
        
        self.submit_btn = ctk.CTkButton(
            btn_frame, 
            text="✅ Create Fund", 
            command=self.create_fund,
            fg_color="#1a73e8",
            width=200,
            height=40,
            font=("Arial", 14, "bold")
        )
        self.submit_btn.pack(side="left", padx=10)
        
        self.cancel_btn = ctk.CTkButton(
            btn_frame, 
            text="❌ Cancel", 
            command=self.go_back,
            fg_color="gray",
            width=150,
            height=40,
            font=("Arial", 14)
        )
        self.cancel_btn.pack(side="left", padx=10)
    
    def go_back(self):
        """Go back to fund list"""
        from src.views.funds.fund_list import FundList
        parent = self.master
        while parent:
            if hasattr(parent, 'show_view'):
                parent.show_view(FundList)
                break
            parent = parent.master
    
    def create_fund(self):
        """Create a new fund"""
        fund_name = self.name_entry.get().strip()
        description = self.desc_entry.get().strip()
        fund_type = self.type_combo.get()
        
        # Validate
        if not fund_name:
            messagebox.showerror("Error", "Fund name is required")
            self.name_entry.focus()
            return
        
        if len(fund_name) < 3:
            messagebox.showerror("Error", "Fund name must be at least 3 characters")
            return
        
        # Check if fund already exists
        existing = get_all_funds()
        for fund in existing:
            if fund["fund_name"].lower() == fund_name.lower():
                messagebox.showerror("Error", f"Fund '{fund_name}' already exists!")
                return
        
        try:
            # Create fund - FIXED: passing fund_type
            fund_id = create_fund(fund_name, description, 1, fund_type)  # ← CHANGED HERE
            
            messagebox.showinfo(
                "Success", 
                f"✅ Fund created successfully!\n\n"
                f"Fund Name: {fund_name}\n"
                f"Type: {fund_type}\n"
                f"Description: {description if description else 'N/A'}"
            )
            
            # Clear form
            self.clear_form()
            
            # Go back to fund list
            self.go_back()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create fund: {e}")
    
    def clear_form(self):
        """Clear all form fields"""
        self.name_entry.delete(0, "end")
        self.desc_entry.delete(0, "end")
        self.type_combo.set("General")