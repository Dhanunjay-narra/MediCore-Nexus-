"""
Tests for Doctor Profiles and Schedules
"""

def test_list_doctors(client):
    response = client.get("/api/v1/doctors")
    assert response.status_code == 200
    docs = response.json()
    assert len(docs) >= 3
    assert any(d["specialization"] == "Interventional Cardiology" for d in docs)


def test_doctor_specialization_filter(client):
    response = client.get("/api/v1/doctors?specialization=neurology")
    assert response.status_code == 200
    docs = response.json()
    assert len(docs) == 1
    assert "Taylor" in docs[0]["full_name"]
