from pydantic import BaseModel
from typing import Optional, List
from schemas.column_definition import ColumnDefinitionCreate, ColumnDefinitionRead
from models import ColumnDefinition

class TableConfigurationCreate(BaseModel):
    name: str
    years_to_collect: int
    created_by: int
    updated_by: Optional[int]
    columns: List[ColumnDefinitionCreate]

class TableConfigurationUpdate(BaseModel):
    name: Optional[str]
    years_to_collect: Optional[int]
    updated_by: int

class TableConfigurationRead(BaseModel):
    id: int
    name: str
    years_to_collect: int
    created_by: int
    updated_by: Optional[int]
    columns: List[ColumnDefinitionRead]

    class Config:
        orm_mode = True
