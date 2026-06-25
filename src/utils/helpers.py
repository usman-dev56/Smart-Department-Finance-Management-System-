# src/utils/helpers.py
"""
Utility Helpers
"""
import os
import random
import string
from datetime import datetime
from pathlib import Path


# ─── Path Helpers ────────────────────────────────────────────

def get_data_dir():
    """Get data directory path"""
    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)
    return str(data_dir)


def get_receipt_dir():
    """Get receipts directory path"""
    receipt_dir = Path("data/receipts")
    receipt_dir.mkdir(parents=True, exist_ok=True)
    return str(receipt_dir)


def get_export_dir():
    """Get exports directory path"""
    export_dir = Path("data/exports")
    export_dir.mkdir(parents=True, exist_ok=True)
    return str(export_dir)


def get_backup_dir():
    """Get backups directory path"""
    backup_dir = Path("data/backups")
    backup_dir.mkdir(parents=True, exist_ok=True)
    return str(backup_dir)


def get_logs_dir():
    """Get logs directory path"""
    logs_dir = Path("data/logs")
    logs_dir.mkdir(parents=True, exist_ok=True)
    return str(logs_dir)


def get_db_path():
    """Get database path"""
    db_dir = Path("data/database")
    db_dir.mkdir(parents=True, exist_ok=True)
    return str(db_dir / "dffms.db")


def create_directory(path: str) -> str:
    """Create directory if it doesn't exist"""
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


def ensure_directories():
    """Create all required directories"""
    directories = [
        get_data_dir(),
        get_receipt_dir(),
        get_export_dir(),
        get_backup_dir(),
        get_logs_dir(),
        Path("data/database"),
        Path("data/receipts/qr"),
        Path("data/exports/pdf"),
        Path("data/exports/excel"),
    ]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    return True


# ─── File Helpers ────────────────────────────────────────────

def clean_filename(filename):
    """Clean filename by removing invalid characters"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename.strip()


def safe_filename(name, extension=""):
    """Generate a safe filename from name"""
    clean = clean_filename(name)
    if extension and not extension.startswith('.'):
        extension = f".{extension}"
    return f"{clean}{extension}"


# ─── Formatting Helpers ─────────────────────────────────────

def format_currency(amount: float, symbol: str = "Rs.") -> str:
    try:
        return f"{symbol} {float(amount):,.2f}"
    except (TypeError, ValueError):
        return f"{symbol} 0.00"


def format_date(date_str: str, fmt_out: str = "%d-%b-%Y") -> str:
    if not date_str:
        return ""
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(date_str, fmt).strftime(fmt_out)
        except ValueError:
            continue
    return date_str


def today_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def datetime_str() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


# ─── Random Generators ──────────────────────────────────────

def generate_random_password(length: int = 10) -> str:
    chars = string.ascii_letters + string.digits + "!@#$"
    return "".join(random.choices(chars, k=length))


def generate_random_id(prefix: str = "", length: int = 8) -> str:
    """Generate a random ID with optional prefix"""
    chars = string.ascii_uppercase + string.digits
    random_part = "".join(random.choices(chars, k=length))
    return f"{prefix}{random_part}" if prefix else random_part


# ─── String Helpers ─────────────────────────────────────────

def truncate(text: str, max_len: int = 30) -> str:
    if not text:
        return ""
    return text if len(text) <= max_len else text[:max_len - 3] + "..."


def clean_text(text: str) -> str:
    """Clean text by stripping whitespace"""
    if not text:
        return ""
    return str(text).strip()


def is_empty(value) -> bool:
    """Check if value is empty"""
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    if isinstance(value, (list, dict, tuple)):
        return len(value) == 0
    return False


# ─── List Helpers ───────────────────────────────────────────

def chunk_list(lst, chunk_size):
    """Split a list into chunks"""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


def unique_list(lst):
    """Get unique items from list while preserving order"""
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]


# ─── Dictionary Helpers ─────────────────────────────────────

def get_nested(data, keys, default=None):
    """Get nested value from dictionary using list of keys"""
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current


def filter_dict(data, keys):
    """Filter dictionary to only include specified keys"""
    return {k: v for k, v in data.items() if k in keys}


def exclude_keys(data, keys):
    """Exclude specified keys from dictionary"""
    return {k: v for k, v in data.items() if k not in keys}


# ─── Initialize directories ────────────────────────────────

# Auto-create directories when module is imported
ensure_directories()


if __name__ == "__main__":
    # Test helpers
    print(f"Data dir: {get_data_dir()}")
    print(f"Receipt dir: {get_receipt_dir()}")
    print(f"Export dir: {get_export_dir()}")
    print(f"Backup dir: {get_backup_dir()}")
    print(f"Logs dir: {get_logs_dir()}")
    print(f"DB path: {get_db_path()}")
    print(f"Today: {today_str()}")
    print(f"Currency: {format_currency(1234.56)}")
    print(f"Random password: {generate_random_password()}")