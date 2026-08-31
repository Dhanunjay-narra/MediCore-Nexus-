"""
Tests for Appointment Scheduling & EMR Encounters
"""

def test_list_appointments(client):
    response = client.get("/api/v1/appointments")
    assert response.status_code == 200
    apts = response.json()
    assert len(apts) >= 3


def test_appointment_check_in(client):
    response = client.put("/api/v1/appointments/apt-001/check-in")
    assert response.status_code == 200
    apt = response.json()
    assert apt["status"] == "Checked-In"
    assert apt["checked_in_at"] is not None


def test_emr_encounters(client):
    response = client.get("/api/v1/emr/encounters?patient_id=pat-001")
    assert response.status_code == 200
    encs = response.json()
    assert len(encs) >= 1
    assert encs[0]["vitals"]["blood_pressure_systolic"] == 128
    assert len(encs[0]["diagnoses"]) >= 2
