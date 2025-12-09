from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_user_registration_and_login():
    # Use random email to avoid collisions
    email = f"user_{uuid.uuid4().hex[:6]}@test.com"
    register_data = {
        "username": "TestUser",
        "email": email,
        "password": "password123"
    }

    reg_response = client.post("/users/register", json=register_data)
    assert reg_response.status_code == 200
    assert "user_id" in reg_response.json()

    login_response = client.post("/users/login", json={
        "email": email,
        "password": "password123"
    })
    assert login_response.status_code == 200
    data = login_response.json()
    assert "access_token" in data
    assert data["message"] == "Login successful"
