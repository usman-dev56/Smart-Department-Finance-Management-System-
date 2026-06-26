# src/controllers/student_controller.py
"""Student Controller"""
from src.models.student import Student
from src.models.program import Program
from src.models.session import Session
from src.database.db_manager import get_db


def generate_roll_number(program_code, session_name):
    """Generate roll number: BSCS-2024-001"""
    db = get_db()
    prefix = f"{program_code}-{session_name}"
    row = db.fetchone(
        "SELECT roll_number FROM students WHERE roll_number LIKE ? ORDER BY roll_number DESC LIMIT 1",
        (f"{prefix}-%",)
    )
    if row:
        last_num = int(row["roll_number"].split("-")[-1])
        next_num = last_num + 1
    else:
        next_num = 1
    return f"{prefix}-{next_num:03d}"


def register_student(data):
    """Register a new student"""
    program = Program.find(data["program_id"])
    session = Session.find(data["session_id"])
    
    if not program or not session:
        raise ValueError("Invalid program or session")
    
    roll = generate_roll_number(program.program_code, session.session_name)
    
    student_data = {
        "department_id": data.get("department_id", 1),
        "roll_number": roll,
        "student_name": data["student_name"].strip(),
        "program_id": data["program_id"],
        "session_id": data["session_id"],
        "semester": data.get("semester", 1),
        "section_id": data.get("section_id"),
        "shift_id": data.get("shift_id"),
        "phone": data.get("phone", ""),
        "email": data.get("email", ""),
        "is_active": 1,
    }
    db = get_db()
    new_id = db.insert("students", student_data)
    return new_id, roll


def get_student_payments(student_id):
    """Get all payments for a student"""
    db = get_db()
    return db.fetchall(
        """SELECT p.*, c.campaign_name, f.fund_name
           FROM payments p
           JOIN campaigns c ON p.campaign_id = c.id
           LEFT JOIN funds f ON c.fund_id = f.id
           WHERE p.student_id = ?
           ORDER BY p.payment_date DESC""",
        (student_id,)
    )


def search_students(query):
    """Search students by name or roll number"""
    if not query or query.strip() == "":
        return get_all_students()
    return Student.search(query)


def delete_student(student_id):
    """Delete a student (only if no payments exist)"""
    db = get_db()
    # Check if has payments
    pay = db.fetchone("SELECT id FROM payments WHERE student_id=?", (student_id,))
    if pay:
        raise ValueError("Cannot delete student with existing payments")
    db.delete("students", "id=?", (student_id,))
    return True




def update_student(student_id, data):
    """Update student information"""
    db = get_db()
    
    # Check if student exists
    student = db.fetchone("SELECT id FROM students WHERE id = ?", (student_id,))
    if not student:
        raise ValueError("Student not found")
    
    # Build update data
    update_data = {}
    if "student_name" in data:
        update_data["student_name"] = data["student_name"].strip()
    if "program_id" in data:
        update_data["program_id"] = data["program_id"]
    if "session_id" in data:
        update_data["session_id"] = data["session_id"]
    if "semester" in data:
        update_data["semester"] = data["semester"]
    if "section_id" in data:
        update_data["section_id"] = data["section_id"]
    if "shift_id" in data:
        update_data["shift_id"] = data["shift_id"]
    if "phone" in data:
        update_data["phone"] = data["phone"]
    if "email" in data:
        update_data["email"] = data["email"]
    
    if not update_data:
        return True
    
    # Update student
    set_clause = ", ".join([f"{k} = ?" for k in update_data.keys()])
    query = f"UPDATE students SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
    values = list(update_data.values()) + [student_id]
    db.execute(query, values)
    return True


def get_student_by_id(student_id):
    """Get student by ID with all details"""
    db = get_db()
    return db.fetchone(
        """SELECT s.*, p.program_name, p.program_code,
                  ss.session_name, sec.section_name, sh.shift_name
           FROM students s
           LEFT JOIN programs p ON s.program_id = p.id
           LEFT JOIN sessions ss ON s.session_id = ss.id
           LEFT JOIN sections sec ON s.section_id = sec.id
           LEFT JOIN shifts sh ON s.shift_id = sh.id
           WHERE s.id = ?""",
        (student_id,)
    )

