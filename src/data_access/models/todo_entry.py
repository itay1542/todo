from typing import Union

from sqlalchemy import Column, Integer, ForeignKey, DateTime, VARCHAR
from sqlalchemy.orm import relationship

from .serializable_model import SerializableModel
from .user_model import User


class TodoEntry(SerializableModel):
    __tablename__ = "TodoEntries"

    id: Union[int, Column] = Column('ID', Integer, primary_key=True, autoincrement=True, nullable=True)
    user_id = Column("UserId", Integer, ForeignKey(F"{User.__tablename__}.ID"), nullable=False)
    user = relationship("User", backref="todos")
    title: Union[str, Column] = Column('Title', VARCHAR(50), nullable=False)
    date_time = Column('DateTime', DateTime)

    def __init__(self, todo_builder):
        self.user_id = todo_builder.user_id
        self.title = todo_builder.title
        self.date_time = todo_builder.datetime

    def toDict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user": self.user.toDict(),
            "title": self.title,
            "date_time": self.date_time
        }
