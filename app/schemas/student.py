from pydantic import BaseModel
from datetime import date

class StudentCreate(BaseModel):
    name : str
    email: str
    phone: str
    date_of_birth: date | None = None

