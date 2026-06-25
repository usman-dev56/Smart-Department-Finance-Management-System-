# src/views/expenses/expense_list.py
import customtkinter as ctk
from tkinter import messagebox
import os
from src.controllers.expense_controller import (
    get_all_expenses,
    delete_expense,
    get_expense_by_id
)
from src.controllers.fund_controller import get_active_funds


class ExpenseList(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.create_header()
        self.create_filters()
        self.create_table()
        self.load_expenses()
    
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="#021635")
        header.pack(fill="x", padx=10, pady=25)
        
        ctk.CTkLabel(
            header, 
            text=" Expense Management", 
           font=("Arial", 33, "bold"),
        ).pack(side="left")
        
        ctk.CTkLabel(
            header, 
            text="Track and manage department expenses", 
            font=("Arial", 20),
            text_color="gray"
        ).pack(side="left", padx=50)
        
        # Add Expense Button
        self.add_btn = ctk.CTkButton(
            header,
            text="➕ Add Expense",
            font=("Arial", 15, "bold"),
            command=self.open_add_expense,
            fg_color="#1a73e8",
            width=130,
            height=50
        )
        self.add_btn.pack(side="right", padx=10, pady=(18, 10))
    
    def create_filters(self):
        """Filter by fund"""
        filter_frame = ctk.CTkFrame(self)
        filter_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            filter_frame, 
            text="Filter by Fund:", 
            font=("Arial", 13, "bold")
        ).pack(side="left", padx=5)
        
        self.fund_filter = ctk.CTkComboBox(
            filter_frame,
            values=["All Funds"],
            width=200
        )
        self.fund_filter.set("All Funds")
        self.fund_filter.pack(side="left", padx=5)
        self.fund_filter.bind("<<ComboboxSelected>>", self.apply_filter)
        
        self.filter_btn = ctk.CTkButton(
            filter_frame,
            text="🔄 Apply Filter",
            command=self.apply_filter,
            fg_color="#0f9d58",
            width=120
        )
        self.filter_btn.pack(side="left", padx=10)
        
        # Total
        self.total_label = ctk.CTkLabel(
            filter_frame,
            text="Total Expenses: Rs. 0.00",
            font=("Arial", 13, "bold"),
            text_color="#db4437"
        )
        self.total_label.pack(side="right", padx=10)
        
        self.load_filter_options()
    
    def load_filter_options(self):
        """Load funds into filter dropdown"""
        try:
            funds = get_active_funds()
            fund_names = ["All Funds"] + [f["fund_name"] for f in funds] if funds else ["All Funds"]
            self.fund_filter.configure(values=fund_names)
            self.fund_filter.set("All Funds")
        except Exception as e:
            print(f"Error loading filters: {e}")
    
    def apply_filter(self, event=None):
        """Apply fund filter"""
        fund_name = self.fund_filter.get()
        self.load_expenses(fund_name)
    
    def create_table(self):
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        headers_frame = ctk.CTkFrame(table_frame, fg_color="#2a2a3d")
        headers_frame.pack(fill="x", pady=(0, 2))
        
        headers = ["ID", "Title", "Fund", "Amount", "Date", "Created By", "Actions"]
        widths = [40, 200, 150, 100, 120, 120, 150]
        
        for i, (header, width) in enumerate(zip(headers, widths)):
            ctk.CTkLabel(
                headers_frame, 
                text=header, 
                font=("Arial", 12, "bold"),
                width=width
            ).pack(side="left", padx=5, pady=5)
        
        self.table_body = ctk.CTkScrollableFrame(table_frame, fg_color="transparent")
        self.table_body.pack(fill="both", expand=True)
    
    def load_expenses(self, fund_name=None):
        """Load expenses with optional fund filter"""
        for widget in self.table_body.winfo_children():
            widget.destroy()
        
        expenses = get_all_expenses()
        
        # Apply fund filter
        if fund_name and fund_name != "All Funds":
            expenses = [e for e in expenses if e.get("fund_name") == fund_name]
        
        # Calculate total
        total = sum(e.get("amount", 0) for e in expenses)
        self.total_label.configure(text=f"Total Expenses: Rs. {total:,.2f}")
        
        if not expenses:
            ctk.CTkLabel(
                self.table_body, 
                text="No expenses found.\nClick 'Add Expense' to record your first expense!", 
                font=("Arial", 14),
                text_color="gray"
            ).pack(pady=40)
            return
        
        for expense in expenses:
            self.create_row(expense)
    
    def create_row(self, expense):
        row = ctk.CTkFrame(self.table_body)
        row.pack(fill="x", pady=2)
        
        # ID
        ctk.CTkLabel(row, text=str(expense["id"]), width=40).pack(side="left", padx=5, pady=5)
        
        # Title
        ctk.CTkLabel(row, text=expense["expense_title"], width=200).pack(side="left", padx=5, pady=5)
        
        # Fund
        ctk.CTkLabel(row, text=expense.get("fund_name", "-"), width=150).pack(side="left", padx=5, pady=5)
        
        # Amount
        ctk.CTkLabel(
            row, 
            text=f"Rs. {expense['amount']:,.2f}", 
            width=100,
            font=("Arial", 11, "bold"),
            text_color="#db4437"
        ).pack(side="left", padx=5, pady=5)
        
        # Date
        ctk.CTkLabel(row, text=expense.get("expense_date", "-"), width=120).pack(side="left", padx=5, pady=5)
        
        # Created By
        ctk.CTkLabel(row, text=expense.get("created_by", "-"), width=120).pack(side="left", padx=5, pady=5)
        
        # Actions
        actions_frame = ctk.CTkFrame(row, fg_color="transparent")
        actions_frame.pack(side="right", padx=5, pady=5)
        
        # View Receipt
        if expense.get("receipt_image_path"):
            ctk.CTkButton(
                actions_frame,
                text="📄",
                command=lambda e=expense: self.view_receipt(e),
                fg_color="#1a73e8",
                width=30,
                height=28
            ).pack(side="left", padx=2)
        
        # Delete
        ctk.CTkButton(
            actions_frame,
            text="🗑",
            command=lambda e=expense: self.delete_expense(e),
            fg_color="#db4437",
            width=30,
            height=28
        ).pack(side="left", padx=2)
    
    def view_receipt(self, expense):
        """View receipt image"""
        path = expense.get("receipt_image_path")
        if path and os.path.exists(path):
            os.startfile(path)
        else:
            messagebox.showinfo("Info", "Receipt file not found")
    
    def delete_expense(self, expense):
        """Delete expense"""
        if messagebox.askyesno(
            "Confirm Delete", 
            f"Are you sure you want to delete this expense?\n\n"
            f"Title: {expense['expense_title']}\n"
            f"Amount: Rs. {expense['amount']:,.2f}"
        ):
            try:
                delete_expense(expense["id"])
                self.apply_filter()
                messagebox.showinfo("Success", "Expense deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def open_add_expense(self):
        """Open add expense view"""
        from src.views.expenses.add_expense import AddExpense
        parent = self.master
        while parent:
            if hasattr(parent, 'show_view'):
                parent.show_view(AddExpense)
                break
            parent = parent.master