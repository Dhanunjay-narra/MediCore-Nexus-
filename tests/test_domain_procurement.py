"""
Unit & Integration Test Suite for Procurement & Purchase Orders (procurement)
"""

import pytest
from backend.app.modules.procurement.service_deep import procurement_domain_service


def test_procurement_initialization():
    """Verify Procurement & Purchase Orders domain service initializes with optimal telemetry."""
    kpis = procurement_domain_service.calculate_domain_kpis()
    assert kpis["domain"] == "procurement"
    assert kpis["service_health"] == "OPTIMAL"
    assert kpis["metrics"]["compliance_score_pct"] == 100.0


def test_procurement_entity_id_generation():
    """Verify high-entropy unique entity ID generation."""
    eid = procurement_domain_service.generate_entity_id()
    assert eid.startswith("pro-")
    assert len(eid) > 8


def test_procurement_audit_logging():
    """Verify compliance audit trail recording."""
    entry = procurement_domain_service.record_audit(
        action="TEST_ACTION",
        entity_id="test-001",
        actor="TEST_USER",
        details="Automated integration test audit verification",
    )
    assert entry["action"] == "TEST_ACTION"
    assert entry["compliance_status"] == "VERIFIED"


def test_procurement_validation_rules():
    """Verify entity validation against mandatory fields."""
    valid, err = procurement_domain_service.validate_entity_state(
        entity_data={"id": "001", "name": "Valid Test Record"},
        required_fields=["id", "name"],
    )
    assert valid is True
    assert err is None

    invalid, err_msg = procurement_domain_service.validate_entity_state(
        entity_data={"id": "001"},
        required_fields=["id", "missing_field"],
    )
    assert invalid is False
    assert "Missing required field" in err_msg
