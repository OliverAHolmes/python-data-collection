from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from models import (
    ColumnDefinition,
    ColumnConstraint,
)
from schemas.column_definition import ColumnDefinitionRead


def create_column_definition(
    db: Session, table_configuration_id: int, table_configuration_data: ColumnDefinition
) -> ColumnDefinition:
    # Convert the Pydantic model into a dictionary
    column_definition_dict = table_configuration_data.dict()
    # Extract columns from the dictionary
    column_constraint = column_definition_dict.pop("column_constraint", None)

    db_column_definition = ColumnDefinition(**column_definition_dict)
    db_column_definition.table_configuration_id = table_configuration_id

    # Commit the db_column_definition first to get an ID
    db.add(db_column_definition)
    db.commit()

    if column_constraint:
        column_constraint["column_definition_id"] = db_column_definition.id
        db_column_constraint = ColumnConstraint(**column_constraint)
        db.add(db_column_constraint)
        db.commit()

    # Adjust the filtering condition
    related_columns_data = (
        db.query(ColumnDefinition)
        .options(joinedload(ColumnDefinition.column_constraint))
        .filter(ColumnDefinition.id == db_column_definition.id)
        .first()
    )

    return related_columns_data


# Get a column definition by its ID
def get_column_definition(
    db: Session, column_definition_id: int
) -> Optional[ColumnDefinition]:
    return (
        db.query(ColumnDefinition)
        .filter(ColumnDefinition.id == column_definition_id)
        .first()
    )


# Update a column definition
def update_column_definition(
    db: Session, column_definition_id: int, column_definition_data: ColumnDefinition
) -> ColumnDefinition:
    existing_column_definition = db.get(ColumnDefinition, column_definition_id)
    if not existing_column_definition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ColumnDefinition not found",
        )
    # Update the fields of the existing column definition
    for key, value in column_definition_data.dict(exclude_unset=True).items():
        setattr(existing_column_definition, key, value)

    db.add(existing_column_definition)
    db.commit()
    db.refresh(existing_column_definition)

    return existing_column_definition


# Delete a column definition
def delete_column_definition(db: Session, column_definition_id: int) -> bool:
    db_column_definition = (
        db.query(ColumnDefinition)
        .filter(ColumnDefinition.id == column_definition_id)
        .first()
    )
    if db_column_definition:
        db.delete(db_column_definition)
        db.commit()
        return True
    return False


# List all column definitions (optional)
def list_column_definitions(db: Session) -> List[ColumnDefinition]:
    return db.query(ColumnDefinition).all()
