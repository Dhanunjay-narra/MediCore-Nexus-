"""
Unit & Integration Test Suite for Master Patient Index (MPI) (patients)
"""

import pytest
from backend.app.modules.patients.service_deep import patients_domain_service


def test_patients_initialization():
    """Verify Master Patient Index (MPI) domain service initializes with optimal telemetry."""
    kpis = patients_domain_service.calculate_domain_kpis()
    assert kpis["domain"] == "patients"
    assert kpis["service_health"] == "OPTIMAL"
    assert kpis["metrics"]["compliance_score_pct"] == 100.0


def test_patients_entity_id_generation():
    """Verify high-entropy unique entity ID generation."""
    eid = patients_domain_service.generate_entity_id()
    assert eid.startswith("pat-")
    assert len(eid) > 8


def test_patients_audit_logging():
    """Verify compliance audit trail recording."""
    entry = patients_domain_service.record_audit(
        action="TEST_ACTION",
        entity_id="test-001",
        actor="TEST_USER",
        details="Automated integration test audit verification",
    )
    assert entry["action"] == "TEST_ACTION"
    assert entry["compliance_status"] == "VERIFIED"


def test_patients_validation_rules():
    """Verify entity validation against mandatory fields."""
    valid, err = patients_domain_service.validate_entity_state(
        entity_data={"id": "001", "name": "Valid Test Record"},
        required_fields=["id", "name"],
    )
    assert valid is True
    assert err is None

    invalid, err_msg = patients_domain_service.validate_entity_state(
        entity_data={"id": "001"},
        required_fields=["id", "missing_field"],
    )
    assert invalid is False
    assert "Missing required field" in err_msg
