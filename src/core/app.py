# src/core/app.py
"""
Main Application Class
"""
import customtkinter as ctk
import sys
import os
from src.core.constants import (
    APP_TITLE, WINDOW_SIZE, MIN_WINDOW_SIZE,
    DB_PATH, SCHEMA_PATH, DEFAULT_THEME, DEFAULT_COLOR
)
from src.database.db_manager import DatabaseManager
from src.database.seed_data import seed_database
from src.models.base_model import BaseModel
from src.utils.logger import get_logger

logger = get_logger()


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class SDFFMSApp(ctk.CTk):
    def __init__(self):
        ctk.set_appearance_mode(DEFAULT_THEME)
        ctk.set_default_color_theme(DEFAULT_COLOR)

        super().__init__()
        self.title(APP_TITLE)
        self.geometry(WINDOW_SIZE)
        self.minsize(*MIN_WINDOW_SIZE)

        self._init_database()
        self._decide_first_view()

    def _init_database(self):
        """Initialize DB, run schema, seed defaults."""
        # Handle DB path for EXE
        db_path = DB_PATH
        if getattr(sys, 'frozen', False):
            # When running as EXE, database should be in current directory
            db_path = os.path.join(os.path.abspath("."), "data", "database", "dffms.db")
            logger.info(f"EXE mode - Using database at: {db_path}")
        
        logger.info("Initialising database at %s", db_path)
        self.db = DatabaseManager(db_path)
        self.db.connect()
        
        # Handle schema path for EXE
        if getattr(sys, 'frozen', False):
            schema_path = get_resource_path("src/database/schema.sql")
            logger.info(f"EXE mode - Using schema at: {schema_path}")
        else:
            schema_path = SCHEMA_PATH
        
        self.db.initialize_schema(schema_path)
        BaseModel.DB = self.db

        # Check if department exists before seeding
        dept = self.db.fetchone("SELECT department_id FROM departments LIMIT 1")
        if dept:
            logger.info("Department found, seeding data...")
            seed_database(self.db, dept["department_id"])
        else:
            logger.info("No department found. Data will be seeded after department setup.")

    def _decide_first_view(self):
        dept = self.db.fetchone("SELECT department_id FROM departments LIMIT 1")
        if dept:
            self._show_main_window()
        else:
            self._show_wizard()

    def _show_wizard(self):
        from src.views.setup.first_run_wizard import FirstRunWizard
        wizard = FirstRunWizard(self, on_complete=self._on_wizard_complete)
        wizard.pack(fill="both", expand=True)

    def _on_wizard_complete(self):
        """Called after the first-run wizard finishes."""
        for widget in self.winfo_children():
            widget.destroy()
        self._show_main_window()

    def _show_main_window(self):
        from src.views.main_window import MainWindow
        mw = MainWindow(self)
        mw.pack(fill="both", expand=True)

    def on_close(self):
        logger.info("Application closing.")
        if hasattr(self, 'db') and self.db:
            self.db.close()
        self.destroy()

    def run(self):
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.mainloop()