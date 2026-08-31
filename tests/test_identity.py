"""
Tests for Identity, Auth, and RBAC
"""

def test_login_success(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"username_or_email": "admin@medicorenexus.io", "password": "Admin@12345"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["role"] == "Super Admin"
    assert data["token_type"] == "bearer"


def test_doctor_login(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"username_or_email": "dr.sarah.chen@medicorenexus.io", "password": "Doctor@12345"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["role"] == "Doctor"
    assert data["user"]["username"] == "dr.sarah"


def test_list_users(client, auth_headers):
    response = client.get("/api/v1/auth/users", headers=auth_headers)
    assert response.status_code == 200
    users = response.json()
    assert len(users) >= 5


def test_system_health(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["modules_active"] == 24
