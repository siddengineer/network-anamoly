import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["models"]["random_forest"] == "ready"
    assert data["groq_assistant"]["configured"] is True

def test_dashboard_summary():
    response = client.get("/api/dashboard/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_analyzed"] >= 1000
    assert data["anomaly_percentage"] > 0
    assert "BENIGN" in data["class_distribution"]

def test_dashboard_trends():
    response = client.get("/api/dashboard/trends")
    assert response.status_code == 200
    data = response.json()
    assert len(data["port_distribution"]) > 0
    assert len(data["duration_distribution"]) > 0

def test_model_performance():
    response = client.get("/api/models/performance")
    assert response.status_code == 200
    data = response.json()
    assert "random_forest" in data
    assert "isolation_forest" in data
    assert data["random_forest"]["test_accuracy"] >= 0.80

def test_alerts_listing_and_patch():
    response = client.get("/api/alerts?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] > 0
    first_alert = data["alerts"][0]
    alert_id = first_alert["id"]
    
    # Test patch alert status
    patch_resp = client.patch(f"/api/alerts/{alert_id}", json={
        "investigation_status": "Investigating",
        "notes": "Analyst inspecting flow volume."
    })
    assert patch_resp.status_code == 200
    assert patch_resp.json()["investigation_status"] == "Investigating"

def test_detection_results_pagination():
    response = client.get("/api/detection/results?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1000
    assert len(data["records"]) == 10
    rec = data["records"][0]
    assert "destination_port" in rec
    assert "predicted_label" in rec

def test_chat_assistant():
    response = client.post("/api/chat", json={
        "message": "Summarize the detection run. How many normal and anomalous packets?"
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data["response"]) > 0
    assert data["grounded_stats"] is not None
    assert data["grounded_stats"]["total_records"] >= 1000
