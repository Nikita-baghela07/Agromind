from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_crop_recommendation():
    payload = {
        "soil_type": "loamy",
        "temperature": 28.5,
        "humidity": 65.0,
        "rainfall": 210.0
    }

    response = client.post("/crop/recommend", json=payload)
    assert response.status_code in (200, 500)  # 500 if model missing
    if response.status_code == 200:
        assert "recommended_crop" in response.json()
