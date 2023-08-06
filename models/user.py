from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime as dt

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    created_at: dt = Field(default_factory=dt.utcnow)