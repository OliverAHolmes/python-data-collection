from fastapi import status
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
base_url = "/columns/"

def create_column_definition(client, data) -> dict:
    response = client.post(base_url, json=data)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()

def get_column_definition_by_id(client, column_id: int) -> dict:
    response = client.get(f"{base_url}{column_id}")
    assert response.status_code == status.HTTP_200_OK
    return response.json()

def update_column_definition(client, column_id: int, data: dict) -> dict:
    response = client.put(f"{base_url}{column_id}", json=data)
    assert response.status_code == status.HTTP_200_OK
    return response.json()

def delete_column_definition(client, column_id: int):
    response = client.delete(f"{base_url}{column_id}")
    assert response.status_code == status.HTTP_200_OK

def get_all_column_definitions(client) -> dict:
    response = client.get(base_url)
    assert response.status_code == status.HTTP_200_OK
    return response.json()

def test_column_definition_endpoints():
    # Create a column definition
    column_definition_data = {
        "name": "test_column",
        "column_order": 1,
        "type": "VARCHAR",
        "description": "A test column"
    }
    created_column = create_column_definition(client, column_definition_data)

    # Read the created column definition by ID
    fetched_column = get_column_definition_by_id(client, created_column["id"])
    assert fetched_column["name"] == "test_column"

    # Update the column definition
    update_data = {
        "name": "updated_column",
        "column_order": 1,
        "type": "INT",
        "description": "An updated test column"
    }
    updated_column = update_column_definition(client, created_column["id"], update_data)
    assert updated_column["name"] == "updated_column"
    assert updated_column["type"] == "INT"
    assert updated_column["description"] == "An updated test column"

    # Delete the column definition and confirm it was deleted
    delete_column_definition(client, created_column["id"])
    all_columns = get_all_column_definitions(client)
    assert all(column["id"] != created_column["id"] for column in all_columns)
