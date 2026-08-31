"""
Tests for AI Intelligence, Audit Trails, Documents, and Security Headers
"""

def test_ai_nlp_query_expiry(client):
    response = client.post(
        "/api/v1/ai/query",
        json={"query": "Which medicines expire within 30 days?"},
    )
    assert response.status_code == 200
    res = response.json()
    assert res["intent"] == "EXPIRING_INVENTORY_LOOKUP"
    assert res["confidence_score"] >= 0.85


def test_ai_predictive_inventory(client):
    response = client.get("/api/v1/ai/predictive-inventory")
    assert response.status_code == 200
    items = response.json()
    assert len(items) >= 3
    assert any(i["estimated_days_until_stockout"] <= 10 for i in items)


def test_audit_logs(client):
    response = client.get("/api/v1/audit/logs")
    assert response.status_code == 200
    logs = response.json()
    assert len(logs) >= 3
    assert all(l["compliance_tag"] in ["HIPAA_AUDITABLE", "SOC2_AUDITABLE"] for l in logs)


def test_documents_vault(client):
    response = client.get("/api/v1/documents?patient_id=pat-001")
    assert response.status_code == 200
    docs = response.json()
    assert len(docs) >= 1
    assert docs[0]["is_encrypted"]


def test_security_headers(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"
    assert response.headers.get("X-XSS-Protection") == "1; mode=block"
