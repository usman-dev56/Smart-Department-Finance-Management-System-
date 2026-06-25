# src/views/payments/payment_history.py
import customtkinter as ctk
from src.views.payments.collect_payment import CollectPayment
from src.views.campaigns.payment_status import PaymentStatus


class PaymentHistory(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.create_header()
        self.create_dashboard_cards()
        self.create_filters()
        self.create_table()
        self.load_payments()
    
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="#021635")
        header.pack(fill="x",  padx=10, pady=25)
        
        ctk.CTkLabel(
            header, 
            text=" Payment Management", 
            font=("Arial", 33, "bold")
        ).pack(side="left")
        
        ctk.CTkLabel(
            header, 
            text="Collect payments, view history, and check status", 
            font=("Arial", 20),
            text_color="gray"
        ).pack(side="left", padx=35)
    
    def create_dashboard_cards(self):
        """Create 3 cards: Collect Payment, Payment History, Payment Status"""
        cards_frame = ctk.CTkFrame(self)
        cards_frame.pack(fill="x", padx=20, pady=10)
        
        # ─── Card 1: Collect Payment ──────────────────────────────────
        card1 = ctk.CTkFrame(cards_frame, corner_radius=10, fg_color="#1a73e8")
        card1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        cards_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            card1, 
            text="💰", 
            font=("Arial", 32)
        ).pack(pady=(15, 0))
        
        ctk.CTkLabel(
            card1, 
            text="Collect Payment", 
            font=("Arial", 16, "bold"),
            text_color="white"
        ).pack(pady=5)
        
        ctk.CTkLabel(
            card1, 
            text="Collect money from students\nand generate receipts", 
            font=("Arial", 11),
            text_color="#d0d0d0",
            justify="center"
        ).pack(pady=5)
        
        ctk.CTkButton(
            card1,
            text="→ Collect Now",
            command=self.open_collect_payment,
            fg_color="white",
            text_color="#1a73e8",
            width=150,
            height=35,
            font=("Arial", 12, "bold")
        ).pack(pady=(10, 15))
        
        # ─── Card 2: Payment History ──────────────────────────────────
        card2 = ctk.CTkFrame(cards_frame, corner_radius=10, fg_color="#0f9d58")
        card2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        cards_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            card2, 
            text="📄", 
            font=("Arial", 32)
        ).pack(pady=(15, 0))
        
        ctk.CTkLabel(
            card2, 
            text="Payment History", 
            font=("Arial", 16, "bold"),
            text_color="white"
        ).pack(pady=5)
        
        ctk.CTkLabel(
            card2, 
            text="View all past payments\nand receipts", 
            font=("Arial", 11),
            text_color="#d0d0d0",
            justify="center"
        ).pack(pady=5)
        
        ctk.CTkButton(
            card2,
            text="→ View History",
            command=self.show_history,
            fg_color="white",
            text_color="#0f9d58",
            width=150,
            height=35,
            font=("Arial", 12, "bold")
        ).pack(pady=(10, 15))
        
        # ─── Card 3: Payment Status ──────────────────────────────────
        card3 = ctk.CTkFrame(cards_frame, corner_radius=10, fg_color="#f4b400")
        card3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        cards_frame.grid_columnconfigure(2, weight=1)
        
        ctk.CTkLabel(
            card3, 
            text="💳", 
            font=("Arial", 32)
        ).pack(pady=(15, 0))
        
        ctk.CTkLabel(
            card3, 
            text="Payment Status", 
            font=("Arial", 16, "bold"),
            text_color="white"
        ).pack(pady=5)
        
        ctk.CTkLabel(
            card3, 
            text="Check student payment\nstatus across campaigns", 
            font=("Arial", 11),
            text_color="#d0d0d0",
            justify="center"
        ).pack(pady=5)
        
        ctk.CTkButton(
            card3,
            text="→ Check Status",
            command=self.open_payment_status,
            fg_color="white",
            text_color="#f4b400",
            width=150,
            height=35,
            font=("Arial", 12, "bold")
        ).pack(pady=(10, 15))
    
    def create_filters(self):
        """Filter/search section (hidden by default, shown when viewing history)"""
        self.filter_frame = ctk.CTkFrame(self)
        # Initially hidden
        self.filter_frame.pack_forget()
        
        # We'll show this when "View History" is clicked
        self.filter_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            self.filter_frame, 
            text="Search Receipt:", 
            font=("Arial", 13)
        ).pack(side="left", padx=5)
        
        self.search_entry = ctk.CTkEntry(
            self.filter_frame, 
            placeholder_text="Enter receipt number",
            width=200
        )
        self.search_entry.pack(side="left", padx=5)
        
        self.search_btn = ctk.CTkButton(
            self.filter_frame,
            text="🔍 Search",
            command=self.search_payment,
            fg_color="#1a73e8",
            width=80
        ).pack(side="left", padx=5)
        
        self.refresh_btn = ctk.CTkButton(
            self.filter_frame,
            text="🔄 Refresh",
            command=self.load_payments,
            fg_color="gray",
            width=80
        ).pack(side="left", padx=5)
        
        self.back_btn = ctk.CTkButton(
            self.filter_frame,
            text="← Back to Dashboard",
            command=self.show_dashboard,
            fg_color="gray",
            width=150
        ).pack(side="right", padx=5)
    
    def create_table(self):
        """Payment history table"""
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        headers_frame = ctk.CTkFrame(self.table_frame, fg_color="#2a2a3d")
        headers_frame.pack(fill="x", pady=(0, 2))
        
        headers = ["Receipt No", "Date", "Student", "Campaign", "Amount", "Method", "Received By", "Actions"]
        widths = [100, 100, 150, 150, 80, 100, 120, 80]
        
        for i, (header, width) in enumerate(zip(headers, widths)):
            ctk.CTkLabel(
                headers_frame, 
                text=header, 
                font=("Arial", 12, "bold"),
                width=width
            ).pack(side="left", padx=5, pady=5)
        
        self.table_body = ctk.CTkScrollableFrame(self.table_frame, fg_color="transparent")
        self.table_body.pack(fill="both", expand=True)
    
    def show_dashboard(self):
        """Show the dashboard cards, hide table and filters"""
        # Hide filter and table
        self.filter_frame.pack_forget()
        self.table_frame.pack_forget()
        
        # Show cards (they're already created but might be hidden)
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and widget not in [self.filter_frame, self.table_frame]:
                widget.pack(fill="x", padx=20, pady=10)
    
    def show_history(self):
        """Show payment history with filters and table"""
        # Hide cards
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and widget not in [self.filter_frame, self.table_frame]:
                widget.pack_forget()
        
        # Show filter and table
        self.filter_frame.pack(fill="x", padx=20, pady=10)
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.load_payments()
    
    def load_payments(self):
        """Load all payments"""
        from src.controllers.payment_controller import get_payment_history
        
        for widget in self.table_body.winfo_children():
            widget.destroy()
        
        payments = get_payment_history()
        
        if not payments:
            ctk.CTkLabel(
                self.table_body, 
                text="No payments found", 
                font=("Arial", 14),
                text_color="gray"
            ).pack(pady=40)
            return
        
        for payment in payments:
            self.create_row(payment)
    
    def create_row(self, payment):
        row = ctk.CTkFrame(self.table_body)
        row.pack(fill="x", pady=2)
        
        ctk.CTkLabel(row, text=payment.get("receipt_number", "-"), width=100).pack(side="left", padx=5, pady=5)
        ctk.CTkLabel(row, text=payment.get("payment_date", "-"), width=100).pack(side="left", padx=5, pady=5)
        ctk.CTkLabel(row, text=payment.get("student_name", "-"), width=150).pack(side="left", padx=5, pady=5)
        ctk.CTkLabel(row, text=payment.get("campaign_name", "-"), width=150).pack(side="left", padx=5, pady=5)
        ctk.CTkLabel(
            row, 
            text=f"Rs. {payment.get('amount', 0):,.2f}", 
            width=80,
            font=("Arial", 11, "bold"),
            text_color="#0f9d58"
        ).pack(side="left", padx=5, pady=5)
        ctk.CTkLabel(row, text=payment.get("payment_method", "-"), width=100).pack(side="left", padx=5, pady=5)
        ctk.CTkLabel(row, text=payment.get("received_by", "-"), width=120).pack(side="left", padx=5, pady=5)
        
        actions_frame = ctk.CTkFrame(row, fg_color="transparent")
        actions_frame.pack(side="right", padx=5, pady=5)
        
        ctk.CTkButton(
            actions_frame,
            text="📄",
            command=lambda p=payment: self.view_receipt(p),
            fg_color="#1a73e8",
            width=30,
            height=28
        ).pack(side="left", padx=2)
    
    def search_payment(self):
        from src.controllers.payment_controller import get_payment_by_receipt
        
        receipt = self.search_entry.get().strip()
        
        if not receipt:
            self.load_payments()
            return
        
        payment = get_payment_by_receipt(receipt)
        
        for widget in self.table_body.winfo_children():
            widget.destroy()
        
        if payment:
            self.create_row(payment)
        else:
            ctk.CTkLabel(
                self.table_body, 
                text=f"No payment found with receipt: {receipt}", 
                font=("Arial", 14),
                text_color="gray"
            ).pack(pady=40)
    
    def view_receipt(self, payment):
        import os
        path = payment.get("receipt_path")
        if path and os.path.exists(path):
            os.startfile(path)
        else:
            from tkinter import messagebox
            messagebox.showinfo("Info", "Receipt file not found")
    
    def open_collect_payment(self):
        from src.views.payments.collect_payment import CollectPayment
        parent = self.master
        while parent:
            if hasattr(parent, 'show_view'):
                parent.show_view(CollectPayment)
                break
            parent = parent.master
    
    def open_payment_status(self):
        from src.views.campaigns.payment_status import PaymentStatus
        parent = self.master
        while parent:
            if hasattr(parent, 'show_view'):
                parent.show_view(PaymentStatus)
                break
            parent = parent.master