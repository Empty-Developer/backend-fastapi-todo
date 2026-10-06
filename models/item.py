from database.database import Base
from datetime import date as py_date
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    is_check = Column(Boolean, nullable=False, server_default="False")
    created_at = Column(Date, nullable=False, default=py_date.today, server_default="NOW()")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="items")