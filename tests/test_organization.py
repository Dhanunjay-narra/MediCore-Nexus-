"""
Tests for Organization, Hospital, Department, and Bed Management
"""

def test_list_hospitals(client):
    response = client.get("/api/v1/organizations/hospitals")
    assert response.status_code == 200
    hospitals = response.json()
    assert len(hospitals) >= 2
    assert hospitals[0]["code"] == "MCH-01"


def test_list_departments(client):
    response = client.get("/api/v1/organizations/departments?hospital_id=hosp-001")
    assert response.status_code == 200
    depts = response.json()
    assert any(d["code"] == "PHARM" for d in depts)
    assert any(d["code"] == "CARD" for d in depts)


def test_list_beds(client):
    response = client.get("/api/v1/organizations/beds?hospital_id=hosp-001")
    assert response.status_code == 200
    beds = response.json()
    assert len(beds) >= 3
