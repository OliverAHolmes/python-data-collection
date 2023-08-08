from fastapi import status
from fastapi.testclient import TestClient
from main import app
from tests.test_utils import create_table_configuration

client = TestClient(app)
base_url = "/table-configurations/"


def test_get_all_table_configuration(db_session) -> dict:
    create_table_configuration(client)
    response = client.get(base_url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


def test_get_all_table_configuration_when_none(db_session) -> dict:
    response = client.get(base_url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0


def test_get_table_configuration_by_id(db_session) -> dict:
    # Create a table configuration
    response = create_table_configuration(client)
    table_configuration_id = response["id"]

    # Get entry
    response = client.get(f"{base_url}{table_configuration_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == table_configuration_id
    assert response.json()["name"] == "sample_table"


def test_get_table_configuration_by_id_not_found(db_session) -> dict:
    # Create a table configuration id
    table_configuration_id = 2

    # Get entry where none exists
    response = client.get(f"{base_url}{table_configuration_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Table Configuration not found"}


def test_update_table_configuration(db_session):
    # Create a table configuration
    response = create_table_configuration(client)
    table_configuration_id = response["id"]

    updated_data = {
        "name": "updated_table",
        "years_to_collect": 10,
        "updated_by": 3,
    }
    response = client.put(f"{base_url}{table_configuration_id}", json=updated_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == updated_data["name"]


def test_update_table_configuration_when_none(db_session):
    # Create a table configuration id
    table_configuration_id = 2

    updated_data = {
        "name": "updated_table",
        "years_to_collect": 10,
        "updated_by": 3,
    }
    response = client.put(f"{base_url}{table_configuration_id}", json=updated_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Table Configuration not found"}


def test_delete_table_configuration(db_session):
    response = create_table_configuration(client)
    table_configuration_id = response["id"]
    response = client.delete(f"{base_url}{table_configuration_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_table_configuration_when_none(db_session):
    # Create a table configuration id
    table_configuration_id = 2
    response = client.delete(f"{base_url}{table_configuration_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Table Configuration not found"}


def test_unsupported_column_constraint(db_session):
    # Create an entry with an unsupported column constraint
    response = client.post(
        base_url,
        json={
            "name": "invalid_table",
            "years_to_collect": 5,
            "created_by": 1,
            "columns": [
                {
                    "name": "Invalid Column",
                    "column_order": 1,
                    "column_constraint": {
                        "constraint_type": "UNSUPPORTED_CONSTRAINT",
                        "parameters": {},
                    },
                }
            ],
        },
    )
    # Expecting an Unprocessable Entity response
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "value is not a valid enumeration member" in response.json()

    # Ensure the invalid table was not created
    response = client.get(base_url)
    all_tables = response.json()
    assert not any(table["name"] == "invalid_table" for table in all_tables)
