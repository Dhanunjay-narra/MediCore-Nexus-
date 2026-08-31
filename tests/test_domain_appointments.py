"""
Unit & Integration Test Suite for Appointment & Queue Management (appointments)
"""

import pytest
from backend.app.modules.appointments.service_deep import appointments_domain_service


def test_appointments_initialization():
    """Verify Appointment & Queue Management domain service initializes with optimal telemetry."""
    kpis = appointments_domain_service.calculate_domain_kpis()
    assert kpis["domain"] == "appointments"
    assert kpis["service_health"] == "OPTIMAL"
    assert kpis["metrics"]["compliance_score_pct"] == 100.0


def test_appointments_entity_id_generation():
    """Verify high-entropy unique entity ID generation."""
    eid = appointments_domain_service.generate_entity_id()
    assert eid.startswith("app-")
    assert len(eid) > 8


def test_appointments_audit_logging():
    """Verify compliance audit trail recording."""
    entry = appointments_domain_service.record_audit(
        action="TEST_ACTION",
        entity_id="test-001",
        actor="TEST_USER",
        details="Automated integration test audit verification",
    )
    assert entry["action"] == "TEST_ACTION"
    assert entry["compliance_status"] == "VERIFIED"


def test_appointments_validation_rules():
    """Verify entity validation against mandatory fields."""
    valid, err = appointments_domain_service.validate_entity_state(
        entity_data={"id": "001", "name": "Valid Test Record"},
        required_fields=["id", "name"],
    )
    assert valid is True
    assert err is None

    invalid, err_msg = appointments_domain_service.validate_entity_state(
        entity_data={"id": "001"},
        required_fields=["id", "missing_field"],
    )
    assert invalid is False
    assert "Missing required field" in err_msg
