import os
import psycopg
from typing import Optional
from fastapi import FastAPI, Response, HTTPException, status
from fastapi.params import Body
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
 
try:
    conn = psycopg.connect(
        host=os.getenv("HOST"),
        dbname=os.getenv("DBNAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("PASSWORD"),
        port=os.getenv("PORT"),
    ) 
    print("Connected to the database successfully!")
except Exception as e:
    print(f"Error connecting to the database: {e}")
 
class Item(BaseModel):
    title: str
    data: str
    completed: bool = False

@app.get("/items") 
async def get_all_items(response: Response):
    if not items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No items found")
    return {"items": items}

@app.post("/create/items", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    item_dict = item.dict()
    items.append(item_dict)
    return {"message": f"{item.title}: {item.data}", "completed": item.completed}

# source .venv/bin/activate  
# uvicorn main:app --reload 