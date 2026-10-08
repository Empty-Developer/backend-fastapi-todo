from fastapi import Depends, HTTPException, status, APIRouter, Response
from database.database import get_db
from sqlalchemy.orm import Session
from schemas.user_schemas import UserLogin
from models import User
from core import verify 

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(user_credentials: UserLogin, response: Response, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == user_credentials.email).first()

    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")

    verified = verify(user_credentials.password, user.password)

    if not verified:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Incorrect password")

    return {"message": "Login successful", "user_id": user.id}