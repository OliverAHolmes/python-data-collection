from fastapi import status
from fastapi.testclient import TestClient
from main import app
from tests.test_utils import create_table_configuration

client = TestClient(app)
BASE_URL = "/columns/"


def test_create_column_definition_route_success(db_session):
    response = create_table_configuration(client)
    table_configuration_id = response["id"]

    column_data = {
        "name": "Sample Column 1",
        "column_order": 1,
        "column_constraint": {
            "constraint_type": "PICKLIST",
            "parameters": {"options": ["corn", "wheat", "barley", "hops"]},
        },
    }

    response = client.post(f"{BASE_URL}{table_configuration_id}", json=column_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == column_data["name"]
    assert response.json()["column_order"] == column_data["column_order"]
    assert (
        response.json()["column_constraint"]["parameters"]["options"]
        == column_data["column_constraint"]["parameters"]["options"]
    )


def test_get_column_definition_route_success(db_session):
    response = create_table_configuration(client)
    column_definition_id = response["columns"][0]["id"]

    response = client.get(f"{BASE_URL}{column_definition_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Sample Column 1"


def test_get_column_definition_route_not_found(db_session):
    column_definition_id = 1
    response = client.get(f"{BASE_URL}{column_definition_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Column Definition not found"}


def test_update_column_definition_route_success(db_session):
    response = create_table_configuration(client)
    column_definition_id = response["columns"][0]["id"]

    update_data = {
        "name": "Sample Column 2",
        "column_order": 2,
    }

    response = client.put(f"{BASE_URL}{column_definition_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == update_data["name"]
    assert response.json()["column_order"] == update_data["column_order"]

def test_update_column_definition_route_not_found(db_session):
    column_definition_id = 1

    update_data = {
        "name": "Sample Column 2",
        "column_order": 2,
    }

    response = client.put(f"{BASE_URL}{column_definition_id}", json=update_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Column Definition not found"}

def test_list_column_definitions_route_success(db_session):
    create_table_configuration(client)
    response = client.get(BASE_URL)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5


def test_delete_column_definition_route_success(db_session):
    response = create_table_configuration(client)
    column_definition_id = response["columns"][0]["id"]

    response = client.delete(f"{BASE_URL}{column_definition_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify deletion by trying to get the deleted column
    response = client.get(f"{BASE_URL}{column_definition_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_column_definition_route_not_found(db_session):
    column_definition_id = 1

    response = client.delete(f"{BASE_URL}{column_definition_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_column_definition_route_with_invalid_id_type(db_session):
    # Using a string as the table_configuration_id instead of an integer
    column_definition_id = "invalid_id"
    response = client.delete(f"{BASE_URL}{column_definition_id}")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "value is not a valid integer" in response.json()["detail"][0]["msg"]