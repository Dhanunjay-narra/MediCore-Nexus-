"""
MediCore Nexus - Audit, Compliance & Security Logs
Immutable access logs, prescription change histories, and HIPAA compliance records
"""

from typing import List, Optional, Dict
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel
from fastapi import APIRouter

class AuditLogItem(BaseModel):
    id: str
    event_time: datetime
    actor_user_id: str
    actor_name: str
    actor_role: str
    action_type: str  # READ, CREATE, UPDATE, DELETE, DISPENSE, LOGIN, OVERRIDE
    resource_type: str  # PATIENT_RECORD, PRESCRIPTION, INVENTORY, BILLING, SECURITY
    resource_id: str
    ip_address: str
    details: str
    compliance_tag: str = "HIPAA_AUDITABLE"

AUDIT_LOGS: List[Dict] = [
    {
        "id": "aud-001",
        "event_time": datetime.now(timezone.utc) - timedelta(minutes=12),
        "actor_user_id": "usr-pharm-01",
        "actor_name": "Marcus Vance, PharmD",
        "actor_role": "Pharmacist",
        "action_type": "DISPENSE",
        "resource_type": "PRESCRIPTION",
        "resource_id": "rx-001",
        "ip_address": "192.168.1.104",
        "details": "Validated and dispensed 30 tabs Atorvastatin 40mg under Smart FEFO protocol.",
        "compliance_tag": "HIPAA_AUDITABLE",
    },
    {
        "id": "aud-002",
        "event_time": datetime.now(timezone.utc) - timedelta(minutes=45),
        "actor_user_id": "usr-doc-01",
        "actor_name": "Dr. Sarah Chen, MD",
        "actor_role": "Doctor",
        "action_type": "CREATE",
        "resource_type": "PRESCRIPTION",
        "resource_id": "rx-001",
        "ip_address": "192.168.1.52",
        "details": "Signed electronic prescription with ECDSA hash SIG-ECDSA-SHA256-CHEN-99210.",
        "compliance_tag": "HIPAA_AUDITABLE",
    },
    {
        "id": "aud-003",
        "event_time": datetime.now(timezone.utc) - timedelta(hours=2),
        "actor_user_id": "usr-admin-01",
        "actor_name": "Dr. Alexander Wright, MD",
        "actor_role": "Super Admin",
        "action_type": "UPDATE",
        "resource_type": "SECURITY",
        "resource_id": "sec-pol-01",
        "ip_address": "10.0.4.1",
        "details": "Enforced mandatory MFA policy across all pharmacy and hospital administrator accounts.",
        "compliance_tag": "SOC2_AUDITABLE",
    }
]

router = APIRouter(prefix="/audit", tags=["Audit, Compliance & Security"])

@router.get("/logs", response_model=List[AuditLogItem])
async def list_audit_logs():
    return AUDIT_LOGS
