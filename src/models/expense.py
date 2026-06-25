# src/models/expense.py
from .base_model import BaseModel

class Expense(BaseModel):
    TABLE = "expenses"
    PRIMARY_KEY = "id"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get("id")
        self.department_id = kwargs.get("department_id")
        self.fund_id = kwargs.get("fund_id")
        self.expense_title = kwargs.get("expense_title")
        self.expense_description = kwargs.get("expense_description")
        self.amount = kwargs.get("amount")
        self.expense_date = kwargs.get("expense_date")
        self.created_by = kwargs.get("created_by")
        self.created_at = kwargs.get("created_at")
        self.updated_at = kwargs.get("updated_at")

    def get_fund(self):
        """Get the fund for this expense"""
        from .fund import Fund
        return Fund.find(self.fund_id)