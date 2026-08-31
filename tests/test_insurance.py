"""
Tests for Insurance Claims and Telemedicine
"""

def test_list_insurance_claims(client):
    response = client.get("/api/v1/insurance/claims")
    assert response.status_code == 200
    claims = response.json()
    assert len(claims) >= 1
    assert claims[0]["status"] == "Approved"


def test_telemedicine_session_join(client):
    response = client.put("/api/v1/telemedicine/sessions/tel-001/join")
    assert response.status_code == 200
    res = response.json()
    assert res["status"] == "In-Call"
    assert "webrtc_ice_servers" in res
