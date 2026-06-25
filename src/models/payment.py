# src/models/payment.py
from .base_model import BaseModel

class Payment(BaseModel):
    TABLE = "payments"
    PRIMARY_KEY = "id"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get("id")
        self.department_id = kwargs.get("department_id")
        self.receipt_number = kwargs.get("receipt_number")
        self.campaign_id = kwargs.get("campaign_id")
        self.student_id = kwargs.get("student_id")
        self.amount = kwargs.get("amount")
        self.payment_date = kwargs.get("payment_date")
        self.payment_method = kwargs.get("payment_method", "Cash")
        self.received_by = kwargs.get("received_by")
        self.qr_code_path = kwargs.get("qr_code_path")
        self.receipt_path = kwargs.get("receipt_path")
        self.notes = kwargs.get("notes")
        self.created_at = kwargs.get("created_at")

    @classmethod
    def get_with_details(cls, payment_id):
        """Get payment with student and campaign details"""
        db = cls._db()
        row = db.fetchone(
            """SELECT p.*, s.student_name, s.roll_number, 
                      c.campaign_name, f.fund_name
               FROM payments p
               JOIN students s ON p.student_id = s.id
               JOIN campaigns c ON p.campaign_id = c.id
               LEFT JOIN funds f ON c.fund_id = f.id
               WHERE p.id = ?""",
            (payment_id,)
        )
        return row if row else None

    @classmethod
    def list_all_with_details(cls, filters=None):
        """Get all payments with student and campaign details"""
        db = cls._db()
        query = """
            SELECT p.*, s.student_name, s.roll_number, 
                   c.campaign_name, f.fund_name
            FROM payments p
            JOIN students s ON p.student_id = s.id
            JOIN campaigns c ON p.campaign_id = c.id
            LEFT JOIN funds f ON c.fund_id = f.id
        """
        params = []
        conditions = []
        
        if filters:
            if filters.get("student_id"):
                conditions.append("p.student_id = ?")
                params.append(filters["student_id"])
            if filters.get("campaign_id"):
                conditions.append("p.campaign_id = ?")
                params.append(filters["campaign_id"])
            if filters.get("start_date"):
                conditions.append("p.payment_date >= ?")
                params.append(filters["start_date"])
            if filters.get("end_date"):
                conditions.append("p.payment_date <= ?")
                params.append(filters["end_date"])
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY p.payment_date DESC"
        
        return db.fetchall(query, params)

    def get_student(self):
        """Get the student who made this payment"""
        from .student import Student
        return Student.find(self.student_id)

    def get_campaign(self):
        """Get the campaign for this payment"""
        from .campaign import Campaign
        return Campaign.find(self.campaign_id)