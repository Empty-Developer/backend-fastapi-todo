from pydantic import BaseModel
from datetime import date

class ItemModel(BaseModel):
    title: str
    date: date

class UpdateItemModel(BaseModel):
    is_check: bool