# src/views/campaigns/create_campaign.py
import customtkinter as ctk
from tkinter import messagebox
from src.controllers.campaign_controller import create_campaign
from src.controllers.fund_controller import get_active_funds
from src.controllers.academic_controller import get_active_sessions, get_active_programs, get_active_shifts


class CreateCampaign(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.create_header()
        self.create_form()
        self.load_dropdowns()
    
    def create_header(self):
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            header, 
            text="📋 Create Campaign", 
            font=("Arial", 24, "bold")
        ).pack(side="left")
        
        ctk.CTkLabel(
            header, 
            text="Create collection campaigns linked to funds", 
            font=("Arial", 12),
            text_color="gray"
        ).pack(side="left", padx=20)
    
    def create_form(self):
        # Main form frame
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # ─── Row 1: Campaign Name ──────────────────────────────────────
        ctk.CTkLabel(form_frame, text="Campaign Name *", font=("Arial", 13)).grid(
            row=0, column=0, padx=10, pady=10, sticky="w")
        self.name_entry = ctk.CTkEntry(
            form_frame, 
            width=350, 
            placeholder_text="e.g., Study Tour Collection 2024"
        )
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # ─── Row 2: Fund ────────────────────────────────────────────────
        ctk.CTkLabel(form_frame, text="Select Fund *", font=("Arial", 13)).grid(
            row=1, column=0, padx=10, pady=10, sticky="w")
        self.fund_combo = ctk.CTkComboBox(form_frame, width=350, values=["Loading..."])
        self.fund_combo.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # ─── Row 3: Target Program ──────────────────────────────────────
        ctk.CTkLabel(form_frame, text="Target Program", font=("Arial", 13)).grid(
            row=2, column=0, padx=10, pady=10, sticky="w")
        self.program_combo = ctk.CTkComboBox(form_frame, width=350, values=["All Programs"])
        self.program_combo.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        ctk.CTkLabel(
            form_frame, 
            text="(Leave as 'All Programs' for all programs)", 
            font=("Arial", 9),
            text_color="gray"
        ).grid(row=2, column=2, padx=5, pady=10, sticky="w")
        
        # ─── Row 4: Target Session ──────────────────────────────────────
        ctk.CTkLabel(form_frame, text="Target Session", font=("Arial", 13)).grid(
            row=3, column=0, padx=10, pady=10, sticky="w")
        self.session_combo = ctk.CTkComboBox(form_frame, width=350, values=["All Sessions"])
        self.session_combo.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        ctk.CTkLabel(
            form_frame, 
            text="(Leave as 'All Sessions' for all sessions)", 
            font=("Arial", 9),
            text_color="gray"
        ).grid(row=3, column=2, padx=5, pady=10, sticky="w")
        
        # ─── Row 5: Target Semester ──────────────────────────────────────
        ctk.CTkLabel(form_frame, text="Target Semester", font=("Arial", 13)).grid(
            row=4, column=0, padx=10, pady=10, sticky="w")
        self.semester_combo = ctk.CTkComboBox(
            form_frame, 
            width=350, 
            values=["All Semesters", "1", "2", "3", "4", "5", "6", "7", "8"]
        )
        self.semester_combo.set("All Semesters")
        self.semester_combo.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        ctk.CTkLabel(
            form_frame, 
            text="(Select specific semester or all)", 
            font=("Arial", 9),
            text_color="gray"
        ).grid(row=4, column=2, padx=5, pady=10, sticky="w")
        
        # ─── Row 6: Target Shift ────────────────────────────────────────
        ctk.CTkLabel(form_frame, text="Target Shift", font=("Arial", 13)).grid(
            row=5, column=0, padx=10, pady=10, sticky="w")
        self.shift_combo = ctk.CTkComboBox(form_frame, width=350, values=["All Shifts"])
        self.shift_combo.grid(row=5, column=1, padx=10, pady=10, sticky="w")
        ctk.CTkLabel(
            form_frame, 
            text="(Leave as 'All Shifts' for all shifts)", 
            font=("Arial", 9),
            text_color="gray"
        ).grid(row=5, column=2, padx=5, pady=10, sticky="w")
        
        # ─── Row 7: Required Amount ──────────────────────────────────────
        ctk.CTkLabel(form_frame, text="Required Amount (Rs.) *", font=("Arial", 13)).grid(
            row=6, column=0, padx=10, pady=10, sticky="w")
        self.amount_entry = ctk.CTkEntry(
            form_frame, 
            width=350, 
            placeholder_text="e.g., 2000"
        )
        self.amount_entry.grid(row=6, column=1, padx=10, pady=10, sticky="w")
        
        # ─── Submit Button ─────────────────────────────────────────────
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=7, column=0, columnspan=2, pady=30)
        
        self.submit_btn = ctk.CTkButton(
            btn_frame, 
            text="✅ Create Campaign", 
            command=self.create_campaign,
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
    
    def load_dropdowns(self):
        """Load all dropdown values from database"""
        try:
            # Load Funds
            funds = get_active_funds()
            fund_names = [f["fund_name"] for f in funds] if funds else ["No funds found"]
            self.fund_combo.configure(values=fund_names)
            if fund_names and fund_names[0] != "No funds found":
                self.fund_combo.set(fund_names[0])
            else:
                self.fund_combo.set("No funds found")
                messagebox.showwarning(
                    "Warning", 
                    "No funds found! Please create a fund first."
                )
            
            # Load Programs
            programs = get_active_programs()
            program_names = ["All Programs"] + [p["program_name"] for p in programs] if programs else ["All Programs"]
            self.program_combo.configure(values=program_names)
            self.program_combo.set("All Programs")
            
            # Load Sessions
            sessions = get_active_sessions()
            session_names = ["All Sessions"] + [s["session_name"] for s in sessions] if sessions else ["All Sessions"]
            self.session_combo.configure(values=session_names)
            self.session_combo.set("All Sessions")
            
            # Load Shifts
            shifts = get_active_shifts()
            shift_names = ["All Shifts"] + [s["shift_name"] for s in shifts] if shifts else ["All Shifts"]
            self.shift_combo.configure(values=shift_names)
            self.shift_combo.set("All Shifts")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")
    
    def go_back(self):
        """Go back to campaign list"""
        from src.views.campaigns.campaign_list import CampaignList
        parent = self.master
        while parent:
            if hasattr(parent, 'show_view'):
                parent.show_view(CampaignList)
                break
            parent = parent.master
    
    def create_campaign(self):
        """Create a new campaign"""
        campaign_name = self.name_entry.get().strip()
        fund_name = self.fund_combo.get()
        program_name = self.program_combo.get()
        session_name = self.session_combo.get()
        semester = self.semester_combo.get()
        shift_name = self.shift_combo.get()
        amount = self.amount_entry.get().strip()
        
        # ─── Validate ──────────────────────────────────────────────────
        if not campaign_name:
            messagebox.showerror("Error", "Campaign name is required")
            return
        
        if fund_name in ["Loading...", "No funds found"]:
            messagebox.showerror("Error", "Please select a valid fund")
            return
        
        if not amount:
            messagebox.showerror("Error", "Required amount is required")
            return
        
        try:
            amount = float(amount)
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")
            return
        
        # ─── Get IDs from names ────────────────────────────────────────
        funds = get_active_funds()
        fund_id = next((f["id"] for f in funds if f["fund_name"] == fund_name), None)
        
        programs = get_active_programs()
        program_id = None
        if program_name != "All Programs":
            program_id = next((p["id"] for p in programs if p["program_name"] == program_name), None)
        
        sessions = get_active_sessions()
        session_id = None
        if session_name != "All Sessions":
            session_id = next((s["id"] for s in sessions if s["session_name"] == session_name), None)
        
        shifts = get_active_shifts()
        shift_id = None
        if shift_name != "All Shifts":
            shift_id = next((s["id"] for s in shifts if s["shift_name"] == shift_name), None)
        
        semester_val = None
        if semester != "All Semesters":
            try:
                semester_val = int(semester)
            except ValueError:
                pass
        
        if not fund_id:
            messagebox.showerror("Error", "Invalid fund selected")
            return
        
        # ─── Prepare data ──────────────────────────────────────────────
        campaign_data = {
            "campaign_name": campaign_name,
            "fund_id": fund_id,
            "program_id": program_id,
            "session_id": session_id,
            "semester": semester_val,
            "shift_id": shift_id,
            "required_amount": amount,
            "department_id": 1
        }
        
        try:
            campaign_id = create_campaign(campaign_data)
            
            messagebox.showinfo(
                "Success", 
                f"✅ Campaign created successfully!\n\n"
                f"Name: {campaign_name}\n"
                f"Fund: {fund_name}\n"
                f"Target: {self.get_target_summary()}\n"
                f"Required Amount: Rs. {amount:,.2f}"
            )
            
            self.clear_form()
            self.go_back()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create campaign: {e}")
    
    def get_target_summary(self):
        """Get summary of target selection"""
        parts = []
        
        program = self.program_combo.get()
        if program != "All Programs":
            parts.append(f"Program: {program}")
        
        session = self.session_combo.get()
        if session != "All Sessions":
            parts.append(f"Session: {session}")
        
        semester = self.semester_combo.get()
        if semester != "All Semesters":
            parts.append(f"Semester: {semester}")
        
        shift = self.shift_combo.get()
        if shift != "All Shifts":
            parts.append(f"Shift: {shift}")
        
        return ", ".join(parts) if parts else "All Students"
    
    def clear_form(self):
        """Clear all form fields"""
        self.name_entry.delete(0, "end")
        self.amount_entry.delete(0, "end")
        self.program_combo.set("All Programs")
        self.session_combo.set("All Sessions")
        self.semester_combo.set("All Semesters")
        self.shift_combo.set("All Shifts")