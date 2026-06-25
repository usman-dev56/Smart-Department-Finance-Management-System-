# src/models/shift.py
from .base_model import BaseModel

class Shift(BaseModel):
    TABLE = "shifts"
    PRIMARY_KEY = "id"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get("id")
        self.department_id = kwargs.get("department_id")
        self.shift_name = kwargs.get("shift_name")
        self.is_active = kwargs.get("is_active", 1)
        self.created_at = kwargs.get("created_at")