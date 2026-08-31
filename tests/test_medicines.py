"""
Tests for Medicine Catalog Master and Barcodes
"""

def test_list_medicines(client):
    response = client.get("/api/v1/medicines")
    assert response.status_code == 200
    meds = response.json()
    assert len(meds) >= 6


def test_medicine_search_by_barcode(client):
    response = client.get("/api/v1/medicines?query=8901088231901")
    assert response.status_code == 200
    meds = response.json()
    assert len(meds) == 1
    assert meds[0]["brand_name"] == "Lipitor"
    assert meds[0]["strength"] == "40 mg"
