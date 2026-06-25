# src/views/payments/receipt_generator.py
import customtkinter as ctk
from tkinter import messagebox, filedialog
import os
from datetime import datetime
from src.controllers.payment_controller import get_payment_by_receipt, get_payment_history
from src.services.pdf_service import generate_receipt_pdf
from src.services.qr_service import generate_qr_code
from src.controllers.department_controller import get_current_department


class ReceiptGenerator(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.create_header()
        self.create_search_section()
        self.create_receipt_preview()
    
    def create_header(self):
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            header, 
            text="📄 Receipt Generator", 
            font=("Arial", 24, "bold")
        ).pack(side="left")
        
        ctk.CTkLabel(
            header, 
            text="View, regenerate, and print receipts", 
            font=("Arial", 12),
            text_color="gray"
        ).pack(side="left", padx=20)
    
    def create_search_section(self):
        """Search receipt by number"""
        search_frame = ctk.CTkFrame(self)
        search_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            search_frame, 
            text="Receipt Number:", 
            font=("Arial", 14, "bold")
        ).pack(side="left", padx=10)
        
        self.receipt_entry = ctk.CTkEntry(
            search_frame, 
            placeholder_text="e.g., CS-00001",
            width=200
        )
        self.receipt_entry.pack(side="left", padx=10)
        
        self.search_btn = ctk.CTkButton(
            search_frame,
            text="🔍 Search",
            command=self.search_receipt,
            fg_color="#1a73e8",
            width=100
        )
        self.search_btn.pack(side="left", padx=10)
        
        self.refresh_btn = ctk.CTkButton(
            search_frame,
            text="🔄 Recent",
            command=self.show_recent,
            fg_color="gray",
            width=100
        )
        self.refresh_btn.pack(side="left", padx=10)
        
        self.regenerate_btn = ctk.CTkButton(
            search_frame,
            text="🔄 Regenerate",
            command=self.regenerate_receipt,
            fg_color="#f4b400",
            width=120
        )
        self.regenerate_btn.pack(side="left", padx=10)
        
        self.print_btn = ctk.CTkButton(
            search_frame,
            text="🖨️ Print",
            command=self.print_receipt,
            fg_color="#0f9d58",
            width=100
        )
        self.print_btn.pack(side="left", padx=10)
    
    def create_receipt_preview(self):
        """Display receipt preview"""
        self.preview_frame = ctk.CTkFrame(self)
        self.preview_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Initial message
        self.preview_label = ctk.CTkLabel(
            self.preview_frame, 
            text="Enter a receipt number above to view", 
            font=("Arial", 18),
            text_color="gray"
        )
        self.preview_label.pack(expand=True)
    
    def search_receipt(self):
        """Search and display receipt"""
        receipt_no = self.receipt_entry.get().strip()
        
        if not receipt_no:
            messagebox.showerror("Error", "Please enter a receipt number")
            return
        
        payment = get_payment_by_receipt(receipt_no)
        
        if not payment:
            messagebox.showerror("Error", f"Receipt '{receipt_no}' not found")
            return
        
        self.display_receipt(payment)
    
    def show_recent(self):
        """Show most recent receipts"""
        payments = get_payment_history()
        
        if not payments:
            messagebox.showinfo("Info", "No payments found")
            return
        
        # Show last 5 receipts
        recent = payments[:5]
        self.receipt_entry.delete(0, "end")
        
        # Display first recent receipt
        self.display_receipt(recent[0])
        
        # Show other recent receipts as options
        message = "Recent Receipts:\n\n"
        for i, p in enumerate(recent, 1):
            message += f"{i}. {p['receipt_number']} - {p['student_name']} - Rs. {p['amount']:,.2f}\n"
        
        messagebox.showinfo("Recent Receipts", message)
    
    def display_receipt(self, payment):
        """Display receipt preview"""
        # Clear preview
        for widget in self.preview_frame.winfo_children():
            widget.destroy()
        
        # Create receipt card
        card = ctk.CTkFrame(self.preview_frame)
        card.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        dept = get_current_department()
        uni_name = dept.get("university_name", "University") if dept else "University"
        dept_name = dept.get("department_name", "Department") if dept else "Department"
        
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            header_frame, 
            text=uni_name.upper(), 
            font=("Arial", 20, "bold")
        ).pack()
        
        ctk.CTkLabel(
            header_frame, 
            text=f"Department of {dept_name}", 
            font=("Arial", 14),
            text_color="gray"
        ).pack()
        
        ctk.CTkLabel(
            header_frame, 
            text="=" * 50, 
            font=("Arial", 12)
        ).pack(pady=5)
        
        ctk.CTkLabel(
            header_frame, 
            text="PAYMENT RECEIPT", 
            font=("Arial", 18, "bold"),
            text_color="#1a73e8"
        ).pack(pady=5)
        
        ctk.CTkLabel(
            header_frame, 
            text="=" * 50, 
            font=("Arial", 12)
        ).pack(pady=5)
        
        # Receipt details in table format
        details_frame = ctk.CTkFrame(card, fg_color="transparent")
        details_frame.pack(fill="x", pady=10)
        
        # Create a 2-column grid for receipt details
        details = [
            ("Receipt No:", payment.get("receipt_number", "-")),
            ("Date:", payment.get("payment_date", "-")),
            ("Student Name:", payment.get("student_name", "-")),
            ("Roll Number:", payment.get("roll_number", "-")),
            ("Campaign:", payment.get("campaign_name", "-")),
            ("Fund:", payment.get("fund_name", "-")),
            ("Amount:", f"Rs. {payment.get('amount', 0):,.2f}"),
            ("Payment Method:", payment.get("payment_method", "-")),
            ("Received By:", payment.get("received_by", "-"))
        ]
        
        for i, (label, value) in enumerate(details):
            row_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(
                row_frame, 
                text=label, 
                font=("Arial", 12, "bold"),
                width=120,
                anchor="e"
            ).pack(side="left", padx=5)
            
            if "Amount" in label:
                ctk.CTkLabel(
                    row_frame, 
                    text=value, 
                    font=("Arial", 14, "bold"),
                    text_color="#0f9d58"
                ).pack(side="left", padx=5)
            else:
                ctk.CTkLabel(
                    row_frame, 
                    text=value, 
                    font=("Arial", 12)
                ).pack(side="left", padx=5)
        
        # Footer
        ctk.CTkLabel(
            card, 
            text="=" * 50, 
            font=("Arial", 12)
        ).pack(pady=10)
        
        ctk.CTkLabel(
            card, 
            text="This is a computer-generated receipt. No signature required.", 
            font=("Arial", 10),
            text_color="gray"
        ).pack()
        
        ctk.CTkLabel(
            card, 
            text=f"Generated on {datetime.now().strftime('%d-%b-%Y %H:%M')}", 
            font=("Arial", 9),
            text_color="gray"
        ).pack()
        
        # QR Code
        if payment.get("qr_code_path") and os.path.exists(payment["qr_code_path"]):
            try:
                from PIL import Image
                import customtkinter as ctk
                qr_image = ctk.CTkImage(
                    light_image=Image.open(payment["qr_code_path"]),
                    dark_image=Image.open(payment["qr_code_path"]),
                    size=(100, 100)
                )
                qr_label = ctk.CTkLabel(card, image=qr_image, text="")
                qr_label.pack(pady=10)
            except Exception as e:
                pass
        
        # Store current payment for actions
        self.current_payment = payment
    
    def regenerate_receipt(self):
        """Regenerate receipt PDF"""
        if not hasattr(self, 'current_payment') or not self.current_payment:
            messagebox.showerror("Error", "Please search for a receipt first")
            return
        
        payment = self.current_payment
        dept = get_current_department()
        
        try:
            # Generate new receipt
            receipt_path = generate_receipt_pdf(payment, dept, payment.get("qr_code_path"))
            
            if receipt_path:
                messagebox.showinfo(
                    "Success", 
                    f"Receipt regenerated successfully!\n\nSaved at: {receipt_path}"
                )
            else:
                messagebox.showerror("Error", "Failed to regenerate receipt")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to regenerate receipt: {e}")
    
    def print_receipt(self):
        """Print the receipt"""
        if not hasattr(self, 'current_payment') or not self.current_payment:
            messagebox.showerror("Error", "Please search for a receipt first")
            return
        
        payment = self.current_payment
        path = payment.get("receipt_path")
        
        if path and os.path.exists(path):
            try:
                os.startfile(path)
                # After opening, user can print from PDF viewer
                messagebox.showinfo("Info", "Receipt opened. Use the PDF viewer to print.")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open receipt: {e}")
        else:
            # Try to regenerate first
            messagebox.showinfo("Info", "Receipt file not found. Regenerating...")
            self.regenerate_receipt()