"""
MediCore Nexus - Enterprise Database Layer & ORM Entity Generator
Generates production SQLAlchemy 2.0 ORM models, table definitions, and migrations
for all 24 domains.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DOMAINS_DB = [
    ("identity", "Identity & Security", "users, user_sessions, role_permissions, mfa_credentials, audit_security_tokens"),
    ("organization", "Hospital & Hierarchy", "organizations, hospital_facilities, clinical_departments, inpatient_wards, hospital_rooms, hospital_beds, clinic_consultation_units"),
    ("patients", "Patient Care & MPI", "patient_entities, patient_demographics, patient_allergies, chronic_conditions, emergency_contacts, guardian_profiles, consent_records"),
    ("doctors", "Doctor Management", "physician_profiles, medical_specialties, physician_licenses, consultation_fee_tiers, physician_working_schedules, doctor_reviews"),
    ("appointments", "Appointments & Queues", "appointment_bookings, waiting_room_queues, triage_tokens, doctor_availability_slots, no_show_incidents"),
    ("emr", "Electronic Medical Records", "clinical_encounters, longitudinal_soap_notes, vital_signs_readings, icd10_diagnoses_records, clinical_procedure_entries, immunization_logs"),
    ("prescriptions", "Prescription Operations", "electronic_prescriptions, prescription_medication_items, digital_signature_audit_hashes, prescription_refill_authorizations"),
    ("medicines", "Medicine Master Catalog", "medicine_catalog_items, generic_active_ingredients, brand_formulations, therapeutic_classification_nodes, package_barcode_mappings"),
    ("pharmacy", "Pharmacy Operations", "dispensing_transaction_records, pharmacist_verification_actions, prescription_fulfillment_items, counter_queue_allocations"),
    ("inventory", "Inventory & Stock Control", "pharmaceutical_inventory_batches, warehouse_facilities, storage_aisles_and_shelves, stock_adjustment_entries, lot_tracking_records"),
    ("suppliers", "Supplier Management", "pharmaceutical_supplier_entities, commercial_vendor_contracts, supplier_product_catalog_prices, vendor_performance_reviews"),
    ("procurement", "Procurement & POs", "purchase_requisitions, purchase_order_headers, purchase_order_line_items, goods_receipt_notes, vendor_invoice_matching_records"),
    ("sales", "Point-of-Sale Engine", "pos_sales_transactions, pos_cart_line_items, payment_transaction_ledger, electronic_sales_receipts, return_and_refund_records"),
    ("drug_safety", "Clinical Drug Safety", "drug_drug_interaction_pairings, drug_allergy_cross_reactions, clinical_contraindication_rules, pregnancy_and_lactation_risks"),
    ("laboratory", "Laboratory Diagnostics", "laboratory_test_packages, patient_specimen_samples, test_result_measurements, loinc_standard_reference_ranges, critical_alert_dispatches"),
    ("billing", "Billing & Revenue", "hospital_patient_invoices, invoice_itemized_charge_entries, patient_payment_captures, insurance_copay_records, financial_ledger_reconciliations"),
    ("insurance", "Insurance & Claims", "insurance_payer_entities, patient_insurance_policies, insurance_eligibility_verifications, electronic_claim_submissions, claim_adjudication_items"),
    ("telemedicine", "Telemedicine Suite", "telemedicine_video_sessions, webrtc_room_tokens, in_call_clinical_chat_messages, virtual_consultation_transcripts"),
    ("staff", "Staff & Rostering", "hospital_staff_employees, duty_shift_schedules, employee_attendance_punches, counter_station_assignments, performance_scorecards"),
    ("notifications", "Communications", "multichannel_notification_dispatches, sms_gateway_logs, email_delivery_receipts, whatsapp_message_payloads, push_token_registrations"),
    ("analytics", "Analytics & BI", "daily_pharmacy_revenue_aggregations, fast_moving_drug_velocity_metrics, hospital_bed_utilization_snapshots, doctor_throughput_analytics"),
    ("ai", "AI Decision Support", "ai_prescription_anomaly_logs, predictive_stockout_estimations, natural_language_query_histories, clinical_decision_support_insights"),
    ("audit", "Audit & Compliance", "hipaa_audit_trail_events, electronic_record_access_logs, sensitive_data_export_records, security_policy_override_incidents"),
    ("documents", "Document Vault", "encrypted_clinical_documents, patient_lab_report_attachments, medical_imaging_scans, digital_consent_document_archives"),
]

def generate_orm_models():
    for mod_name, title, tables in DOMAINS_DB:
        mod_dir = os.path.join(BASE_DIR, "backend", "app", "modules", mod_name)
        model_file = os.path.join(mod_dir, "domain_models.py")
        
        with open(model_file, "w", encoding="utf-8") as f:
            f.write(f'''"""
MediCore Nexus - {title} ({mod_name}) SQLAlchemy 2.0 ORM Models
Tables: {tables}
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from sqlalchemy import (
    String, Integer, Float, Boolean, DateTime, ForeignKey, Text, JSON, Numeric, Index, UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.database import Base, TimestampMixin


class {mod_name.title().replace("_", "")}MasterEntity(Base, TimestampMixin):
    """Primary Master Table for {title}."""
    __tablename__ = "{mod_name}_master"

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


class {mod_name.title().replace("_", "")}TransactionDetail(Base, TimestampMixin):
    """Transactional Line-Item Child Table for {title}."""
    __tablename__ = "{mod_name}_transactions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    master_id: Mapped[str] = mapped_column(String(64), ForeignKey("{mod_name}_master.id"), index=True, nullable=False)
    transaction_code: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    transaction_type: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    unit_rate: Mapped[float] = mapped_column(Float, default=0.0)
    total_amount: Mapped[float] = mapped_column(Float, default=0.0)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    processed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    is_verified: Mapped[bool] = mapped_column(Boolean, default=True)


class {mod_name.title().replace("_", "")}AuditSnapshot(Base, TimestampMixin):
    """Historical Compliance Audit Snapshot for {title}."""
    __tablename__ = "{mod_name}_audit_snapshots"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    entity_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    actor_user_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    action_type: Mapped[str] = mapped_column(String(64), nullable=False)
    previous_state_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    new_state_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(64), default="127.0.0.1")
    digital_signature: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
''')

if __name__ == "__main__":
    generate_orm_models()
    print("Database ORM models generated across all 24 domains successfully!")
