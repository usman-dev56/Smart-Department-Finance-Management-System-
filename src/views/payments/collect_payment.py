# src/views/payments/collect_payment.py
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from src.controllers.student_controller import get_student_by_roll
from src.controllers.payment_controller import (
    collect_payment,
    get_campaign_eligible_for_student,
    get_payment_by_receipt
)
from src.controllers.campaign_controller import get_campaign_by_id


class CollectPayment(ctk.CTkFrame):
    def __init__(self, master, student_id=None):
        super().__init__(master)
        self.student = None
        self.selected_campaign = None
        self.student_id = student_id 
        self.create_header()
        self.create_search_section()
        self.create_student_info()
        self.create_campaign_selection()
        self.create_payment_form()
          
        if student_id:
           self.load_student_by_id(student_id)


    def load_student_by_id(self, student_id):
        """Load student by ID (used when coming from student list)"""
        from src.controllers.student_controller import get_student_by_id
        
        student = get_student_by_id(student_id)
        if student:
            self.student = student
            self.student_label.configure(
                text=f"👨‍🎓 {student['student_name']} | Roll: {student['roll_number']}",
                text_color="white"
            )
            self.roll_entry.delete(0, "end")
            self.roll_entry.insert(0, student["roll_number"])
            self.load_campaigns()
    
    def create_header(self):
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=10, pady=25)
        
        ctk.CTkLabel(
            header, 
            text="💳 Collect Payment", 
            font=("Arial", 30, "bold")
        ).pack(side="left")
        
        ctk.CTkLabel(
            header, 
            text="Collect payments from students and generate receipts", 
            font=("Arial", 20),
            text_color="gray"
        ).pack(side="left", padx=50)
    
    def create_search_section(self):
        """Search student by roll number"""
        search_frame = ctk.CTkFrame(self)
        search_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            search_frame, 
            text="Enter Roll Number:", 
            font=("Arial", 14, "bold")
        ).pack(side="left", padx=10)
        
        self.roll_entry = ctk.CTkEntry(
            search_frame, 
            placeholder_text="e.g., BSCS-2024-001",
            width=250
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
            command=self.clear_all,
            fg_color="gray",
            width=80
        )
        self.clear_btn.pack(side="left", padx=10)
    
    def create_student_info(self):
        """Display student information"""
        self.student_frame = ctk.CTkFrame(self)
        self.student_frame.pack(fill="x", padx=20, pady=10)
        
        self.student_label = ctk.CTkLabel(
            self.student_frame, 
            text="No student selected", 
            font=("Arial", 14),
            text_color="gray"
        )
        self.student_label.pack(pady=10)
    
    def create_campaign_selection(self):
        """Campaign selection dropdown"""
        campaign_frame = ctk.CTkFrame(self)
        campaign_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            campaign_frame, 
            text="Select Campaign:", 
            font=("Arial", 14, "bold")
        ).pack(side="left", padx=10)
        
        self.campaign_combo = ctk.CTkComboBox(
            campaign_frame, 
            values=["Search student first"],
            width=350
        )
        self.campaign_combo.set("Search student first")
        self.campaign_combo.pack(side="left", padx=10)
        
        # Campaign info
        self.campaign_info = ctk.CTkLabel(
            campaign_frame, 
            text="", 
            font=("Arial", 12),
            text_color="gray"
        )
        self.campaign_info.pack(side="left", padx=20)
    
    def create_payment_form(self):
        """Payment form with amount and method"""
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="x", padx=20, pady=10)
        
        # Amount
        ctk.CTkLabel(
            form_frame, 
            text="Amount (Rs.):", 
            font=("Arial", 14, "bold")
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.amount_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Enter amount",
            width=200
        )
        self.amount_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Payment Method
        ctk.CTkLabel(
            form_frame, 
            text="Payment Method:", 
            font=("Arial", 14, "bold")
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.method_combo = ctk.CTkComboBox(
            form_frame, 
            values=["Cash", "Bank Transfer", "Online Payment", "Cheque"],
            width=200
        )
        self.method_combo.set("Cash")
        self.method_combo.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # Received By
        ctk.CTkLabel(
            form_frame, 
            text="Received By:", 
            font=("Arial", 14, "bold")
        ).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        
        self.received_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Your name",
            width=200
        )
        self.received_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        # Submit Button
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        self.submit_btn = ctk.CTkButton(
            btn_frame,
            text="✅ Collect Payment & Generate Receipt",
            command=self.collect_payment,
            fg_color="#0f9d58",
            width=300,
            height=45,
            font=("Arial", 14, "bold")
        )
        self.submit_btn.pack()
    
    def search_student(self):
        """Search student by roll number"""
        roll = self.roll_entry.get().strip()
        
        if not roll:
            messagebox.showerror("Error", "Please enter a roll number")
            return
        
        student = get_student_by_roll(roll)
        
        if not student:
            messagebox.showerror("Error", f"Student with roll number '{roll}' not found")
            return
        
        self.student = student
        
        # Update student info
        self.student_label.configure(
            text=f"👨‍🎓 {student['student_name']} | Roll: {student['roll_number']} | "
                 f"Program: {student['program_name']} | Semester: {student['semester']}",
            text_color="white"
        )
        
        # Load eligible campaigns
        self.load_campaigns()
    
    def load_campaigns(self):
        """Load eligible campaigns for the student"""
        if not self.student:
            return
        
        campaigns = get_campaign_eligible_for_student(self.student["id"])
        
        if not campaigns:
            self.campaign_combo.configure(values=["No campaigns available"])
            self.campaign_combo.set("No campaigns available")
            messagebox.showinfo(
                "Info", 
                "Student has already paid for all campaigns or no eligible campaigns found."
            )
            return
        
        campaign_names = [c["campaign_name"] for c in campaigns]
        self.campaign_combo.configure(values=campaign_names)
        self.campaign_combo.set(campaign_names[0])
        self.campaign_combo.bind("<<ComboboxSelected>>", self.on_campaign_select)
        
        # Auto-select first campaign
        self.selected_campaign = campaigns[0]
        self.update_campaign_info()
        self.amount_entry.delete(0, "end")
        self.amount_entry.insert(0, str(campaigns[0]["required_amount"]))
    
    def on_campaign_select(self, event):
        """Handle campaign selection change"""
        campaign_name = self.campaign_combo.get()
        campaigns = get_campaign_eligible_for_student(self.student["id"])
        
        for c in campaigns:
            if c["campaign_name"] == campaign_name:
                self.selected_campaign = c
                self.update_campaign_info()
                self.amount_entry.delete(0, "end")
                self.amount_entry.insert(0, str(c["required_amount"]))
                break
    
    def update_campaign_info(self):
        """Update campaign info label"""
        if self.selected_campaign:
            self.campaign_info.configure(
                text=f"💰 Fund: {self.selected_campaign.get('fund_name', 'N/A')} | "
                     f"Required: Rs. {self.selected_campaign['required_amount']:,.2f}"
            )
    
    def collect_payment(self):
        """Collect payment and generate receipt"""
        if not self.student:
            messagebox.showerror("Error", "Please search for a student first")
            return
        
        if not self.selected_campaign:
            messagebox.showerror("Error", "Please select a campaign")
            return
        
        amount = self.amount_entry.get().strip()
        
        if not amount:
            messagebox.showerror("Error", "Please enter the amount")
            return
        
        try:
            amount = float(amount)
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")
            return
        
        method = self.method_combo.get()
        received_by = self.received_entry.get().strip() or "Admin"
        
        # Prepare payment data
        payment_data = {
            "student_id": self.student["id"],
            "student_name": self.student["student_name"],
            "campaign_id": self.selected_campaign["id"],
            "amount": amount,
            "payment_method": method,
            "received_by": received_by,
            "payment_date": datetime.now().strftime("%Y-%m-%d"),
            "department_id": 1
        }
        
        try:
            payment_id, receipt_no, receipt_path = collect_payment(payment_data)
            
            # Show success message
            messagebox.showinfo(
                "✅ Payment Successful!",
                f"Payment collected successfully!\n\n"
                f"Receipt No: {receipt_no}\n"
                f"Student: {self.student['student_name']}\n"
                f"Amount: Rs. {amount:,.2f}\n"
                f"Campaign: {self.selected_campaign['campaign_name']}"
            )
            
            # ─── OPEN RECEIPT IN POPUP ──────────────────────────────────────
            self.open_receipt_popup(receipt_no)
            
            # Reset form
            self.clear_all()
            
        except Exception as e:
            messagebox.showerror("Error", f"Payment failed: {e}")
    
    def open_receipt_popup(self, receipt_no):
        """Open receipt in a popup window"""
        payment = get_payment_by_receipt(receipt_no)
        
        if not payment:
            messagebox.showerror("Error", "Receipt not found")
            return
        
        # Create popup window
        popup = ctk.CTkToplevel(self)
        popup.title("Payment Receipt")
        popup.geometry("450x550")
        popup.resizable(False, False)
        popup.configure(fg_color="#021635")
        
        # Make it modal
        popup.transient(self)
        popup.grab_set()
        popup.focus_set()
        
        # ─── Popup Content ──────────────────────────────────────────────────
        main_frame = ctk.CTkFrame(popup, fg_color="#021635")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(
            main_frame, 
            text="📄 PAYMENT RECEIPT", 
            font=("Arial", 20, "bold"),
            text_color="#4fc3f7"
        ).pack(pady=(10, 10))
        
        ctk.CTkLabel(
            main_frame, 
            text="=" * 40, 
            font=("Courier", 10),
            text_color="#666666"
        ).pack()
        
        # Receipt details in scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(main_frame, fg_color="#1a1a2e", height=300)
        scroll_frame.pack(fill="both", expand=True, padx=5, pady=10)
        
        details = [
            ("Receipt No:", payment.get('receipt_number', 'N/A')),
            ("Date:", payment.get('payment_date', 'N/A')),
            ("Student:", payment.get('student_name', 'N/A')),
            ("Roll No:", payment.get('roll_number', 'N/A')),
            ("Campaign:", payment.get('campaign_name', 'N/A')),
            ("Fund:", payment.get('fund_name', 'N/A')),
            ("Amount:", f"Rs. {payment.get('amount', 0):,.2f}"),
            ("Method:", payment.get('payment_method', 'N/A')),
            ("Received By:", payment.get('received_by', 'N/A')),
        ]
        
        for label, value in details:
            row = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=3)
            
            ctk.CTkLabel(
                row, 
                text=label, 
                font=("Arial", 12, "bold"),
                text_color="#a0a0b0",
                width=110,
                anchor="e"
            ).pack(side="left", padx=5)
            
            ctk.CTkLabel(
                row, 
                text=value, 
                font=("Arial", 12),
                text_color="#ffffff",
                anchor="w"
            ).pack(side="left", padx=5)
        
        ctk.CTkLabel(
            scroll_frame, 
            text="=" * 40, 
            font=("Courier", 10),
            text_color="#666666"
        ).pack(pady=(10, 5))
        
        ctk.CTkLabel(
            scroll_frame, 
            text="Thank you!", 
            font=("Arial", 14, "bold"),
            text_color="#0f9d58"
        ).pack(pady=(0, 10))
        
        # ─── Buttons ──────────────────────────────────────────────────────────
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        # Open PDF Button
        if payment.get('receipt_path'):
            ctk.CTkButton(
                btn_frame,
                text="📄 Open PDF",
                command=lambda: self.open_receipt(payment['receipt_path']),
                fg_color="#1a73e8",
                hover_color="#1557b0",
                width=140,
                height=38,
                corner_radius=8,
                font=("Arial", 13, "bold")
            ).pack(side="left", padx=10)
        
        # Close Button
        ctk.CTkButton(
            btn_frame,
            text="✖ Close",
            command=popup.destroy,
            fg_color="#db4437",
            hover_color="#b8322a",
            width=120,
            height=38,
            corner_radius=8,
            font=("Arial", 13, "bold")
        ).pack(side="left", padx=10)
    
    def open_receipt(self, path):
        """Open receipt PDF"""
        import os
        if path and os.path.exists(path):
            os.startfile(path)
        else:
            messagebox.showerror("Error", "Receipt file not found")
    
    def clear_all(self):
        """Clear all fields"""
        self.roll_entry.delete(0, "end")
        self.student_label.configure(text="No student selected", text_color="gray")
        self.campaign_combo.configure(values=["Search student first"])
        self.campaign_combo.set("Search student first")
        self.campaign_info.configure(text="")
        self.amount_entry.delete(0, "end")
        self.received_entry.delete(0, "end")
        self.student = None
        self.selected_campaign = None