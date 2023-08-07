from typing import Optional
from pydantic import BaseModel
from datetime import datetime as dt
from schemas.column_constraint import ConstraintCreate, ConstraintRead


# Pydantic models
class ColumnDefinitionBase(BaseModel):
    name: str
    column_order: int
    table_configuration_id: Optional[int]
    column_constraint: ConstraintCreate


class ColumnDefinitionCreate(ColumnDefinitionBase):
    pass


class ColumnDefinitionUpdate(BaseModel):
    name: Optional[str]
    column_order: Optional[int]
    table_configuration_id: Optional[int]


class ColumnDefinitionRead(BaseModel):
    id: int
    name: str
    column_order: int
    table_configuration_id: int
    created_at: dt
    column_constraint: ConstraintRead

    class Config:
        orm_mode = True
