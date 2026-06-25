# src/views/students/student_registration.py
import customtkinter as ctk
from tkinter import messagebox
from src.controllers.student_controller import register_student_with_roll
from src.controllers.academic_controller import get_active_sessions, get_active_programs, get_active_shifts, get_active_sections


class StudentRegistration(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.create_header()
        self.create_form()
        self.load_dropdowns()
    
    def create_header(self):
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            header, 
            text="👨‍🎓 Student Registration", 
            font=("Arial", 24, "bold")
        ).pack(side="left")
        
        ctk.CTkLabel(
            header, 
            text="Register new students with manual roll number entry", 
            font=("Arial", 12),
            text_color="gray"
        ).pack(side="left", padx=20)
    
    def create_form(self):
        # Main form frame
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # ─── Row 1: Roll Number ──────────────────────────────────────
        ctk.CTkLabel(form_frame, text="Roll Number *", font=("Arial", 13)).grid(
            row=0, column=0, padx=10, pady=10, sticky="w")
        self.roll_entry = ctk.CTkEntry(form_frame, width=300, placeholder_text="e.g., BSCS-2024-001")
        self.roll_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        ctk.CTkLabel(
            form_frame, 
            text="Format: PROGRAM-SESSION-SEQUENCE (e.g., BSCS-2024-001)", 
            font=("Arial", 10),
            text_color="gray"
        ).grid(row=0, column=2, padx=10, pady=10, sticky="w")
        
        # ─── Row 2: Student Name ──────────────────────────────────────
        ctk.CTkLabel(form_frame, text="Student Name *", font=("Arial", 13)).grid(
            row=1, column=0, padx=10, pady=10, sticky="w")
        self.name_entry = ctk.CTkEntry(form_frame, width=300, placeholder_text="Enter full name")
        self.name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # ─── Row 3: Program ────────────────────────────────────────────
        ctk.CTkLabel(form_frame, text="Program *", font=("Arial", 13)).grid(
            row=2, column=0, padx=10, pady=10, sticky="w")
        self.program_combo = ctk.CTkComboBox(form_frame, width=300, values=["Loading..."])
        self.program_combo.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        # ─── Row 4: Session ────────────────────────────────────────────
        ctk.CTkLabel(form_frame, text="Session *", font=("Arial", 13)).grid(
            row=3, column=0, padx=10, pady=10, sticky="w")
        self.session_combo = ctk.CTkComboBox(form_frame, width=300, values=["Loading..."])
        self.session_combo.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        
        # ─── Row 5: Semester ───────────────────────────────────────────
        ctk.CTkLabel(form_frame, text="Semester *", font=("Arial", 13)).grid(
            row=4, column=0, padx=10, pady=10, sticky="w")
        self.semester_combo = ctk.CTkComboBox(
            form_frame, 
            width=300, 
            values=["1", "2", "3", "4", "5", "6", "7", "8"]
        )
        self.semester_combo.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        
        # ─── Row 6: Section ────────────────────────────────────────────
        ctk.CTkLabel(form_frame, text="Section", font=("Arial", 13)).grid(
            row=5, column=0, padx=10, pady=10, sticky="w")
        self.section_combo = ctk.CTkComboBox(form_frame, width=300, values=["Loading..."])
        self.section_combo.grid(row=5, column=1, padx=10, pady=10, sticky="w")
        
        # ─── Row 7: Shift ──────────────────────────────────────────────
        ctk.CTkLabel(form_frame, text="Shift", font=("Arial", 13)).grid(
            row=6, column=0, padx=10, pady=10, sticky="w")
        self.shift_combo = ctk.CTkComboBox(form_frame, width=300, values=["Loading..."])
        self.shift_combo.grid(row=6, column=1, padx=10, pady=10, sticky="w")
        
        # ─── Row 8: Phone (Optional) ──────────────────────────────────
        ctk.CTkLabel(form_frame, text="Phone (Optional)", font=("Arial", 13)).grid(
            row=7, column=0, padx=10, pady=10, sticky="w")
        self.phone_entry = ctk.CTkEntry(form_frame, width=300, placeholder_text="e.g., 03XX-XXXXXXX")
        self.phone_entry.grid(row=7, column=1, padx=10, pady=10, sticky="w")
        
        # ─── Row 9: Email (Optional) ──────────────────────────────────
        ctk.CTkLabel(form_frame, text="Email (Optional)", font=("Arial", 13)).grid(
            row=8, column=0, padx=10, pady=10, sticky="w")
        self.email_entry = ctk.CTkEntry(form_frame, width=300, placeholder_text="student@email.com")
        self.email_entry.grid(row=8, column=1, padx=10, pady=10, sticky="w")
        
        # ─── Submit Button ─────────────────────────────────────────────
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=9, column=0, columnspan=2, pady=30)
        
        self.submit_btn = ctk.CTkButton(
            btn_frame, 
            text="✅ Register Student", 
            command=self.register_student,
            fg_color="#1a73e8",
            width=200,
            height=40,
            font=("Arial", 14, "bold")
        )
        self.submit_btn.pack()
    
    def load_dropdowns(self):
        """Load all dropdown values from database"""
        try:
            # Load Programs
            programs = get_active_programs()
            program_names = [p["program_name"] for p in programs] if programs else ["No programs found"]
            self.program_combo.configure(values=program_names)
            if program_names:
                self.program_combo.set(program_names[0])
            
            # Load Sessions
            sessions = get_active_sessions()
            session_names = [s["session_name"] for s in sessions] if sessions else ["No sessions found"]
            self.session_combo.configure(values=session_names)
            if session_names:
                self.session_combo.set(session_names[0])
            
            # Load Sections
            sections = get_active_sections()
            section_names = [s["section_name"] for s in sections] if sections else ["No sections found"]
            self.section_combo.configure(values=section_names)
            if section_names:
                self.section_combo.set(section_names[0])
            
            # Load Shifts
            shifts = get_active_shifts()
            shift_names = [s["shift_name"] for s in shifts] if shifts else ["No shifts found"]
            self.shift_combo.configure(values=shift_names)
            if shift_names:
                self.shift_combo.set(shift_names[0])
            
            # Set default semester
            self.semester_combo.set("1")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")
    
    def register_student(self):
        """Register a new student with manual roll number"""
        # Get form data
        roll_number = self.roll_entry.get().strip()
        student_name = self.name_entry.get().strip()
        program_name = self.program_combo.get()
        session_name = self.session_combo.get()
        semester = self.semester_combo.get()
        section_name = self.section_combo.get()
        shift_name = self.shift_combo.get()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        
        # Validate
        if not roll_number:
            messagebox.showerror("Error", "Roll Number is required")
            self.roll_entry.focus()
            return
        
        if not student_name:
            messagebox.showerror("Error", "Student name is required")
            self.name_entry.focus()
            return
        
        if program_name in ["Loading...", "No programs found"]:
            messagebox.showerror("Error", "Please select a valid program")
            return
        
        if session_name in ["Loading...", "No sessions found"]:
            messagebox.showerror("Error", "Please select a valid session")
            return
        
        try:
            semester = int(semester)
            if semester < 1 or semester > 8:
                messagebox.showerror("Error", "Semester must be between 1 and 8")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid semester")
            return
        
        # Get IDs from names
        programs = get_active_programs()
        program_id = next((p["id"] for p in programs if p["program_name"] == program_name), None)
        
        sessions = get_active_sessions()
        session_id = next((s["id"] for s in sessions if s["session_name"] == session_name), None)
        
        sections = get_active_sections()
        section_id = next((s["id"] for s in sections if s["section_name"] == section_name), None)
        
        shifts = get_active_shifts()
        shift_id = next((s["id"] for s in shifts if s["shift_name"] == shift_name), None)
        
        if not program_id or not session_id:
            messagebox.showerror("Error", "Invalid program or session selected")
            return
        
        # Prepare data
        student_data = {
            "roll_number": roll_number,
            "student_name": student_name,
            "program_id": program_id,
            "session_id": session_id,
            "semester": semester,
            "section_id": section_id,
            "shift_id": shift_id,
            "phone": phone,
            "email": email,
            "department_id": 1
        }
        
        try:
            # Register student
            student_id = register_student_with_roll(student_data)
            
            # Show success
            messagebox.showinfo(
                "Success", 
                f"✅ Student registered successfully!\n\n"
                f"Name: {student_name}\n"
                f"Roll Number: {roll_number}\n"
                f"Program: {program_name}\n"
                f"Session: {session_name}\n"
                f"Semester: {semester}"
            )
            
            # ─── Redirect to Student List ──────────────────────────────────
            from src.views.students.student_list import StudentList
            parent = self.master
            while parent:
                if hasattr(parent, 'show_view'):
                    parent.show_view(StudentList)
                    break
                parent = parent.master
            
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {e}")
    
    def clear_form(self):
        """Clear all form fields"""
        self.roll_entry.delete(0, "end")
        self.name_entry.delete(0, "end")
        self.phone_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.semester_combo.set("1")
        
        # Reset dropdowns
        self.load_dropdowns()