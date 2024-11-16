from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/users/",
        json={"name": "Test User", "email": "test@example.com", "password": "1234"}
    )

    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"