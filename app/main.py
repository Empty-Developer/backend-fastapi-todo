from fastapi import FastAPI
from routers import item_router, user_router, auth
from database.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router.router)
app.include_router(item_router.router)
app.include_router(auth.router)

# source .venv/bin/activate  
# uvicorn main:app --reload 

