# src/views/academics/shift_manager.py
import customtkinter as ctk
from tkinter import messagebox
from src.controllers.academic_controller import (
    create_shift,
    get_all_shifts,
    delete_shift,
    toggle_shift_status
)


class ShiftManager(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.create_header()
        self.create_form()
        self.create_table()
        self.load_shifts()
    
    def create_header(self):
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            header, 
            text="🕐 Shift Management", 
            font=("Arial", 24, "bold")
        ).pack(side="left")
        
        ctk.CTkLabel(
            header, 
            text="Manage shifts (Morning, Evening...)", 
            font=("Arial", 12),
            text_color="gray"
        ).pack(side="left", padx=20)
    
    def create_form(self):
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            form_frame, 
            text="Add New Shift:", 
            font=("Arial", 14, "bold")
        ).pack(side="left", padx=10)
        
        self.shift_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="e.g., Morning",
            width=200
        )
        self.shift_entry.pack(side="left", padx=10)
        
        self.add_btn = ctk.CTkButton(
            form_frame, 
            text="➕ Add Shift",
            command=self.add_shift,
            fg_color="#1a73e8"
        )
        self.add_btn.pack(side="left", padx=10)
    
    def create_table(self):
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        headers_frame = ctk.CTkFrame(table_frame, fg_color="#2a2a3d")
        headers_frame.pack(fill="x", pady=(0, 2))
        
        ctk.CTkLabel(headers_frame, text="ID", width=50).pack(side="left", padx=10, pady=5)
        ctk.CTkLabel(headers_frame, text="Shift Name", width=250, font=("Arial", 12, "bold")).pack(side="left", padx=10, pady=5)
        ctk.CTkLabel(headers_frame, text="Status", width=100, font=("Arial", 12, "bold")).pack(side="left", padx=10, pady=5)
        ctk.CTkLabel(headers_frame, text="Actions", width=200, font=("Arial", 12, "bold")).pack(side="right", padx=10, pady=5)
        
        self.table_body = ctk.CTkScrollableFrame(table_frame, fg_color="transparent")
        self.table_body.pack(fill="both", expand=True)
    
    def load_shifts(self):
        for widget in self.table_body.winfo_children():
            widget.destroy()
        
        shifts = get_all_shifts()
        
        if not shifts:
            ctk.CTkLabel(
                self.table_body, 
                text="No shifts found. Add your first shift above!",
                font=("Arial", 14),
                text_color="gray"
            ).pack(pady=20)
            return
        
        for shift in shifts:
            row = ctk.CTkFrame(self.table_body)
            row.pack(fill="x", pady=2)
            
            ctk.CTkLabel(row, text=str(shift["id"]), width=50).pack(side="left", padx=10, pady=5)
            ctk.CTkLabel(row, text=shift["shift_name"], width=250, font=("Arial", 13)).pack(side="left", padx=10, pady=5)
            
            status_text = "✅ Active" if shift["is_active"] else "❌ Inactive"
            status_color = "#0f9d58" if shift["is_active"] else "#db4437"
            ctk.CTkLabel(row, text=status_text, width=100, text_color=status_color).pack(side="left", padx=10, pady=5)
            
            actions_frame = ctk.CTkFrame(row, fg_color="transparent")
            actions_frame.pack(side="right", padx=10, pady=5)
            
            toggle_text = "Deactivate" if shift["is_active"] else "Activate"
            toggle_color = "#db4437" if shift["is_active"] else "#0f9d58"
            ctk.CTkButton(
                actions_frame,
                text=toggle_text,
                command=lambda: self.toggle_status(shift["id"]),
                fg_color=toggle_color,
                width=80,
                height=28
            ).pack(side="left", padx=5)
            
            ctk.CTkButton(
                actions_frame,
                text="🗑 Delete",
                command=lambda: self.delete_shift(shift["id"]),
                fg_color="#db4437",
                width=80,
                height=28
            ).pack(side="left", padx=5)
    
    def add_shift(self):
        shift_name = self.shift_entry.get().strip()
        if not shift_name:
            messagebox.showerror("Error", "Please enter a shift name")
            return
        
        try:
            create_shift(shift_name)
            self.shift_entry.delete(0, "end")
            self.load_shifts()
            messagebox.showinfo("Success", f"Shift '{shift_name}' added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def delete_shift(self, shift_id):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this shift?"):
            try:
                delete_shift(shift_id)
                self.load_shifts()
                messagebox.showinfo("Success", "Shift deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def toggle_status(self, shift_id):
        try:
            toggle_shift_status(shift_id)
            self.load_shifts()
        except Exception as e:
            messagebox.showerror("Error", str(e))