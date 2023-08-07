from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import select, Session
from db_internal import SessionLocal
from crud.table_configuration import create_table_configuration, get_table_configuration, update_table_configuration, delete_table_configuration, list_table_configurations
from schemas.table_configuration import TableConfigurationCreate, TableConfigurationUpdate, TableConfigurationRead

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=TableConfigurationRead,
)
def create_table_config_endpoint(table_configuration_data: TableConfigurationCreate, db: Session = Depends(get_db)):
    return create_table_configuration(db, table_configuration_data)

@router.get(
    "/{table_configuration_id}",
    response_model=TableConfigurationRead
)
def get_table_config_endpoint(table_configuration_id: int, db: Session = Depends(get_db)):
    table_config = get_table_configuration(db, table_configuration_id)
    if not table_config:
        raise HTTPException(status_code=404, detail="TableConfiguration not found")
    return table_config

@router.put(
    "/{table_configuration_id}",
    response_model=TableConfigurationRead
)
def update_table_config_endpoint(table_configuration_id: int, table_configuration_data: TableConfigurationUpdate, db: Session = Depends(get_db)):
    return update_table_configuration(db, table_configuration_id, table_configuration_data)

@router.delete(
    "/{table_configuration_id}",
    response_model=bool
)
def delete_table_config_endpoint(table_configuration_id: int, db: Session = Depends(get_db)):
    success = delete_table_configuration(db, table_configuration_id)
    if not success:
        raise HTTPException(status_code=404, detail="TableConfiguration not found")
    return True

@router.get(
    "/",
    response_model=list[TableConfigurationRead]
)
def list_table_configs_endpoint(db: Session = Depends(get_db)):
    return list_table_configurations(db)
