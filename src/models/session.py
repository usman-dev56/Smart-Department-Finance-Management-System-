# src/models/session.py
from .base_model import BaseModel

class Session(BaseModel):
    TABLE = "sessions"
    PRIMARY_KEY = "id"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get("id")
        self.department_id = kwargs.get("department_id")
        self.session_name = kwargs.get("session_name")
        self.is_active = kwargs.get("is_active", 1)
        self.created_at = kwargs.get("created_at")