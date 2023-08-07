from fastapi import status
from fastapi.testclient import TestClient
from main import app
from tests.test_utils import create_table_configuration

client = TestClient(app)
base_url = "/columns/"


def create_column_definition_endpoint(client, table_configuration_id, data) -> dict:
    response = client.post(f"{base_url}{table_configuration_id}", json=data)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


def get_column_definition_endpoint(client, column_definition_id: int) -> dict:
    response = client.get(f"{base_url}{column_definition_id}")
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def update_column_definition_endpoint(
    client, column_definition_id: int, data: dict
) -> dict:
    response = client.put(f"{base_url}{column_definition_id}", json=data)
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def delete_column_definition_endpoint(client, column_definition_id: int):
    response = client.delete(f"{base_url}{column_definition_id}")
    assert response.status_code == status.HTTP_200_OK


def list_column_definitions_endpoint(client) -> list:
    response = client.get(base_url)
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def test_column_definition_endpoints(db_session):
    response = create_table_configuration(client)
    table_configuration_id = response["id"]

    # Create a column definition
    column_data = {
        "name": "Sample Column 1",
        "column_order": 1,
        "column_constraint": {
            "constraint_type": "PICKLIST",
            "parameters": {"options": ["corn", "wheat", "barley", "hops"]},
        },
    }
    response = create_column_definition_endpoint(
        client, table_configuration_id, column_data
    )
    column_definition_id = response["id"]

    # Fetch and verify
    fetched_column = get_column_definition_endpoint(client, column_definition_id)
    assert fetched_column["name"] == column_data["name"]
    assert fetched_column["column_order"] == column_data["column_order"]
    assert (
        fetched_column["column_constraint"]["parameters"]["options"]
        == column_data["column_constraint"]["parameters"]["options"]
    )

    # Update the column definition
    update_data = {
        "name": "Sample Column 2",
        "column_order": 2,
    }
    updated_column = update_column_definition_endpoint(
        client, column_definition_id, update_data
    )
    assert updated_column["name"] == update_data["name"]
    assert updated_column["column_order"] == update_data["column_order"]

    # List all column definitions and check
    all_columns = list_column_definitions_endpoint(client)
    assert len(all_columns) >= 1

    # Delete and verify deletion
    delete_column_definition_endpoint(client, column_definition_id)
    all_columns_after_deletion = list_column_definitions_endpoint(client)
    assert not any(
        column["id"] == column_definition_id for column in all_columns_after_deletion
    )
