from typing import Optional
from sqlmodel import Field, SQLModel, Column, JSON, Relationship, ForeignKey, Integer
from datetime import datetime as dt
from schemas.column_constraint import ConstraintType


class ColumnConstraint(SQLModel, table=True):
    __tablename__ = "column_constraint"
    id: Optional[int] = Field(default=None, primary_key=True)
    constraint_type: ConstraintType = Field(
        description="Type of constraint. E.g. 'picklist', 'float', 'regex', 'bool'."
    )
    parameters: dict = Field(
        sa_column=Column(JSON),
        description="Constraint parameters. E.g. '[corn, wheat, barley, hops]' for picklist, '0 <= x < 10' for float, etc. Could be stored as JSON string.",
    )
    column_definition_id: int = Field(
        sa_column=Column(
            Integer, ForeignKey("column_definition.id", ondelete="CASCADE")
        ),
        unique=True,  # This ensures the one-to-one relationship
        description="ID of the associated column definition.",
    )
    column_definition: "ColumnDefinition" = Relationship(
        back_populates="column_constraint"
    )
    created_at: dt = Field(
        default_factory=dt.utcnow,
        description="Timestamp of when the constraint was created.",
    )
