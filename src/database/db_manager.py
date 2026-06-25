# src/database/db_manager.py
"""
Database Manager - Handles all SQLite database operations
"""
import sqlite3
import os
import shutil
import sys
from datetime import datetime
from src.utils.logger import get_logger

logger = get_logger(__name__)


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


class DatabaseManager:
    """Centralized database management class"""

    _instance = None

    def __new__(cls, db_path=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, db_path=None):
        if self._initialized:
            return
        self.db_path = db_path or os.path.join("data", "database", "dffms.db")
        self.connection = None
        self._initialized = True
        self.connect()
        self.initialize_schema()

    def connect(self):
        """Open database connection with foreign key support"""
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
            self.connection.execute("PRAGMA foreign_keys = ON")
            self.connection.execute("PRAGMA journal_mode = WAL")
            logger.info(f"Connected to database: {self.db_path}")
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise

    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("Database connection closed")

    def initialize_schema(self, schema_path=None):
        """Load and execute schema SQL"""
        try:
            if schema_path is None:
                # Check if running as executable or script
                if getattr(sys, 'frozen', False):
                    # Running as executable (PyInstaller)
                    base_path = sys._MEIPASS
                    schema_path = os.path.join(base_path, "src", "database", "schema.sql")
                    logger.info(f"Looking for schema in: {schema_path}")
                else:
                    # Running as script
                    schema_path = os.path.join("src", "database", "schema.sql")
            
            # Check if file exists, try alternative paths
            if not os.path.exists(schema_path):
                logger.warning(f"Schema file not found at: {schema_path}")
                
                # Try alternative paths
                alt_paths = [
                    os.path.join(os.path.dirname(__file__), "schema.sql"),
                    os.path.join("src", "database", "schema.sql"),
                    "schema.sql"
                ]
                
                for alt in alt_paths:
                    if os.path.exists(alt):
                        schema_path = alt
                        logger.info(f"Found schema at: {schema_path}")
                        break
                else:
                    raise FileNotFoundError(f"Schema file not found. Tried: {schema_path}")
            
            # Read and execute schema
            with open(schema_path, "r") as f:
                schema_sql = f.read()
            
            self.connection.executescript(schema_sql)
            self.connection.commit()
            logger.info("Schema initialized successfully")
            
        except Exception as e:
            logger.error(f"Schema initialization error: {e}")
            raise

    def execute(self, query, params=()):
        """Execute a single query"""
        try:
            cursor = self.connection.execute(query, params)
            self.connection.commit()
            return cursor
        except Exception as e:
            logger.error(f"Query error: {e}\nQuery: {query}\nParams: {params}")
            self.connection.rollback()
            raise

    def fetchall(self, query, params=()):
        """Fetch all rows as list of dicts"""
        try:
            cursor = self.connection.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Fetchall error: {e}")
            raise

    def fetchone(self, query, params=()):
        """Fetch single row as dict"""
        try:
            cursor = self.connection.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Fetchone error: {e}")
            raise

    def insert(self, table, data):
        """Insert a record and return last row id"""
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor = self.execute(query, list(data.values()))
        return cursor.lastrowid

    def update(self, table, data, condition, condition_params=()):
        """Update records matching condition"""
        set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        values = list(data.values()) + list(condition_params)
        return self.execute(query, values)

    def delete(self, table, condition, condition_params=()):
        """Delete records matching condition"""
        query = f"DELETE FROM {table} WHERE {condition}"
        return self.execute(query, condition_params)

    def backup(self, backup_dir="data/backups"):
        """Create a backup of the database"""
        try:
            os.makedirs(backup_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(backup_dir, f"dffms_backup_{timestamp}.db")
            shutil.copy2(self.db_path, backup_path)
            logger.info(f"Backup created: {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"Backup error: {e}")
            raise

    def table_exists(self, table_name):
        """Check if a table exists"""
        result = self.fetchone(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,)
        )
        return result is not None


# Global instance accessor
_db_manager = None


def get_db():
    """Get the global database manager instance"""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager