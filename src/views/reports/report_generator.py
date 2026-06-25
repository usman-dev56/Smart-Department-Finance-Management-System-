# src/views/reports/report_generator.py
import customtkinter as ctk
from tkinter import messagebox, filedialog
import os
from datetime import datetime
from src.controllers.report_controller import (
    get_collection_report,
    get_expense_report,
    get_fund_performance_report,
    get_overall_summary,
    get_daily_summary
)
from src.controllers.department_controller import get_current_department
from src.services.pdf_service import (
    generate_collection_report_pdf,
    generate_expense_report_pdf,
    generate_student_report_pdf
)
from src.services.excel_service import (
    export_payments,
    export_expenses,
    export_report
)
from src.views.reports.charts import Charts


class ReportGenerator(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.create_header()
        self.create_dashboard_cards()
        self.create_tabs()
    
    def create_header(self):
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            header, 
            text="📈 Reports & Analytics", 
            font=("Arial", 33, "bold")
        ).pack(side="left")
        
        ctk.CTkLabel(
            header, 
            text="View reports, charts, and export data", 
            font=("Arial", 20),
            text_color="gray"
        ).pack(side="left", padx=40)
    
    def create_dashboard_cards(self):
        """Create summary cards"""
        cards_frame = ctk.CTkFrame(self)
        cards_frame.pack(fill="x", padx=20, pady=12)
        
        summary = get_overall_summary()
        
        cards = [
            ("👨‍🎓 Total Students", summary.get("total_students", 0), "#1a73e8"),
            ("💰 Total Collection", f"Rs. {summary.get('total_collection', 0):,.2f}", "#0f9d58"),
            ("📤 Total Expenses", f"Rs. {summary.get('total_expenses', 0):,.2f}", "#db4437"),
            ("💵 Balance", f"Rs. {summary.get('balance', 0):,.2f}", "#f4b400"),
            ("📋 Active Campaigns", summary.get("active_campaigns", 0), "#9c27b0"),
            ("💰 Active Funds", summary.get("active_funds", 0), "#00bcd4")
        ]
        
        for i, (label, value, color) in enumerate(cards):
            frame = ctk.CTkFrame(cards_frame, corner_radius=10, fg_color=color)
            frame.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
            cards_frame.grid_columnconfigure(i, weight=1)
            
            ctk.CTkLabel(
                frame, 
                text=str(value), 
                font=("Arial", 20, "bold"),
                text_color="white"
            ).pack(pady=(10, 0))
            
            ctk.CTkLabel(
                frame, 
                text=label, 
                font=("Arial", 11,"bold"),
                text_color="#fffcfc"
            ).pack(pady=(0, 10))
    
    def create_tabs(self):
        """Create report tabs"""
        tabview = ctk.CTkTabview(self)
        tabview.pack(fill="both", expand=True, padx=20, pady=10)
        
        tabview.add("📊 Collection Report")
        tabview.add("📤 Expense Report")
        tabview.add("💰 Fund Performance")
        tabview.add("📈 Charts")
        
        
        # ─── Collection Report Tab ──────────────────────────────────────
        self.create_collection_tab(tabview.tab("📊 Collection Report"))
        
        # ─── Expense Report Tab ──────────────────────────────────────────
        self.create_expense_tab(tabview.tab("📤 Expense Report"))
        
        # ─── Fund Performance Tab ────────────────────────────────────────
        self.create_fund_performance_tab(tabview.tab("💰 Fund Performance"))
        
        # ─── Charts Tab ──────────────────────────────────────────────────
        self.create_charts_tab(tabview.tab("📈 Charts"))
    
    def create_collection_tab(self, parent):
        """Collection report tab"""
        # Filters
        filter_frame = ctk.CTkFrame(parent)
        filter_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(filter_frame, text="Date Range:", font=("Arial", 13)).pack(side="left", padx=5)
        
        self.col_start_date = ctk.CTkEntry(filter_frame, placeholder_text="Start Date", width=120)
        self.col_start_date.pack(side="left", padx=5)
        self.col_start_date.insert(0, datetime.now().strftime("%Y-%m-01"))
        
        ctk.CTkLabel(filter_frame, text="to", font=("Arial", 13)).pack(side="left", padx=5)
        
        self.col_end_date = ctk.CTkEntry(filter_frame, placeholder_text="End Date", width=120)
        self.col_end_date.pack(side="left", padx=5)
        self.col_end_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        self.col_refresh_btn = ctk.CTkButton(
            filter_frame,
            text="🔄 Refresh",
            command=lambda: self.load_collection_report(),
            fg_color="#1a73e8",
            width=100
        )
        self.col_refresh_btn.pack(side="left", padx=10)
        
        self.col_export_pdf_btn = ctk.CTkButton(
            filter_frame,
            text="📄 Export PDF",
            command=self.export_collection_pdf,
            fg_color="#db4437",
            width=100
        )
        self.col_export_pdf_btn.pack(side="left", padx=5)
        
        self.col_export_excel_btn = ctk.CTkButton(
            filter_frame,
            text="📊 Export Excel",
            command=self.export_collection_excel,
            fg_color="#0f9d58",
            width=100
        )
        self.col_export_excel_btn.pack(side="left", padx=5)
        
        # Table
        self.col_table_frame = ctk.CTkScrollableFrame(parent)
        self.col_table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.load_collection_report()
    
    def load_collection_report(self):
        """Load collection report data"""
        for widget in self.col_table_frame.winfo_children():
            widget.destroy()
        
        start_date = self.col_start_date.get()
        end_date = self.col_end_date.get()
        
        data = get_collection_report(start_date=start_date, end_date=end_date)
        
        if not data:
            ctk.CTkLabel(
                self.col_table_frame, 
                text="No collection data found for this period", 
                font=("Arial", 14),
                text_color="gray"
            ).pack(pady=20)
            return
        
        # Headers
        headers = ["Receipt", "Date", "Student", "Roll No", "Campaign", "Fund", "Amount", "Method"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                self.col_table_frame, 
                text=header, 
                font=("Arial", 12, "bold"),
                width=120
            ).grid(row=0, column=i, padx=5, pady=5, sticky="w")
        
        # Data rows
        total = 0
        for idx, row in enumerate(data, 1):
            total += row.get("amount", 0)
            ctk.CTkLabel(self.col_table_frame, text=row.get("receipt_number", "-"), width=120).grid(
                row=idx, column=0, padx=5, pady=2, sticky="w")
            ctk.CTkLabel(self.col_table_frame, text=row.get("payment_date", "-"), width=120).grid(
                row=idx, column=1, padx=5, pady=2, sticky="w")
            ctk.CTkLabel(self.col_table_frame, text=row.get("student_name", "-"), width=120).grid(
                row=idx, column=2, padx=5, pady=2, sticky="w")
            ctk.CTkLabel(self.col_table_frame, text=row.get("roll_number", "-"), width=120).grid(
                row=idx, column=3, padx=5, pady=2, sticky="w")
            ctk.CTkLabel(self.col_table_frame, text=row.get("campaign_name", "-"), width=120).grid(
                row=idx, column=4, padx=5, pady=2, sticky="w")
            ctk.CTkLabel(self.col_table_frame, text=row.get("fund_name", "-"), width=120).grid(
                row=idx, column=5, padx=5, pady=2, sticky="w")
            ctk.CTkLabel(
                self.col_table_frame, 
                text=f"Rs. {row.get('amount', 0):,.2f}", 
                width=120,
                font=("Arial", 11, "bold"),
                text_color="#0f9d58"
            ).grid(row=idx, column=6, padx=5, pady=2, sticky="w")
            ctk.CTkLabel(self.col_table_frame, text=row.get("payment_method", "-"), width=120).grid(
                row=idx, column=7, padx=5, pady=2, sticky="w")
        
        # Total row
        total_row = idx + 1
        ctk.CTkLabel(
            self.col_table_frame, 
            text="TOTAL", 
            font=("Arial", 12, "bold"),
            width=120
        ).grid(row=total_row, column=5, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(
            self.col_table_frame, 
            text=f"Rs. {total:,.2f}", 
            font=("Arial", 12, "bold"),
            text_color="#0f9d58",
            width=120
        ).grid(row=total_row, column=6, padx=5, pady=5, sticky="w")
    
    def export_collection_pdf(self):
        """Export collection report to PDF"""
        data = get_collection_report()
        dept = get_current_department()
        
        if not data:
            messagebox.showerror("Error", "No data to export")
            return
        
        # Format data for PDF
        campaigns_data = []
        for row in data:
            campaigns_data.append({
                "campaign_name": row.get("campaign_name", ""),
                "fund_name": row.get("fund_name", ""),
                "total_collected": row.get("amount", 0)
            })
        
        result = generate_collection_report_pdf(campaigns_data, dept)
        if result:
            messagebox.showinfo("Success", f"PDF exported successfully!\n\nSaved at: {result}")
            os.startfile(result)
        else:
            messagebox.showerror("Error", "Failed to export PDF")
    
    def export_collection_excel(self):
        """Export collection report to Excel"""
        data = get_collection_report()
        if not data:
            messagebox.showerror("Error", "No data to export")
            return
        
        result = export_payments(data)
        if result:
            messagebox.showinfo("Success", f"Excel exported successfully!\n\nSaved at: {result}")
            os.startfile(result)
        else:
            messagebox.showerror("Error", "Failed to export Excel")
    
    def create_expense_tab(self, parent):
        """Expense report tab"""
        filter_frame = ctk.CTkFrame(parent)
        filter_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(filter_frame, text="Date Range:", font=("Arial", 13)).pack(side="left", padx=5)
        
        self.exp_start_date = ctk.CTkEntry(filter_frame, placeholder_text="Start Date", width=120)
        self.exp_start_date.pack(side="left", padx=5)
        self.exp_start_date.insert(0, datetime.now().strftime("%Y-%m-01"))
        
        ctk.CTkLabel(filter_frame, text="to", font=("Arial", 13)).pack(side="left", padx=5)
        
        self.exp_end_date = ctk.CTkEntry(filter_frame, placeholder_text="End Date", width=120)
        self.exp_end_date.pack(side="left", padx=5)
        self.exp_end_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        self.exp_refresh_btn = ctk.CTkButton(
            filter_frame,
            text="🔄 Refresh",
            command=lambda: self.load_expense_report(),
            fg_color="#1a73e8",
            width=100
        )
        self.exp_refresh_btn.pack(side="left", padx=10)
        
        self.exp_export_pdf_btn = ctk.CTkButton(
            filter_frame,
            text="📄 Export PDF",
            command=self.export_expense_pdf,
            fg_color="#db4437",
            width=100
        )
        self.exp_export_pdf_btn.pack(side="left", padx=5)
        
        self.exp_export_excel_btn = ctk.CTkButton(
            filter_frame,
            text="📊 Export Excel",
            command=self.export_expense_excel,
            fg_color="#0f9d58",
            width=100
        )
        self.exp_export_excel_btn.pack(side="left", padx=5)
        
        self.exp_table_frame = ctk.CTkScrollableFrame(parent)
        self.exp_table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.load_expense_report()
    
    def load_expense_report(self):
        """Load expense report data"""
        for widget in self.exp_table_frame.winfo_children():
            widget.destroy()
        
        start_date = self.exp_start_date.get()
        end_date = self.exp_end_date.get()
        
        data = get_expense_report(start_date=start_date, end_date=end_date)
        
        if not data:
            ctk.CTkLabel(
                self.exp_table_frame, 
                text="No expense data found for this period", 
                font=("Arial", 14),
                text_color="gray"
            ).pack(pady=20)
            return
        
        headers = ["ID", "Title", "Fund", "Amount", "Date", "Created By"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                self.exp_table_frame, 
                text=header, 
                font=("Arial", 12, "bold"),
                width=120
            ).grid(row=0, column=i, padx=5, pady=5, sticky="w")
        
        total = 0
        for idx, row in enumerate(data, 1):
            total += row.get("amount", 0)
            ctk.CTkLabel(self.exp_table_frame, text=str(row.get("id", "-")), width=120).grid(
                row=idx, column=0, padx=5, pady=2, sticky="w")
            ctk.CTkLabel(self.exp_table_frame, text=row.get("expense_title", "-"), width=120).grid(
                row=idx, column=1, padx=5, pady=2, sticky="w")
            ctk.CTkLabel(self.exp_table_frame, text=row.get("fund_name", "-"), width=120).grid(
                row=idx, column=2, padx=5, pady=2, sticky="w")
            ctk.CTkLabel(
                self.exp_table_frame, 
                text=f"Rs. {row.get('amount', 0):,.2f}", 
                width=120,
                font=("Arial", 11, "bold"),
                text_color="#db4437"
            ).grid(row=idx, column=3, padx=5, pady=2, sticky="w")
            ctk.CTkLabel(self.exp_table_frame, text=row.get("expense_date", "-"), width=120).grid(
                row=idx, column=4, padx=5, pady=2, sticky="w")
            ctk.CTkLabel(self.exp_table_frame, text=row.get("created_by", "-"), width=120).grid(
                row=idx, column=5, padx=5, pady=2, sticky="w")
        
        total_row = idx + 1
        ctk.CTkLabel(
            self.exp_table_frame, 
            text="TOTAL", 
            font=("Arial", 12, "bold"),
            width=120
        ).grid(row=total_row, column=2, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(
            self.exp_table_frame, 
            text=f"Rs. {total:,.2f}", 
            font=("Arial", 12, "bold"),
            text_color="#db4437",
            width=120
        ).grid(row=total_row, column=3, padx=5, pady=5, sticky="w")
    
    def export_expense_pdf(self):
        """Export expense report to PDF"""
        data = get_expense_report()
        dept = get_current_department()
        
        if not data:
            messagebox.showerror("Error", "No data to export")
            return
        
        result = generate_expense_report_pdf(data, dept)
        if result:
            messagebox.showinfo("Success", f"PDF exported successfully!\n\nSaved at: {result}")
            os.startfile(result)
        else:
            messagebox.showerror("Error", "Failed to export PDF")
    
    def export_expense_excel(self):
        """Export expense report to Excel"""
        data = get_expense_report()
        if not data:
            messagebox.showerror("Error", "No data to export")
            return
        
        result = export_expenses(data)
        if result:
            messagebox.showinfo("Success", f"Excel exported successfully!\n\nSaved at: {result}")
            os.startfile(result)
        else:
            messagebox.showerror("Error", "Failed to export Excel")
    
    def create_fund_performance_tab(self, parent):
        """Fund performance tab"""
        self.fund_table_frame = ctk.CTkScrollableFrame(parent)
        self.fund_table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.load_fund_performance()
    
    def load_fund_performance(self):
        """Load fund performance data"""
        for widget in self.fund_table_frame.winfo_children():
            widget.destroy()
        
        data = get_fund_performance_report()
        
        if not data:
            ctk.CTkLabel(
                self.fund_table_frame, 
                text="No fund data found", 
                font=("Arial", 14),
                text_color="gray"
            ).pack(pady=20)
            return
        
        headers = ["Fund", "Total Collection", "Total Expenses", "Balance", "Status"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                self.fund_table_frame, 
                text=header, 
                font=("Arial", 15, "bold"),
                width=150,
                height=125
            ).grid(row=0, column=i, padx=5, pady=5, sticky="w")
        
        for idx, row in enumerate(data, 1):
            balance = row.get("balance", 0)
            status = "✅ Profitable" if balance > 0 else "❌ Loss" if balance < 0 else "⚖️ Break-even"
            status_color = "#0f9d58" if balance > 0 else "#db4437" if balance < 0 else "#f4b400"
            
            ctk.CTkLabel(self.fund_table_frame, text=row.get("fund_name", "-"), width=150).grid(
                row=idx, column=0, padx=5, pady=2, sticky="w")
            ctk.CTkLabel(
                self.fund_table_frame, 
                text=f"Rs. {row.get('total_collected', 0):,.2f}", 
                width=150
            ).grid(row=idx, column=1, padx=5, pady=2, sticky="w")
            ctk.CTkLabel(
                self.fund_table_frame, 
                text=f"Rs. {row.get('total_expenses', 0):,.2f}", 
                width=150
            ).grid(row=idx, column=2, padx=5, pady=2, sticky="w")
            ctk.CTkLabel(
                self.fund_table_frame, 
                text=f"Rs. {balance:,.2f}", 
                width=150,
                font=("Arial", 11, "bold"),
                text_color="#0f9d58" if balance >= 0 else "#db4437"
            ).grid(row=idx, column=3, padx=5, pady=2, sticky="w")
            ctk.CTkLabel(
                self.fund_table_frame, 
                text=status, 
                width=150,
                text_color=status_color
            ).grid(row=idx, column=4, padx=5, pady=2, sticky="w")
    
    def create_charts_tab(self, parent):
        """Charts tab - uses standalone Charts component"""
        Charts(parent).pack(fill="both", expand=True)