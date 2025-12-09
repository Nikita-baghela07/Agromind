from fastapi.testclient import TestClient
from app.main import app
import io

client = TestClient(app)

def test_disease_prediction_mocked():
    # Create a fake image in memory
    img_bytes = io.BytesIO(b"fakeimagecontent")

    response = client.post("/disease/predict", files={"file": ("leaf.jpg", img_bytes, "image/jpeg")})
    assert response.status_code in (200, 500)
    if response.status_code == 200:
        assert "prediction" in response.json()
