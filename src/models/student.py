# src/models/student.py
from .base_model import BaseModel
from .payment import Payment

class Student(BaseModel):
    TABLE = "students"
    PRIMARY_KEY = "id"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get("id")
        self.department_id = kwargs.get("department_id")
        self.roll_number = kwargs.get("roll_number")
        self.student_name = kwargs.get("student_name")
        self.program_id = kwargs.get("program_id")
        self.session_id = kwargs.get("session_id")
        self.semester = kwargs.get("semester", 1)
        self.section_id = kwargs.get("section_id")
        self.shift_id = kwargs.get("shift_id")
        self.phone = kwargs.get("phone")
        self.email = kwargs.get("email")
        self.is_active = kwargs.get("is_active", 1)
        self.created_at = kwargs.get("created_at")
        self.updated_at = kwargs.get("updated_at")

    def get_payments(self):
        """Get all payments for this student"""
        return Payment.where(student_id=self.id)

    def get_total_paid(self):
        """Get total amount paid by this student"""
        payments = self.get_payments()
        return sum(p.amount for p in payments) if payments else 0

    def has_paid_campaign(self, campaign_id):
        """Check if student has paid for a specific campaign"""
        payments = Payment.where(student_id=self.id, campaign_id=campaign_id)
        return len(payments) > 0