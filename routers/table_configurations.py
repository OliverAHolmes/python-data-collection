from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session
from db_internal import get_db
from crud.table_configuration import (
    create_table_configuration,
    get_table_configuration,
    update_table_configuration,
    delete_table_configuration,
    list_table_configurations,
)
from schemas.table_configuration import (
    TableConfigurationCreate,
    TableConfigurationUpdate,
    TableConfigurationRead,
)
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=TableConfigurationRead,
)
async def create_table_config(
    table_configuration_data: TableConfigurationCreate, db: Session = Depends(get_db)
):
    return create_table_configuration(db, table_configuration_data)


@router.get("/{table_configuration_id}", response_model=TableConfigurationRead)
async def get_table_config(table_configuration_id: int, db: Session = Depends(get_db)):
    table_config = get_table_configuration(db, table_configuration_id)
    if not table_config:
        raise HTTPException(status_code=404, detail="Table Configuration not found")
    return table_config


@router.put("/{table_configuration_id}", response_model=TableConfigurationRead)
async def update_table_config(
    table_configuration_id: int,
    table_configuration_data: TableConfigurationUpdate,
    db: Session = Depends(get_db),
):
    # existing_config = get_table_configuration(db, table_configuration_id)
    # if not existing_config:
    #     raise HTTPException(status_code=404, detail="Table Configuration not found")
    return update_table_configuration(
        db, table_configuration_id, table_configuration_data
    )


@router.delete("/{table_configuration_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_table_config(
    table_configuration_id: int, db: Session = Depends(get_db)
):
    success = delete_table_configuration(db, table_configuration_id)
    if not success:
        raise HTTPException(status_code=404, detail="Table Configuration not found")


@router.get("/", response_model=list[TableConfigurationRead])
async def list_table_configs(db: Session = Depends(get_db)):
    return list_table_configurations(db)
