"""
Tests for Patient Registry, MPI, and Longitudinal Timeline
"""

def test_list_patients(client):
    response = client.get("/api/v1/patients")
    assert response.status_code == 200
    patients = response.json()
    assert len(patients) >= 3
    assert any(p["first_name"] == "Eleanor" for p in patients)


def test_patient_search_by_mrn(client):
    response = client.get("/api/v1/patients?query=MRN-2026-004128")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["last_name"] == "Vance"


def test_patient_timeline(client):
    response = client.get("/api/v1/patients/pat-001/timeline")
    assert response.status_code == 200
    timeline = response.json()
    assert timeline["patient_id"] == "pat-001"
    assert len(timeline["events"]) >= 3
