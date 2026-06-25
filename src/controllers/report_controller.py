# src/controllers/report_controller.py
"""Report Controller - Handles report generation and data"""
from src.database.db_manager import get_db
from src.models.payment import Payment
from src.models.expense import Expense
from src.models.student import Student
from src.models.campaign import Campaign
from src.models.fund import Fund
from src.utils.helpers import today_str


def get_collection_report(department_id=1, start_date=None, end_date=None):
    """Get collection report data"""
    db = get_db()
    
    query = """
        SELECT p.*, s.student_name, s.roll_number,
               c.campaign_name, f.fund_name
        FROM payments p
        JOIN students s ON p.student_id = s.id
        JOIN campaigns c ON p.campaign_id = c.id
        LEFT JOIN funds f ON c.fund_id = f.id
        WHERE p.department_id = ?
    """
    params = [department_id]
    
    if start_date:
        query += " AND p.payment_date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND p.payment_date <= ?"
        params.append(end_date)
    
    query += " ORDER BY p.payment_date DESC"
    
    return db.fetchall(query, params)


def get_campaign_report(campaign_id):
    """Get detailed report for a specific campaign"""
    db = get_db()
    
    # Get campaign details
    campaign = Campaign.get_with_details(campaign_id)
    if not campaign:
        return None
    
    # Get paid students
    paid = db.fetchall(
        """SELECT s.*, p.payment_date, p.amount, p.receipt_number
           FROM payments p
           JOIN students s ON p.student_id = s.id
           WHERE p.campaign_id = ?
           ORDER BY s.student_name""",
        (campaign_id,)
    )
    
    # Get pending students
    pending = get_pending_students_for_campaign(campaign_id)
    
    return {
        "campaign": campaign,
        "paid_students": paid,
        "pending_students": pending,
        "summary": {
            "total_paid": len(paid),
            "total_pending": len(pending),
            "total_collected": sum(p["amount"] for p in paid) if paid else 0,
            "total_eligible": len(paid) + len(pending)
        }
    }


def get_pending_students_for_campaign(campaign_id):
    """Get pending students for a campaign"""
    db = get_db()
    campaign = db.fetchone("SELECT * FROM campaigns WHERE id = ?", (campaign_id,))
    if not campaign:
        return []
    
    # Get all eligible students
    query = "SELECT s.* FROM students s WHERE s.is_active = 1"
    params = []
    
    if campaign["program_id"]:
        query += " AND s.program_id = ?"
        params.append(campaign["program_id"])
    if campaign["session_id"]:
        query += " AND s.session_id = ?"
        params.append(campaign["session_id"])
    if campaign["semester"]:
        query += " AND s.semester = ?"
        params.append(campaign["semester"])
    if campaign["shift_id"]:
        query += " AND s.shift_id = ?"
        params.append(campaign["shift_id"])
    
    students = db.fetchall(query, params)
    
    # Get paid student IDs
    paid = db.fetchall("SELECT student_id FROM payments WHERE campaign_id = ?", (campaign_id,))
    paid_ids = {p["student_id"] for p in paid}
    
    return [s for s in students if s["id"] not in paid_ids]


def get_expense_report(department_id=1, start_date=None, end_date=None):
    """Get expense report data"""
    db = get_db()
    
    query = """
        SELECT e.*, f.fund_name
        FROM expenses e
        LEFT JOIN funds f ON e.fund_id = f.id
        WHERE e.department_id = ?
    """
    params = [department_id]
    
    if start_date:
        query += " AND e.expense_date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND e.expense_date <= ?"
        params.append(end_date)
    
    query += " ORDER BY e.expense_date DESC"
    
    return db.fetchall(query, params)


