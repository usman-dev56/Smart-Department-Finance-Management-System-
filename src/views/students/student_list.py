# src/views/students/student_list.py
import customtkinter as ctk
from tkinter import messagebox
from src.controllers.student_controller import get_all_students, search_students, delete_student, get_students_by_program
from src.controllers.academic_controller import get_active_sessions, get_active_programs


class StudentList(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.current_students = []
        self.create_header()
        self.create_filters()
        self.create_table()
        self.load_students()
    
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="#021635")
        header.pack(fill="x", padx=10, pady=(30,25))
        
        ctk.CTkLabel(
            header, 
            text=" Student Management", 
            font=("Arial", 33, "bold"),
           
        ).pack(side="left")
        
        ctk.CTkLabel(
            header, 
            text="View, filter, and manage students", 
            font=("Arial", 20),
            text_color="gray"
        ).pack(side="left", padx=50)
    
    def create_filters(self):
        """Create filter section with dropdowns"""
        filter_frame = ctk.CTkFrame(self)
        filter_frame.pack(fill="x", padx=20, pady=10)
        
        # ─── Row 1: Search Bar ──────────────────────────────────────────
        search_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        search_frame.pack(fill="x", pady=5)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Search by name or roll number...",
            width=350
        )
        self.search_entry.pack(side="left", padx=5)
        
        self.search_btn = ctk.CTkButton(
            search_frame,
            text="Search",
            command=self.search_students,
            fg_color="#1a73e8",
            width=80
        )
        self.search_btn.pack(side="left", padx=5)
        
        self.clear_btn = ctk.CTkButton(
            search_frame,
            text="Clear",
            command=self.load_students,
            fg_color="gray",
            width=80
        )
        self.clear_btn.pack(side="left", padx=5)

         # Add Student Button
        self.add_btn = ctk.CTkButton(
            search_frame,
            text="➕ Add Student",
            font=("Arial", 15, "bold"),
            command=self.open_registration,
            fg_color="#1a73e8",
            width=120
        )
        self.add_btn.pack(side="right", padx=10)

        
        
        # ─── Row 2: Filters ─────────────────────────────────────────────
        filters_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        filters_frame.pack(fill="x", pady=5)
        
        # Session Filter
        ctk.CTkLabel(
            filters_frame, 
            text="Session:", 
            font=("Arial", 13, "bold")
        ).pack(side="left", padx=5)
        
        self.session_filter = ctk.CTkComboBox(
            filters_frame,
            values=["All Sessions"],
            width=120
        )
        self.session_filter.set("All Sessions")
        self.session_filter.pack(side="left", padx=5)
        self.session_filter.bind("<<ComboboxSelected>>", self.apply_filters)
        
        # Semester Filter
        ctk.CTkLabel(
            filters_frame, 
            text="Semester:", 
            font=("Arial", 13, "bold")
        ).pack(side="left", padx=(20, 5))
        
        self.semester_filter = ctk.CTkComboBox(
            filters_frame,
            values=["All Semesters", "1", "2", "3", "4", "5", "6", "7", "8"],
            width=100
        )
        self.semester_filter.set("All Semesters")
        self.semester_filter.pack(side="left", padx=5)
        self.semester_filter.bind("<<ComboboxSelected>>", self.apply_filters)
        
        # Program Filter
        ctk.CTkLabel(
            filters_frame, 
            text="Program:", 
            font=("Arial", 13, "bold")
        ).pack(side="left", padx=(20, 5))
        
        self.program_filter = ctk.CTkComboBox(
            filters_frame,
            values=["All Programs"],
            width=120
        )
        self.program_filter.set("All Programs")
        self.program_filter.pack(side="left", padx=5)
        self.program_filter.bind("<<ComboboxSelected>>", self.apply_filters)
        
        # Filter Button
        self.filter_btn = ctk.CTkButton(
            filters_frame,
            text="🔄 Apply Filters",
            command=self.apply_filters,
            fg_color="#0f9d58",
            width=120
        )
        self.filter_btn.pack(side="left", padx=20)
        
        # Total count
        self.count_label = ctk.CTkLabel(
            filters_frame,
            text="Total: 0 students",
            font=("Arial", 12),
            text_color="gray"
        )
        self.count_label.pack(side="right", padx=10)
        
        # Load filter options
        self.load_filter_options()
    
    def load_filter_options(self):
        """Load sessions and programs into filter dropdowns"""
        try:
            # Load Sessions
            sessions = get_active_sessions()
            session_names = ["All Sessions"] + [s["session_name"] for s in sessions] if sessions else ["All Sessions"]
            self.session_filter.configure(values=session_names)
            self.session_filter.set("All Sessions")
            
            # Load Programs
            programs = get_active_programs()
            program_names = ["All Programs"] + [p["program_name"] for p in programs] if programs else ["All Programs"]
            self.program_filter.configure(values=program_names)
            self.program_filter.set("All Programs")
            
        except Exception as e:
            print(f"Error loading filters: {e}")
    
    def create_table(self):
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Headers
        headers_frame = ctk.CTkFrame(table_frame, fg_color="#2a2a3d")
        headers_frame.pack(fill="x", pady=(0, 2))
        
        headers = ["Roll No", "Name", "Program", "Session", "Semester", "Section", "Shift", "Actions"]
        widths = [100, 180, 120, 80, 70, 70, 80, 150]
        
        for i, (header, width) in enumerate(zip(headers, widths)):
            ctk.CTkLabel(
                headers_frame, 
                text=header, 
                font=("Arial", 12, "bold"),
                width=width
            ).pack(side="left", padx=10, pady=5)
        
        self.table_body = ctk.CTkScrollableFrame(
            table_frame, 
            fg_color="transparent"
        )
        self.table_body.pack(fill="both", expand=True)
    
    def load_students(self):
        """Load all students"""
        self.search_entry.delete(0, "end")
        self.session_filter.set("All Sessions")
        self.semester_filter.set("All Semesters")
        self.program_filter.set("All Programs")
        students = get_all_students()
        self.current_students = students
        self.display_students(students)
    
    def search_students(self):
        """Search students by query"""
        query = self.search_entry.get().strip()
        if not query:
            self.load_students()
            return
        
        students = search_students(query)
        self.current_students = students
        self.display_students(students)
    
    def apply_filters(self, event=None):
        """Apply session, semester, and program filters"""
        session = self.session_filter.get()
        semester = self.semester_filter.get()
        program = self.program_filter.get()
        
        # Start with all students
        students = get_all_students()
        
        # Filter by Session
        if session != "All Sessions":
            students = [s for s in students if s.get("session_name") == session]
        
        # Filter by Semester
        if semester != "All Semesters":
            try:
                sem_int = int(semester)
                students = [s for s in students if s.get("semester") == sem_int]
            except ValueError:
                pass
        
        # Filter by Program
        if program != "All Programs":
            students = [s for s in students if s.get("program_name") == program]
        
        self.current_students = students
        self.display_students(students)
    
    def display_students(self, students):
        """Display students in the table"""
        # Clear table
        for widget in self.table_body.winfo_children():
            widget.destroy()
        
        if not students:
            ctk.CTkLabel(
                self.table_body, 
                text="No students found", 
                font=("Arial", 14),
                text_color="gray"
            ).pack(pady=20)
            self.count_label.configure(text="Total: 0 students")
            return
        
        for student in students:
            self.create_row(student)
        
        self.count_label.configure(text=f"Total: {len(students)} students")
    
    def create_row(self, student):
        """Create a row for a student"""
        row = ctk.CTkFrame(self.table_body)
        row.pack(fill="x", pady=2)
        
        # Roll Number
        ctk.CTkLabel(
            row, 
            text=student.get("roll_number", ""), 
            width=100,
            font=("Arial", 11, "bold")
        ).pack(side="left", padx=10, pady=5)
        
        # Name
        ctk.CTkLabel(
            row, 
            text=student.get("student_name", ""), 
            width=180
        ).pack(side="left", padx=10, pady=5)
        
        # Program
        ctk.CTkLabel(
            row, 
            text=student.get("program_name", ""), 
            width=120
        ).pack(side="left", padx=10, pady=5)
        
        # Session
        ctk.CTkLabel(
            row, 
            text=student.get("session_name", ""), 
            width=80
        ).pack(side="left", padx=10, pady=5)
        
        # Semester
        ctk.CTkLabel(
            row, 
            text=str(student.get("semester", "")), 
            width=70
        ).pack(side="left", padx=10, pady=5)
        
        # Section
        ctk.CTkLabel(
            row, 
            text=student.get("section_name", ""), 
            width=70
        ).pack(side="left", padx=10, pady=5)
        
        # Shift
        ctk.CTkLabel(
            row, 
            text=student.get("shift_name", ""), 
            width=80
        ).pack(side="left", padx=10, pady=5)
        
        # ─── Actions ──────────────────────────────────────────────────────
        actions_frame = ctk.CTkFrame(row, fg_color="transparent")
        actions_frame.pack(side="right", padx=10, pady=5)
        
        # View Button
        ctk.CTkButton(
            actions_frame,
            text="👁 View",
            command=lambda s=student: self.view_student(s),
            fg_color="#1a73e8",
            width=60,
            height=28
        ).pack(side="left", padx=2)
        
        # Delete Button
        ctk.CTkButton(
            actions_frame,
            text="🗑 Delete",
            command=lambda s=student: self.delete_student(s),
            fg_color="#db4437",
            width=60,
            height=28
        ).pack(side="left", padx=2)
        
        # ─── Quick Pay Button ──────────────────────────────────────────
        ctk.CTkButton(
            actions_frame,
            text="💰 Pay",
            command=lambda s=student: self.quick_pay(s),
            fg_color="#0f9d58",
            width=55,
            height=28
        ).pack(side="left", padx=2)
    
    def view_student(self, student):
        """Show student details"""
        messagebox.showinfo(
            "Student Details",
            f"📋 Student Details\n\n"
            f"Name: {student.get('student_name', '')}\n"
            f"Roll No: {student.get('roll_number', '')}\n"
            f"Program: {student.get('program_name', '')}\n"
            f"Session: {student.get('session_name', '')}\n"
            f"Semester: {student.get('semester', '')}\n"
            f"Section: {student.get('section_name', '')}\n"
            f"Shift: {student.get('shift_name', '')}\n"
            f"Phone: {student.get('phone', 'N/A')}\n"
            f"Email: {student.get('email', 'N/A')}"
        )
    
    def delete_student(self, student):
        """Delete a student"""
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {student.get('student_name')}?"):
            try:
                delete_student(student["id"])
                self.apply_filters()
                messagebox.showinfo("Success", "Student deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def quick_pay(self, student):
        """Quick pay for a student"""
        from src.views.payments.collect_payment import CollectPayment
        
        parent = self.master
        while parent:
            if hasattr(parent, 'show_view'):
                parent.show_view(CollectPayment, student_id=student["id"])
                break
            parent = parent.master
    
    def open_registration(self):
        """Open student registration view"""
        from src.views.students.student_registration import StudentRegistration
        
        parent = self.master
        while parent:
            if hasattr(parent, 'show_view'):
                parent.show_view(StudentRegistration)
                break
            parent = parent.master