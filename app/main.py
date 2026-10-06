from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from schemas.items_schemas import ItemModel, UpdateItemModel
from database.database import Base, engine, get_db
from models import Item, User

Base.metadata.create_all(bind=engine)

app = FastAPI()

# source .venv/bin/activate  
# uvicorn main:app --reload 

# method for getting items
@app.get("/items")
async def get_items():
    cursor.execute("""SELECT * FROM items""")
    items = cursor.fetchall()
    return {"items": items}

# method for creating a new item
@app.post("/create-item", status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemModel):
    cursor.execute("""INSERT INTO items (title, date) VALUES (%s, %s) RETURNING *""", (item.title, item.date))
    new_item = cursor.fetchone()
    conn.commit()
    return {"created_item": new_item}

# method for getting a single item by ID
@app.get("/items/{id}")
async def get_item(id: int):
    cursor.execute("""SELECT * FROM items WHERE id = %s""", (id,))
    item = cursor.fetchone()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return {"item": item}

# method for deleting an item
@app.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(id: int):
    cursor.execute("""DELETE FROM items WHERE id = %s RETURNING *""", (id,))
    deleted_item = cursor.fetchone()
    conn.commit()
    if not deleted_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return {"deleted_item": deleted_item}


# method for updating an item
@app.put("/items/{id}", status_code=status.HTTP_200_OK)
async def update_item(id: int, item: ItemModel):
    cursor.execute("""UPDATE items SET title = %s, date = %s WHERE id = %s RETURNING *""", (item.title, item.date, id))
    updated_item = cursor.fetchone()
    conn.commit()
    if not updated_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return {"updated_item": updated_item}

# method update one property of an item
@app.patch("/items/{id}", status_code=status.HTTP_200_OK)
async def update_one_property(id: int, item: UpdateItemModel):
    if item.is_check is not None:
        cursor.execute("""UPDATE items SET is_check = %s WHERE id = %s RETURNING *""", (item.is_check, id))
    updated_item = cursor.fetchone()
    conn.commit()
    if not updated_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return {"updated_item": updated_item}

@app.get("get_items")
def test_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return {"items": items}