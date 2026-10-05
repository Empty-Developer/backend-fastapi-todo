import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

# database connection setup
DATABASE_URL = f"postgresql+psycopg://{os.getenv("DB_USER")}:{os.getenv("DBNAME")}@{os.getenv("HOST")}:{os.getenv("PORT")}/{os.getenv("PASSWORD")}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# while True:
    
#     try:
#         conn = psycopg.connect(
#             host=os.getenv("HOST"),
#             dbname=os.getenv("DBNAME"),
#             user=os.getenv("DB_USER"),
#             password=os.getenv("PASSWORD"),
#             port=os.getenv("PORT"),
#             row_factory=dict_row
#         )
#         cursor = conn.cursor() 
#         print("Connected to the database successfully!")
#         break
#     except Exception as err:
#         print(f"Error connecting to the database: {err}")
#         time.sleep(5)  # wait for 5 seconds before retrying