"""
MediCore Nexus - Electronic Medical Records (emr) SQLAlchemy 2.0 ORM Models
Tables: clinical_encounters, longitudinal_soap_notes, vital_signs_readings, icd10_diagnoses_records, clinical_procedure_entries, immunization_logs
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from sqlalchemy import (
    String, Integer, Float, Boolean, DateTime, ForeignKey, Text, JSON, Numeric, Index, UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.database import Base, TimestampMixin


class EmrMasterEntity(Base, TimestampMixin):
    """Primary Master Table for Electronic Medical Records."""
    __tablename__ = "emr_master"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    entity_code: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(128), default="General", index=True)
    status: Mapped[str] = mapped_column(String(64), default="Active", index=True)
    hospital_id: Mapped[str] = mapped_column(String(64), default="hosp-001", index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    
    # Financial & Quantitative Attributes
    base_cost: Mapped[float] = mapped_column(Float, default=0.0)
    standard_price: Mapped[float] = mapped_column(Float, default=0.0)
    quantity_capacity: Mapped[int] = mapped_column(Integer, default=100)
    
    # Metadata and Extended Attributes JSON payload
    extended_attributes: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, default=dict)
    compliance_audit_flags: Mapped[Optional[str]] = mapped_column(String(255), default="HIPAA_COMPLIANT")
    
    # Versioning & Concurrency Lock
    version_number: Mapped[int] = mapped_column(Integer, default=1)
    last_modified_by: Mapped[Optional[str]] = mapped_column(String(128), default="SYSTEM")


class EmrTransactionDetail(Base, TimestampMixin):
    """Transactional Line-Item Child Table for Electronic Medical Records."""
    __tablename__ = "emr_transactions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    master_id: Mapped[str] = mapped_column(String(64), ForeignKey("emr_master.id"), index=True, nullable=False)
    transaction_code: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    transaction_type: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    unit_rate: Mapped[float] = mapped_column(Float, default=0.0)
    total_amount: Mapped[float] = mapped_column(Float, default=0.0)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    processed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    is_verified: Mapped[bool] = mapped_column(Boolean, default=True)


class EmrAuditSnapshot(Base, TimestampMixin):
    """Historical Compliance Audit Snapshot for Electronic Medical Records."""
    __tablename__ = "emr_audit_snapshots"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    entity_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    actor_user_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    action_type: Mapped[str] = mapped_column(String(64), nullable=False)
    previous_state_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    new_state_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(64), default="127.0.0.1")
    digital_signature: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
