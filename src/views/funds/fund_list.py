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
        header = ctk.CTkFrame(self, fg_color="#021635")
        header.pack(fill="x", padx=10, pady=25)
        
        ctk.CTkLabel(
            header, 
            text="💰 Fund Management", 
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
            hover_color="#1557b0",
            width=130,
            height=42,
            corner_radius=8
        )
        self.add_btn.pack(side="right", padx=10, pady=(18, 10))
    
    def open_fund_creation(self):
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
        
        # ─── Headers ──────────────────────────────────────────────────────────
        headers_frame = ctk.CTkFrame(table_frame, fg_color="#1a1a2e")
        headers_frame.pack(fill="x", pady=(0, 2))
        
        # Column configurations: (text, width, align)
        columns = [
            ("ID", 50, "s"),
            ("Fund Name", 180, "s"),
            ("Description", 250, "s"),
            ("Type", 100, "s"),
            ("Status", 100, "s"),
            ("Actions", 310, "s")
        ]
        
        for i, (text, width, align) in enumerate(columns):
            ctk.CTkLabel(
                headers_frame, 
                text=text, 
                font=("Arial", 12, "bold"),
                width=width,
                anchor=align,
                text_color="#a0a0b0"
            ).grid(row=0, column=i, padx=5, pady=8, sticky=align)
        
        # ─── Table Body ──────────────────────────────────────────────────────
        self.table_body = ctk.CTkScrollableFrame(
            table_frame, 
            fg_color="transparent"
        )
        self.table_body.pack(fill="both", expand=True)
    
    def load_funds(self):
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
            self.create_row(fund)
    
    def create_row(self, fund):
        """Create a row with perfect alignment using grid"""
        row = ctk.CTkFrame(self.table_body, fg_color="transparent")
        row.pack(fill="x", pady=2)
        
        # Column widths (must match headers)
        col_widths = [50, 180, 250, 100, 100, 310]
        aligns = ["s", "s", "s", "s", "s", "s"]
        
        # ─── Column 0: ID ──────────────────────────────────────────────────
        ctk.CTkLabel(
            row, 
            text=str(fund["id"]), 
            width=col_widths[0],
            anchor=aligns[0]
        ).grid(row=0, column=0, padx=5, pady=5, sticky=aligns[0])
        
        # ─── Column 1: Fund Name ──────────────────────────────────────────
        ctk.CTkLabel(
            row, 
            text=fund["fund_name"], 
            width=col_widths[1],
            font=("Arial", 13, "bold"),
            anchor=aligns[1]
        ).grid(row=0, column=1, padx=5, pady=5, sticky=aligns[1])
        
       # ─── Column 2: Description ──────────────────────────────────────────
        desc = fund.get("fund_description", "") or "-"

        desc_frame = ctk.CTkFrame(row, fg_color="transparent")
        desc_frame.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        if len(desc) > 25:
            desc_display = desc[:25] + "..."
            
            # Description label - takes all available space
            ctk.CTkLabel(
                desc_frame, 
                text=desc_display, 
                width=col_widths[2] - 60,  # Leave space for View button
                anchor="w",
                text_color="#4fc3f7"
            ).pack(side="left")
            
            # View button - sits right after the text
            ctk.CTkButton(
                desc_frame,
                text="View",
                command=lambda d=desc, name=fund["fund_name"]: self.view_description(d, name),
                fg_color="transparent",
                hover_color="#1a3a6b",
                width=45,
                height=24,
                text_color="#4ff7f7",
                font=("Arial", 10)
            ).pack(side="left", padx=(2, 0))
        else:
            # No View button needed - full width
            ctk.CTkLabel(
                desc_frame, 
                text=desc, 
                width=col_widths[2],
                anchor="w"
            ).pack(side="left")

            
        
        # ─── Column 3: Type ──────────────────────────────────────────────────
        fund_type = fund.get("fund_type", "General")
        ctk.CTkLabel(
            row, 
            text=fund_type, 
            width=col_widths[3],
            anchor=aligns[3]
        ).grid(row=0, column=3, padx=5, pady=5, sticky=aligns[3])
        
        # ─── Column 4: Status ──────────────────────────────────────────────
        status_text = "Active" if fund["is_active"] else "Inactive"
        status_color = "#0f9d58" if fund["is_active"] else "#db4437"
        ctk.CTkLabel(
            row, 
            text=status_text, 
            width=col_widths[4],
            anchor=aligns[4],
            text_color=status_color,
            font=("Arial", 11, "bold")
        ).grid(row=0, column=4, padx=5, pady=5, sticky=aligns[4])
        
        # ─── Column 5: Actions ──────────────────────────────────────────────
        actions_frame = ctk.CTkFrame(row, fg_color="transparent")
        actions_frame.grid(row=0, column=5, padx=5, pady=5, sticky="e")
        
        # Details Button
        ctk.CTkButton(
            actions_frame,
            text="📊 Details",
            command=lambda f=fund: self.view_fund_details(f),
            fg_color="#1a73e8",
            hover_color="#1557b0",
            width=80,
            height=30,
            corner_radius=6,
            font=("Arial", 11)
        ).pack(side="left", padx=2)
        
        # Toggle Status Button
        if fund["is_active"]:
            toggle_text = "🔴 Deactivate"
            toggle_color = "#db4437"
            hover_color = "#b8322a"
        else:
            toggle_text = "🟢 Activate"
            toggle_color = "#0f9d58"
            hover_color = "#0b7e45"
        
        ctk.CTkButton(
            actions_frame,
            text=toggle_text,
            command=lambda f=fund: self.toggle_status(f),
            fg_color=toggle_color,
            hover_color=hover_color,
            width=100,
            height=30,
            corner_radius=6,
            font=("Arial", 11)
        ).pack(side="left", padx=2)
        
        # Delete Button
        ctk.CTkButton(
            actions_frame,
            text="🗑 Delete",
            command=lambda f=fund: self.delete_fund(f),
            fg_color="#db4437",
            hover_color="#b8322a",
            width=80,
            height=30,
            corner_radius=6,
            font=("Arial", 11)
        ).pack(side="left", padx=2)
    
    def view_description(self, description, fund_name):
        messagebox.showinfo(
            f" Fund Description",
            f" {fund_name}\n\n{description}"
        )
    
    def view_fund_details(self, fund):
        try:
            summary = get_fund_summary(fund["id"])
            
            details = (
                f"   Fund: {fund['fund_name']}\n"
                f"   Description: {fund.get('fund_description', 'N/A')}\n"
                f"   Type: {fund.get('fund_type', 'General')}\n"
                f"   Status: {'Active' if fund['is_active'] else 'Inactive'}\n"
            )
            
            if summary:
                details += (
                    f"\n  Financial Summary:\n"
                    f"      Total Collected: Rs. {summary.get('total_collected', 0):,.2f}\n"
                    f"      Total Expenses: Rs. {summary.get('total_expenses', 0):,.2f}\n"
                    f"      Balance: Rs. {summary.get('balance', 0):,.2f}\n"
                    f"      Campaigns: {len(summary.get('campaigns', []))}"
                )
            
            messagebox.showinfo(f"Fund Details: {fund['fund_name']}", details)
            
        except Exception:
            messagebox.showinfo(
                f" Fund Details: {fund['fund_name']}",
                f" Fund: {fund['fund_name']}\n"
                f" Description: {fund.get('fund_description', 'N/A')}\n"
                f" Type: {fund.get('fund_type', 'General')}\n"
                f" Status: {'Active' if fund['is_active'] else 'Inactive'}"
            )
    
    def toggle_status(self, fund):
        try:
            new_status = toggle_fund_status(fund["id"])
            status_text = "activated" if new_status else "deactivated"
            self.load_funds()
            messagebox.showinfo("Success", f"Fund '{fund['fund_name']}' {status_text} successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def delete_fund(self, fund):
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