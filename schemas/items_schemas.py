from pydantic import BaseModel
from datetime import date

class ItemBase(BaseModel):
    title: str
    date: date

class UpdateItemBase(BaseModel):
    is_check: bool