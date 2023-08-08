from fastapi import APIRouter, Depends, HTTPException, status
from schemas.column_definition import (
    ColumnDefinitionRead,
    ColumnDefinitionCreate,
    ColumnDefinitionUpdate,
)
from sqlmodel import Session
from crud.column_definition import (
    create_column_definition,
    get_column_definition,
    update_column_definition,
    delete_column_definition,
    list_column_definitions,
)
from db_internal import get_db
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/{table_configuration_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=ColumnDefinitionRead,
)
async def create_column_definition_endpoint(
    table_configuration_id: int,
    column_definition_data: ColumnDefinitionCreate,
    db: Session = Depends(get_db),
):
    return create_column_definition(db, table_configuration_id, column_definition_data)


@router.get("/{column_definition_id}", response_model=ColumnDefinitionRead)
async def get_column_definition_endpoint(
    column_definition_id: int, db: Session = Depends(get_db)
):
    column_def = get_column_definition(db, column_definition_id)
    if not column_def:
        raise HTTPException(status_code=404, detail="Column Definition not found")
    return column_def


@router.put("/{column_definition_id}", response_model=ColumnDefinitionRead)
async def update_column_definition_endpoint(
    column_definition_id: int,
    column_definition_data: ColumnDefinitionUpdate,
    db: Session = Depends(get_db),
):
    return update_column_definition(db, column_definition_id, column_definition_data)


@router.delete("/{column_definition_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_column_definition_endpoint(
    column_definition_id: int, db: Session = Depends(get_db)
):
    success = delete_column_definition(db, column_definition_id)
    if not success:
        raise HTTPException(status_code=404, detail="Column Definition not found")


@router.get("/", response_model=list[ColumnDefinitionRead])
async def list_column_definitions_endpoint(db: Session = Depends(get_db)):
    return list_column_definitions(db)
