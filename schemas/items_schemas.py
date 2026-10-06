from pydantic import BaseModel
from datetime import date

class ItemModel(BaseModel):
    title: str
    date: date
    user_id: int

class UpdateItemModel(BaseModel):
    is_check: bool