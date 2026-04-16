def test_submit_feedback(client):
    payload = {
        "transaction_id": "txn_12345",
        "correct_decision": "block",
        "analyst_notes": "Confirmed fraud by analyst"
    }
    
    response = client.post("/api/v1/feedback", json=payload)
    
    assert response.status_code == 200
    assert response.json()["status"] == "received"