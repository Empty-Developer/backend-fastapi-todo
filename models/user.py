from database.database import Base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from datetime import date as py_date

# user orm schema
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(Date, nullable=False, default=py_date.today, server_default="NOW()")

    items = relationship("Item", back_populates="user", cascade="all, delete-orphan")