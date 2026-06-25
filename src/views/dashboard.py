# src/views/dashboard.py
import customtkinter as ctk
from datetime import datetime
from src.controllers.department_controller import get_department_summary
from src.controllers.payment_controller import get_payment_history
from src.controllers.report_controller import get_overall_summary, get_daily_summary
from src.controllers.department_controller import get_current_department


class Dashboard(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#1a1a2e")
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=0)  # Quick Actions
        self.grid_rowconfigure(2, weight=1)  # Stats
        self.grid_rowconfigure(3, weight=1)  # Charts & Activity
        
        self.create_header()
        self.create_quick_actions()
        self.create_stats_cards()
        self.create_bottom_section()
    
    def create_header(self):
        """Create welcome header with date/time below"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=25, pady=(20, 10))
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Welcome text
        dept = get_current_department()
        dept_name = dept.get("department_name", "Department") if dept else "Department"
        
        welcome_text = f"👋 Welcome to {dept_name} Finance & Fund Management Dashboard"
        ctk.CTkLabel(
            header_frame, 
            text=welcome_text, 
            font=("Arial", 26, "bold"),
            text_color="#ffffff"
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))
        
        # Date/Time Below Welcome
        now = datetime.now()
        date_text = now.strftime("%A, %B %d, %Y")
        time_text = now.strftime("%I:%M %p")
        
        datetime_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        datetime_frame.grid(row=1, column=0, sticky="w")
        
        ctk.CTkLabel(
            datetime_frame, 
            text=f"📅 {date_text}  •  ⏰ {time_text}", 
            font=("Arial", 14),
            text_color="#a0a0b0"
        ).pack(side="left")
    
    def create_quick_actions(self):
        """Create quick action buttons"""
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.grid(row=1, column=0, sticky="ew", padx=25, pady=(0, 15))
        
        ctk.CTkLabel(
            actions_frame, 
            text="⚡ Quick Actions", 
            font=("Arial", 16, "bold"),
            text_color="#ffffff"
        ).pack(anchor="w", pady=(0, 10))
        
        btn_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        btn_frame.pack(anchor="w")
        
        actions = [
            ("💰 Collect Payment", self.open_collect_payment, "#2e7d32", "#43a047"),
            ("👨‍🎓 Add Student", self.open_add_student, "#1a237e", "#3949ab"),
            ("📋 New Campaign", self.open_campaign, "#e65100", "#f57c00"),
            ("📤 Add Expense", self.open_expense, "#b71c1c", "#e53935"),
        ]
        
        for text, command, bg_color, hover_color in actions:
            ctk.CTkButton(
                btn_frame,
                text=text,
                command=command,
                fg_color=bg_color,
                hover_color=hover_color,
                width=170,
                height=38,
                corner_radius=8,
                font=("Arial", 13, "bold"),
                text_color="#ffffff"
            ).pack(side="left", padx=6)
    
    def create_stats_cards(self):
        """Create professional stats cards"""
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.grid(row=2, column=0, sticky="nsew", padx=25, pady=10)
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)
        stats_frame.grid_rowconfigure(0, weight=1)
        stats_frame.grid_rowconfigure(1, weight=1)
        
        summary = get_overall_summary()
        
        # Card configurations
        cards = [
            {
                "icon": "👨‍🎓",
                "title": "Total Students",
                "value": summary.get("total_students", 0),
                "bg_color": "#1a237e",
            },
            {
                "icon": "💰",
                "title": "Total Collection",
                "value": f"Rs. {summary.get('total_collection', 0):,.0f}",
                "bg_color": "#1b5e20",
            },
            {
                "icon": "📤",
                "title": "Total Expenses",
                "value": f"Rs. {summary.get('total_expenses', 0):,.0f}",
                "bg_color": "#b71c1c",
            },
            {
                "icon": "💵",
                "title": "Balance",
                "value": f"Rs. {summary.get('balance', 0):,.0f}",
                "bg_color": "#e65100",
            },
            {
                "icon": "📋",
                "title": "Campaigns",
                "value": summary.get("active_campaigns", 0),
                "bg_color": "#4a148c",
            },
            {
                "icon": "📊",
                "title": "Funds",
                "value": summary.get("active_funds", 0),
                "bg_color": "#004d40",
            }
        ]
        
        for i, card in enumerate(cards):
            row = i // 3
            col = i % 3
            
            card_frame = ctk.CTkFrame(
                stats_frame,
                corner_radius=12,
                fg_color=card["bg_color"],
                border_width=0
            )
            card_frame.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            stats_frame.grid_rowconfigure(row, weight=1)
            stats_frame.grid_columnconfigure(col, weight=1)
            
            # Inner content with better padding
            inner_frame = ctk.CTkFrame(
                card_frame,
                fg_color="transparent"
            )
            inner_frame.pack(fill="both", expand=True, padx=15, pady=8)
            
            # Top row: Icon and Value
            top_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
            top_frame.pack(fill="x")
            
            # Icon
            ctk.CTkLabel(
                top_frame, 
                text=card["icon"], 
                font=("Arial", 20)
            ).pack(side="left")
            
            # Value - smaller font for large numbers
            value_text = str(card["value"])
            font_size = 18 if len(value_text) > 10 else 20
            ctk.CTkLabel(
                top_frame, 
                text=value_text, 
                font=("Arial", font_size, "bold"),
                text_color="#ffffff"
            ).pack(side="right")
            
            # Title - with better spacing
            ctk.CTkLabel(
                inner_frame, 
                text=card["title"], 
                font=("Arial", 12),
                text_color="#d0d0d0"
            ).pack(anchor="w", pady=(8, 0))
            
            # Progress bar for main cards
            if card["title"] in ["Collection", "Expenses"]:
                progress_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
                progress_frame.pack(fill="x", pady=(8, 0))
                
                progress = ctk.CTkProgressBar(
                    progress_frame,
                    height=4,
                    corner_radius=2,
                    progress_color="#ffffff",
                    fg_color="#2d2d4a"
                )
                progress.pack(fill="x")
                
                if summary.get("total_collection", 0) > 0:
                    if card["title"] == "Collection":
                        progress.set(1.0)
                    else:
                        ratio = summary.get("total_expenses", 0) / max(summary.get("total_collection", 1), 1)
                        progress.set(min(ratio, 1.0))
    
    def create_bottom_section(self):
        """Create bottom section with recent activity and quick stats"""
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.grid(row=3, column=0, sticky="nsew", padx=25, pady=(10, 20))
        bottom_frame.grid_columnconfigure(0, weight=2)
        bottom_frame.grid_columnconfigure(1, weight=1)
        bottom_frame.grid_rowconfigure(0, weight=1)
        
        # ─── Left: Recent Activity ──────────────────────────────────────
        activity_frame = ctk.CTkFrame(
            bottom_frame,
            corner_radius=12,
            fg_color="#1e1e3a",
            border_width=1,
            border_color="#2d2d4a"
        )
        activity_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Header
        header_frame = ctk.CTkFrame(activity_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(
            header_frame, 
            text="🔄 Recent Activity", 
            font=("Arial", 16, "bold"),
            text_color="#ffffff"
        ).pack(side="left")
        
        ctk.CTkLabel(
            header_frame, 
            text="Last 5 transactions", 
            font=("Arial", 11),
            text_color="#a0a0b0"
        ).pack(side="left", padx=10)
        
        # Activity list
        activity_list = ctk.CTkScrollableFrame(
            activity_frame,
            fg_color="transparent",
            height=200
        )
        activity_list.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Load recent payments
        payments = get_payment_history()
        
        if payments:
            for payment in payments[:5]:
                self.create_activity_item(activity_list, payment)
        else:
            ctk.CTkLabel(
                activity_list, 
                text="No recent activity",
                font=("Arial", 14),
                text_color="#a0a0b0"
            ).pack(pady=30)
        
        # ─── Right: Today's Summary ──────────────────────────────────────
        summary_frame = ctk.CTkFrame(
            bottom_frame,
            corner_radius=12,
            fg_color="#1e1e3a",
            border_width=1,
            border_color="#2d2d4a"
        )
        summary_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(
            summary_frame, 
            text="📊 Today's Summary", 
            font=("Arial", 16, "bold"),
            text_color="#ffffff"
        ).pack(anchor="w", padx=15, pady=15)
        
        daily = get_daily_summary()
        
        # Today's stats with colored values
        stats_data = [
            ("💰 Collection", f"Rs. {daily.get('total_collection', 0):,.2f}", "#43a047"),
            ("📤 Expenses", f"Rs. {daily.get('total_expense', 0):,.2f}", "#e53935"),
            ("💵 Balance", f"Rs. {daily.get('balance', 0):,.2f}", "#f57c00"),
        ]
        
        for label, value, color in stats_data:
            stat_frame = ctk.CTkFrame(summary_frame, fg_color="transparent")
            stat_frame.pack(fill="x", padx=15, pady=8)
            
            ctk.CTkLabel(
                stat_frame, 
                text=label, 
                font=("Arial", 13),
                text_color="#a0a0b0"
            ).pack(side="left")
            
            ctk.CTkLabel(
                stat_frame, 
                text=value, 
                font=("Arial", 16, "bold"),
                text_color=color
            ).pack(side="right")
        
        # Divider
        ctk.CTkFrame(
            summary_frame, 
            height=1, 
            fg_color="#2d2d4a"
        ).pack(fill="x", padx=15, pady=10)
        
        # Total students today
        total_students = get_overall_summary().get("total_students", 0)
        stat_frame = ctk.CTkFrame(summary_frame, fg_color="transparent")
        stat_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(
            stat_frame, 
            text="👨‍🎓 Total Students", 
            font=("Arial", 13),
            text_color="#a0a0b0"
        ).pack(side="left")
        
        ctk.CTkLabel(
            stat_frame, 
            text=str(total_students), 
            font=("Arial", 16, "bold"),
            text_color="#4fc3f7"
        ).pack(side="right")
        
        # Footer
        ctk.CTkLabel(
            summary_frame, 
            text=f"📅 {datetime.now().strftime('%B %d, %Y')}", 
            font=("Arial", 11),
            text_color="#a0a0b0"
        ).pack(anchor="w", padx=15, pady=(15, 15))
    
    def create_activity_item(self, parent, payment):
        """Create a single activity item"""
        item_frame = ctk.CTkFrame(parent, fg_color="transparent")
        item_frame.pack(fill="x", pady=4)
        
        # Left side: Icon and name
        left_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        left_frame.pack(side="left")
        
        # Avatar circle
        avatar = ctk.CTkFrame(
            left_frame,
            width=38,
            height=38,
            corner_radius=19,
            fg_color="#2d2d4a"
        )
        avatar.pack(side="left")
        avatar.pack_propagate(False)
        
        ctk.CTkLabel(
            avatar, 
            text="👤", 
            font=("Arial", 16)
        ).pack(expand=True)
        
        # Name and details
        details_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        details_frame.pack(side="left", padx=(12, 0))
        
        name = payment.get("student_name", "Unknown")
        ctk.CTkLabel(
            details_frame, 
            text=name, 
            font=("Arial", 14, "bold"),
            text_color="#ffffff",
            anchor="w"
        ).pack(anchor="w")
        
        campaign = payment.get("campaign_name", "")
        ctk.CTkLabel(
            details_frame, 
            text=campaign[:35] + ("..." if len(campaign) > 35 else ""),
            font=("Arial", 12),
            text_color="#a0a0b0",
            anchor="w"
        ).pack(anchor="w")
        
        # Right side: Amount and time
        right_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        right_frame.pack(side="right")
        
        amount = payment.get("amount", 0)
        ctk.CTkLabel(
            right_frame, 
            text=f"+ Rs. {amount:,.2f}", 
            font=("Arial", 15, "bold"),
            text_color="#43a047"
        ).pack(anchor="e")
        
        date = payment.get("payment_date", "")
        if date:
            try:
                dt = datetime.strptime(date, "%Y-%m-%d")
                date = dt.strftime("%d %b, %I:%M %p")
            except:
                pass
        
        ctk.CTkLabel(
            right_frame, 
            text=date, 
            font=("Arial", 11),
            text_color="#a0a0b0"
        ).pack(anchor="e")
        
        # Separator
        ctk.CTkFrame(
            parent, 
            height=1, 
            fg_color="#2d2d4a"
        ).pack(fill="x", pady=5)
    
    # ─── Navigation Methods ──────────────────────────────────────────────
    
    def open_collect_payment(self):
        from src.views.payments.collect_payment import CollectPayment
        self.navigate_to(CollectPayment)
    
    def open_add_student(self):
        from src.views.students.student_registration import StudentRegistration
        self.navigate_to(StudentRegistration)
    
    def open_campaign(self):
        from src.views.campaigns.create_campaign import CreateCampaign
        self.navigate_to(CreateCampaign)
    
    def open_expense(self):
        from src.views.expenses.add_expense import AddExpense
        self.navigate_to(AddExpense)
    
    def navigate_to(self, view_class):
        parent = self.master
        while parent:
            if hasattr(parent, 'show_view'):
                parent.show_view(view_class)
                break
            parent = parent.master