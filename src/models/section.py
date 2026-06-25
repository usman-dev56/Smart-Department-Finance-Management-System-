# src/models/section.py
from .base_model import BaseModel

class Section(BaseModel):
    TABLE = "sections"
    PRIMARY_KEY = "id"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get("id")
        self.department_id = kwargs.get("department_id")
        self.section_name = kwargs.get("section_name")
        self.is_active = kwargs.get("is_active", 1)
        self.created_at = kwargs.get("created_at")