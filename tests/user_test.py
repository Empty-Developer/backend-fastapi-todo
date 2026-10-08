from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/users",
        json={
            "email": "test_user_1@gmail.com",
            "password": "testpassword123"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "test_user_1@gmail.com"
    assert "password" not in data
    assert "id" in data

def test_login_user():
    response = client.post(
        "/login",
        data={
            "username": "test_user_1@gmail.com",
            "password": "testpassword123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"