from fastapi import status
from fastapi.testclient import TestClient
from main import app
import db_internal

db_internal.create_db()

client = TestClient(app)
base_url = "/table-configurations/"


def create_table_configuration(client) -> dict:
    response = client.post(
        base_url,
        json={
            "name": "sample_table",
            "years_to_collect": 5,
            "created_by": 1,
            "columns": [
                {
                    "name": "Sample Column 1",
                    "column_order": 1,
                    "column_constraint": {
                        "constraint_type": "PICKLIST",
                        "parameters": {
                            "options": ["corn", "wheat", "barley", "hops"]
                        }
                    }
                },
                {
                    "name": "Sample Column 2",
                    "column_order": 2,
                    "column_constraint": {
                        "constraint_type": "FLOAT",
                        "parameters": {
                            "number": 3.14
                        }
                    }
                },
                {
                    "name": "Sample Column 3",
                    "column_order": 3,
                    "column_constraint": {
                        "constraint_type": "RANGE",
                        "parameters": {
                            "min": 1.0,
                            "max": 10.0
                        }
                    }
                },
                {
                    "name": "Sample Column 4",
                    "column_order": 4,
                    "column_constraint": {
                        "constraint_type": "REGEX",
                        "parameters": {
                            "pattern": "^[a-zA-Z]+$"
                        }
                    }
                },
                {
                    "name": "Sample Column 5",
                    "column_order": 5,
                    "column_constraint": {
                        "constraint_type": "BOOL"
                    }
                }
            ]
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


def get_table_configuration_by_id(client, table_configuration_id: int) -> dict:
    response = client.get(f"{base_url}{table_configuration_id}")
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def update_table_configuration(client, table_configuration_id: int, data: dict):
    response = client.put(f"{base_url}{table_configuration_id}", json=data)
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def delete_table_configuration(client, table_configuration_id: int):
    response = client.delete(f"{base_url}{table_configuration_id}")
    assert response.status_code == status.HTTP_200_OK


def get_all_table_configurations(client) -> dict:
    response = client.get(base_url)
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def test_table_configuration_endpoints():

    # Expect nothing in fresh db
    response = get_all_table_configurations(client)
    assert len(response) == 0
    # Create an entry
    response = create_table_configuration(client)
    table_config_id = response["id"]

    # Get entry
    response = get_table_configuration_by_id(client, table_config_id)
    assert response["id"] == table_config_id
    assert response["name"] == "sample_table"

    # Update entry
    updated_data = {
        "name": "updated_table",
        "years_to_collect": 10,
        "updated_by": 3,
    }
    response = update_table_configuration(client, table_config_id, updated_data)
    assert response["name"] == "updated_table"

    # List entries and check the updated data
    response = get_all_table_configurations(client)
    assert len(response) == 1
    assert response[0]["name"] == "updated_table"

    # Delete the entry
    delete_table_configuration(client, table_config_id)
    response = get_all_table_configurations(client)
    assert len(response) == 0

def test_unsupported_column_constraint():

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
                        "parameters": {}
                    }
                }
            ]
        },
    )
    # Expecting an Unprocessable Entity response
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'value is not a valid enumeration member' in response.json()

    # Ensure the invalid table was not created
    all_tables = get_all_table_configurations(client)
    assert not any(table['name'] == 'invalid_table' for table in all_tables)
