# src/views/campaigns/campaign_details.py
import customtkinter as ctk
from tkinter import messagebox
from src.controllers.campaign_controller import (
    get_campaign_summary,
    get_paid_students,
    get_pending_students,
    get_campaign_by_id
)
from src.controllers.student_controller import get_student_by_id


class CampaignDetails(ctk.CTkFrame):
    def __init__(self, master, campaign_id=None):
        super().__init__(master)
        self.campaign_id = campaign_id
        self.create_header()
        self.create_summary_cards()
        self.create_student_lists()
        if campaign_id:
            self.load_campaign_data()
    
    def create_header(self):
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            header, 
            text="📊 Campaign Details", 
            font=("Arial", 24, "bold")
        ).pack(side="left")
        
        self.back_btn = ctk.CTkButton(
            header,
            text="← Back to Campaigns",
            command=self.go_back,
            fg_color="gray",
            width=150
        )
        self.back_btn.pack(side="right", padx=10)
    
    def go_back(self):
        """Go back to campaign list"""
        from src.views.campaigns.campaign_list import CampaignList
        parent = self.master
        while parent:
            if hasattr(parent, 'show_view'):
                parent.show_view(CampaignList)
                break
            parent = parent.master
    
    def create_summary_cards(self):
        """Create summary cards for the campaign"""
        self.summary_frame = ctk.CTkFrame(self)
        self.summary_frame.pack(fill="x", padx=20, pady=10)
    
    def create_student_lists(self):
        """Create tabs for paid and pending students"""
        tabview = ctk.CTkTabview(self)
        tabview.pack(fill="both", expand=True, padx=20, pady=10)
        
        tabview.add("✅ Paid Students")
        tabview.add("⏳ Pending Students")
        
        # Paid Students Tab
        self.paid_frame = ctk.CTkScrollableFrame(tabview.tab("✅ Paid Students"))
        self.paid_frame.pack(fill="both", expand=True)
        
        # Pending Students Tab
        self.pending_frame = ctk.CTkScrollableFrame(tabview.tab("⏳ Pending Students"))
        self.pending_frame.pack(fill="both", expand=True)
    
    def load_campaign_data(self):
        """Load and display campaign data"""
        if not self.campaign_id:
            return
        
        summary = get_campaign_summary(self.campaign_id)
        if not summary:
            messagebox.showerror("Error", "Campaign not found")
            self.go_back()
            return
        
        campaign = summary.get("campaign", {})
        
        # ─── Clear and rebuild summary ──────────────────────────────────
        for widget in self.summary_frame.winfo_children():
            widget.destroy()
        
        # Campaign info
        info_frame = ctk.CTkFrame(self.summary_frame)
        info_frame.pack(fill="x", pady=5)
        
        info_text = (
            f"📋 {campaign.get('campaign_name', '')}\n"
            f"💰 Fund: {campaign.get('fund_name', '-')}\n"
            f"💵 Required: Rs. {campaign.get('required_amount', 0):,.2f}"
        )
        ctk.CTkLabel(
            info_frame, 
            text=info_text, 
            font=("Arial", 14),
            justify="left"
        ).pack(side="left", padx=10, pady=5)
        
        # Statistics Cards
        stats_frame = ctk.CTkFrame(self.summary_frame)
        stats_frame.pack(fill="x", pady=5)
        
        stats = [
            ("👨‍🎓 Total Students", summary.get('total_eligible', 0)),
            ("✅ Paid", summary.get('total_paid', 0)),
            ("⏳ Pending", summary.get('total_pending', 0)),
            ("💰 Collected", f"Rs. {summary.get('total_collected', 0):,.2f}"),
            ("📈 Collection %", f"{summary.get('collection_percent', 0):.1f}%")
        ]
        
        for i, (label, value) in enumerate(stats):
            frame = ctk.CTkFrame(stats_frame)
            frame.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            stats_frame.grid_columnconfigure(i, weight=1)
            
            ctk.CTkLabel(
                frame, 
                text=str(value), 
                font=("Arial", 20, "bold")
            ).pack(pady=5)
            
            ctk.CTkLabel(
                frame, 
                text=label, 
                font=("Arial", 11),
                text_color="gray"
            ).pack(pady=5)
        
        # ─── Load students ──────────────────────────────────────────────
        self.load_paid_students()
        self.load_pending_students()
    
    def load_paid_students(self):
        """Load paid students list"""
        for widget in self.paid_frame.winfo_children():
            widget.destroy()
        
        paid = get_paid_students(self.campaign_id)
        
        if not paid:
            ctk.CTkLabel(
                self.paid_frame, 
                text="No students have paid yet", 
                font=("Arial", 14),
                text_color="gray"
            ).pack(pady=20)
            return
        
        # Headers
        headers = ["Roll No", "Name", "Amount", "Date", "Receipt"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                self.paid_frame, 
                text=header, 
                font=("Arial", 12, "bold"),
                width=150 if i < 2 else 120
            ).grid(row=0, column=i, padx=10, pady=5, sticky="w")
        
        for idx, student in enumerate(paid, 1):
            row_frame = ctk.CTkFrame(self.paid_frame)
            row_frame.grid(row=idx, column=0, columnspan=5, sticky="ew", pady=2)
            
            ctk.CTkLabel(row_frame, text=student.get("roll_number", ""), width=150).pack(side="left", padx=10)
            ctk.CTkLabel(row_frame, text=student.get("student_name", ""), width=150).pack(side="left", padx=10)
            ctk.CTkLabel(
                row_frame, 
                text=f"Rs. {student.get('amount', 0):,.2f}", 
                width=120
            ).pack(side="left", padx=10)
            ctk.CTkLabel(row_frame, text=student.get("payment_date", ""), width=120).pack(side="left", padx=10)
            ctk.CTkLabel(row_frame, text=student.get("receipt_number", ""), width=120).pack(side="left", padx=10)
    
    def load_pending_students(self):
        """Load pending students list"""
        for widget in self.pending_frame.winfo_children():
            widget.destroy()
        
        pending = get_pending_students(self.campaign_id)
        
        if not pending:
            ctk.CTkLabel(
                self.pending_frame, 
                text="All students have paid! 🎉", 
                font=("Arial", 14),
                text_color="#0f9d58"
            ).pack(pady=20)
            return
        
        # Headers
        headers = ["Roll No", "Name", "Program", "Semester"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                self.pending_frame, 
                text=header, 
                font=("Arial", 12, "bold"),
                width=150
            ).grid(row=0, column=i, padx=10, pady=5, sticky="w")
        
        for idx, student in enumerate(pending, 1):
            row_frame = ctk.CTkFrame(self.pending_frame)
            row_frame.grid(row=idx, column=0, columnspan=4, sticky="ew", pady=2)
            
            ctk.CTkLabel(row_frame, text=student.get("roll_number", ""), width=150).pack(side="left", padx=10)
            ctk.CTkLabel(row_frame, text=student.get("student_name", ""), width=150).pack(side="left", padx=10)
            ctk.CTkLabel(row_frame, text=student.get("program_name", ""), width=150).pack(side="left", padx=10)
            ctk.CTkLabel(row_frame, text=str(student.get("semester", "")), width=150).pack(side="left", padx=10)
    
    def refresh(self):
        """Refresh the campaign data"""
        if self.campaign_id:
            self.load_campaign_data()