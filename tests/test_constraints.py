from fastapi import status
from fastapi.testclient import TestClient
from main import app

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

def test_constraint_endpoints():
    # Create a constraint
    constraint_data = {
        "constraint_type": "PICKLIST",
        "parameters": {"options": ["corn", "wheat", "barley", "hops"]},
    }
    created_constraint = create_constraint(client, constraint_data)

    # Read the created constraint by ID
    fetched_constraint = get_constraint_by_id(client, created_constraint["id"])
    assert fetched_constraint["parameters"]["options"] == ["corn", "wheat", "barley", "hops"]

    # Update the constraint
    update_data = {
        "constraint_type": "PICKLIST",
        "parameters": {"options": ["rice", "quinoa", "oats"]},
    }
    updated_constraint = update_constraint(client, created_constraint["id"], update_data)
    assert updated_constraint["parameters"]["options"] == ["rice", "quinoa", "oats"]

    # Delete the constraint and confirm it was deleted
    delete_constraint(client, created_constraint["id"])
    all_constraints = get_all_constraints(client)
    assert all(constraint["id"] != created_constraint["id"] for constraint in all_constraints)
