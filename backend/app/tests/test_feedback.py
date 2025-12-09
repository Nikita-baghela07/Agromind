from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_feedback_submission():
    # Dummy feedback (assuming user_id=1 exists in DB)
    feedback_data = {
        "user_id": 1,
        "message": "This model works great!",
        "prediction_result": "Healthy"
    }

    response = client.post("/feedback/", json=feedback_data)
    assert response.status_code == 200
    assert "feedback_id" in response.json()
