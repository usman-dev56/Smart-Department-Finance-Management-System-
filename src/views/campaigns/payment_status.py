# src/views/campaigns/payment_status.py
import customtkinter as ctk
from tkinter import messagebox
from src.controllers.campaign_controller import (
    get_all_campaigns,
    get_paid_students,
    get_pending_students
)
from src.controllers.student_controller import get_student_by_roll


class PaymentStatus(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.create_header()
        self.create_search()
        self.create_results()
    
    def create_header(self):
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            header, 
            text="💳 Payment Status", 
            font=("Arial", 24, "bold")
        ).pack(side="left")
        
        ctk.CTkLabel(
            header, 
            text="Check student payment status across campaigns", 
            font=("Arial", 12),
            text_color="gray"
        ).pack(side="left", padx=20)
    
    def create_search(self):
        """Create search section"""
        search_frame = ctk.CTkFrame(self)
        search_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            search_frame, 
            text="Search Student:", 
            font=("Arial", 14, "bold")
        ).pack(side="left", padx=10)
        
        self.roll_entry = ctk.CTkEntry(
            search_frame, 
            placeholder_text="Enter Roll Number (e.g., BSCS-2024-001)",
            width=300
        )
        self.roll_entry.pack(side="left", padx=10)
        
        self.search_btn = ctk.CTkButton(
            search_frame,
            text="🔍 Search",
            command=self.search_student,
            fg_color="#1a73e8",
            width=100
        )
        self.search_btn.pack(side="left", padx=10)
        
        self.clear_btn = ctk.CTkButton(
            search_frame,
            text="Clear",
            command=self.clear_results,
            fg_color="gray",
            width=80
        )
        self.clear_btn.pack(side="left", padx=10)
    
    def create_results(self):
        """Create results area"""
        self.results_frame = ctk.CTkFrame(self)
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Student info
        self.student_info = ctk.CTkFrame(self.results_frame)
        self.student_info.pack(fill="x", pady=5)
        
        # Campaign list
        self.campaigns_frame = ctk.CTkScrollableFrame(
            self.results_frame, 
            label_text="Campaign Status"
        )
        self.campaigns_frame.pack(fill="both", expand=True, pady=10)
    
    def search_student(self):
        """Search and display student payment status"""
        roll_number = self.roll_entry.get().strip()
        
        if not roll_number:
            messagebox.showerror("Error", "Please enter a roll number")
            return
        
        # Get student details
        student = get_student_by_roll(roll_number)
        if not student:
            messagebox.showerror("Error", f"Student with roll number '{roll_number}' not found")
            return
        
        # Clear previous results
        for widget in self.student_info.winfo_children():
            widget.destroy()
        for widget in self.campaigns_frame.winfo_children():
            widget.destroy()
        
        # ─── Display Student Info ──────────────────────────────────────────
        info_text = (
            f"👨‍🎓 {student.get('student_name', '')}\n"
            f"📚 Roll No: {student.get('roll_number', '')}\n"
            f"📖 Program: {student.get('program_name', '')} | "
            f"Session: {student.get('session_name', '')} | "
            f"Semester: {student.get('semester', '')}"
        )
        ctk.CTkLabel(
            self.student_info, 
            text=info_text, 
            font=("Arial", 14),
            justify="left"
        ).pack(anchor="w", padx=10, pady=10)
        
        # ─── Get all campaigns ──────────────────────────────────────────────
        campaigns = get_all_campaigns()
        
        if not campaigns:
            ctk.CTkLabel(
                self.campaigns_frame, 
                text="No campaigns found", 
                font=("Arial", 14),
                text_color="gray"
            ).pack(pady=20)
            return
        
        # ─── Headers ──────────────────────────────────────────────────────
        headers_frame = ctk.CTkFrame(self.campaigns_frame)
        headers_frame.pack(fill="x", pady=5)
        
        header_labels = ["Campaign", "Fund", "Amount", "Status", "Date"]
        for header in header_labels:
            ctk.CTkLabel(
                headers_frame, 
                text=header, 
                font=("Arial", 12, "bold"),
                width=150
            ).pack(side="left", padx=10, pady=5)
        
        campaigns_shown = 0
        
        for campaign in campaigns:
            # ─── Check if student is eligible ──────────────────────────────
            # NULL means "ALL" - so only check if value is not None
            is_eligible = True
            
            if campaign.get("program_id") is not None and campaign["program_id"] != student.get("program_id"):
                is_eligible = False
            if campaign.get("session_id") is not None and campaign["session_id"] != student.get("session_id"):
                is_eligible = False
            if campaign.get("semester") is not None and campaign["semester"] != student.get("semester"):
                is_eligible = False
            if campaign.get("shift_id") is not None and campaign["shift_id"] != student.get("shift_id"):
                is_eligible = False
            
            # ─── Check if paid ──────────────────────────────────────────────
            is_paid = False
            payment_date = ""
            
            paid_students = get_paid_students(campaign["id"])
            for paid in paid_students:
                if paid.get("roll_number") == roll_number:
                    is_paid = True
                    payment_date = paid.get("payment_date", "")
                    break
            
            # Only show if eligible OR already paid
            if not is_eligible and not is_paid:
                continue
            
            campaigns_shown += 1
            
            row = ctk.CTkFrame(self.campaigns_frame)
            row.pack(fill="x", pady=2)
            
            # Campaign Name
            ctk.CTkLabel(row, text=campaign["campaign_name"], width=150).pack(side="left", padx=10)
            
            # Fund
            ctk.CTkLabel(row, text=campaign.get("fund_name", "-"), width=150).pack(side="left", padx=10)
            
            # Amount
            ctk.CTkLabel(
                row, 
                text=f"Rs. {campaign.get('required_amount', 0):,.2f}", 
                width=150
            ).pack(side="left", padx=10)
            
            # Status
            if is_paid:
                status_text = "✅ Paid"
                status_color = "#0f9d58"
                display_text = payment_date
            else:
                status_text = "⏳ Pending"
                status_color = "#db4437"
                display_text = "-"
            
            ctk.CTkLabel(
                row, 
                text=status_text, 
                width=150,
                text_color=status_color
            ).pack(side="left", padx=10)
            
            # Date
            ctk.CTkLabel(row, text=display_text, width=150).pack(side="left", padx=10)
        
        if campaigns_shown == 0:
            ctk.CTkLabel(
                self.campaigns_frame, 
                text="No eligible campaigns found for this student", 
                font=("Arial", 14),
                text_color="gray"
            ).pack(pady=20)
    
    def clear_results(self):
        """Clear search results"""
        self.roll_entry.delete(0, "end")
        for widget in self.student_info.winfo_children():
            widget.destroy()
        for widget in self.campaigns_frame.winfo_children():
            widget.destroy()