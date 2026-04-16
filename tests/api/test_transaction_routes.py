def test_evaluate_transaction(client):
    payload = {
        "transaction_id": "txn_12345",
        "user_id": "user_001",
        "amount": 7500.0,
        "merchant": "Amazon",
        "device": {
            "device_id": "dev_001",
            "ip_address": "192.168.1.1"
        },
        "metadata": {"rapid": True}
    }
    
    response = client.post("/api/v1/transaction/evaluate", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["transaction_id"] == "txn_12345"
    assert "risk_score" in data
    assert data["decision"] in ["approve", "flag", "block", "escalate"]
    assert len(data["agent_votes"]) > 0


def test_health_check(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"