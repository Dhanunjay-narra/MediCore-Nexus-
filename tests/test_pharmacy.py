"""
Tests for Prescriptions, Pharmacy Command Center, and Sales POS
"""

def test_list_prescriptions(client):
    response = client.get("/api/v1/prescriptions")
    assert response.status_code == 200
    rxs = response.json()
    assert len(rxs) >= 2


def test_validate_prescription(client):
    response = client.put("/api/v1/prescriptions/rx-002/validate")
    assert response.status_code == 200
    rx = response.json()
    assert rx["status"] == "Validated"
    assert rx["validated_by_pharmacist"] is not None


def test_pharmacy_command_center(client):
    response = client.get("/api/v1/pharmacy/command-center")
    assert response.status_code == 200
    data = response.json()
    assert data["today_gross_sales"] > 0
    assert data["fefo_compliance_rate_pct"] >= 90
    assert len(data["recent_alerts"]) >= 3


def test_pos_checkout(client):
    checkout_payload = {
        "customer_name": "Test Walk-in Patient",
        "payment_method": "Credit Card",
        "subtotal": 18.00,
        "tax_amount": 0.90,
        "total_paid": 18.90,
        "items": [
            {
                "medicine_id": "med-001",
                "medicine_name": "Lipitor 40mg",
                "batch_id": "bat-001",
                "batch_number": "ATV-2026-B1",
                "quantity": 1,
                "unit_price": 18.00,
                "total_line_amount": 18.90,
            }
        ]
    }
    response = client.post("/api/v1/sales/checkout", json=checkout_payload)
    assert response.status_code == 201
    res = response.json()
    assert res["status"] == "Paid"
    assert "INV-POS" in res["invoice_number"]
