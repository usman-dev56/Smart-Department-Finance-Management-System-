# src/models/department.py
from .base_model import BaseModel

class Department(BaseModel):
    TABLE = "departments"
    PRIMARY_KEY = "department_id"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.department_id = kwargs.get("department_id")
        self.department_name = kwargs.get("department_name")
        self.university_name = kwargs.get("university_name")
        self.logo_path = kwargs.get("logo_path")
        self.email = kwargs.get("email")
        self.phone = kwargs.get("phone")
        self.address = kwargs.get("address")
        self.receipt_prefix = kwargs.get("receipt_prefix", "DEPT")
        self.next_receipt_number = kwargs.get("next_receipt_number", 1)
        self.created_at = kwargs.get("created_at")
        self.updated_at = kwargs.get("updated_at")

    # ─── Get Current Department ──────────────────────────────────────────

    @classmethod
    def get_current(cls):
        """Get the current/active department"""
        db = cls._db()
        row = db.fetchone("SELECT * FROM departments LIMIT 1")
        if row:
            return cls(**row)
        return None

    # ─── Relationships ──────────────────────────────────────────────────

    def get_students(self):
        """Get all students in this department"""
        from .student import Student
        return Student.where(department_id=self.department_id)

    def get_funds(self):
        """Get all funds in this department"""
        from .fund import Fund
        return Fund.where(department_id=self.department_id)

    def get_campaigns(self):
        """Get all campaigns in this department"""
        from .campaign import Campaign
        return Campaign.where(department_id=self.department_id)

    def get_payments(self):
        """Get all payments in this department"""
        from .payment import Payment
        return Payment.where(department_id=self.department_id)

    def get_expenses(self):
        """Get all expenses in this department"""
        from .expense import Expense
        return Expense.where(department_id=self.department_id)

    # ─── Financial Summary ─────────────────────────────────────────────

    def get_total_collection(self):
        """Get total collection for this department"""
        db = self._db()
        result = db.fetchone(
            "SELECT COALESCE(SUM(amount), 0) as total FROM payments WHERE department_id = ?",
            (self.department_id,)
        )
        return result['total'] if result else 0

    def get_total_expenses(self):
        """Get total expenses for this department"""
        db = self._db()
        result = db.fetchone(
            "SELECT COALESCE(SUM(amount), 0) as total FROM expenses WHERE department_id = ?",
            (self.department_id,)
        )
        return result['total'] if result else 0

    def get_balance(self):
        """Get current balance (collection - expenses)"""
        return self.get_total_collection() - self.get_total_expenses()

    def get_student_count(self):
        """Get total number of students in this department"""
        db = self._db()
        result = db.fetchone(
            "SELECT COUNT(*) as count FROM students WHERE department_id = ? AND is_active = 1",
            (self.department_id,)
        )
        return result['count'] if result else 0

    def get_campaign_count(self):
        """Get total number of active campaigns in this department"""
        db = self._db()
        result = db.fetchone(
            "SELECT COUNT(*) as count FROM campaigns WHERE department_id = ? AND is_active = 1",
            (self.department_id,)
        )
        return result['count'] if result else 0

    # ─── Receipt Settings ──────────────────────────────────────────────

    def get_next_receipt_number(self):
        """Get next receipt number and increment"""
        db = self._db()
        current = self.next_receipt_number or 1
        db.execute(
            "UPDATE departments SET next_receipt_number = next_receipt_number + 1 WHERE department_id = ?",
            (self.department_id,)
        )
        return current

    def generate_receipt_number(self):
        """Generate a receipt number with prefix"""
        num = self.get_next_receipt_number()
        return f"{self.receipt_prefix}-{num:05d}"

    # ─── Department Info ──────────────────────────────────────────────

    def get_full_name(self):
        """Get full department name with university"""
        return f"{self.university_name} - Department of {self.department_name}"

    def to_dict(self):
        """Convert department to dictionary with computed fields"""
        data = super().to_dict()
        data['student_count'] = self.get_student_count()
        data['total_collection'] = self.get_total_collection()
        data['total_expenses'] = self.get_total_expenses()
        data['balance'] = self.get_balance()
        return data