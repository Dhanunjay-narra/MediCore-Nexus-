"""
Tests for Laboratory Diagnostics and Results
"""

def test_list_lab_orders(client):
    response = client.get("/api/v1/laboratory/orders")
    assert response.status_code == 200
    orders = response.json()
    assert len(orders) >= 1


def test_verify_lab_results(client):
    response = client.put("/api/v1/laboratory/orders/lab-001/verify")
    assert response.status_code == 200
    order = response.json()
    assert order["status"] == "Verified"
    assert order["technician_name"] == "David Kim, MLS"
    assert len(order["tests"]) >= 3
