from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_predict():
    sample = {
        "features": {
            "Date": "2023-01-01",
            "Event_Type": "Festival",
            "Location": "Montreal",
            "Season": "Winter",
            "Weather_Forecast": "Snow",
            "Indoor_Outdoor": "Outdoor",
            "Competition_Level": "Medium",
            "Day_of_week": "Monday",
            "Participants": 150,
            "Distance_km": 4.5,
        }
    }

    response = client.post("/predict", json=sample)
    assert response.status_code == 200
    assert "prediction" in response.json()
