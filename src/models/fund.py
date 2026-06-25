# src/models/fund.py
from .base_model import BaseModel

class Fund(BaseModel):
    TABLE = "funds"
    PRIMARY_KEY = "id"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get("id")
        self.department_id = kwargs.get("department_id")
        self.fund_name = kwargs.get("fund_name")
        self.fund_description = kwargs.get("fund_description")
        self.is_active = kwargs.get("is_active", 1)
        self.created_at = kwargs.get("created_at")
        self.updated_at = kwargs.get("updated_at")

    def get_campaigns(self):
        """Get all campaigns for this fund"""
        from .campaign import Campaign
        return Campaign.where(fund_id=self.id)