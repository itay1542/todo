from typing import Union

from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from src.data_access.models.serializable_model import SerializableModel


class User(SerializableModel):
    __tablename__ = "Users"

    id: Union[int, Column] = Column('ID', Integer, primary_key=True, autoincrement=True, nullable=True)
    username: Union[str, Column] = Column('Username', VARCHAR(50), nullable=False, unique=True)
    password_hash: Union[str, Column] = Column('PasswordHash', VARCHAR(200), nullable=False)
    todos: relationship("TodoEntry", back_populates="user")

    def __init__(self, username: str, password: str):
        self.username = username
        self.password_hash = generate_password_hash(password)

    @property
    def password(self):
        raise AttributeError('password is not accessible')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def toDict(self):
        return {
            "username": self.username
        }