def get_student_by_roll(roll_number):
    """Get student by roll number with all details"""
    db = get_db()
    return db.fetchone(
        """SELECT s.*, p.program_name, p.program_code,
                  ss.session_name, sec.section_name, sh.shift_name
           FROM students s
           LEFT JOIN programs p ON s.program_id = p.id
           LEFT JOIN sessions ss ON s.session_id = ss.id
           LEFT JOIN sections sec ON s.section_id = sec.id
           LEFT JOIN shifts sh ON s.shift_id = sh.id
           WHERE s.roll_number = ? AND s.is_active = 1""",
        (roll_number,)
    )


def get_student_by_id(student_id):
    """Get student by ID with all details"""
    db = get_db()
    return db.fetchone(
        """SELECT s.*, p.program_name, p.program_code,
                  ss.session_name, sec.section_name, sh.shift_name
           FROM students s
           LEFT JOIN programs p ON s.program_id = p.id
           LEFT JOIN sessions ss ON s.session_id = ss.id
           LEFT JOIN sections sec ON s.section_id = sec.id
           LEFT JOIN shifts sh ON s.shift_id = sh.id
           WHERE s.id = ?""",
        (student_id,)
    )


def get_all_students(department_id=1):
    """Get all active students with their details"""
    db = get_db()
    return db.fetchall(
        """SELECT s.*, p.program_name, p.program_code,
                  ss.session_name, sec.section_name, sh.shift_name
           FROM students s
           LEFT JOIN programs p ON s.program_id = p.id
           LEFT JOIN sessions ss ON s.session_id = ss.id
           LEFT JOIN sections sec ON s.section_id = sec.id
           LEFT JOIN shifts sh ON s.shift_id = sh.id
           WHERE s.is_active = 1 AND s.department_id = ?
           ORDER BY s.student_name""",
        (department_id,)
    )


def update_student(student_id, data):
    """Update student information"""
    db = get_db()
    student = Student.find(student_id)
    if not student:
        raise ValueError("Student not found")
    
    update_data = {}
    if "student_name" in data:
        update_data["student_name"] = data["student_name"].strip()
    if "program_id" in data:
        update_data["program_id"] = data["program_id"]
    if "session_id" in data:
        update_data["session_id"] = data["session_id"]
    if "semester" in data:
        update_data["semester"] = data["semester"]
    if "section_id" in data:
        update_data["section_id"] = data["section_id"]
    if "shift_id" in data:
        update_data["shift_id"] = data["shift_id"]
    if "phone" in data:
        update_data["phone"] = data["phone"]
    if "email" in data:
        update_data["email"] = data["email"]
    
    if not update_data:
        return True
    
    db.update("students", update_data, "id = ?", (student_id,))
    return True


def get_student_count(department_id=1):
    """Get total number of active students"""
    db = get_db()
    result = db.fetchone(
        "SELECT COUNT(*) as count FROM students WHERE is_active = 1 AND department_id = ?",
        (department_id,)
    )
    return result["count"] if result else 0


def get_students_by_program(program_id):
    """Get all students in a specific program"""
    db = get_db()
    return db.fetchall(
        """SELECT s.*, ss.session_name, sec.section_name, sh.shift_name
           FROM students s
           LEFT JOIN sessions ss ON s.session_id = ss.id
           LEFT JOIN sections sec ON s.section_id = sec.id
           LEFT JOIN shifts sh ON s.shift_id = sh.id
           WHERE s.program_id = ? AND s.is_active = 1
           ORDER BY s.student_name""",
        (program_id,)
    )



def register_student_with_roll(data):
    """Register a new student with manual roll number"""
    db = get_db()
    
    # Check if roll number already exists
    existing = db.fetchone("SELECT id FROM students WHERE roll_number = ?", (data["roll_number"],))
    if existing:
        raise ValueError(f"Roll number '{data['roll_number']}' already exists! Please use a unique roll number.")
    
    student_data = {
        "department_id": data.get("department_id", 1),
        "roll_number": data["roll_number"].strip(),
        "student_name": data["student_name"].strip(),
        "program_id": data["program_id"],
        "session_id": data["session_id"],
        "semester": data.get("semester", 1),
        "section_id": data.get("section_id"),
        "shift_id": data.get("shift_id"),
        "phone": data.get("phone", ""),
        "email": data.get("email", ""),
        "is_active": 1,
    }
    
    new_id = db.insert("students", student_data)
    return new_id