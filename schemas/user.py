from pydantic import BaseModel
from datetime import datetime as dt
from typing import Optional

# Pydantic models
class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    name: Optional[str]

class UserInDB(UserBase):
    id: int
    created_at: dt

class UserRead(UserInDB):
    pass
