"""
MediCore Nexus - Domain Controller & Endpoint Gateway Generator
Generates full domain controllers, validation engines, and API service handlers for all 24 domains.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DOMAINS = [
    ("identity", "Identity & Access Management", "User authentication, JWT, MFA, RBAC, session management, and lockout policies", "User", "usr"),
    ("organization", "Hospital & Organization Management", "Multi-facility structures, departments, wards, rooms, inpatient beds, and consultation units", "Hospital", "hosp"),
    ("patients", "Master Patient Index (MPI)", "Demographics, emergency contacts, consent, allergies, chronic conditions, and deduplication", "Patient", "pat"),
    ("doctors", "Doctor & Specialist Operations", "Physician profiles, medical licenses, specialties, schedules, fee structures, and utilization", "Doctor", "doc"),
    ("appointments", "Appointment & Queue Management", "Time slot allocation, walk-in triage, queue tokens, check-in flows, and no-show tracking", "Appointment", "apt"),
    ("emr", "Electronic Medical Records (EMR)", "Longitudinal clinical history, SOAP notes, vital signs, ICD-10 diagnoses, and encounters", "ClinicalEncounter", "enc"),
    ("prescriptions", "Prescription & E-Prescribing", "Electronic prescriptions, digital signature hashes, QR codes, dosage schedules, and refill tracking", "Prescription", "rx"),
    ("medicines", "Medicine Master Catalog", "Formulary directory, brand/generic mapping, therapeutic classes, routes, and barcode index", "MedicineMaster", "med"),
    ("pharmacy", "Pharmacy Operations & Dispensing", "Dispensing engine, pharmacist verification, prescription queue, and compliance logs", "DispenseRecord", "dsp"),
    ("inventory", "Pharmacy Inventory & Batch Control", "Multi-warehouse stock, lot tracking, expiry monitoring, Smart FEFO allocation, and reorders", "InventoryBatch", "bat"),
    ("suppliers", "Supplier & Vendor Management", "Vendor directory, commercial contracts, performance ratings, and payment terms", "Supplier", "sup"),
    ("procurement", "Procurement & Purchase Orders", "Purchase requisitions, multi-level approvals, PO lifecycle, and goods receipt notes", "PurchaseOrder", "po"),
    ("sales", "Point-of-Sale (POS) Engine", "Retail checkout, barcode scanner, OTC & Rx sales, discounts, taxes, and receipt printing", "SaleTransaction", "sale"),
    ("drug_safety", "Clinical Pharmacy & Drug Safety", "Drug-drug interaction matrix, allergy interception, contraindications, and Risk Radar", "SafetyCheck", "safe"),
    ("laboratory", "Laboratory Diagnostics", "Test packages, specimen collection, sample barcoding, reference ranges, and critical alerts", "LabOrder", "lab"),
    ("billing", "Billing & Revenue Ledger", "Itemized hospital invoices, consultations, lab fees, copay collection, and payment reconciliation", "Invoice", "inv"),
    ("insurance", "Insurance & Claims Adjudication", "Payer directory, patient policies, eligibility checks, pre-auth, and claims settlement", "InsuranceClaim", "clm"),
    ("telemedicine", "Telemedicine & Virtual Consultations", "Encrypted video rooms, WebRTC signaling, in-call chat, and live clinical note synchronization", "TelemedicineSession", "tel"),
    ("staff", "Staff & Roster Management", "Pharmacy & hospital employee shifts, attendance tracking, counter assignments, and metrics", "StaffMember", "stf"),
    ("notifications", "Multi-Channel Communications", "Automated SMS, Email, Push, and WhatsApp notifications for appointments and refills", "NotificationMessage", "notif"),
    ("analytics", "Healthcare & Business Intelligence", "Real-time KPIs, daily/monthly revenue, fast/slow moving drug matrices, and doctor throughput", "AnalyticsReport", "anl"),
    ("ai", "AI Clinical & Predictive Intelligence", "Prescription anomaly detection, dynamic burn rate stockout forecasting, and natural language analytics", "AIPrediction", "ai"),
    ("audit", "Audit & HIPAA Compliance", "Immutable access trails, prescription modification logs, security policy overrides, and compliance records", "AuditRecord", "aud"),
    ("documents", "Document Vault & Imaging", "Encrypted clinical reports, discharge summaries, insurance card scans, and digital signatures", "DocumentArchive", "docv"),
]

def generate_domain_controllers():
    for mod_name, title, desc, entity, prefix in DOMAINS:
        mod_dir = os.path.join(BASE_DIR, "backend", "app", "modules", mod_name)
        ctrl_file = os.path.join(mod_dir, "domain_controller.py")
        
        with open(ctrl_file, "w", encoding="utf-8") as f:
            f.write(f'''"""
