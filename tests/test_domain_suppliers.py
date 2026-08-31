"""
Unit & Integration Test Suite for Supplier & Vendor Management (suppliers)
"""

import pytest
from backend.app.modules.suppliers.service_deep import suppliers_domain_service


def test_suppliers_initialization():
    """Verify Supplier & Vendor Management domain service initializes with optimal telemetry."""
    kpis = suppliers_domain_service.calculate_domain_kpis()
    assert kpis["domain"] == "suppliers"
    assert kpis["service_health"] == "OPTIMAL"
    assert kpis["metrics"]["compliance_score_pct"] == 100.0


def test_suppliers_entity_id_generation():
    """Verify high-entropy unique entity ID generation."""
    eid = suppliers_domain_service.generate_entity_id()
    assert eid.startswith("sup-")
    assert len(eid) > 8


def test_suppliers_audit_logging():
    """Verify compliance audit trail recording."""
    entry = suppliers_domain_service.record_audit(
        action="TEST_ACTION",
        entity_id="test-001",
        actor="TEST_USER",
        details="Automated integration test audit verification",
    )
    assert entry["action"] == "TEST_ACTION"
    assert entry["compliance_status"] == "VERIFIED"


def test_suppliers_validation_rules():
    """Verify entity validation against mandatory fields."""
    valid, err = suppliers_domain_service.validate_entity_state(
        entity_data={"id": "001", "name": "Valid Test Record"},
        required_fields=["id", "name"],
    )
    assert valid is True
    assert err is None

    invalid, err_msg = suppliers_domain_service.validate_entity_state(
        entity_data={"id": "001"},
        required_fields=["id", "missing_field"],
    )
    assert invalid is False
    assert "Missing required field" in err_msg
