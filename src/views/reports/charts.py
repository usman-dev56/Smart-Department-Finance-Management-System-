# src/views/reports/charts.py
import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')
from src.controllers.report_controller import (
    get_fund_performance_report,
    get_daily_summary,
    get_overall_summary,
    get_collection_report,
    get_expense_report
)
from src.controllers.campaign_controller import (
    get_all_campaigns,
    get_campaign_summary,
    get_paid_students
)
from src.controllers.student_controller import get_all_students
from src.controllers.payment_controller import get_payment_history
from src.database.db_manager import get_db
from datetime import datetime, timedelta


class Charts(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#1a1a2e")
        self.create_header()
        self.create_chart_area()
    
    def create_header(self):
        """Create header with title"""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            header, 
            text="📈 Complete Charts Dashboard", 
            font=("Arial", 24, "bold"),
            text_color="#ffffff"
        ).pack(anchor="center")
        
        ctk.CTkLabel(
            header, 
            text="10 comprehensive charts for complete financial overview", 
            font=("Arial", 13),
            text_color="#a0a0b0"
        ).pack(anchor="center", pady=(5, 0))
    
    def create_chart_area(self):
        """Create chart area with generate button"""
        self.chart_container = ctk.CTkScrollableFrame(self, fg_color="#1a1a2e")
        self.chart_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.generate_btn = ctk.CTkButton(
            self.chart_container,
            text="📊 Generate Complete Dashboard (10 Charts)",
            command=self.generate_all_charts,
            fg_color="#1a73e8",
            hover_color="#1557b0",
            width=350,
            height=50,
            font=("Arial", 16, "bold"),
            corner_radius=10
        )
        self.generate_btn.pack(pady=30)
    
    def get_daily_collection(self, days=7):
        """Get daily collection for last N days"""
        payments = get_payment_history()
        daily_data = {}
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            daily_data[date] = 0
        
        for p in payments:
            if p.get("payment_date") in daily_data:
                daily_data[p["payment_date"]] += p.get("amount", 0)
        
        sorted_dates = sorted(daily_data.keys())
        return sorted_dates, [daily_data[d] for d in sorted_dates]
    
    def get_monthly_collection(self):
        """Get monthly collection data"""
        payments = get_payment_history()
        monthly_data = {}
        
        for p in payments:
            if p.get("payment_date"):
                try:
                    month = datetime.strptime(p["payment_date"], "%Y-%m-%d").strftime("%b %Y")
                    monthly_data[month] = monthly_data.get(month, 0) + p.get("amount", 0)
                except:
                    pass
        
        sorted_months = sorted(monthly_data.keys(), key=lambda x: datetime.strptime(x, "%b %Y"))
        return sorted_months, [monthly_data[m] for m in sorted_months]
    
    def get_semester_collection(self):
        """Get collection by semester - Direct database query"""
        db = get_db()
        
        query = """
            SELECT p.amount, s.semester 
            FROM payments p
            JOIN students s ON p.student_id = s.id
            WHERE s.semester IS NOT NULL AND s.semester != ''
        """
        results = db.fetchall(query)
        
        semester_data = {}
        for row in results:
            semester = row.get("semester")
            if semester:
                try:
                    sem_int = int(semester)
                    sem_key = f"Sem {sem_int}"
                    semester_data[sem_key] = semester_data.get(sem_key, 0) + row.get("amount", 0)
                except (ValueError, TypeError):
                    continue
        
        return semester_data
    
    def generate_all_charts(self):
        """Generate all 10 charts"""
        try:
            self.generate_btn.configure(state="disabled", text="⏳ Generating Charts...")
            self.chart_container.update()
            
            # Get data
            fund_data = get_fund_performance_report()
            campaigns = get_all_campaigns()
            all_students = get_all_students()
            
            if not fund_data:
                messagebox.showinfo("Info", "No fund data available to generate charts")
                self.generate_btn.configure(state="normal", text="📊 Generate Complete Dashboard")
                return
            
            # Clear previous charts
            for widget in self.chart_container.winfo_children():
                if widget != self.generate_btn:
                    widget.destroy()
            
            # ─── Create Figure with 5x2 Grid ──────────────────────────────────
            fig = plt.figure(figsize=(22, 20))
            fig.patch.set_facecolor('#1a1a2e')
            
            # Define grid (5 rows, 2 columns)
            gs = fig.add_gridspec(5, 2, hspace=0.4, wspace=0.3)
            
            # ─── Chart 1: Semester-wise Collection (Bar Chart) ────────────────
            ax1 = fig.add_subplot(gs[0, 0])
            ax1.set_facecolor('#2a2a3d')
            
            semester_data = self.get_semester_collection()
            
            if semester_data:
                sem_items = sorted(semester_data.items(), key=lambda x: int(x[0].split()[1]))
                sem_labels = [item[0] for item in sem_items]
                sem_values = [item[1] for item in sem_items]
                
                bars = ax1.bar(sem_labels, sem_values, color='#9C27B0')
                ax1.set_xlabel("Semester", color='white', fontsize=10)
                ax1.set_ylabel("Collection (Rs.)", color='white', fontsize=10)
                ax1.set_title("📊 Semester-wise Collection", color='white', fontsize=13, fontweight='bold')
                ax1.tick_params(colors='white')
                for spine in ax1.spines.values():
                    spine.set_color('#555')
                
                for bar in bars:
                    h = bar.get_height()
                    if h > 0:
                        ax1.text(bar.get_x() + bar.get_width()/2., h,
                                f'{h:,.0f}', ha='center', va='bottom', 
                                fontsize=8, color='white')
            else:
                ax1.text(0.5, 0.5, "No semester data", ha="center", va="center", fontsize=14, color='white')
                ax1.set_title("📊 Semester-wise Collection", color='white', fontsize=13, fontweight='bold')
            
            # ─── Chart 2: Collection vs Expenses by Fund ──────────────────────
            ax2 = fig.add_subplot(gs[0, 1])
            ax2.set_facecolor('#2a2a3d')
            
            funds = []
            for f in fund_data:
                name = f["fund_name"]
                if len(name) > 12:
                    name = name[:10] + ".."
                funds.append(name)
            
            collections = [f["total_collected"] for f in fund_data]
            expenses = [f["total_expenses"] for f in fund_data]
            
            x = range(len(funds))
            width = 0.35
            
            bars1 = ax2.bar([i - width/2 for i in x], collections, width, 
                           label="Collection", color="#4CAF50")
            bars2 = ax2.bar([i + width/2 for i in x], expenses, width, 
                           label="Expenses", color="#f44336")
            
            ax2.set_xlabel("Funds", color='white', fontsize=10)
            ax2.set_ylabel("Amount (Rs.)", color='white', fontsize=10)
            ax2.set_title("💰 Collection vs Expenses", color='white', fontsize=13, fontweight='bold')
            ax2.set_xticks(x)
            ax2.set_xticklabels(funds, rotation=20, ha="right", color='white', fontsize=8)
            ax2.legend(loc='upper right', facecolor='#2a2a3d', edgecolor='#555')
            ax2.legend_.get_texts()[0].set_color('white')
            ax2.legend_.get_texts()[1].set_color('white')
            ax2.tick_params(colors='white')
            for spine in ax2.spines.values():
                spine.set_color('#555')
            
            # ─── Chart 3: Collection Distribution by Fund (Pie) ──────────────
            ax3 = fig.add_subplot(gs[1, 0])
            ax3.set_facecolor('#1a1a2e')
            
            fund_labels = []
            fund_values = []
            for f in fund_data:
                if f["total_collected"] > 0:
                    name = f["fund_name"]
                    if len(name) > 12:
                        name = name[:10] + ".."
                    fund_labels.append(name)
                    fund_values.append(f["total_collected"])
            
            if fund_values:
                colors_pie = ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0', '#00BCD4', '#FF5722', '#8BC34A', '#E91E63']
                colors_pie = colors_pie[:len(fund_values)]
                ax3.pie(fund_values, labels=fund_labels, autopct='%1.1f%%',
                        colors=colors_pie, startangle=90,
                        textprops={'color': 'white', 'fontsize': 9})
                ax3.set_title("📊 Collection Distribution", color='white', fontsize=13, fontweight='bold')
            else:
                ax3.text(0.5, 0.5, "No data", ha="center", va="center", fontsize=14, color='white')
                ax3.set_title("📊 Collection Distribution", color='white', fontsize=13, fontweight='bold')
            
            # ─── Chart 4: Fund Performance (Balance) ──────────────────────────
            ax4 = fig.add_subplot(gs[1, 1])
            ax4.set_facecolor('#2a2a3d')
            
            balances = [f["balance"] for f in fund_data]
            balance_colors = ["#4CAF50" if b >= 0 else "#f44336" for b in balances]
            
            bars = ax4.bar(funds, balances, color=balance_colors)
            ax4.set_xlabel("Funds", color='white', fontsize=10)
            ax4.set_ylabel("Balance (Rs.)", color='white', fontsize=10)
            ax4.set_title("📊 Fund Performance", color='white', fontsize=13, fontweight='bold')
            ax4.set_xticklabels(funds, rotation=20, ha="right", color='white', fontsize=8)
            ax4.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
            ax4.tick_params(colors='white')
            for spine in ax4.spines.values():
                spine.set_color('#555')
            
            # ─── Chart 5: Student Payment Status (Pie) ────────────────────────
            ax5 = fig.add_subplot(gs[2, 0])
            ax5.set_facecolor('#1a1a2e')
            
            total_students = len(all_students) if all_students else 0
            
            paid_students_set = set()
            for campaign in campaigns:
                if campaign.get("is_active", 1):
                    paid = get_paid_students(campaign["id"])
                    for student in paid:
                        paid_students_set.add(student.get("id"))
            
            paid_count = len(paid_students_set)
            pending_count = total_students - paid_count
            
            if total_students > 0:
                ax5.pie([paid_count, pending_count], 
                        labels=['✅ Paid', '⏳ Pending'], 
                        autopct='%1.1f%%',
                        colors=['#4CAF50', '#f44336'],
                        startangle=90,
                        textprops={'color': 'white', 'fontsize': 10})
                ax5.set_title(f"👨‍🎓 Student Payment\nStatus (Total: {total_students})", 
                             color='white', fontsize=13, fontweight='bold')
            else:
                ax5.text(0.5, 0.5, "No data", ha="center", va="center", fontsize=14, color='white')
                ax5.set_title("👨‍🎓 Student Payment Status", color='white', fontsize=13, fontweight='bold')
            
            # ─── Chart 6: Campaign Performance ──────────────────────────────────
            ax6 = fig.add_subplot(gs[2, 1])
            ax6.set_facecolor('#2a2a3d')
            
            camp_names = []
            camp_collected = []
            for c in campaigns[:8]:
                summary = get_campaign_summary(c["id"])
                if summary:
                    name = c["campaign_name"]
                    if len(name) > 12:
                        name = name[:10] + ".."
                    camp_names.append(name)
                    camp_collected.append(summary.get("total_collected", 0))
            
            if camp_names:
                bars = ax6.bar(camp_names, camp_collected, color='#2196F3')
                ax6.set_xlabel("Campaigns", color='white', fontsize=10)
                ax6.set_ylabel("Collected (Rs.)", color='white', fontsize=10)
                ax6.set_title("📋 Campaign Performance", color='white', fontsize=13, fontweight='bold')
                ax6.set_xticklabels(camp_names, rotation=20, ha="right", color='white', fontsize=8)
                ax6.tick_params(colors='white')
                for spine in ax6.spines.values():
                    spine.set_color('#555')
            else:
                ax6.text(0.5, 0.5, "No data", ha="center", va="center", fontsize=14, color='white')
                ax6.set_title("📋 Campaign Performance", color='white', fontsize=13, fontweight='bold')
            
            # ─── Chart 7: Expense Breakdown by Fund (Pie) ──────────────────────
            ax7 = fig.add_subplot(gs[3, 0])
            ax7.set_facecolor('#1a1a2e')
            
            expense_labels = []
            expense_values = []
            for f in fund_data:
                if f["total_expenses"] > 0:
                    name = f["fund_name"]
                    if len(name) > 12:
                        name = name[:10] + ".."
                    expense_labels.append(name)
                    expense_values.append(f["total_expenses"])
            
            if expense_values:
                colors_pie2 = ['#f44336', '#FF5722', '#FF9800', '#9C27B0', '#E91E63', '#795548']
                colors_pie2 = colors_pie2[:len(expense_values)]
                ax7.pie(expense_values, labels=expense_labels, autopct='%1.1f%%',
                        colors=colors_pie2, startangle=90,
                        textprops={'color': 'white', 'fontsize': 9})
                ax7.set_title("📤 Expense Breakdown", color='white', fontsize=13, fontweight='bold')
            else:
                ax7.text(0.5, 0.5, "No data", ha="center", va="center", fontsize=14, color='white')
                ax7.set_title("📤 Expense Breakdown", color='white', fontsize=13, fontweight='bold')
            
            # ─── Chart 8: Daily Collection (Last 7 Days) ──────────────────────
            ax8 = fig.add_subplot(gs[3, 1])
            ax8.set_facecolor('#2a2a3d')
            
            dates, daily_amounts = self.get_daily_collection(7)
            date_labels = [d[5:] for d in dates]
            
            bars = ax8.bar(date_labels, daily_amounts, color='#00BCD4')
            ax8.set_xlabel("Date", color='white', fontsize=10)
            ax8.set_ylabel("Collection (Rs.)", color='white', fontsize=10)
            ax8.set_title("📅 Daily Collection (Last 7 Days)", color='white', fontsize=13, fontweight='bold')
            ax8.tick_params(colors='white')
            for spine in ax8.spines.values():
                spine.set_color('#555')
            
            # ─── Chart 9: Monthly Collection Trends ─────────────────────────────
            ax9 = fig.add_subplot(gs[4, 0])
            ax9.set_facecolor('#2a2a3d')
            
            months, month_amounts = self.get_monthly_collection()
            
            if months:
                ax9.plot(months, month_amounts, marker='o', color='#FF9800', linewidth=2, markersize=8)
                ax9.fill_between(months, month_amounts, color='#FF9800', alpha=0.2)
                ax9.set_xlabel("Month", color='white', fontsize=10)
                ax9.set_ylabel("Collection (Rs.)", color='white', fontsize=10)
                ax9.set_title("📈 Monthly Collection Trend", color='white', fontsize=13, fontweight='bold')
                ax9.tick_params(colors='white')
                ax9.set_xticklabels(months, rotation=25, ha="right", color='white', fontsize=8)
                for spine in ax9.spines.values():
                    spine.set_color('#555')
            else:
                ax9.text(0.5, 0.5, "No data", ha="center", va="center", fontsize=14, color='white')
                ax9.set_title("📈 Monthly Collection Trend", color='white', fontsize=13, fontweight='bold')
            
            # ─── Chart 10: Fund Health Status (Pie) ────────────────────────────
            ax10 = fig.add_subplot(gs[4, 1])
            ax10.set_facecolor('#1a1a2e')
            
            profitable = len([f for f in fund_data if f["balance"] > 0])
            loss = len([f for f in fund_data if f["balance"] < 0])
            break_even = len([f for f in fund_data if f["balance"] == 0])
            
            if profitable > 0 or loss > 0 or break_even > 0:
                health_labels = ['✅ Profitable', '❌ Loss', '⚖️ Break-even']
                health_values = [profitable, loss, break_even]
                health_colors = ['#4CAF50', '#f44336', '#FF9800']
                
                filtered_labels = []
                filtered_values = []
                filtered_colors = []
                for i, val in enumerate(health_values):
                    if val > 0:
                        filtered_labels.append(health_labels[i])
                        filtered_values.append(val)
                        filtered_colors.append(health_colors[i])
                
                if filtered_values:
                    ax10.pie(filtered_values, labels=filtered_labels, autopct='%1.1f%%',
                            colors=filtered_colors, startangle=90,
                            textprops={'color': 'white', 'fontsize': 10})
                    ax10.set_title(f"🏥 Fund Health Status\n(Total: {len(fund_data)} Funds)", 
                                 color='white', fontsize=13, fontweight='bold')
                else:
                    ax10.text(0.5, 0.5, "No data", ha="center", va="center", fontsize=14, color='white')
                    ax10.set_title("🏥 Fund Health Status", color='white', fontsize=13, fontweight='bold')
            else:
                ax10.text(0.5, 0.5, "No fund data", ha="center", va="center", fontsize=14, color='white')
                ax10.set_title("🏥 Fund Health Status", color='white', fontsize=13, fontweight='bold')
            
            plt.tight_layout()
            
            # ─── Embed in Tkinter ──────────────────────────────────────────
            canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
            
            plt.close(fig)
            
            self.generate_btn.configure(
                state="normal", 
                text="🔄 Refresh Charts",
                fg_color="#4CAF50",
                hover_color="#388E3C"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate charts: {str(e)}")
            self.generate_btn.configure(state="normal", text="📊 Generate Complete Dashboard")