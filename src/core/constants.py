# src/core/constants.py
"""Application constants"""

# ─── Application Info ──────────────────────────────────────────────────────

APP_NAME = "SDFFMS"
APP_VERSION = "1.0.0"
APP_TITLE = "Smart Department Finance  Management System"

# ─── Window Settings ──────────────────────────────────────────────────────

WINDOW_SIZE = "1280x780"
MIN_WINDOW_SIZE = (1024, 768)
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 780

# ─── Database Paths ───────────────────────────────────────────────────────

DB_PATH = "data/database/dffms.db"
SCHEMA_PATH = "src/database/schema.sql"

# ─── Theme Settings ──────────────────────────────────────────────────────

DEFAULT_THEME = "dark"
DEFAULT_COLOR = "blue"

# ─── Payment Methods ─────────────────────────────────────────────────────

PAYMENT_METHODS = ["Cash", "Bank Transfer", "Online Transfer", "Cheque"]

# ─── Expense Categories ──────────────────────────────────────────────────

EXPENSE_CATEGORIES = [
    "Equipment",
    "Maintenance",
    "Event",
    "Travel",
    "Printing",
    "Stationery",
    "Miscellaneous"
]

# ─── Status Constants ────────────────────────────────────────────────────

STATUS_ACTIVE = 1
STATUS_INACTIVE = 0

# ─── Semesters ───────────────────────────────────────────────────────────

SEMESTERS = [1, 2, 3, 4, 5, 6, 7, 8]

# ─── Theme Colors ────────────────────────────────────────────────────────

COLORS = {
    "primary": "#1a73e8",
    "primary_hover": "#1557b0",
    "success": "#0f9d58",
    "success_hover": "#0b7e45",
    "warning": "#f4b400",
    "warning_hover": "#d49a00",
    "danger": "#db4437",
    "danger_hover": "#b8322a",
    "dark_bg": "#1e1e2e",
    "sidebar_bg": "#181825",
    "card_bg": "#2a2a3d",
    "text_primary": "#ffffff",
    "text_secondary": "#a0a0b0",
    "border": "#3a3a4d",
    "input_bg": "#2d2d40",
}

THEME_COLORS = {
    "primary": "#1a73e8",
    "success": "#0f9d58",
    "warning": "#f4b400",
    "danger": "#db4437",
    "dark_bg": "#1e1e2e",
    "sidebar_bg": "#181825",
    "card_bg": "#2a2a3d",
    "text_primary": "#ffffff",
    "text_secondary": "#a0a0b0",
}

# ─── Receipt Settings ────────────────────────────────────────────────────

RECEIPT_PREFIX = "DEPT"
CURRENCY_SYMBOL = "PKR"

# ─── Fund Types ──────────────────────────────────────────────────────────

FUND_TYPES = [
    "Department Fund",
    "Study Tour Fund",
    "Lab Fund",
    "Sports Fund",
    "Workshop Fund",
    "Farewell Fund",
    "Event Fund",
    "Industrial Visit Fund"
]

# ─── User Roles ──────────────────────────────────────────────────────────

USER_ROLES = {
    "admin": "Administrator",
    "finance_officer": "Finance Officer",
    "department_head": "Department Head"
}