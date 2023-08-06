from sqlalchemy.orm import Session
from typing import List, Optional
from models import ColumnDefinition  # Ensure this model is imported from your models module

# Create a new column definition
def create_column_definition(db: Session, column_definition_data: ColumnDefinition) -> ColumnDefinition:
    db_column_definition = ColumnDefinition(**column_definition_data.dict())
    db.add(db_column_definition)
    db.commit()
    db.refresh(db_column_definition)
    return db_column_definition

# Get a column definition by its ID
def get_column_definition(db: Session, column_definition_id: int) -> Optional[ColumnDefinition]:
    return db.query(ColumnDefinition).filter(ColumnDefinition.id == column_definition_id).first()

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
    db_column_definition = db.query(ColumnDefinition).filter(ColumnDefinition.id == column_definition_id).first()
    if db_column_definition:
        db.delete(db_column_definition)
        db.commit()
        return True
    return False

# List all column definitions (optional)
def list_column_definitions(db: Session) -> List[ColumnDefinition]:
    return db.query(ColumnDefinition).all()
