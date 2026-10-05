import os
import psycopg
import time
from typing import Optional
from fastapi import FastAPI, Response, HTTPException, status
from fastapi.params import Body
from pydantic import BaseModel
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv()

app = FastAPI()

# database connection setup

while True:
    
    try:
        conn = psycopg.connect(
            host=os.getenv("HOST"),
            dbname=os.getenv("DBNAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("PASSWORD"),
            port=os.getenv("PORT"),
            row_factory=dict_row
        )
        cursor = conn.cursor() 
        print("Connected to the database successfully!")
        break
    except Exception as err:
        print(f"Error connecting to the database: {err}")
        time.sleep(5)  # wait for 5 seconds before retrying

# source .venv/bin/activate  
# uvicorn main:app --reload 

@app.get("/items")
async def get_items():
    cursor.execute("""SELECT * FROM items""")
    items = cursor.fetchall()
    return {"items": items}