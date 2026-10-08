from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def create_user(email: str, password: str):
    response = client.post(
        "/users",
        json={
            "email": email,
            "password": password
        }
    )

    return response


def login_user(email: str, password: str):
    response = client.post(
        "/login",
        data={
            "username": email,
            "password": password
        }
    )

    return response.json()["access_token"]


def test_user_a_cannot_access_user_b_item():

    create_user(
        "user_a@gmail.com",
        "password123"
    )

    create_user(
        "user_b@gmail.com",
        "password123"
    )

    token_a = login_user(
        "user_a@gmail.com",
        "password123"
    )

    token_b = login_user(
        "user_b@gmail.com",
        "password123"
    )

    headers_a = {
        "Authorization": f"Bearer {token_a}"
    }

    headers_b = {
        "Authorization": f"Bearer {token_b}"
    }

    response = client.post(
        "/items",
        headers=headers_a,
        json={
            "title": "Item User A",
            "date": "2026-10-08"
        }
    )

    assert response.status_code == 201

    item_id = response.json()["created_item"]["id"]

    response = client.get(
        f"/items/{item_id}",
        headers=headers_b
    )

    assert response.status_code == 404
    response = client.put(
        f"/items/{item_id}",
        headers=headers_b,
        json={
            "title": "HACKED",
            "date": "2026-10-09"
        }
    )

    assert response.status_code == 404

    response = client.delete(
        f"/items/{item_id}",
        headers=headers_b
    )

    assert response.status_code == 404

    response = client.get(
        f"/items/{item_id}",
        headers=headers_a
    )

    assert response.status_code == 200

def test_user_gets_only_own_items():

    create_user(
        "user_c@gmail.com",
        "password123"
    )

    create_user(
        "user_d@gmail.com",
        "password123"
    )

    token_c = login_user(
        "user_c@gmail.com",
        "password123"
    )

    token_d = login_user(
        "user_d@gmail.com",
        "password123"
    )

    headers_c = {
        "Authorization": f"Bearer {token_c}"
    }

    headers_d = {
        "Authorization": f"Bearer {token_d}"
    }

    client.post(
        "/items",
        headers=headers_c,
        json={
            "title": "C item",
            "date": "2026-10-08"
        }
    )

    client.post(
        "/items",
        headers=headers_d,
        json={
            "title": "D item",
            "date": "2026-10-08"
        }
    )

    response = client.get(
        "/items",
        headers=headers_c
    )

    assert response.status_code == 200
    items = response.json()["items"]
    titles = [item["title"] for item in items]
    assert "C item" in titles
    assert "D item" not in titles