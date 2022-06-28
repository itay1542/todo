from src.data_access.database import db


class SerializableModel(db.Model):
    __abstract__ = True

    def serialize(self) -> dict:
        pass
