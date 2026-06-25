"""Base Model - all models extend this"""
from src.database.db_manager import get_db
from datetime import datetime


class BaseModel:
    TABLE = ""
    PRIMARY_KEY = "id"

    def __init__(self, **kwargs):
        self._data = kwargs
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def _db(cls):
        return get_db()

    @classmethod
    def all(cls):
        db = cls._db()
        rows = db.fetchall(f"SELECT * FROM {cls.TABLE}")
        return [cls(**row) for row in rows]

    @classmethod
    def find(cls, pk):
        db = cls._db()
        row = db.fetchone(
            f"SELECT * FROM {cls.TABLE} WHERE {cls.PRIMARY_KEY} = ?", (pk,)
        )
        return cls(**row) if row else None

    @classmethod
    def where(cls, **conditions):
        db = cls._db()
        where = " AND ".join([f"{k} = ?" for k in conditions])
        vals = list(conditions.values())
        rows = db.fetchall(f"SELECT * FROM {cls.TABLE} WHERE {where}", vals)
        return [cls(**row) for row in rows]

    @classmethod
    def where_raw(cls, condition, params=()):
        db = cls._db()
        rows = db.fetchall(f"SELECT * FROM {cls.TABLE} WHERE {condition}", params)
        return [cls(**row) for row in rows]

    @classmethod
    def count(cls, condition="1=1", params=()):
        db = cls._db()
        row = db.fetchone(f"SELECT COUNT(*) as cnt FROM {cls.TABLE} WHERE {condition}", params)
        return row["cnt"] if row else 0

    def save(self):
        db = self._db()
        data = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        pk = data.pop(self.PRIMARY_KEY, None)
        if pk:
            db.update(self.TABLE, data, f"{self.PRIMARY_KEY} = ?", (pk,))
            return pk
        else:
            new_id = db.insert(self.TABLE, data)
            setattr(self, self.PRIMARY_KEY, new_id)
            return new_id

    def delete(self):
        pk = getattr(self, self.PRIMARY_KEY, None)
        if pk:
            self._db().delete(self.TABLE, f"{self.PRIMARY_KEY} = ?", (pk,))
            return True
        return False

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}