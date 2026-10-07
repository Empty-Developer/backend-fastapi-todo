from models import User
from fastapi import Depends, HTTPException, status, APIRouter
from database.database import get_db
from schemas.user_schemas import UserCreate, UserOut
from sqlalchemy.orm import Session
from core import hash

router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):

    hashed_password = hash(user.password)
    user.password = hashed_password

    new_user = User(email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users/{id}", response_model=UserOut)
async def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user