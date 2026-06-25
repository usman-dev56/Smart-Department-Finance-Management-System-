# src/views/funds/fund_list.py
import customtkinter as ctk
from tkinter import messagebox
from src.controllers.fund_controller import (
    get_all_funds, 
    delete_fund, 
    toggle_fund_status,
    get_fund_summary
)


class FundList(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.create_header()
        self.create_table()
        self.load_funds()
    
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="#021635" )
        header.pack(fill="x", padx=10, pady=25)
        
        ctk.CTkLabel(
            header, 
            text=" Fund Management", 
            font=("Arial", 33, "bold")
        ).pack(side="left")
        
        ctk.CTkLabel(
            header, 
            text="Create and manage department funds", 
            font=("Arial", 20),
            text_color="gray"
        ).pack(side="left", padx=50)
        
        # Add Fund Button
        self.add_btn = ctk.CTkButton(
            header,
            text="➕ Add Fund",
            font=("Arial", 15, "bold"),
            command=self.open_fund_creation,
            fg_color="#1a73e8",
            width=120,
            height=50
        )
        self.add_btn.pack(side="right", padx=10, pady=(18, 10))
    
    def open_fund_creation(self):
        """Open fund creation view"""
        from src.views.funds.fund_creation import FundCreation
        parent = self.master
        while parent:
            if hasattr(parent, 'show_view'):
                parent.show_view(FundCreation)
                break
            parent = parent.master
    
    def create_table(self):
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Headers
        headers_frame = ctk.CTkFrame(table_frame, fg_color="#2a2a3d")
        headers_frame.pack(fill="x", pady=(0, 2))
        
        headers = ["ID", "Fund Name", "Description", "Type", "Status", "Actions"]
        widths = [50, 200, 250, 120, 100, 180]
        
        for i, (header, width) in enumerate(zip(headers, widths)):
            ctk.CTkLabel(
                headers_frame, 
                text=header, 
                font=("Arial", 12, "bold"),
                width=width
            ).pack(side="left", padx=10, pady=5)
        
        self.table_body = ctk.CTkScrollableFrame(
            table_frame, 
            fg_color="transparent"
        )
        self.table_body.pack(fill="both", expand=True)
    
    def load_funds(self):
        """Load and display all funds"""
        # Clear table
        for widget in self.table_body.winfo_children():
            widget.destroy()
        
        funds = get_all_funds()
        
        if not funds:
            ctk.CTkLabel(
                self.table_body, 
                text="No funds created yet.\nClick 'Add Fund' to create your first fund!", 
                font=("Arial", 14),
                text_color="gray"
            ).pack(pady=40)
            return
        
        for fund in funds:
            row = ctk.CTkFrame(self.table_body)
            row.pack(fill="x", pady=2)
            
            # ID
            ctk.CTkLabel(row, text=str(fund["id"]), width=50).pack(side="left", padx=10, pady=5)
            
            # Fund Name
            ctk.CTkLabel(
                row, 
                text=fund["fund_name"], 
                width=200, 
                font=("Arial", 13, "bold")
            ).pack(side="left", padx=10, pady=5)
            
            # Description
            desc = fund.get("fund_description", "") or "-"
            desc = desc[:30] + "..." if len(desc) > 30 else desc
            ctk.CTkLabel(row, text=desc, width=250).pack(side="left", padx=10, pady=5)
            
            # Type
            fund_type = fund.get("fund_type", "General")
            ctk.CTkLabel(row, text=fund_type, width=120).pack(side="left", padx=10, pady=5)
            
            # Status
            status_text = "✅ Active" if fund["is_active"] else "❌ Inactive"
            status_color = "#0f9d58" if fund["is_active"] else "#db4437"
            ctk.CTkLabel(
                row, 
                text=status_text, 
                width=100, 
                text_color=status_color
            ).pack(side="left", padx=10, pady=5)
            
            # Actions
            actions_frame = ctk.CTkFrame(row, fg_color="transparent")
            actions_frame.pack(side="right", padx=10, pady=5)
            
            toggle_text = "Deactivate" if fund["is_active"] else "Activate"
            toggle_color = "#db4437" if fund["is_active"] else "#0f9d58"
            ctk.CTkButton(
                actions_frame,
                text=toggle_text,
                command=lambda f=fund: self.toggle_status(f),
                fg_color=toggle_color,
                width=70,
                height=28
            ).pack(side="left", padx=2)
            
            ctk.CTkButton(
                actions_frame,
                text="🗑 Delete",
                command=lambda f=fund: self.delete_fund(f),
                fg_color="#db4437",
                width=70,
                height=28
            ).pack(side="left", padx=2)
    
    def toggle_status(self, fund):
        """Toggle fund active/inactive status"""
        try:
            new_status = toggle_fund_status(fund["id"])
            status_text = "activated" if new_status else "deactivated"
            self.load_funds()
            messagebox.showinfo("Success", f"Fund '{fund['fund_name']}' {status_text} successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def delete_fund(self, fund):
        """Delete a fund"""
        if messagebox.askyesno(
            "Confirm Delete", 
            f"Are you sure you want to delete '{fund['fund_name']}'?\n\n"
            "This will remove the fund from the system.\n"
            "Campaigns linked to this fund will also be affected."
        ):
            try:
                delete_fund(fund["id"])
                self.load_funds()
                messagebox.showinfo("Success", f"Fund '{fund['fund_name']}' deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))