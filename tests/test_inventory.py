"""
Tests for Pharmacy Inventory and Smart FEFO Sorting
"""

def test_list_inventory(client):
    response = client.get("/api/v1/inventory")
    assert response.status_code == 200
    batches = response.json()
    assert len(batches) >= 6


def test_smart_fefo_recommendation(client):
    # For Lipitor med-001, bat-001 expires in 2026-11-30 while bat-002 expires in 2027-04-30
    response = client.get("/api/v1/inventory/fefo-recommendation/med-001")
    assert response.status_code == 200
    batches = response.json()
    assert len(batches) >= 2
    # Ensure sorted by earliest expiry
    assert batches[0]["expiry_date"] < batches[1]["expiry_date"]
    assert batches[0]["batch_number"] == "ATV-2026-B1"


def test_low_stock_filter(client):
    response = client.get("/api/v1/inventory?low_stock_only=true")
    assert response.status_code == 200
    batches = response.json()
    assert len(batches) >= 1
    assert any(b["medicine_name"].startswith("Glucophage") for b in batches)
