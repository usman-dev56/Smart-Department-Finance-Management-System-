# src/controllers/academic_controller.py
"""Academic Controller - Handles sessions, programs, shifts, sections"""
from src.database.db_manager import get_db
from src.models.session import Session
from src.models.program import Program
from src.models.shift import Shift
from src.models.section import Section


# ─── SESSIONS ──────────────────────────────────────────────

def create_session(session_name, department_id=1):
    """Create a new academic session"""
    db = get_db()
    existing = db.fetchone(
        "SELECT id FROM sessions WHERE session_name = ? AND department_id = ?",
        (session_name, department_id)
    )
    if existing:
        raise ValueError(f"Session '{session_name}' already exists")
    
    data = {
        "department_id": department_id,
        "session_name": session_name,
        "is_active": 1
    }
    return db.insert("sessions", data)


def get_all_sessions(department_id=1):
    """Get all sessions for a department"""
    db = get_db()
    return db.fetchall(
        "SELECT * FROM sessions WHERE department_id = ? ORDER BY session_name DESC",
        (department_id,)
    )


def get_active_sessions(department_id=1):
    """Get all active sessions"""
    db = get_db()
    return db.fetchall(
        "SELECT * FROM sessions WHERE department_id = ? AND is_active = 1 ORDER BY session_name DESC",
        (department_id,)
    )


def delete_session(session_id):
    """Delete a session (only if no students linked)"""
    db = get_db()
    # Check if students exist
    students = db.fetchone("SELECT id FROM students WHERE session_id = ? LIMIT 1", (session_id,))
    if students:
        raise ValueError("Cannot delete session with linked students")
    db.delete("sessions", "id = ?", (session_id,))
    return True


def toggle_session_status(session_id):
    """Activate/deactivate a session"""
    db = get_db()
    session = db.fetchone("SELECT is_active FROM sessions WHERE id = ?", (session_id,))
    if not session:
        raise ValueError("Session not found")
    new_status = 0 if session["is_active"] else 1
    db.execute("UPDATE sessions SET is_active = ? WHERE id = ?", (new_status, session_id))
    return new_status


# ─── PROGRAMS ──────────────────────────────────────────────

def create_program(program_name, program_code, department_id=1):
    """Create a new program"""
    db = get_db()
    existing = db.fetchone(
        "SELECT id FROM programs WHERE program_code = ? AND department_id = ?",
        (program_code.upper(), department_id)
    )
    if existing:
        raise ValueError(f"Program code '{program_code}' already exists")
    
    data = {
        "department_id": department_id,
        "program_name": program_name,
        "program_code": program_code.upper(),
        "is_active": 1
    }
    return db.insert("programs", data)


def get_all_programs(department_id=1):
    """Get all programs for a department"""
    db = get_db()
    return db.fetchall(
        "SELECT * FROM programs WHERE department_id = ? ORDER BY program_name",
        (department_id,)
    )


def get_active_programs(department_id=1):
    """Get all active programs"""
    db = get_db()
    return db.fetchall(
        "SELECT * FROM programs WHERE department_id = ? AND is_active = 1 ORDER BY program_name",
        (department_id,)
    )


def delete_program(program_id):
    """Delete a program (only if no students linked)"""
    db = get_db()
    students = db.fetchone("SELECT id FROM students WHERE program_id = ? LIMIT 1", (program_id,))
    if students:
        raise ValueError("Cannot delete program with linked students")
    db.delete("programs", "id = ?", (program_id,))
    return True


def toggle_program_status(program_id):
    """Activate/deactivate a program"""
    db = get_db()
    program = db.fetchone("SELECT is_active FROM programs WHERE id = ?", (program_id,))
    if not program:
        raise ValueError("Program not found")
    new_status = 0 if program["is_active"] else 1
    db.execute("UPDATE programs SET is_active = ? WHERE id = ?", (new_status, program_id))
    return new_status


# ─── SHIFTS ──────────────────────────────────────────────

