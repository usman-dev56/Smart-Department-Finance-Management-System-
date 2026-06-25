# src/views/campaigns/campaign_list.py
import customtkinter as ctk
from tkinter import messagebox
from src.controllers.campaign_controller import (
    get_all_campaigns,
    get_campaign_summary,
    deactivate_campaign,
    activate_campaign,
    delete_campaign
)


class CampaignList(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.create_header()
        self.create_table()
        self.load_campaigns()
    
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="#021635" )
        header.pack(fill="x", padx=10, pady=25)
        
        ctk.CTkLabel(
            header, 
            text=" Campaign Management", 
            font=("Arial", 33, "bold")
        ).pack(side="left")
        
        ctk.CTkLabel(
            header, 
            text="Create and manage collection campaigns", 
            font=("Arial", 20),
            text_color="gray"
        ).pack(side="left", padx=50)
        
        # Add Campaign Button
        self.add_btn = ctk.CTkButton(
            header,
            text="➕ Add Campaign",
            command=self.open_campaign_creation,
            fg_color="#1a73e8",
            width=140
        )
        self.add_btn.pack(side="right", padx=10)
    
    def open_campaign_creation(self):
        """Open campaign creation view"""
        from src.views.campaigns.create_campaign import CreateCampaign
        parent = self.master
        while parent:
            if hasattr(parent, 'show_view'):
                parent.show_view(CreateCampaign)
                break
            parent = parent.master
    
    def create_table(self):
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Headers
        headers_frame = ctk.CTkFrame(table_frame, fg_color="#2a2a3d")
        headers_frame.pack(fill="x", pady=(0, 2))
        
        headers = ["ID", "Campaign", "Fund", "Target", "Amount", "Collected", "Status", "Actions"]
        widths = [40, 160, 140, 150, 80, 100, 80, 180]
        
        for i, (header, width) in enumerate(zip(headers, widths)):
            ctk.CTkLabel(
                headers_frame, 
                text=header, 
                font=("Arial", 12, "bold"),
                width=width
            ).pack(side="left", padx=5, pady=5)
        
        self.table_body = ctk.CTkScrollableFrame(
            table_frame, 
            fg_color="transparent"
        )
        self.table_body.pack(fill="both", expand=True)
    
    def load_campaigns(self):
        """Load and display all campaigns"""
        for widget in self.table_body.winfo_children():
            widget.destroy()
        
        campaigns = get_all_campaigns()
        
        if not campaigns:
            ctk.CTkLabel(
                self.table_body, 
                text="No campaigns created yet.\nClick 'Add Campaign' to create your first campaign!", 
                font=("Arial", 14),
                text_color="gray"
            ).pack(pady=40)
            return
        
        for campaign in campaigns:
            # Get summary
            summary = get_campaign_summary(campaign["id"])
            if summary:
                eligible = summary.get("total_eligible", 0)
                paid = summary.get("total_paid", 0)
                collected = summary.get("total_collected", 0)
            else:
                eligible = 0
                paid = 0
                collected = 0
            
            row = ctk.CTkFrame(self.table_body)
            row.pack(fill="x", pady=2)
            
            # ID
            ctk.CTkLabel(row, text=str(campaign["id"]), width=40).pack(side="left", padx=5, pady=5)
            
            # Campaign Name
            ctk.CTkLabel(
                row, 
                text=campaign["campaign_name"], 
                width=160, 
                font=("Arial", 13, "bold")
            ).pack(side="left", padx=5, pady=5)
            
            # Fund
            ctk.CTkLabel(row, text=campaign.get("fund_name", "-"), width=140).pack(side="left", padx=5, pady=5)
            
            # Target
            target = self.get_target_summary(campaign)
            ctk.CTkLabel(row, text=target, width=150, font=("Arial", 10)).pack(side="left", padx=5, pady=5)
            
            # Amount
            amount = campaign.get("required_amount", 0)
            ctk.CTkLabel(
                row, 
                text=f"Rs. {amount:,.0f}", 
                width=80,
                font=("Arial", 11, "bold")
            ).pack(side="left", padx=5, pady=5)
            
            # Collected
            ctk.CTkLabel(
                row, 
                text=f"Rs. {collected:,.0f}", 
                width=100,
                text_color="#0f9d58",
                font=("Arial", 11)
            ).pack(side="left", padx=5, pady=5)
            
            # Status
            status_text = "✅ Active" if campaign["is_active"] else "❌ Inactive"
            status_color = "#0f9d58" if campaign["is_active"] else "#db4437"
            ctk.CTkLabel(
                row, 
                text=status_text, 
                width=80,
                text_color=status_color
            ).pack(side="left", padx=5, pady=5)
            
            # Actions
            actions_frame = ctk.CTkFrame(row, fg_color="transparent")
            actions_frame.pack(side="right", padx=5, pady=5)
            
            # View Details
            ctk.CTkButton(
                actions_frame,
                text="📊 Details",
                command=lambda c=campaign: self.view_details(c),
                fg_color="#1a73e8",
                width=65,
                height=28
            ).pack(side="left", padx=2)
            
            # Toggle Status
            toggle_text = "Deactivate" if campaign["is_active"] else "Activate"
            toggle_color = "#db4437" if campaign["is_active"] else "#0f9d58"
            ctk.CTkButton(
                actions_frame,
                text=toggle_text,
                command=lambda c=campaign: self.toggle_status(c),
                fg_color=toggle_color,
                width=70,
                height=28
            ).pack(side="left", padx=2)
            
            # Delete
            ctk.CTkButton(
                actions_frame,
                text="🗑",
                command=lambda c=campaign: self.delete_campaign(c),
                fg_color="#db4437",
                width=35,
                height=28
            ).pack(side="left", padx=2)
    
    def get_target_summary(self, campaign):
        """Get target summary for a campaign"""
        parts = []
        
        if campaign.get("program_id"):
            parts.append(f"Program ID: {campaign['program_id']}")
        if campaign.get("session_id"):
            parts.append(f"Session ID: {campaign['session_id']}")
        if campaign.get("semester"):
            parts.append(f"Sem {campaign['semester']}")
        if campaign.get("shift_id"):
            parts.append(f"Shift ID: {campaign['shift_id']}")
        
        return ", ".join(parts) if parts else "All Students"
    
    def view_details(self, campaign):
        """Show campaign details"""
        summary = get_campaign_summary(campaign["id"])
        if not summary:
            messagebox.showerror("Error", "Could not load campaign details")
            return
        
        messagebox.showinfo(
            f"📊 Campaign Details: {campaign['campaign_name']}",
            f"📋 Campaign: {campaign['campaign_name']}\n"
            f"💰 Fund: {campaign.get('fund_name', '-')}\n"
            f"💵 Required Amount: Rs. {campaign.get('required_amount', 0):,.2f}\n"
            f"\n📊 Collection Summary:\n"
            f"   Total Students: {summary.get('total_eligible', 0)}\n"
            f"   ✅ Paid: {summary.get('total_paid', 0)}\n"
            f"   ⏳ Pending: {summary.get('total_pending', 0)}\n"
            f"   💰 Collected: Rs. {summary.get('total_collected', 0):,.2f}\n"
            f"   📈 Collection: {summary.get('collection_percent', 0):.1f}%"
        )
    
    def toggle_status(self, campaign):
        """Toggle campaign active/inactive status"""
        try:
            if campaign["is_active"]:
                deactivate_campaign(campaign["id"])
                status = "deactivated"
            else:
                activate_campaign(campaign["id"])
                status = "activated"
            
            self.load_campaigns()
            messagebox.showinfo("Success", f"Campaign '{campaign['campaign_name']}' {status} successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def delete_campaign(self, campaign):
        """Delete a campaign"""
        if messagebox.askyesno(
            "Confirm Delete", 
            f"Are you sure you want to delete '{campaign['campaign_name']}'?\n\n"
            "This will remove the campaign and all its payment records."
        ):
            try:
                delete_campaign(campaign["id"])
                self.load_campaigns()
                messagebox.showinfo("Success", f"Campaign '{campaign['campaign_name']}' deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))