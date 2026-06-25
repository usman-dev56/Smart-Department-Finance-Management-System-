# src/models/program.py
from .base_model import BaseModel

class Program(BaseModel):
    TABLE = "programs"
    PRIMARY_KEY = "id"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get("id")
        self.department_id = kwargs.get("department_id")
        self.program_name = kwargs.get("program_name")
        self.program_code = kwargs.get("program_code")
        self.is_active = kwargs.get("is_active", 1)
        self.created_at = kwargs.get("created_at")