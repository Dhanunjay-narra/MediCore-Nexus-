"""
Tests for Billing & Revenue Management
"""

def test_list_invoices(client):
    response = client.get("/api/v1/billing/invoices")
    assert response.status_code == 200
    invoices = response.json()
    assert len(invoices) >= 1
    assert invoices[0]["payment_status"] == "Paid"


def test_create_invoice(client):
    inv_payload = {
        "patient_id": "pat-002",
        "patient_name": "Michael Chang",
        "hospital_id": "hosp-001",
        "insurance_coverage_amount": 100.0,
        "patient_copay_amount": 25.0,
        "items": [
            {
                "service_type": "Consultation",
                "description": "Pulmonology Follow-up",
                "quantity": 1,
                "unit_price": 125.0,
                "discount": 0.0,
                "tax": 0.0,
                "net_total": 125.0,
            }
        ],
    }
    response = client.post("/api/v1/billing/invoices", json=inv_payload)
    assert response.status_code == 201
    res = response.json()
    assert res["gross_total"] == 125.0
    assert res["balance_due"] == 25.0
