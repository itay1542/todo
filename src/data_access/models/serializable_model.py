from abc import abstractmethod

from src.data_access.database import db


class SerializableModel(db.Model):
    __abstract__ = True

    @abstractmethod
    def toDict(self):
        pass
