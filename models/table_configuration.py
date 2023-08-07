from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime as dt
from models.column_definition import ColumnDefinition


class TableConfiguration(SQLModel, table=True):
    __tablename__ = "table_configuration"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(description="Name of the table configuration.")
    years_to_collect: int = Field(
        description="Integer, how many years of data we wish to collect (number of rows to render)."
    )
    created_by: int = Field(
        foreign_key="user.id", description="User ID of the creator."
    )
    updated_by: int = Field(
        default=None,
        foreign_key="user.id",
        description="User ID of the last person to update.",
    )
    created_at: dt = Field(default_factory=dt.utcnow)
    updated_at: dt = Field(default_factory=dt.utcnow)
    columns: List[ColumnDefinition] = Relationship(back_populates="table_configuration")
