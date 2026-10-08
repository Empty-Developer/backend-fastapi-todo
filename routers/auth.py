from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from database.database import get_db
from sqlalchemy.orm import Session
from schemas.user_schemas import UserLogin
from models import User
from core import verify, create_access_token


router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == user_credentials.username).first()

    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")

    verified = verify(user_credentials.password, user.password)

    if not verified:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Incorrect password")

    access_token = create_access_token(data={"user_id": user.id})

    return {"message": "Login successful", "access_token": access_token, "token_type": "bearer"}