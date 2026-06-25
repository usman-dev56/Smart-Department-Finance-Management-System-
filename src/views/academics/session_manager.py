# src/views/academics/session_manager.py
import customtkinter as ctk
from tkinter import messagebox
from src.controllers.academic_controller import (
    create_session,
    get_all_sessions,
    delete_session,
    toggle_session_status
)


class SessionManager(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.create_header()
        self.create_form()
        self.create_table()
        self.load_sessions()
    
    def create_header(self):
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            header, 
            text="📚 Session Management", 
            font=("Arial", 24, "bold")
        ).pack(side="left")
        
        ctk.CTkLabel(
            header, 
            text="Manage academic sessions (2022, 2023, 2024...)", 
            font=("Arial", 12),
            text_color="gray"
        ).pack(side="left", padx=20)
    
    def create_form(self):
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            form_frame, 
            text="Add New Session:", 
            font=("Arial", 14, "bold")
        ).pack(side="left", padx=10)
        
        self.session_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="e.g., 2024",
            width=150
        )
        self.session_entry.pack(side="left", padx=10)
        
        self.add_btn = ctk.CTkButton(
            form_frame, 
            text="➕ Add Session",
            command=self.add_session,
            fg_color="#1a73e8"
        )
        self.add_btn.pack(side="left", padx=10)
    
    def create_table(self):
        # Table Frame
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Headers
        headers_frame = ctk.CTkFrame(table_frame, fg_color="#2a2a3d")
        headers_frame.pack(fill="x", pady=(0, 2))
        
        ctk.CTkLabel(
            headers_frame, 
            text="ID", 
            font=("Arial", 12, "bold"),
            width=50
        ).pack(side="left", padx=10, pady=5)
        
        ctk.CTkLabel(
            headers_frame, 
            text="Session", 
            font=("Arial", 12, "bold"),
            width=200
        ).pack(side="left", padx=10, pady=5)
        
        ctk.CTkLabel(
            headers_frame, 
            text="Status", 
            font=("Arial", 12, "bold"),
            width=100
        ).pack(side="left", padx=10, pady=5)
        
        ctk.CTkLabel(
            headers_frame, 
            text="Actions", 
            font=("Arial", 12, "bold"),
            width=150
        ).pack(side="right", padx=10, pady=5)
        
        # Scrollable table body
        self.table_body = ctk.CTkScrollableFrame(
            table_frame, 
            fg_color="transparent"
        )
        self.table_body.pack(fill="both", expand=True)
    
    def load_sessions(self):
        # Clear existing rows
        for widget in self.table_body.winfo_children():
            widget.destroy()
        
        sessions = get_all_sessions()
        
        if not sessions:
            ctk.CTkLabel(
                self.table_body, 
                text="No sessions found. Add your first session above!",
                font=("Arial", 14),
                text_color="gray"
            ).pack(pady=20)
            return
        
        for session in sessions:
            self.create_row(session)
    
    def create_row(self, session):
        row = ctk.CTkFrame(self.table_body)
        row.pack(fill="x", pady=2)
        
        # ID
        ctk.CTkLabel(
            row, 
            text=str(session["id"]), 
            width=50
        ).pack(side="left", padx=10, pady=5)
        
        # Session Name
        ctk.CTkLabel(
            row, 
            text=session["session_name"], 
            width=200,
            font=("Arial", 13)
        ).pack(side="left", padx=10, pady=5)
        
        # Status
        status_text = "✅ Active" if session["is_active"] else "❌ Inactive"
        status_color = "#0f9d58" if session["is_active"] else "#db4437"
        ctk.CTkLabel(
            row, 
            text=status_text, 
            width=100,
            text_color=status_color
        ).pack(side="left", padx=10, pady=5)
        
        # Actions
        actions_frame = ctk.CTkFrame(row, fg_color="transparent")
        actions_frame.pack(side="right", padx=10, pady=5)
        
        # Toggle Status Button
        toggle_text = "Deactivate" if session["is_active"] else "Activate"
        toggle_color = "#db4437" if session["is_active"] else "#0f9d58"
        ctk.CTkButton(
            actions_frame,
            text=toggle_text,
            command=lambda: self.toggle_status(session["id"]),
            fg_color=toggle_color,
            width=80,
            height=28
        ).pack(side="left", padx=5)
        
        # Delete Button
        ctk.CTkButton(
            actions_frame,
            text="🗑 Delete",
            command=lambda: self.delete_session(session["id"]),
            fg_color="#db4437",
            width=80,
            height=28
        ).pack(side="left", padx=5)
    
    def add_session(self):
        session_name = self.session_entry.get().strip()
        
        if not session_name:
            messagebox.showerror("Error", "Please enter a session name")
            return
        
        try:
            create_session(session_name)
            self.session_entry.delete(0, "end")
            self.load_sessions()
            messagebox.showinfo("Success", f"Session '{session_name}' added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def delete_session(self, session_id):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this session?"):
            try:
                delete_session(session_id)
                self.load_sessions()
                messagebox.showinfo("Success", "Session deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def toggle_status(self, session_id):
        try:
            toggle_session_status(session_id)
            self.load_sessions()
        except Exception as e:
            messagebox.showerror("Error", str(e))