# src/controllers/department_controller.py
"""Department Controller - Handles department operations"""
from src.models.department import Department
from src.database.db_manager import get_db


def save_department(data):
    """Save department data to database"""
    try:
        db = get_db()
        
        # Check if department exists
        existing = db.fetchone("SELECT department_id FROM departments LIMIT 1")
        
        if existing:
            # Update existing department
            dept_id = existing["department_id"]
            update_data = {
                "department_name": data.get("department_name"),
                "university_name": data.get("university_name"),
                "logo_path": data.get("logo_path"),
                "email": data.get("email"),
                "phone": data.get("phone"),
                "address": data.get("address"),
                "receipt_prefix": data.get("receipt_prefix", "DEPT"),
                "next_receipt_number": data.get("next_receipt_number", 1)
            }
            # Remove None values
            update_data = {k: v for k, v in update_data.items() if v is not None}
            db.update("departments", update_data, "department_id = ?", (dept_id,))
            return dept_id
        else:
            # Insert new department
            insert_data = {
                "department_name": data.get("department_name"),
                "university_name": data.get("university_name"),
                "logo_path": data.get("logo_path"),
                "email": data.get("email"),
                "phone": data.get("phone"),
                "address": data.get("address"),
                "receipt_prefix": data.get("receipt_prefix", "DEPT"),
                "next_receipt_number": data.get("next_receipt_number", 1)
            }
            return db.insert("departments", insert_data)
            
    except Exception as e:
        raise Exception(f"Failed to save department: {e}")


def get_department(department_id=1):
    """Get department by ID"""
    return Department.find(department_id)


def get_current_department():
    """Get the first/current department"""
    db = get_db()
    result = db.fetchone("SELECT * FROM departments LIMIT 1")
    if result:
        return result
    return None


def update_department(department_id, data):
    """Update department"""
    dept = Department.find(department_id)
    if not dept:
        raise Exception("Department not found")
    
    for key, value in data.items():
        if hasattr(dept, key):
            setattr(dept, key, value)
    
    return dept.save()


def department_exists():
    """Check if any department exists"""
    db = get_db()
    result = db.fetchone("SELECT department_id FROM departments LIMIT 1")
    return result is not None


def get_receipt_prefix():
    """Get the receipt prefix from current department"""
    dept = get_current_department()
    if dept:
        return dept.get("receipt_prefix", "DEPT")
    return "DEPT"


def get_next_receipt_number():
    """Get and increment the next receipt number"""
    db = get_db()
    result = db.fetchone("SELECT next_receipt_number FROM departments LIMIT 1")
    if result:
        current = result["next_receipt_number"]
        db.execute("UPDATE departments SET next_receipt_number = next_receipt_number + 1")
        return current
    return 1


def get_department_summary():
    """Get summary of department statistics"""
    db = get_db()
    
    # Get totals
    student_count = db.fetchone("SELECT COUNT(*) as count FROM students WHERE is_active=1")
    total_collection = db.fetchone("SELECT COALESCE(SUM(amount), 0) as total FROM payments")
    total_expenses = db.fetchone("SELECT COALESCE(SUM(amount), 0) as total FROM expenses")
    
    return {
        "total_students": student_count["count"] if student_count else 0,
        "total_collection": total_collection["total"] if total_collection else 0,
        "total_expenses": total_expenses["total"] if total_expenses else 0,
        "balance": (total_collection["total"] if total_collection else 0) - 
                   (total_expenses["total"] if total_expenses else 0)
    }