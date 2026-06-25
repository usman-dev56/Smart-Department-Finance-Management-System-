# src/views/expenses/add_expense.py
import customtkinter as ctk
from tkinter import messagebox, filedialog
import os
import shutil
from datetime import datetime
from src.controllers.expense_controller import add_expense
from src.controllers.fund_controller import get_active_funds
from src.controllers.department_controller import get_current_department
from src.utils.helpers import today_str


class AddExpense(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.receipt_path = None
        self.create_header()
        self.create_form()
        self.load_dropdowns()
    
    def create_header(self):
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            header, 
            text="📤 Add Expense", 
            font=("Arial", 24, "bold")
        ).pack(side="left")
        
        ctk.CTkLabel(
            header, 
            text="Record department expenses", 
            font=("Arial", 12),
            text_color="gray"
        ).pack(side="left", padx=20)
    
    def create_form(self):
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # ─── Row 1: Expense Title ──────────────────────────────────────
        ctk.CTkLabel(form_frame, text="Expense Title *", font=("Arial", 13)).grid(
            row=0, column=0, padx=10, pady=10, sticky="w")
        self.title_entry = ctk.CTkEntry(
            form_frame, 
            width=400, 
            placeholder_text="e.g., Lab Equipment Purchase"
        )
        self.title_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # ─── Row 2: Fund ────────────────────────────────────────────────
        ctk.CTkLabel(form_frame, text="Fund *", font=("Arial", 13)).grid(
            row=1, column=0, padx=10, pady=10, sticky="w")
        self.fund_combo = ctk.CTkComboBox(form_frame, width=400, values=["Loading..."])
        self.fund_combo.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # ─── Row 3: Amount ──────────────────────────────────────────────
        ctk.CTkLabel(form_frame, text="Amount (Rs.) *", font=("Arial", 13)).grid(
            row=2, column=0, padx=10, pady=10, sticky="w")
        self.amount_entry = ctk.CTkEntry(
            form_frame, 
            width=400, 
            placeholder_text="e.g., 5000"
        )
        self.amount_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        # ─── Row 4: Description ──────────────────────────────────────────
        ctk.CTkLabel(form_frame, text="Description", font=("Arial", 13)).grid(
            row=3, column=0, padx=10, pady=10, sticky="w")
        self.desc_entry = ctk.CTkTextbox(form_frame, width=400, height=80)
        self.desc_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        
        # ─── Row 5: Date ────────────────────────────────────────────────
        ctk.CTkLabel(form_frame, text="Date", font=("Arial", 13)).grid(
            row=4, column=0, padx=10, pady=10, sticky="w")
        self.date_entry = ctk.CTkEntry(
            form_frame, 
            width=400, 
            placeholder_text="YYYY-MM-DD (Leave empty for today)"
        )
        self.date_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        self.date_entry.insert(0, today_str())
        
        # ─── Row 6: Receipt Upload ──────────────────────────────────────
        ctk.CTkLabel(form_frame, text="Receipt Image", font=("Arial", 13)).grid(
            row=5, column=0, padx=10, pady=10, sticky="w")
        
        upload_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        upload_frame.grid(row=5, column=1, padx=10, pady=10, sticky="w")
        
        self.upload_btn = ctk.CTkButton(
            upload_frame,
            text="📎 Upload Receipt",
            command=self.upload_receipt,
            fg_color="#1a73e8",
            width=120
        )
        self.upload_btn.pack(side="left", padx=5)
        
        self.receipt_label = ctk.CTkLabel(
            upload_frame, 
            text="No file selected", 
            text_color="gray"
        )
        self.receipt_label.pack(side="left", padx=10)
        
        # ─── Submit Button ─────────────────────────────────────────────
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=6, column=0, columnspan=2, pady=30)
        
        self.submit_btn = ctk.CTkButton(
            btn_frame, 
            text="✅ Add Expense", 
            command=self.add_expense,
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
        """Load funds into dropdown"""
        try:
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
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load funds: {e}")
    
    def upload_receipt(self):
        """Upload receipt image"""
        file_path = filedialog.askopenfilename(
            title="Select Receipt Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("PDF files", "*.pdf"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.receipt_path = file_path
            filename = os.path.basename(file_path)
            self.receipt_label.configure(text=f"✅ {filename}", text_color="#0f9d58")
    
    def go_back(self):
        """Go back to expense list"""
        from src.views.expenses.expense_list import ExpenseList
        parent = self.master
        while parent:
            if hasattr(parent, 'show_view'):
                parent.show_view(ExpenseList)
                break
            parent = parent.master
    
    def add_expense(self):
        """Add expense"""
        title = self.title_entry.get().strip()
        fund_name = self.fund_combo.get()
        amount = self.amount_entry.get().strip()
        description = self.desc_entry.get("1.0", "end-1c").strip()
        expense_date = self.date_entry.get().strip()
        
        # ─── Validate ──────────────────────────────────────────────────
        if not title:
            messagebox.showerror("Error", "Expense title is required")
            return
        
        if fund_name in ["Loading...", "No funds found"]:
            messagebox.showerror("Error", "Please select a valid fund")
            return
        
        if not amount:
            messagebox.showerror("Error", "Amount is required")
            return
        
        try:
            amount = float(amount)
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")
            return
        
        # Get fund ID
        funds = get_active_funds()
        fund_id = next((f["id"] for f in funds if f["fund_name"] == fund_name), None)
        
        if not fund_id:
            messagebox.showerror("Error", "Invalid fund selected")
            return
        
        # Handle receipt upload
        receipt_path = None
        if self.receipt_path:
            try:
                # Create receipts directory
                receipt_dir = os.path.join("data", "receipts", "expenses")
                os.makedirs(receipt_dir, exist_ok=True)
                
                # Copy file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                ext = os.path.splitext(self.receipt_path)[1]
                filename = f"expense_{timestamp}{ext}"
                dest_path = os.path.join(receipt_dir, filename)
                shutil.copy2(self.receipt_path, dest_path)
                receipt_path = dest_path
            except Exception as e:
                messagebox.showerror("Error", f"Failed to upload receipt: {e}")
                return
        
        # Prepare data
        expense_data = {
            "expense_title": title,
            "fund_id": fund_id,
            "amount": amount,
            "expense_description": description,
            "expense_date": expense_date or today_str(),
            "created_by": "Admin",
            "department_id": 1
        }
        
        try:
            expense_id = add_expense(expense_data)
            
            # Update receipt path if uploaded
            if receipt_path:
                db = get_db()
                db.execute(
                    "UPDATE expenses SET receipt_image_path = ? WHERE id = ?",
                    (receipt_path, expense_id)
                )
            
            messagebox.showinfo(
                "Success", 
                f"✅ Expense added successfully!\n\n"
                f"Title: {title}\n"
                f"Fund: {fund_name}\n"
                f"Amount: Rs. {amount:,.2f}"
            )
            
            self.clear_form()
            self.go_back()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add expense: {e}")
    
    def clear_form(self):
        """Clear all form fields"""
        self.title_entry.delete(0, "end")
        self.amount_entry.delete(0, "end")
        self.desc_entry.delete("1.0", "end")
        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, today_str())
        self.receipt_label.configure(text="No file selected", text_color="gray")
        self.receipt_path = None