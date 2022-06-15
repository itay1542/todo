from typing import Union, Optional

from sqlalchemy import Column, Integer, ForeignKey, DateTime, VARCHAR
from sqlalchemy.orm import relationship
from datetime import datetime

from .serializable_model import SerializableModel
from .user_model import User


class TodoEntry(SerializableModel):
    __tablename__ = "TodoEntries"

    id: Union[int, Column] = Column('ID', Integer, primary_key=True, autoincrement=True, nullable=True)
    user_id: Union[int, Column] = Column("UserId", Integer, ForeignKey(F"{User.__tablename__}.ID"), nullable=False)
    user: Optional[User] = relationship("User", backref="todos")
    title: Union[str, Column] = Column('Title', VARCHAR(50), nullable=False)
    date_time: Union[datetime, Column]  = Column('DateTime', DateTime)

    def __init__(self, user_id: int, title: str, date_time: datetime = None):
        self.user_id = user_id
        self.title = title
        self.date_time = date_time

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user": self.user.to_dict(),
            "title": self.title,
            "date_time": self.date_time
        }
