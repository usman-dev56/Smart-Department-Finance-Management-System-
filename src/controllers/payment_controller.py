# src/controllers/payment_controller.py
"""Payment Controller"""
from src.database.db_manager import get_db
from src.models.department import Department
from src.models.payment import Payment
from src.services.pdf_service import generate_receipt_pdf
from src.services.qr_service import generate_qr_code
from src.utils.helpers import today_str, get_receipt_dir
import os


def generate_receipt_number():
    """Generate a unique receipt number"""
    db = get_db()
    dept = Department.get_current()
    prefix = dept.receipt_prefix if dept else "DEPT"
    row = db.fetchone("SELECT next_receipt_number FROM departments LIMIT 1")
    num = row["next_receipt_number"] if row else 1
    receipt_no = f"{prefix}-{num:05d}"
    db.execute("UPDATE departments SET next_receipt_number = next_receipt_number + 1")
    return receipt_no


def collect_payment(data):
    """Process a payment and generate receipt"""
    receipt_no = generate_receipt_number()
    db = get_db()

    # Build QR data
    qr_data = f"Receipt:{receipt_no}|Student:{data.get('student_name','')}|Amount:{data['amount']}|Date:{today_str()}"
    qr_path = generate_qr_code(qr_data, receipt_no)

    # Get department_id
    dept = Department.get_current()
    department_id = dept.department_id if dept else 1

    payment_data = {
        "department_id": department_id,
        "receipt_number": receipt_no,
        "campaign_id": data["campaign_id"],
        "student_id": data["student_id"],
        "amount": float(data["amount"]),
        "payment_date": data.get("payment_date", today_str()),
        "payment_method": data.get("payment_method", "Cash"),
        "received_by": data.get("received_by", "Admin"),
        "qr_code_path": qr_path,
        "notes": data.get("notes", "")
    }
    payment_id = db.insert("payments", payment_data)

    # ─── Get Student Details for Receipt ──────────────────────────────────
    # Get complete student info including semester, section, shift
    student = db.fetchone(
        """SELECT s.*, p.program_name, ss.session_name, 
                  sec.section_name, sh.shift_name
           FROM students s
           LEFT JOIN programs p ON s.program_id = p.id
           LEFT JOIN sessions ss ON s.session_id = ss.id
           LEFT JOIN sections sec ON s.section_id = sec.id
           LEFT JOIN shifts sh ON s.shift_id = sh.id
           WHERE s.id = ?""",
        (data["student_id"],)
    )
    
    # Get campaign details
    campaign = db.fetchone(
        """SELECT c.*, f.fund_name
           FROM campaigns c
           LEFT JOIN funds f ON c.fund_id = f.id
           WHERE c.id = ?""",
        (data["campaign_id"],)
    )
    
    # Build complete payment data for receipt
    payment_full = {
        "receipt_number": receipt_no,
        "payment_date": data.get("payment_date", today_str()),
        "student_name": student.get("student_name", "") if student else data.get("student_name", ""),
        "roll_number": student.get("roll_number", "") if student else "",
        "semester": student.get("semester", "") if student else "",
        "section": student.get("section_name", "") if student else "",
        "shift": student.get("shift_name", "") if student else "",
        "campaign_name": campaign.get("campaign_name", "") if campaign else "",
        "fund_name": campaign.get("fund_name", "") if campaign else "",
        "amount": float(data["amount"]),
        "payment_method": data.get("payment_method", "Cash"),
        "received_by": data.get("received_by", "Admin"),
        "qr_code_path": qr_path
    }

    # Generate receipt PDF
    receipt_path = generate_receipt_pdf(payment_full, dept, qr_path)
    db.execute("UPDATE payments SET receipt_path=? WHERE id=?", (receipt_path, payment_id))

    return payment_id, receipt_no, receipt_path


def get_payment_history(filters=None):
    """Get payment history with optional filters"""
    return Payment.list_all_with_details(filters)


def get_all_campaigns(department_id=1):
    """Get all campaigns with fund names"""
    db = get_db()
    return db.fetchall(
        """SELECT c.*, f.fund_name 
           FROM campaigns c
           LEFT JOIN funds f ON c.fund_id = f.id
           WHERE c.department_id = ?
           ORDER BY c.created_at DESC""",
        (department_id,)
    )


def get_campaign_eligible_for_student(student_id):
    """Get active campaigns a student can pay for (and hasn't paid yet)"""
    db = get_db()
    student = db.fetchone("SELECT * FROM students WHERE id=?", (student_id,))
    if not student:
        return []
    
    campaigns = db.fetchall(
        """SELECT c.*, f.fund_name FROM campaigns c
           LEFT JOIN funds f ON c.fund_id=f.id
           WHERE c.is_active=1
           AND c.department_id = ?
           AND (c.program_id IS NULL OR c.program_id=?)
           AND (c.session_id IS NULL OR c.session_id=?)
           AND (c.semester IS NULL OR c.semester=?)
           AND (c.shift_id IS NULL OR c.shift_id=?)""",
        (student["department_id"], student["program_id"], 
         student["session_id"], student["semester"], student["shift_id"])
    )
    
    # Filter out already paid
    result = []
    for c in campaigns:
        paid = db.fetchone("SELECT id FROM payments WHERE student_id=? AND campaign_id=?",
                           (student_id, c["id"]))
        if not paid:
            result.append(c)
    return result


def get_payment_by_receipt(receipt_number):
    """Get payment by receipt number"""
    db = get_db()
    return db.fetchone(
        """SELECT p.*, s.student_name, s.roll_number, 
                  c.campaign_name, f.fund_name
           FROM payments p
           JOIN students s ON p.student_id = s.id
           JOIN campaigns c ON p.campaign_id = c.id
           LEFT JOIN funds f ON c.fund_id = f.id
           WHERE p.receipt_number = ?""",
        (receipt_number,)
    )


def get_payments_by_student(student_id):
    """Get all payments for a specific student"""
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




def get_payments_by_campaign(campaign_id):
    """Get all payments for a specific campaign"""
    db = get_db()
    return db.fetchall(
        """SELECT p.*, s.student_name, s.roll_number
           FROM payments p
           JOIN students s ON p.student_id = s.id
           WHERE p.campaign_id = ?
           ORDER BY p.payment_date DESC""",
        (campaign_id,)
    )

# src/controllers/payment_controller.py - Add this function

def delete_payment(payment_id):
    """Delete a payment by ID"""
    db = get_db()
    
    # Check if payment exists
    payment = db.fetchone("SELECT id FROM payments WHERE id = ?", (payment_id,))
    if not payment:
        raise ValueError("Payment not found")
    
    # Delete the payment
    db.delete("payments", "id = ?", (payment_id,))
    return True