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
        header = ctk.CTkFrame(self, fg_color="#021635")
        header.pack(fill="x", padx=10, pady=25)
        
        ctk.CTkLabel(
            header, 
            text="📋 Campaign Management", 
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
            font=("Arial", 15, "bold"),
            command=self.open_campaign_creation,
            fg_color="#1a73e8",
            hover_color="#1557b0",
            width=150,
            height=42,
            corner_radius=8
        )
        self.add_btn.pack(side="right", padx=10, pady=(18, 10))
    
    def open_campaign_creation(self):
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
        
        headers_frame = ctk.CTkFrame(table_frame, fg_color="#1a1a2e")
        headers_frame.pack(fill="x", pady=(0, 2))
        
        col_widths = [45, 150, 170, 170, 90, 90, 80, 130]
        col_aligns = ["w", "w", "w", "w", "w", "w", "w", "e"]
        col_labels = ["ID", "Campaign", "Fund", "Target", "Amount", "Collected", "Status", "Actions"]
        
        for i, (text, width, align) in enumerate(zip(col_labels, col_widths, col_aligns)):
            ctk.CTkLabel(
                headers_frame, 
                text=text, 
                font=("Arial", 12, "bold"),
                width=width,
                anchor=align,
                text_color="#a0a0b0"
            ).grid(row=0, column=i, padx=3, pady=8, sticky=align)
        
        self.table_body = ctk.CTkScrollableFrame(table_frame, fg_color="transparent")
        self.table_body.pack(fill="both", expand=True)
    
    def load_campaigns(self):
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
            self.create_row(campaign)
    
    def create_row(self, campaign):
        summary = get_campaign_summary(campaign["id"])
        collected = summary.get("total_collected", 0) if summary else 0
        is_active = campaign["is_active"]
        
        row = ctk.CTkFrame(self.table_body, fg_color="transparent")
        row.pack(fill="x", pady=2)
        
        col_widths = [45, 150, 170, 170, 90, 90, 80, 130]
        
        # ─── Column 0: ID ──────────────────────────────────────────────────
        ctk.CTkLabel(
            row, 
            text=str(campaign["id"]), 
            width=col_widths[0],
            anchor="w",
            font=("Arial", 12)
        ).grid(row=0, column=0, padx=3, pady=5, sticky="w")
        
        # ─── Column 1: Campaign Name ──────────────────────────────────────
        camp_name = campaign["campaign_name"]
        name_frame = ctk.CTkFrame(row, fg_color="transparent")
        name_frame.grid(row=0, column=1, padx=3, pady=5, sticky="w")
        
        if len(camp_name) > 10:
            name_display = camp_name[:10] + "..."
            ctk.CTkLabel(
                name_frame, 
                text=name_display, 
                width=col_widths[1] - 50,
                anchor="w",
                font=("Arial", 13, "bold"),
                text_color="#ffffff"
            ).grid(row=0, column=0, padx=(0, 2), sticky="w")
            
            ctk.CTkButton(
                name_frame,
                text="👁",
                command=lambda n=camp_name: messagebox.showinfo("Campaign Name", n),
                fg_color="#1a73e8",
                hover_color="#1557b0",
                text_color="#ffffff",
                width=26,
                height=22,
                corner_radius=6,
                font=("Arial", 10)
            ).grid(row=0, column=1, padx=(0, 23), sticky="w")
        else:
            ctk.CTkLabel(
                name_frame, 
                text=camp_name, 
                width=col_widths[1],
                anchor="w",
                font=("Arial", 13, "bold")
            ).grid(row=0, column=0, padx=0, sticky="w")
        
        # ─── Column 2: Fund ──────────────────────────────────────────────────
        fund_name = campaign.get("fund_name", "-")
        fund_frame = ctk.CTkFrame(row, fg_color="transparent")
        fund_frame.grid(row=0, column=2, padx=3, pady=5, sticky="w")
        
        if len(fund_name) > 10:
            fund_display = fund_name[:13] + "..."
            ctk.CTkLabel(
                fund_frame, 
                text=fund_display, 
                width=col_widths[2] - 50,
                anchor="w",
                font=("Arial", 12),
                text_color="#ffffff"
            ).grid(row=0, column=0, padx=(0, 2), sticky="w")
            
            ctk.CTkButton(
                fund_frame,
                text="👁",
                command=lambda n=fund_name: messagebox.showinfo("Fund Name", n),
                fg_color="#1a73e8",
                hover_color="#1557b0",
                text_color="#ffffff",
                width=26,
                height=22,
                corner_radius=6,
                font=("Arial", 10)
            ).grid(row=0, column=1, padx=(0, 23), sticky="w")
        else:
            ctk.CTkLabel(
                fund_frame, 
                text=fund_name, 
                width=col_widths[2],
                anchor="w",
                font=("Arial", 12)
            ).grid(row=0, column=0, padx=0, sticky="w")
        
        # ─── Column 3: Target ──────────────────────────────────────────────
        target = self.get_target_summary(campaign)
        target_frame = ctk.CTkFrame(row, fg_color="transparent")
        target_frame.grid(row=0, column=3, padx=(3,0), pady=5, sticky="w")
        
        if len(target) > 12:
            target_display = target[:14] + "..."
            ctk.CTkLabel(
                target_frame, 
                text=target_display, 
                width=col_widths[3] - 48,
                anchor="w",
                font=("Arial", 12),
                text_color="#ffffff"
            ).grid(row=0, column=0, padx=(0, 0), sticky="w")
            
            ctk.CTkButton(
                target_frame,
                text="👁",
                command=lambda t=target: messagebox.showinfo("Target Details", t),
                fg_color="#1a73e8",
                hover_color="#1557b0",
                text_color="#ffffff",
                width=26,
                height=22,
                corner_radius=6,
                font=("Arial", 10)
            ).grid(row=0, column=1, padx=(0, 21), sticky="w")
        else:
            ctk.CTkLabel(
                target_frame, 
                text=target, 
                width=col_widths[3],
                anchor="w",
                font=("Arial", 12)
            ).grid(row=0, column=0, padx=0, sticky="w")
        
        # ─── Column 4: Amount ──────────────────────────────────────────────
        amount = campaign.get("required_amount", 0)
        ctk.CTkLabel(
            row, 
            text=f"Rs.{amount:,.0f}", 
            width=col_widths[4],
            font=("Arial", 12, "bold"),
            anchor="w"
        ).grid(row=0, column=4, padx=3, pady=5, sticky="w")
        
        # ─── Column 5: Collected ────────────────────────────────────────────
        ctk.CTkLabel(
            row, 
            text=f"Rs.{collected:,.0f}", 
            width=col_widths[5],
            text_color="#0f9d58",
            font=("Arial", 12, "bold"),
            anchor="w"
        ).grid(row=0, column=5, padx=3, pady=5, sticky="w")
        
        # ─── Column 6: Status ──────────────────────────────────────────────
        status_text = "Active" if is_active else "Inactive"
        status_color = "#0f9d58" if is_active else "#db4437"
        ctk.CTkLabel(
            row, 
            text=status_text, 
            width=col_widths[6],
            text_color=status_color,
            font=("Arial", 11, "bold"),
            anchor="w"
        ).grid(row=0, column=6, padx=3, pady=5, sticky="w")
        
        # ─── Column 7: Actions (RIGHT ALIGNED) ──────────────────────────────
        actions_frame = ctk.CTkFrame(row, fg_color="transparent")
        actions_frame.grid(row=0, column=7, padx=(45,5), pady=5, sticky="e")
        
        # Details - Right aligned
        ctk.CTkButton(
            actions_frame,
            text="📊",
            command=lambda c=campaign: self.view_details(c),
            fg_color="#1a73e8",
            hover_color="#1557b0",
            width=30,
            height=26,
            corner_radius=6,
            font=("Arial", 12)
        ).grid(row=0, column=0, padx=1, sticky="e")
        
        # Toggle Status - Right aligned
        toggle_color = "#db4437" if is_active else "#0f9d58"
        toggle_text = "🔴" if is_active else "🟢"
        ctk.CTkButton(
            actions_frame,
            text=toggle_text,
            command=lambda c=campaign: self.toggle_status(c),
            fg_color=toggle_color,
            hover_color="#b8322a" if is_active else "#0b7e45",
            width=30,
            height=26,
            corner_radius=6,
            font=("Arial", 12)
        ).grid(row=0, column=1, padx=1, sticky="e")
        
        # Delete - Right aligned
        ctk.CTkButton(
            actions_frame,
            text="🗑",
            command=lambda c=campaign: self.delete_campaign(c),
            fg_color="#db4437",
            hover_color="#b8322a",
            width=30,
            height=26,
            corner_radius=6,
            font=("Arial", 12)
        ).grid(row=0, column=2, padx=1, sticky="e")
    
    def get_target_summary(self, campaign):
        parts = []
        if campaign.get("program_id"):
            parts.append(f"Prog:{campaign['program_id']}")
        if campaign.get("session_id"):
            parts.append(f"Sess:{campaign['session_id']}")
        if campaign.get("semester"):
            parts.append(f"Sem:{campaign['semester']}")
        if campaign.get("shift_id"):
            parts.append(f"Shift:{campaign['shift_id']}")
        return ", ".join(parts) if parts else "All Students"
    
    def view_details(self, campaign):
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