# src/database/seed_data.py
"""
Seed Data - Default data for first-time setup
"""
from src.database.db_manager import get_db
from src.utils.logger import get_logger

logger = get_logger(__name__)


def seed_default_funds(department_id=1):
    """Insert default fund types for a department"""
    db = get_db()
    
    # Check if department exists
    dept = db.fetchone("SELECT department_id FROM departments WHERE department_id = ?", (department_id,))
    if not dept:
        logger.warning(f"Department {department_id} not found. Skipping fund seeding.")
        return
    
    default_funds = [
        ("Department Fund", "General department fund for administrative expenses"),
        ("Study Tour Fund", "Fund for student study tours and educational trips"),
        ("Lab Fund", "Fund for laboratory equipment and maintenance"),
        ("Sports Fund", "Fund for sports events and equipment"),
        ("Workshop Fund", "Fund for workshops and seminars"),
        ("Farewell Fund", "Fund for farewell ceremonies and events"),
        ("Event Fund", "Fund for departmental events and functions"),
        ("Industrial Visit Fund", "Fund for industrial visits and field trips"),
    ]
    
    existing = db.fetchall(
        "SELECT fund_name FROM funds WHERE department_id = ?", 
        (department_id,)
    )
    existing_names = {f["fund_name"] for f in existing}
    
    for name, desc in default_funds:
        if name not in existing_names:
            try:
                db.insert("funds", {
                    "department_id": department_id,
                    "fund_name": name,
                    "fund_description": desc,
                    "is_active": 1
                })
            except Exception as e:
                logger.error(f"Failed to seed fund '{name}': {e}")
    
    logger.info("Default funds seeded")


def seed_default_academic(department_id=1):
    """Insert default academic structure for a department"""
    db = get_db()
    
    # Check if department exists
    dept = db.fetchone("SELECT department_id FROM departments WHERE department_id = ?", (department_id,))
    if not dept:
        logger.warning(f"Department {department_id} not found. Skipping academic seeding.")
        return
    
    # Default shifts
    for shift in ["Morning", "Evening"]:
        existing = db.fetchone(
            "SELECT id FROM shifts WHERE department_id = ? AND shift_name = ?",
            (department_id, shift)
        )
        if not existing:
            try:
                db.insert("shifts", {
                    "department_id": department_id,
                    "shift_name": shift,
                    "is_active": 1
                })
            except Exception as e:
                logger.error(f"Failed to seed shift '{shift}': {e}")

    # Default sections
    for section in ["A", "B", "C", "D"]:
        existing = db.fetchone(
            "SELECT id FROM sections WHERE department_id = ? AND section_name = ?",
            (department_id, section)
        )
        if not existing:
            try:
                db.insert("sections", {
                    "department_id": department_id,
                    "section_name": section,
                    "is_active": 1
                })
            except Exception as e:
                logger.error(f"Failed to seed section '{section}': {e}")

    logger.info("Default academic data seeded")


def run_seeds(department_id=1):
    """Run all seed functions"""
    seed_default_funds(department_id)
    seed_default_academic(department_id)
    logger.info("All seeds completed")


def seed_database(db, department_id=1):
    """Entry point for seeding from app.py"""
    logger.info("Starting database seeding...")
    
    # Check if department exists
    dept = db.fetchone("SELECT department_id FROM departments LIMIT 1")
    if dept:
        department_id = dept["department_id"]
        logger.info(f"Found existing department ID: {department_id}")
    else:
        logger.info("No department found. Seeding will happen after department setup.")
        return
    
    run_seeds(department_id)