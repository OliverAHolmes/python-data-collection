from sqlalchemy.orm import Session, joinedload
from fastapi import status, HTTPException
from typing import List, Optional
from models import (
    TableConfiguration,
    ColumnDefinition,
    ColumnConstraint,
)

from schemas.table_configuration import TableConfigurationRead


# Create a new table configuration
def create_table_configuration(
    db: Session, table_configuration_data: TableConfiguration
) -> TableConfiguration:
    # Convert the Pydantic model into a dictionary
    table_configuration_dict = table_configuration_data.dict()
    # Extract columns from the dictionary
    columns_data = table_configuration_dict.pop("columns", [])

    # Create the TableConfiguration object using the dictionary
    db_table_configuration = TableConfiguration(**table_configuration_dict)
    db.add(db_table_configuration)
    db.flush()  # Use flush() here so that db_table_configuration gets an ID

    # For each column data, create Column Definition and Column Constraint objects
    for column_data in columns_data:
        constraint_data = column_data.pop("column_constraint", None)
        db_column_definition = ColumnDefinition(**column_data)
        db_column_definition.table_configuration_id = db_table_configuration.id

        db_table_configuration.columns.append(db_column_definition)

        if constraint_data:
            constraint_data["column_definition_id"] = db_column_definition.id
            db_column_constraint = ColumnConstraint(**constraint_data)
            db_column_definition.column_constraint = db_column_constraint

        db.add(db_column_definition)
        db.flush()  # Get the ID for the column definition

    db.commit()
    db.refresh(db_table_configuration)

    related_columns_data = (
        db.query(ColumnDefinition)
        .options(joinedload(ColumnDefinition.column_constraint))
        .filter(ColumnDefinition.table_configuration_id == db_table_configuration.id)
        .all()
    )

    return TableConfigurationRead(
        id=db_table_configuration.id,
        name=db_table_configuration.name,
        years_to_collect=db_table_configuration.years_to_collect,
        created_by=db_table_configuration.created_by,
        columns=related_columns_data,
    )


# Get a table configuration by its ID
def get_table_configuration(
    db: Session, table_configuration_id: int
) -> Optional[TableConfigurationRead]:
    table_configuration = (
        db.query(TableConfiguration)
        .filter(TableConfiguration.id == table_configuration_id)
        .first()
    )

    if not table_configuration:
        return None

    related_columns_data = (
        db.query(ColumnDefinition)
        .options(joinedload(ColumnDefinition.column_constraint))
        .filter(ColumnDefinition.table_configuration_id == table_configuration.id)
        .all()
    )

    return TableConfigurationRead(
        id=table_configuration.id,
        name=table_configuration.name,
        years_to_collect=table_configuration.years_to_collect,
        created_by=table_configuration.created_by,
        columns=related_columns_data,
    )


# Update a table configuration
def update_table_configuration(
    db: Session,
    table_configuration_id: int,
    table_configuration_data: TableConfiguration,
) -> TableConfiguration:
    existing_table_configuration = db.get(TableConfiguration, table_configuration_id)
    if not existing_table_configuration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Table Configuration not found",
        )
    # Update the fields of the existing table configuration
    for key, value in table_configuration_data.dict(exclude_unset=True).items():
        setattr(existing_table_configuration, key, value)

    db.add(existing_table_configuration)
    db.commit()
    db.refresh(existing_table_configuration)

    # Fetch the related Column Definition records
    related_columns_data = (
        db.query(ColumnDefinition)
        .options(joinedload(ColumnDefinition.column_constraint))
        .filter(
            ColumnDefinition.table_configuration_id == existing_table_configuration.id
        )
        .all()
    )

    return TableConfigurationRead(
        id=existing_table_configuration.id,
        name=existing_table_configuration.name,
        years_to_collect=existing_table_configuration.years_to_collect,
        created_by=existing_table_configuration.created_by,
        columns=related_columns_data,
    )


# Delete a table configuration
def delete_table_configuration(db: Session, table_configuration_id: int) -> bool:
    db_table_configuration = (
        db.query(TableConfiguration)
        .filter(TableConfiguration.id == table_configuration_id)
        .first()
    )
    if db_table_configuration:
        db.delete(db_table_configuration)
        db.commit()
        return True
    return False


# List all table configurations (optional)
def list_table_configurations(db: Session) -> List[TableConfigurationRead]:
    all_table_configurations = db.query(TableConfiguration).all()

    result = []
    for table_configuration in all_table_configurations:
        related_columns_data = (
            db.query(ColumnDefinition)
            .options(joinedload(ColumnDefinition.column_constraint))
            .filter(ColumnDefinition.table_configuration_id == table_configuration.id)
            .all()
        )

        table_config_read = TableConfigurationRead(
            id=table_configuration.id,
            name=table_configuration.name,
            years_to_collect=table_configuration.years_to_collect,
            created_by=table_configuration.created_by,
            columns=related_columns_data,
        )
        result.append(table_config_read)

    return result
