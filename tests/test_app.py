from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from api.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get("/")  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {"message": "Olá mundo!"}  # Assert


def test_health_deve_retornar_ok(client):
    response = client.get("/health")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"status": "ok"}


def test_create_user(client):
    new_user = {
        "username": "testUsername",
        "email": "test@email.com",
        "password": "testpassword123",
    }

    response = client.post("/user", json=new_user)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "testUsername",
        "email": "test@email.com",
        "id": 1,
    }


def test_list_users(client):
    response = client.get("/users/")
    assert response.json() == {
        "users": [
            {"username": "testUsername", "email": "test@email.com", "id": 1}
        ]
    }


def test_update_user(client):
    response = client.put(
        "/user/1",
        json={
            "username": "anotherTestUsername",
            "email": "test@email.com",
            "password": "testpassword123",
        },
    )

    assert response.status_code == HTTPStatus.OK


def test_delete_user(client):
    response = client.delete("/user/1")

    response.status_code == HTTPStatus.OK
    response.json() == {"message": "User deleted"}
