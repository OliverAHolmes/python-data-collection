from fastapi import APIRouter, Depends, HTTPException, status
from schemas.column_definition import (
    ColumnDefinitionRead,
    ColumnDefinitionCreate,
    ColumnDefinitionUpdate,
)
from sqlmodel import Session
from db_internal import SessionLocal
from crud.column_definition import (
    create_column_definition,
    get_column_definition,
    update_column_definition,
    delete_column_definition,
    list_column_definitions,
)

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/{table_configuration_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=ColumnDefinitionRead,
)
def create_column_definition_endpoint(
    table_configuration_id: int,
    column_definition_data: ColumnDefinitionCreate,
    db: Session = Depends(get_db),
):
    return create_column_definition(db, table_configuration_id, column_definition_data)


@router.get("/{column_definition_id}", response_model=ColumnDefinitionRead)
def get_column_definition_endpoint(
    column_definition_id: int, db: Session = Depends(get_db)
):
    column_def = get_column_definition(db, column_definition_id)
    if not column_def:
        raise HTTPException(status_code=404, detail="ColumnDefinition not found")
    return column_def


@router.put("/{column_definition_id}", response_model=ColumnDefinitionRead)
def update_column_definition_endpoint(
    column_definition_id: int,
    column_definition_data: ColumnDefinitionUpdate,
    db: Session = Depends(get_db),
):
    return update_column_definition(db, column_definition_id, column_definition_data)


@router.delete("/{column_definition_id}", response_model=bool)
def delete_column_definition_endpoint(
    column_definition_id: int, db: Session = Depends(get_db)
):
    success = delete_column_definition(db, column_definition_id)
    if not success:
        raise HTTPException(status_code=404, detail="ColumnDefinition not found")
    return True


@router.get("/", response_model=list[ColumnDefinitionRead])
def list_column_definitions_endpoint(db: Session = Depends(get_db)):
    return list_column_definitions(db)