def get_fund_performance_report(department_id=1):
    """Get fund performance report"""
    db = get_db()
    
    return db.fetchall(
        """SELECT f.id, f.fund_name,
                  COALESCE((
                      SELECT SUM(p.amount) 
                      FROM payments p
                      JOIN campaigns c ON p.campaign_id = c.id
                      WHERE c.fund_id = f.id
                  ), 0) as total_collected,
                  COALESCE((
                      SELECT SUM(e.amount) 
                      FROM expenses e
                      WHERE e.fund_id = f.id
                  ), 0) as total_expenses,
                  COALESCE((
                      SELECT SUM(p.amount) 
                      FROM payments p
                      JOIN campaigns c ON p.campaign_id = c.id
                      WHERE c.fund_id = f.id
                  ), 0) - COALESCE((
                      SELECT SUM(e.amount) 
                      FROM expenses e
                      WHERE e.fund_id = f.id
                  ), 0) as balance
           FROM funds f
           WHERE f.department_id = ?
           ORDER BY f.fund_name""",
        (department_id,)
    )


def get_student_payment_report(student_id):
    """Get payment report for a specific student"""
    db = get_db()
    student = db.fetchone(
        """SELECT s.*, p.program_name, ss.session_name,
                  sec.section_name, sh.shift_name
           FROM students s
           LEFT JOIN programs p ON s.program_id = p.id
           LEFT JOIN sessions ss ON s.session_id = ss.id
           LEFT JOIN sections sec ON s.section_id = sec.id
           LEFT JOIN shifts sh ON s.shift_id = sh.id
           WHERE s.id = ?""",
        (student_id,)
    )
    
    if not student:
        return None
    
    payments = db.fetchall(
        """SELECT p.*, c.campaign_name, f.fund_name
           FROM payments p
           JOIN campaigns c ON p.campaign_id = c.id
           LEFT JOIN funds f ON c.fund_id = f.id
           WHERE p.student_id = ?
           ORDER BY p.payment_date DESC""",
        (student_id,)
    )
    
    return {
        "student": student,
        "payments": payments,
        "total_paid": sum(p["amount"] for p in payments) if payments else 0
    }


def get_daily_summary(date=None, department_id=1):
    """Get daily collection and expense summary"""
    db = get_db()
    if not date:
        date = today_str()
    
    collections = db.fetchone(
        "SELECT COALESCE(SUM(amount), 0) as total FROM payments WHERE department_id = ? AND payment_date = ?",
        (department_id, date)
    )
    
    expenses = db.fetchone(
        "SELECT COALESCE(SUM(amount), 0) as total FROM expenses WHERE department_id = ? AND expense_date = ?",
        (department_id, date)
    )
    
    return {
        "date": date,
        "total_collection": collections["total"] if collections else 0,
        "total_expense": expenses["total"] if expenses else 0,
        "balance": (collections["total"] if collections else 0) - (expenses["total"] if expenses else 0)
    }


def get_overall_summary(department_id=1):
    """Get overall system summary"""
    db = get_db()
    
    students = db.fetchone("SELECT COUNT(*) as count FROM students WHERE department_id = ?", (department_id,))
    
    total_collection = db.fetchone(
        "SELECT COALESCE(SUM(amount), 0) as total FROM payments WHERE department_id = ?",
        (department_id,)
    )
    
    total_expenses = db.fetchone(
        "SELECT COALESCE(SUM(amount), 0) as total FROM expenses WHERE department_id = ?",
        (department_id,)
    )
    
    campaigns = db.fetchone(
        "SELECT COUNT(*) as count FROM campaigns WHERE department_id = ? AND is_active = 1",
        (department_id,)
    )
    
    funds = db.fetchone(
        "SELECT COUNT(*) as count FROM funds WHERE department_id = ? AND is_active = 1",
        (department_id,)
    )
    
    return {
        "total_students": students["count"] if students else 0,
        "total_collection": total_collection["total"] if total_collection else 0,
        "total_expenses": total_expenses["total"] if total_expenses else 0,
        "balance": (total_collection["total"] if total_collection else 0) - 
                   (total_expenses["total"] if total_expenses else 0),
        "active_campaigns": campaigns["count"] if campaigns else 0,
        "active_funds": funds["count"] if funds else 0
    }