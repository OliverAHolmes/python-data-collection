from fastapi import status
from fastapi.testclient import TestClient
from main import app
from tests.test_utils import create_table_configuration
from unittest.mock import patch
from sqlalchemy.exc import SQLAlchemyError


client = TestClient(app)
BASE_URL = "/constraints"


def test_read_constraint_route_not_found(db_session):
    constraint_id = 1
    response = client.get(f"{BASE_URL}/{constraint_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Constraint not found"}


def test_update_constraint_route_success(db_session):
    response = create_table_configuration(client)
    first_column_constraint_id = response["columns"][0]["column_constraint"]["id"]
    response = client.get(f"{BASE_URL}/{first_column_constraint_id}")

    update_data = {
        "constraint_type": "PICKLIST",
        "parameters": {"options": ["rice", "quinoa", "oats"]},
    }

    response = client.put(f"{BASE_URL}/{first_column_constraint_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["parameters"] == update_data["parameters"]


def test_update_constraint_route_not_found(db_session):
    constraint_id = 2
    update_data = {
        "constraint_type": "PICKLIST",
        "parameters": {"options": ["rice", "quinoa", "oats"]},
    }

    response = client.put(f"{BASE_URL}/{constraint_id}", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Constraint not found"}


def test_list_constraints_route_success(db_session):
    response = create_table_configuration(client)
    response = client.get(f"{BASE_URL}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "constraint_type": "PICKLIST",
            "id": 1,
            "parameters": {"options": ["corn", "wheat", "barley", "hops"]},
        },
        {
            "constraint_type": "FLOAT",
            "id": 2,
            "parameters": {"number": 3.14},
        },
        {
            "constraint_type": "RANGE",
            "id": 3,
            "parameters": {"min": 1.0, "max": 10.0},
        },
        {
            "constraint_type": "REGEX",
            "id": 4,
            "parameters": {"pattern": "^[a-zA-Z]+$"},
        },
        {
            "constraint_type": "BOOL",
            "id": 5,
            "parameters": None,
        },
    ]
