from sqlalchemy import create_engine
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "postgresql+psycopg://postgres:1289@localhost:5434/student_management"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


class Base(DeclarativeBase):
    pass