def create_shift(shift_name, department_id=1):
    """Create a new shift"""
    db = get_db()
    existing = db.fetchone(
        "SELECT id FROM shifts WHERE shift_name = ? AND department_id = ?",
        (shift_name, department_id)
    )
    if existing:
        raise ValueError(f"Shift '{shift_name}' already exists")
    
    data = {
        "department_id": department_id,
        "shift_name": shift_name,
        "is_active": 1
    }
    return db.insert("shifts", data)


def get_all_shifts(department_id=1):
    """Get all shifts for a department"""
    db = get_db()
    return db.fetchall(
        "SELECT * FROM shifts WHERE department_id = ? ORDER BY shift_name",
        (department_id,)
    )


def get_active_shifts(department_id=1):
    """Get all active shifts"""
    db = get_db()
    return db.fetchall(
        "SELECT * FROM shifts WHERE department_id = ? AND is_active = 1 ORDER BY shift_name",
        (department_id,)
    )


def delete_shift(shift_id):
    """Delete a shift (only if no students linked)"""
    db = get_db()
    students = db.fetchone("SELECT id FROM students WHERE shift_id = ? LIMIT 1", (shift_id,))
    if students:
        raise ValueError("Cannot delete shift with linked students")
    db.delete("shifts", "id = ?", (shift_id,))
    return True


def toggle_shift_status(shift_id):
    """Activate/deactivate a shift"""
    db = get_db()
    shift = db.fetchone("SELECT is_active FROM shifts WHERE id = ?", (shift_id,))
    if not shift:
        raise ValueError("Shift not found")
    new_status = 0 if shift["is_active"] else 1
    db.execute("UPDATE shifts SET is_active = ? WHERE id = ?", (new_status, shift_id))
    return new_status


# ─── SECTIONS ──────────────────────────────────────────────

def create_section(section_name, department_id=1):
    """Create a new section"""
    db = get_db()
    existing = db.fetchone(
        "SELECT id FROM sections WHERE section_name = ? AND department_id = ?",
        (section_name, department_id)
    )
    if existing:
        raise ValueError(f"Section '{section_name}' already exists")
    
    data = {
        "department_id": department_id,
        "section_name": section_name,
        "is_active": 1
    }
    return db.insert("sections", data)


def get_all_sections(department_id=1):
    """Get all sections for a department"""
    db = get_db()
    return db.fetchall(
        "SELECT * FROM sections WHERE department_id = ? ORDER BY section_name",
        (department_id,)
    )


def get_active_sections(department_id=1):
    """Get all active sections"""
    db = get_db()
    return db.fetchall(
        "SELECT * FROM sections WHERE department_id = ? AND is_active = 1 ORDER BY section_name",
        (department_id,)
    )


def delete_section(section_id):
    """Delete a section (only if no students linked)"""
    db = get_db()
    students = db.fetchone("SELECT id FROM students WHERE section_id = ? LIMIT 1", (section_id,))
    if students:
        raise ValueError("Cannot delete section with linked students")
    db.delete("sections", "id = ?", (section_id,))
    return True


def toggle_section_status(section_id):
    """Activate/deactivate a section"""
    db = get_db()
    section = db.fetchone("SELECT is_active FROM sections WHERE id = ?", (section_id,))
    if not section:
        raise ValueError("Section not found")
    new_status = 0 if section["is_active"] else 1
    db.execute("UPDATE sections SET is_active = ? WHERE id = ?", (new_status, section_id))
    return new_status


# ─── HELPERS ──────────────────────────────────────────────

def get_academic_data(department_id=1):
    """Get all academic data in one call"""
    db = get_db()
    return {
        "sessions": db.fetchall("SELECT * FROM sessions WHERE department_id = ?", (department_id,)),
        "programs": db.fetchall("SELECT * FROM programs WHERE department_id = ?", (department_id,)),
        "shifts": db.fetchall("SELECT * FROM shifts WHERE department_id = ?", (department_id,)),
        "sections": db.fetchall("SELECT * FROM sections WHERE department_id = ?", (department_id,))
    }


def get_program_by_code(program_code, department_id=1):
    """Get program by code"""
    db = get_db()
    return db.fetchone(
        "SELECT * FROM programs WHERE program_code = ? AND department_id = ?",
        (program_code.upper(), department_id)
    )