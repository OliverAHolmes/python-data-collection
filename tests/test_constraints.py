from fastapi import status
from fastapi.testclient import TestClient
from main import app
from tests.test_utils import create_table_configuration

client = TestClient(app)
base_url = "/constraints/"


def create_constraint(client, data) -> dict:
    response = client.post(base_url, json=data)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


def get_constraint_by_id(client, constraint_id: int) -> dict:
    response = client.get(f"{base_url}{constraint_id}")
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def update_constraint(client, constraint_id: int, data: dict) -> dict:
    response = client.put(f"{base_url}{constraint_id}", json=data)
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def delete_constraint(client, constraint_id: int):
    response = client.delete(f"{base_url}{constraint_id}")
    assert response.status_code == status.HTTP_200_OK


def get_all_constraints(client) -> list:
    response = client.get(base_url)
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def test_constraint_endpoints(db_session):
    response = create_table_configuration(client)
    first_column_constraint_id = response["columns"][0]["column_constraint"]["id"]

    # Read the created constraint by ID
    fetched_constraint = get_constraint_by_id(client, first_column_constraint_id)
    assert fetched_constraint["parameters"]["options"] == [
        "corn",
        "wheat",
        "barley",
        "hops",
    ]

    # Update the constraint
    update_data = {
        "constraint_type": "PICKLIST",
        "parameters": {"options": ["rice", "quinoa", "oats"]},
    }
    updated_constraint = update_constraint(
        client, first_column_constraint_id, update_data
    )
    assert updated_constraint["parameters"]["options"] == ["rice", "quinoa", "oats"]
