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
async def get_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return {"items": items}

# method for getting a single item by ID
@app.get("/items/{id}")
async def get_item(id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return {"item": item}

# method for creating a new item
@app.post("/create-item", status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemModel, db: Session = Depends(get_db)):
    new_item = Item(title=item.title, date=item.date, user_id=item.user_id)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return {"created_item": new_item}

# method for deleting an item
@app.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    db.delete(item)
    db.commit()
    return {"deleted_item": item}

# method for updating an item
@app.put("/items/{id}", status_code=status.HTTP_200_OK)
async def update_item(id: int, item: ItemModel, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == id).first()
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    db_item.title = item.title
    db_item.date = item.date
    db.commit()
    db.refresh(db_item)
    return {"updated_item": db_item}

# method update one property of an item
@app.patch("/items/{id}", status_code=status.HTTP_200_OK)
async def update_one_property(id: int, item: UpdateItemModel, db: Session = Depends(get_db)):
    if item.is_check is not None:
        db_item = db.query(Item).filter(Item.id == id).first()
        if not db_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        db_item.is_check = item.is_check
        db.commit()
        db.refresh(db_item)
    return {"updated_item": db_item}
