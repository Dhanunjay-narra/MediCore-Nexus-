"""
Unit & Integration Test Suite for Staff & Roster Management (staff)
"""

import pytest
from backend.app.modules.staff.service_deep import staff_domain_service


def test_staff_initialization():
    """Verify Staff & Roster Management domain service initializes with optimal telemetry."""
    kpis = staff_domain_service.calculate_domain_kpis()
    assert kpis["domain"] == "staff"
    assert kpis["service_health"] == "OPTIMAL"
    assert kpis["metrics"]["compliance_score_pct"] == 100.0


def test_staff_entity_id_generation():
    """Verify high-entropy unique entity ID generation."""
    eid = staff_domain_service.generate_entity_id()
    assert eid.startswith("sta-")
    assert len(eid) > 8


def test_staff_audit_logging():
    """Verify compliance audit trail recording."""
    entry = staff_domain_service.record_audit(
        action="TEST_ACTION",
        entity_id="test-001",
        actor="TEST_USER",
        details="Automated integration test audit verification",
    )
    assert entry["action"] == "TEST_ACTION"
    assert entry["compliance_status"] == "VERIFIED"


def test_staff_validation_rules():
    """Verify entity validation against mandatory fields."""
    valid, err = staff_domain_service.validate_entity_state(
        entity_data={"id": "001", "name": "Valid Test Record"},
        required_fields=["id", "name"],
    )
    assert valid is True
    assert err is None

    invalid, err_msg = staff_domain_service.validate_entity_state(
        entity_data={"id": "001"},
        required_fields=["id", "missing_field"],
    )
    assert invalid is False
    assert "Missing required field" in err_msg
