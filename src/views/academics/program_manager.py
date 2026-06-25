# src/views/academics/program_manager.py
import customtkinter as ctk
from tkinter import messagebox
from src.controllers.academic_controller import (
    create_program,
    get_all_programs,
    delete_program,
    toggle_program_status
)


class ProgramManager(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.create_header()
        self.create_form()
        self.create_table()
        self.load_programs()
    
    def create_header(self):
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            header, 
            text="📚 Program Management", 
            font=("Arial", 24, "bold")
        ).pack(side="left")
        
        ctk.CTkLabel(
            header, 
            text="Manage academic programs (BSCS, BSSE, BSIT...)", 
            font=("Arial", 12),
            text_color="gray"
        ).pack(side="left", padx=20)
    
    def create_form(self):
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            form_frame, 
            text="Add New Program:", 
            font=("Arial", 14, "bold")
        ).pack(side="left", padx=10)
        
        self.name_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Program Name (e.g., Computer Science)",
            width=200
        )
        self.name_entry.pack(side="left", padx=5)
        
        self.code_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Code (e.g., BSCS)",
            width=120
        )
        self.code_entry.pack(side="left", padx=5)
        
        self.add_btn = ctk.CTkButton(
            form_frame, 
            text="➕ Add Program",
            command=self.add_program,
            fg_color="#1a73e8"
        )
        self.add_btn.pack(side="left", padx=10)
    
    def create_table(self):
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Headers
        headers_frame = ctk.CTkFrame(table_frame, fg_color="#2a2a3d")
        headers_frame.pack(fill="x", pady=(0, 2))
        
        headers = ["ID", "Program Name", "Code", "Status", "Actions"]
        widths = [50, 250, 120, 100, 200]
        
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
    
    def load_programs(self):
        for widget in self.table_body.winfo_children():
            widget.destroy()
        
        programs = get_all_programs()
        
        if not programs:
            ctk.CTkLabel(
                self.table_body, 
                text="No programs found. Add your first program above!",
                font=("Arial", 14),
                text_color="gray"
            ).pack(pady=20)
            return
        
        for program in programs:
            self.create_row(program)
    
    def create_row(self, program):
        row = ctk.CTkFrame(self.table_body)
        row.pack(fill="x", pady=2)
        
        ctk.CTkLabel(row, text=str(program["id"]), width=50).pack(side="left", padx=10, pady=5)
        ctk.CTkLabel(row, text=program["program_name"], width=250).pack(side="left", padx=10, pady=5)
        ctk.CTkLabel(row, text=program["program_code"], width=120, font=("Arial", 13, "bold")).pack(side="left", padx=10, pady=5)
        
        status_text = "✅ Active" if program["is_active"] else "❌ Inactive"
        status_color = "#0f9d58" if program["is_active"] else "#db4437"
        ctk.CTkLabel(row, text=status_text, width=100, text_color=status_color).pack(side="left", padx=10, pady=5)
        
        actions_frame = ctk.CTkFrame(row, fg_color="transparent")
        actions_frame.pack(side="right", padx=10, pady=5)
        
        toggle_text = "Deactivate" if program["is_active"] else "Activate"
        toggle_color = "#db4437" if program["is_active"] else "#0f9d58"
        ctk.CTkButton(
            actions_frame,
            text=toggle_text,
            command=lambda: self.toggle_status(program["id"]),
            fg_color=toggle_color,
            width=80,
            height=28
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            actions_frame,
            text="🗑 Delete",
            command=lambda: self.delete_program(program["id"]),
            fg_color="#db4437",
            width=80,
            height=28
        ).pack(side="left", padx=5)
    
    def add_program(self):
        name = self.name_entry.get().strip()
        code = self.code_entry.get().strip().upper()
        
        if not name or not code:
            messagebox.showerror("Error", "Please enter both name and code")
            return
        
        try:
            create_program(name, code)
            self.name_entry.delete(0, "end")
            self.code_entry.delete(0, "end")
            self.load_programs()
            messagebox.showinfo("Success", f"Program '{name}' added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def delete_program(self, program_id):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this program?"):
            try:
                delete_program(program_id)
                self.load_programs()
                messagebox.showinfo("Success", "Program deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def toggle_status(self, program_id):
        try:
            toggle_program_status(program_id)
            self.load_programs()
        except Exception as e:
            messagebox.showerror("Error", str(e))