# src/models/campaign.py
from .base_model import BaseModel
from .student import Student
from .payment import Payment

class Campaign(BaseModel):
    TABLE = "campaigns"
    PRIMARY_KEY = "id"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get("id")
        self.department_id = kwargs.get("department_id")
        self.campaign_name = kwargs.get("campaign_name")
        self.fund_id = kwargs.get("fund_id")
        self.program_id = kwargs.get("program_id")
        self.session_id = kwargs.get("session_id")
        self.semester = kwargs.get("semester")
        self.shift_id = kwargs.get("shift_id")
        self.required_amount = kwargs.get("required_amount", 0)
        self.is_active = kwargs.get("is_active", 1)
        self.created_at = kwargs.get("created_at")
        self.updated_at = kwargs.get("updated_at")

    # ─── NEW METHOD: Get campaign with details ──────────────────────────
    
    @classmethod
    def get_with_details(cls, campaign_id):
        """Get campaign with fund, program, session, shift details"""
        db = cls._db()
        row = db.fetchone(
            """SELECT c.*, f.fund_name, f.fund_description,
                      p.program_name, s.session_name, sh.shift_name
               FROM campaigns c
               LEFT JOIN funds f ON c.fund_id = f.id
               LEFT JOIN programs p ON c.program_id = p.id
               LEFT JOIN sessions s ON c.session_id = s.id
               LEFT JOIN shifts sh ON c.shift_id = sh.id
               WHERE c.id = ?""",
            (campaign_id,)
        )
        return row if row else None

    # ─── EXISTING METHODS ──────────────────────────────────────────────────

    def get_paid_students(self):
        """Get all students who have paid for this campaign"""
        payments = Payment.where(campaign_id=self.id)
        students = []
        for payment in payments:
            student = Student.find(payment.student_id)
            if student:
                students.append(student)
        return students

    def get_pending_students(self):
        """Get all eligible students who haven't paid yet"""
        paid = self.get_paid_students()
        paid_ids = [s.id for s in paid]
        
        # Get all eligible students
        conditions = {"is_active": 1}
        if self.program_id:
            conditions["program_id"] = self.program_id
        if self.session_id:
            conditions["session_id"] = self.session_id
        if self.semester:
            conditions["semester"] = self.semester
        if self.shift_id:
            conditions["shift_id"] = self.shift_id
        
        all_students = Student.where(**conditions) if conditions else []
        return [s for s in all_students if s.id not in paid_ids]

    def get_collection_summary(self):
        """Get summary of collection for this campaign"""
        payments = Payment.where(campaign_id=self.id)
        paid_students = len(payments)
        total_collected = sum(p.amount for p in payments) if payments else 0
        
        # Get eligible students
        conditions = {"is_active": 1}
        if self.program_id:
            conditions["program_id"] = self.program_id
        if self.session_id:
            conditions["session_id"] = self.session_id
        if self.semester:
            conditions["semester"] = self.semester
        if self.shift_id:
            conditions["shift_id"] = self.shift_id
        
        all_students = Student.where(**conditions) if conditions else []
        total_students = len(all_students)
        
        return {
            "total_collected": total_collected,
            "paid_students": paid_students,
            "total_students": total_students,
            "pending_students": total_students - paid_students,
            "collection_percentage": (paid_students / total_students * 100) if total_students > 0 else 0
        }