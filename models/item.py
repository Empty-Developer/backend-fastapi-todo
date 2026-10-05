from database.database import Base
from datetime import date
from sqlalchemy import Column, Integer, String, Date, Boolean

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    is_check = Column(Boolean, nullable=False, default=False)
    created_at = Column(Date, nullable=False, default=date.today)