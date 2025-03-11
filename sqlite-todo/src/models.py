"""model file"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from src.database import Base


class Users(Base):
    """Schema for users table

    Parameters
    ----------
    Base : Base
    """

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(String)
    age = Column(Integer)


class Todos(Base):
    """Schema for todos table

    Parameters
    ----------
    Base : Base
    """

    __tablename__ = "todos"

    todo_id = Column(Integer, primary_key=True, index=True)
    task = Column(String)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.user_id"))
