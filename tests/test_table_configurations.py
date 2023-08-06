from fastapi import status
from fastapi.testclient import TestClient

from main import app

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
