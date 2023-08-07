from sqlmodel import SQLModel, Field, Relationship, ForeignKey, Column, Integer
from typing import Optional
from datetime import datetime as dt
from models.column_constraint import ColumnConstraint


class ColumnDefinition(SQLModel, table=True):
    __tablename__ = "column_definition"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(description="Name of the column.")
    column_order: int = Field(description="Order of the column in the table.")
    table_configuration_id: int = Field(
        sa_column=Column(
            Integer, ForeignKey("table_configuration.id", ondelete="CASCADE")
        ),
        description="ID of the associated table configuration.",
    )
    created_at: dt = Field(
        default_factory=dt.utcnow,
        description="Timestamp of when the column definition was created.",
    )
    column_constraint: ColumnConstraint = Relationship(
        back_populates="column_definition", sa_relationship_kwargs={"uselist": False}
    )
    table_configuration: "TableConfiguration" = Relationship(back_populates="columns")
