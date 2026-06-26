# src/views/students/student_edit.py
import customtkinter as ctk
from tkinter import messagebox
from src.controllers.student_controller import update_student, get_student_by_id
from src.controllers.academic_controller import get_active_sessions, get_active_programs, get_active_shifts, get_active_sections


class StudentEdit(ctk.CTkFrame):
    def __init__(self, master, student_id):
        super().__init__(master)
        self.student_id = student_id
        self.student = get_student_by_id(student_id)
        
        if not self.student:
            messagebox.showerror("Error", "Student not found")
            self.go_back()
            return
        
        self.create_header()
        self.create_form()
        self.load_dropdowns()
        self.populate_form()
    
    def create_header(self):
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            header, 
            text="✏️ Edit Student", 
            font=("Arial", 24, "bold")
        ).pack(side="left")
        
        ctk.CTkLabel(
            header, 
            text=f"Editing: {self.student.get('student_name', '')}", 
            font=("Arial", 12),
            text_color="gray"
        ).pack(side="left", padx=20)
    
    def create_form(self):
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # ─── Row 1: Roll Number (Read-only) ────────────────────────────
        ctk.CTkLabel(form_frame, text="Roll Number", font=("Arial", 13)).grid(
            row=0, column=0, padx=10, pady=10, sticky="w")
        self.roll_label = ctk.CTkLabel(
            form_frame, 
            text=self.student.get("roll_number", ""), 
            font=("Arial", 13, "bold"),
            text_color="#4fc3f7"
        )
        self.roll_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # ─── Row 2: Student Name ──────────────────────────────────────
        ctk.CTkLabel(form_frame, text="Student Name *", font=("Arial", 13)).grid(
            row=1, column=0, padx=10, pady=10, sticky="w")
        self.name_entry = ctk.CTkEntry(form_frame, width=300)
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
        
        # ─── Buttons ─────────────────────────────────────────────────────
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=9, column=0, columnspan=2, pady=30)
        
        self.save_btn = ctk.CTkButton(
            btn_frame, 
            text="💾 Save Changes", 
            command=self.save_student,
            fg_color="#0f9d58",
            width=200,
            height=40,
            font=("Arial", 14, "bold")
        )
        self.save_btn.pack(side="left", padx=10)
        
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
        """Load all dropdown values from database"""
        try:
            # Load Programs
            programs = get_active_programs()
            program_names = [p["program_name"] for p in programs] if programs else ["No programs found"]
            self.program_combo.configure(values=program_names)
            
            # Load Sessions
            sessions = get_active_sessions()
            session_names = [s["session_name"] for s in sessions] if sessions else ["No sessions found"]
            self.session_combo.configure(values=session_names)
            
            # Load Sections
            sections = get_active_sections()
            section_names = [s["section_name"] for s in sections] if sections else ["No sections found"]
            self.section_combo.configure(values=section_names)
            
            # Load Shifts
            shifts = get_active_shifts()
            shift_names = [s["shift_name"] for s in shifts] if shifts else ["No shifts found"]
            self.shift_combo.configure(values=shift_names)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")
    
    def populate_form(self):
        """Populate form with student data"""
        if not self.student:
            return
        
        self.name_entry.insert(0, self.student.get("student_name", ""))
        self.phone_entry.insert(0, self.student.get("phone", ""))
        self.email_entry.insert(0, self.student.get("email", ""))
        self.semester_combo.set(str(self.student.get("semester", 1)))
        
        # Set program
        program = self.student.get("program_name", "")
        if program:
            self.program_combo.set(program)
        
        # Set session
        session = self.student.get("session_name", "")
        if session:
            self.session_combo.set(session)
        
        # Set section
        section = self.student.get("section_name", "")
        if section:
            self.section_combo.set(section)
        
        # Set shift
        shift = self.student.get("shift_name", "")
        if shift:
            self.shift_combo.set(shift)
    
    def save_student(self):
        """Save student changes"""
        student_name = self.name_entry.get().strip()
        program_name = self.program_combo.get()
        session_name = self.session_combo.get()
        semester = self.semester_combo.get()
        section_name = self.section_combo.get()
        shift_name = self.shift_combo.get()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        
        # Validate
        if not student_name:
            messagebox.showerror("Error", "Student name is required")
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
            messagebox.showerror("Error", "Invalid program or session")
            return
        
        # Prepare data
        student_data = {
            "student_name": student_name,
            "program_id": program_id,
            "session_id": session_id,
            "semester": semester,
            "section_id": section_id,
            "shift_id": shift_id,
            "phone": phone,
            "email": email
        }
        
        try:
            update_student(self.student_id, student_data)
            messagebox.showinfo("Success", "✅ Student updated successfully!")
            self.go_back()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update student: {e}")
    
    def go_back(self):
        """Go back to student list"""
        from src.views.students.student_list import StudentList
        parent = self.master
        while parent:
            if hasattr(parent, 'show_view'):
                parent.show_view(StudentList)
                break
            parent = parent.master