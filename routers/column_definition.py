from fastapi import APIRouter, Depends, status, HTTPException
from models import ColumnDefinition
from sqlmodel import Session
from db_internal import SessionLocal  # Make sure you have this import in your code
from crud.column_definition import (  # Update this import path accordingly
    create_column_definition, 
    get_column_definition, 
    update_column_definition, 
    delete_column_definition, 
    list_column_definitions
)
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ColumnDefinitionIn(BaseModel):
    # Here, you'd specify the input fields needed to create/update a ColumnDefinition.
    # I'm just using a generic set for demonstration purposes. 
    # Adjust the fields according to your model's attributes.
    name: str
    type: str
    description: Optional[str]

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ColumnDefinition,
)
def create_column_definition_endpoint(column_definition_data: ColumnDefinitionIn, db: Session = Depends(get_db)):
    return create_column_definition(db, column_definition_data)

@router.get(
    "/{column_definition_id}",
    response_model=ColumnDefinition
)
def get_column_definition_endpoint(column_definition_id: int, db: Session = Depends(get_db)):
    column_def = get_column_definition(db, column_definition_id)
    if not column_def:
        raise HTTPException(status_code=404, detail="ColumnDefinition not found")
    return column_def

@router.put(
    "/{column_definition_id}",
    response_model=ColumnDefinition
)
def update_column_definition_endpoint(column_definition_id: int, column_definition_data: ColumnDefinitionIn, db: Session = Depends(get_db)):
    return update_column_definition(db, column_definition_id, column_definition_data)

@router.delete(
    "/{column_definition_id}",
    response_model=bool
)
def delete_column_definition_endpoint(column_definition_id: int, db: Session = Depends(get_db)):
    success = delete_column_definition(db, column_definition_id)
    if not success:
        raise HTTPException(status_code=404, detail="ColumnDefinition not found")
    return True

@router.get(
    "/",
    response_model=list[ColumnDefinition]
)
def list_column_definitions_endpoint(db: Session = Depends(get_db)):
    return list_column_definitions(db)