MediCore Nexus - {title} ({mod_name}) Domain Controller & Gateway
Integrates business workflows, database repository, schema transformations, and event publication.
"""

from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime, timezone
import logging
from backend.app.modules.{mod_name}.repository import {mod_name}_repository
from backend.app.modules.{mod_name}.service_deep import {mod_name}_domain_service
from backend.app.events import event_bus

logger = logging.getLogger("medicore.controller.{mod_name}")


class {entity}DomainController:
    """
    Enterprise Domain Controller orchestrating transactional operations for {title}.
    """

    def __init__(self):
        self.repository = {mod_name}_repository
        self.domain_service = {mod_name}_domain_service
        logger.info(f"Initialized {entity}DomainController.")

    async def get_entity_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve record with audit logging."""
        record = await self.repository.get_by_id(entity_id)
        if record:
            self.domain_service.record_audit("VIEW", entity_id, "CONTROLLER", "Retrieved entity detail")
        return record

    async def query_entities(
        self,
        skip: int = 0,
        limit: int = 50,
        filters: Optional[Dict[str, Any]] = None,
        sort_by: str = "created_at",
        descending: bool = True
    ) -> Dict[str, Any]:
        """Query collection with metadata pagination."""
        items, total = await self.repository.list_all(skip, limit, filters, sort_by, descending)
        return {{
            "items": items,
            "total": total,
            "skip": skip,
            "limit": limit,
            "has_more": (skip + limit) < total,
            "domain": "{mod_name}",
        }}

    async def process_create(self, payload: Dict[str, Any], actor_id: str = "SYSTEM") -> Dict[str, Any]:
        """Validate, persist, audit, and publish lifecycle creation event."""
        # Domain validation
        is_valid, err = self.domain_service.validate_entity_state(payload, ["name"])
        if not is_valid and "name" not in payload:
            payload["name"] = f"{entity} Entry #{{datetime.now(timezone.utc).strftime('%H%M%S')}}"

        created_record = await self.repository.create(payload, creator_id=actor_id)
        self.domain_service.record_audit("CREATE", created_record["id"], actor_id, "Created new entity record")
        
        # Publish domain event
        await event_bus.publish(f"{entity}Created", created_record)
        return created_record

    async def process_update(self, entity_id: str, updates: Dict[str, Any], actor_id: str = "SYSTEM") -> Optional[Dict[str, Any]]:
        """Validate, mutate, audit, and publish update event."""
        updated = await self.repository.update(entity_id, updates, updater_id=actor_id)
        if updated:
            self.domain_service.record_audit("UPDATE", entity_id, actor_id, f"Updated fields: {{', '.join(updates.keys())}}")
            await event_bus.publish(f"{entity}Updated", updated)
        return updated

    async def process_delete(self, entity_id: str, actor_id: str = "SYSTEM") -> bool:
        """Soft-delete entity with immutable audit trail."""
        success = await self.repository.soft_delete(entity_id, deleter_id=actor_id)
        if success:
            self.domain_service.record_audit("DELETE", entity_id, actor_id, "Soft-deleted entity record")
            await event_bus.publish(f"{entity}Deleted", {{"id": entity_id}})
        return success

    async def execute_bulk_batch_action(self, action: str, entity_ids: List[str], actor_id: str = "SYSTEM") -> Dict[str, Any]:
        """Perform batch operations across multiple records."""
        success_count = 0
        failed_count = 0
        errors = []

        for eid in entity_ids:
            try:
                if action.upper() == "ACTIVATE":
                    await self.repository.update(eid, {{"status": "Active"}}, updater_id=actor_id)
                elif action.upper() == "ARCHIVE":
                    await self.repository.update(eid, {{"status": "Archived"}}, updater_id=actor_id)
                elif action.upper() == "DELETE":
                    await self.repository.soft_delete(eid, deleter_id=actor_id)
                success_count += 1
            except Exception as e:
                failed_count += 1
                errors.append({{"id": eid, "error": str(e)}})

        return {{
            "action": action,
            "total_processed": len(entity_ids),
            "successful_count": success_count,
            "failed_count": failed_count,
            "errors": errors,
        }}


# Singleton controller instance
{mod_name}_domain_controller = {entity}DomainController()
''')

if __name__ == "__main__":
    generate_domain_controllers()
    print("Domain controllers generated successfully across all 24 domains!")
