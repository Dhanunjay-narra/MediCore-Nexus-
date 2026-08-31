"""
Tests for Drug Safety Engine and Clinical Interaction Matrix
"""

def test_drug_safety_penicillin_allergy_interception(client):
    # Patient pat-001 has Penicillin allergy, testing Amoxil med-003
    response = client.post(
        "/api/v1/drug-safety/check",
        json={"patient_id": "pat-001", "medicine_ids": ["med-003"]},
    )
    assert response.status_code == 200
    res = response.json()
    assert res["overall_risk_level"] == "Critical"
    assert not res["is_safe_to_dispense"]
    assert len(res["allergy_alerts"]) >= 1
    assert "Penicillin" in res["allergy_alerts"][0]["allergen_matched"]


def test_drug_safety_normal_safe_medication(client):
    response = client.post(
        "/api/v1/drug-safety/check",
        json={"patient_id": "pat-001", "medicine_ids": ["med-002"]},  # Metformin
    )
    assert response.status_code == 200
    res = response.json()
    assert res["is_safe_to_dispense"]
    assert res["overall_risk_level"] in ["Normal", "Medium"]
