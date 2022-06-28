from datetime import datetime
from typing import Any, Union, Optional

from sqlalchemy import VARCHAR, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .serializable_model import SerializableModel
from .user_model import User


class TodoEntry(SerializableModel):
    __tablename__ = "TodoEntries"

    id: Union[int, Column] = Column(
        "ID", Integer, primary_key=True, autoincrement=True, nullable=True
    )
    user_id: Union[int, Column] = Column(
        "UserId", Integer, ForeignKey(f"{User.__tablename__}.ID"), nullable=False
    )
    user: Any = relationship("User", backref="todos")
    title: Optional[Union[str, Column]] = Column("Title", VARCHAR(50), nullable=False)
    date_time: Union[datetime, Column] = Column("DateTime", DateTime)

    def __init__(self, user_id: int, title: str, date_time: datetime = None):
        self.user_id = user_id
        self.title = title
        self.date_time = date_time  # type: ignore

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user": self.user.serialize(),
            "title": self.title,
            "date_time": self.date_time,
        }
