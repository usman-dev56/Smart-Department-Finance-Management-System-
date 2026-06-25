"""
First Run Wizard - Shown on first installation to set up department.
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from src.controllers.department_controller import save_department
from src.core.constants import COLORS


class FirstRunWizard(ctk.CTkFrame):
    STEPS = [
        "University Info",
        "Department Info",
        "Contact Details",
        "Receipt Settings",
        "Done",
    ]

    def __init__(self, master, on_complete):
        super().__init__(master)
        self.on_complete = on_complete
        self.data = {}
        self.step = 0
        self.logo_path = None

        self._build_layout()
        self._render_step()

    def _build_layout(self):
        self.configure(fg_color="transparent")

        # Outer centering
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.card = ctk.CTkFrame(self, width=540, height=480, corner_radius=16)
        self.card.grid(row=0, column=0)
        self.card.grid_propagate(False)
        self.card.columnconfigure(0, weight=1)

        # Progress bar
        self.progress = ctk.CTkProgressBar(self.card, width=460)
        self.progress.grid(row=0, column=0, padx=40, pady=(30, 0))
        self.progress.set(0)

        self.step_label = ctk.CTkLabel(self.card, text="", text_color="gray")
        self.step_label.grid(row=1, column=0, pady=(4, 0))

        self.title_lbl = ctk.CTkLabel(self.card, text="", font=ctk.CTkFont(size=22, weight="bold"))
        self.title_lbl.grid(row=2, column=0, pady=(16, 0))

        self.content_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.content_frame.grid(row=3, column=0, padx=40, pady=10, sticky="ew")
        self.content_frame.columnconfigure(0, weight=1)

        # Nav buttons
        btn_row = ctk.CTkFrame(self.card, fg_color="transparent")
        btn_row.grid(row=4, column=0, padx=40, pady=16, sticky="ew")
        btn_row.columnconfigure(1, weight=1)

        self.back_btn = ctk.CTkButton(btn_row, text="← Back", width=100,
                                       fg_color="gray", command=self._back)
        self.back_btn.grid(row=0, column=0, sticky="w")

        self.next_btn = ctk.CTkButton(btn_row, text="Next →", width=120,
                                       command=self._next)
        self.next_btn.grid(row=0, column=1, sticky="e")

    def _clear_content(self):
        for w in self.content_frame.winfo_children():
            w.destroy()

    def _field(self, label: str, placeholder: str = "", row: int = 0) -> ctk.CTkEntry:
        ctk.CTkLabel(self.content_frame, text=label, anchor="w").grid(
            row=row * 2, column=0, sticky="ew", pady=(8, 0))
        entry = ctk.CTkEntry(self.content_frame, placeholder_text=placeholder, height=36)
        entry.grid(row=row * 2 + 1, column=0, sticky="ew")
        return entry

    def _render_step(self):
        self._clear_content()
        progress = (self.step) / (len(self.STEPS) - 1)
        self.progress.set(progress)
        self.step_label.configure(text=f"Step {self.step + 1} of {len(self.STEPS)}")
        self.back_btn.configure(state="normal" if self.step > 0 else "disabled")

        step_name = self.STEPS[self.step]
        self.title_lbl.configure(text=step_name)

        if self.step == 0:
            self.e_uni = self._field("University Name *", "e.g. Government College University", 0)
        elif self.step == 1:
            self.e_dept = self._field("Department Name *", "e.g. Computer Science", 0)
            self.e_code = self._field("Department Code *", "e.g. CS", 1)
            logo_btn = ctk.CTkButton(self.content_frame, text="📁 Upload Logo (optional)",
                                      command=self._pick_logo)
            logo_btn.grid(row=4, column=0, sticky="ew", pady=(12, 0))
            self.logo_lbl = ctk.CTkLabel(self.content_frame, text="No logo selected", text_color="gray")
            self.logo_lbl.grid(row=5, column=0, pady=(2, 0))
        elif self.step == 2:
            self.e_email = self._field("Email", "dept@university.edu", 0)
            self.e_phone = self._field("Phone", "+92-xxx-xxxxxxx", 1)
            self.e_addr = self._field("Address", "Campus address", 2)
        elif self.step == 3:
            self.e_prefix = self._field("Receipt Prefix *", "e.g. CS or MATH", 0)
            ctk.CTkLabel(self.content_frame, text="Receipt numbers will look like: CS-00001",
                          text_color="gray", font=ctk.CTkFont(size=11)).grid(row=2, column=0, pady=(4,0))
            self.next_btn.configure(text="Finish ✓")
        elif self.step == 4:
            self._save_department()
            ctk.CTkLabel(self.content_frame,
                          text="✅  Setup Complete!\n\nYour department has been configured.\nClick Launch to start using SDFFMS.",
                          font=ctk.CTkFont(size=14), justify="center").grid(row=0, column=0, pady=30)
            self.next_btn.configure(text="🚀 Launch")

    def _pick_logo(self):
        path = filedialog.askopenfilename(
            title="Select Logo",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.ico")]
        )
        if path:
            self.logo_path = path
            self.logo_lbl.configure(text=f"✓ {path.split('/')[-1]}", text_color="green")

    def _collect_step_data(self) -> bool:
        if self.step == 0:
            uni = self.e_uni.get().strip()
            if not uni:
                messagebox.showwarning("Required", "University name is required.")
                return False
            self.data["university_name"] = uni
        elif self.step == 1:
            dept = self.e_dept.get().strip()
            code = self.e_code.get().strip().upper()
            if not dept or not code:
                messagebox.showwarning("Required", "Department name and code are required.")
                return False
            self.data["department_name"] = dept
            self.data["receipt_prefix"] = code
            if self.logo_path:
                self.data["logo_path"] = self.logo_path
        elif self.step == 2:
            self.data["email"] = self.e_email.get().strip()
            self.data["phone"] = self.e_phone.get().strip()
            self.data["address"] = self.e_addr.get().strip()
        elif self.step == 3:
            prefix = self.e_prefix.get().strip().upper()
            if not prefix:
                messagebox.showwarning("Required", "Receipt prefix is required.")
                return False
            self.data["receipt_prefix"] = prefix
            self.data["next_receipt_number"] = 1
        return True

    def _save_department(self):
        try:
            save_department(self.data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save department: {e}")

    def _next(self):
        if self.step == len(self.STEPS) - 1:
            self.on_complete()
            return
        if not self._collect_step_data():
            return
        self.step += 1
        self._render_step()

    def _back(self):
        if self.step > 0:
            self.step -= 1
            self._render_step()