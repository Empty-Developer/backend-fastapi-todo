from core import get_current_user
from models import Item
from fastapi import Depends, HTTPException, status, APIRouter
from database.database import get_db
from schemas.items_schemas import ItemBase, UpdateItemBase
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/items"
)

# method for getting items
@router.get("")
async def get_items(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    items = (
        db.query(Item)
        .filter(Item.user_id == current_user.id)
        .all()
    )
    return {"items": items}

# method for getting a single item by ID
@router.get("/{id}")
async def get_item_by_id(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    item = db.query(Item).filter(Item.id == id, Item.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return {"item": item}

# method for creating a new item
@router.post("", status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemBase, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    new_item = Item(title=item.title, date=item.date, user_id=current_user.id)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return {"created_item": new_item}

# method for deleting an item
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    item = (db.query(Item).filter(Item.id == id, Item.user_id == current_user.id).first())
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    db.delete(item)
    db.commit()
    return {"deleted_item": item}

# method for updating an item
@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_item(id: int, item: ItemBase, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_item = db.query(Item).filter(Item.id == id, Item.user_id == current_user.id).first()
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    db_item.title = item.title
    db_item.date = item.date
    db.commit()
    db.refresh(db_item)
    return {"updated_item": db_item}

# method update one property of an item
@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_one_property(id: int, item: UpdateItemBase, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if item.is_check is not None:
        db_item = db.query(Item).filter(Item.id == id, Item.user_id == current_user.id).first()
        if not db_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        db_item.is_check = item.is_check
        db.commit()
        db.refresh(db_item)
    return {"updated_item": db_item}