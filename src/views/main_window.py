# src/views/main_window.py
import customtkinter as ctk
from PIL import Image
import sys
import os
from src.views.dashboard import Dashboard
from src.views.students.student_list import StudentList
from src.views.funds.fund_list import FundList
from src.views.campaigns.campaign_list import CampaignList
from src.views.campaigns.payment_status import PaymentStatus
from src.views.payments.payment_history import PaymentHistory
from src.views.expenses.expense_list import ExpenseList
from src.views.reports.report_generator import ReportGenerator
from src.views.settings.general_settings import GeneralSettings


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class MainWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#021B41")
        self.master = master
        self.current_view = None
        self.current_button = None
        
        # ─── Create Sidebar ──────────────────────────────────────────────
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#041430")
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar.pack_propagate(False)
        
        # ─── Logo Section ──────────────────────────────────────────────
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(pady=(20, 10))
        
        # Load and display logo with EXE support
        try:
            # Check if running as EXE
            if getattr(sys, 'frozen', False):
                logo_path = get_resource_path("src/assets/images/logo2.png")
            else:
                logo_path = "src/assets/images/logo2.png"
            
            logo_image = ctk.CTkImage(
                light_image=Image.open(logo_path),
                dark_image=Image.open(logo_path),
                size=(100, 90)
            )
            ctk.CTkLabel(
                logo_frame, 
                image=logo_image, 
                text=""
            ).pack()
        except Exception as e:
            # Fallback emoji if logo not found
            print(f"Logo error: {e}")
            ctk.CTkLabel(
                logo_frame, 
                text="🏛️", 
                font=("Arial", 36)
            ).pack()
            # App Name
            ctk.CTkLabel(
                logo_frame, 
                text="DFMS", 
                font=("Arial", 22, "bold"),
                text_color="#ffffff"
            ).pack()
        
        # Subtitle
        ctk.CTkLabel(
            logo_frame, 
            text=" Finance Management ", 
            font=("Arial", 15),
            text_color="#6a6a7e"
        ).pack()
        
        # ─── Menu Buttons ──────────────────────────────────────────────
        self.menu_buttons = {}
        
        menu_items = [
            ("📊 Dashboard", self.show_dashboard),
            ("👨‍🎓 Students", self.show_students),
            ("💰 Funds", self.show_funds),
            ("📋 Campaigns", self.show_campaigns),
            ("💳 Payments", self.show_payments),
            ("📤 Expenses", self.show_expenses),
            ("📈 Reports", self.show_reports),
            ("⚙️ Settings", self.show_settings)
        ]
        
        for text, command in menu_items:
            btn = ctk.CTkButton(
                self.sidebar, 
                text=text, 
                command=lambda t=text, cmd=command: self.on_menu_click(t, cmd),
                corner_radius=5,
                height=38,
                font=("Arial", 13, "bold"),
                fg_color="#0a2a4a",          
                hover_color="#1a4a7a",      
                text_color="#8ab4d6",         
                anchor="center"
            )
            btn.pack(pady=3, padx=10, fill="x")
            self.menu_buttons[text] = btn
        
        # Version
        ctk.CTkLabel(
            self.sidebar, 
            text="v1.0.", 
            font=("Arial", 15),
            text_color="#968D8D"
        ).pack(side="bottom", pady=10)
        
        # ─── Content Area ──────────────────────────────────────────────
        self.content_frame = ctk.CTkFrame(self, fg_color="#021635")
        self.content_frame.pack(side="right", fill="both", expand=True, padx=5, pady=0)
        
        # Show Dashboard by default and highlight it
        self.show_dashboard()
        self.highlight_button("📊 Dashboard")
    
    def on_menu_click(self, text, command):
        """Handle menu click - highlight button and show view"""
        command()
        self.highlight_button(text)
    
    def highlight_button(self, text):
        """Highlight the active menu button"""
        for menu_text, btn in self.menu_buttons.items():
            if menu_text == text:
                btn.configure(
                    fg_color="#1a6a9a",
                    text_color="#ffffff"
                )
            else:
                btn.configure(
                    fg_color="#0a2a4a",
                    text_color="#8ab4d6"
                )
    
    def clear_content(self):
        """Clear all widgets from content area"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_view(self, view_class, **kwargs):
        """Show a view in the content area"""
        self.clear_content()
        self.current_view = view_class(self.content_frame, **kwargs)
        self.current_view.pack(fill="both", expand=True)
        self.current_view.configure(fg_color="#021635")
    
    # ─── Navigation Handlers ──────────────────────────────────────────
    
    def show_dashboard(self):
        self.show_view(Dashboard)
        self.highlight_button("📊 Dashboard")
    
    def show_students(self):
        self.show_view(StudentList)
        self.highlight_button("👨‍🎓 Students")
    
    def show_funds(self):
        self.show_view(FundList)
        self.highlight_button("💰 Funds")
    
    def show_campaigns(self):
        self.show_view(CampaignList)
        self.highlight_button("📋 Campaigns")
    
    def show_payment_status(self):
        self.show_view(PaymentStatus)
        self.highlight_button("💳 Payments")
    
    def show_payments(self):
        self.show_view(PaymentHistory)
        self.highlight_button("💳 Payments")
    
    def show_expenses(self):
        self.show_view(ExpenseList)
        self.highlight_button("📤 Expenses")
    
    def show_reports(self):
        self.show_view(ReportGenerator)
        self.highlight_button("📈 Reports")
    
    def show_settings(self):
        self.show_view(GeneralSettings)
        self.highlight_button("⚙️ Settings")