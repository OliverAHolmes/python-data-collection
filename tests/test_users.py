from fastapi import status
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
base_url = "/users"


def create_user(client) -> dict:
    response = client.post(f"{base_url}", json={"name": "foobar"})
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


def get_all_users(client) -> dict:
    response = client.get(f"{base_url}")
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def delete_user(client, user_id: int):
    response = client.delete(f"{base_url}/{user_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_user_endpoints(db_session):
    # get all entries
    response = get_all_users(client)
    assert len(response) == 0
    # create an entry
    response = create_user(client)
    user_id = response["id"]
    # get entry
    response = get_all_users(client)
    assert len(response) == 1
    assert response[0]["id"] == user_id
    assert response[0]["name"] == "foobar"
    response = delete_user(client, user_id=user_id)
    response = get_all_users(client)
    assert len(response) == 0
