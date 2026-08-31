"""
MediCore Nexus - Prescription Management
E-Prescriptions, Items, Dosages, Refills, QR Code Signatures, and Validation
"""

import uuid
from typing import List, Optional, Dict
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, status
from backend.app.events import event_bus, EVENT_PRESCRIPTION_CREATED, EVENT_PRESCRIPTION_VALIDATED

class PrescriptionItemBase(BaseModel):
    medicine_id: str
    medicine_name: str
    dosage: str  # e.g., 40mg
    frequency: str  # Once daily at bedtime (QHS), BID, TID, PRN
    duration_days: int = 30
    quantity: int = 30
    route: str = "Oral"
    instructions: str = "Take with water after dinner."
    refills_allowed: int = 2
    refills_remaining: int = 2

class PrescriptionBase(BaseModel):
    patient_id: str
    patient_name: str
    doctor_id: str
    doctor_name: str
    encounter_id: Optional[str] = None
    diagnosis_summary: str
    clinical_notes: Optional[str] = None
    items: List[PrescriptionItemBase]

class PrescriptionCreate(PrescriptionBase):
    pass

class PrescriptionResponse(PrescriptionBase):
    id: str
    rx_number: str
    digital_signature_hash: str
    qr_code_payload: str
    status: str  # Active, Validated, Dispensed, Refilled, Cancelled, Expired
    created_at: datetime
    validated_at: Optional[datetime] = None
    validated_by_pharmacist: Optional[str] = None

PRESCRIPTIONS_STORE: Dict[str, Dict] = {
    "rx-001": {
        "id": "rx-001",
        "rx_number": "RX-2026-889101",
        "patient_id": "pat-001",
        "patient_name": "Eleanor Vance",
        "doctor_id": "doc-001",
        "doctor_name": "Dr. Sarah Chen, MD",
        "encounter_id": "enc-001",
        "diagnosis_summary": "Essential Hypertension, Type 2 Diabetes Mellitus, Hyperlipidemia",
        "clinical_notes": "Patient advised on regular lipid monitoring and low-sodium diet.",
        "items": [
            {
                "medicine_id": "med-001",
                "medicine_name": "Lipitor (Atorvastatin 40mg)",
                "dosage": "40 mg",
                "frequency": "Once daily at bedtime (QHS)",
                "duration_days": 30,
                "quantity": 30,
                "route": "Oral",
                "instructions": "Take 1 tablet every night before sleep. Do not take with grapefruit juice.",
                "refills_allowed": 3,
                "refills_remaining": 3,
            },
            {
                "medicine_id": "med-002",
                "medicine_name": "Glucophage XR (Metformin 500mg)",
                "dosage": "500 mg",
                "frequency": "Twice daily with meals (BID)",
                "duration_days": 30,
                "quantity": 60,
                "route": "Oral",
                "instructions": "Take with breakfast and dinner. Swallow whole, do not crush.",
                "refills_allowed": 3,
                "refills_remaining": 3,
            }
        ],
        "digital_signature_hash": "SIG-ECDSA-SHA256-CHEN-99210-AUTH-VALID",
        "qr_code_payload": "https://rx.medicorenexus.io/verify/RX-2026-889101?sig=99210",
        "status": "Validated",
        "created_at": datetime.now(timezone.utc) - timedelta(days=2),
        "validated_at": datetime.now(timezone.utc) - timedelta(days=2, hours=-1),
        "validated_by_pharmacist": "Marcus Vance, PharmD",
    },
    "rx-002": {
        "id": "rx-002",
        "rx_number": "RX-2026-889102",
        "patient_id": "pat-002",
        "patient_name": "Michael Chang",
        "doctor_id": "doc-001",
        "doctor_name": "Dr. Sarah Chen, MD",
        "encounter_id": None,
        "diagnosis_summary": "Moderate Persistent Asthma with acute bronchospasm prophylaxis",
        "clinical_notes": "Use spacer device if needed. Keep rescue inhaler accessible at all times.",
        "items": [
            {
                "medicine_id": "med-004",
                "medicine_name": "Ventolin HFA (Albuterol 100mcg)",
                "dosage": "100 mcg",
                "frequency": "1-2 puffs every 4-6 hours as needed for wheezing (PRN)",
                "duration_days": 60,
                "quantity": 1,
                "route": "Inhalation",
                "instructions": "Inhale 2 puffs as needed for shortness of breath or 15 minutes before exercise.",
                "refills_allowed": 2,
                "refills_remaining": 2,
            }
        ],
        "digital_signature_hash": "SIG-ECDSA-SHA256-CHEN-99211-AUTH-VALID",
        "qr_code_payload": "https://rx.medicorenexus.io/verify/RX-2026-889102?sig=99211",
        "status": "Active",
        "created_at": datetime.now(timezone.utc) - timedelta(hours=4),
        "validated_at": None,
        "validated_by_pharmacist": None,
    }
}

router = APIRouter(prefix="/prescriptions", tags=["Prescription Management"])

@router.get("", response_model=List[PrescriptionResponse])
async def list_prescriptions(
    patient_id: Optional[str] = None,
    doctor_id: Optional[str] = None,
    status_filter: Optional[str] = None
):
    res = list(PRESCRIPTIONS_STORE.values())
    if patient_id:
        res = [p for p in res if p["patient_id"] == patient_id]
    if doctor_id:
        res = [p for p in res if p["doctor_id"] == doctor_id]
    if status_filter:
        res = [p for p in res if p["status"].lower() == status_filter.lower()]
    return res

@router.get("/{rx_id}", response_model=PrescriptionResponse)
async def get_prescription(rx_id: str):
    if rx_id not in PRESCRIPTIONS_STORE:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return PRESCRIPTIONS_STORE[rx_id]

@router.post("", response_model=PrescriptionResponse, status_code=status.HTTP_201_CREATED)
async def create_prescription(rx_in: PrescriptionCreate):
    rx_id = f"rx-{uuid.uuid4().hex[:6]}"
    rx_num = f"RX-2026-{uuid.uuid4().hex[:6].upper()}"
    sig = f"SIG-ECDSA-SHA256-{uuid.uuid4().hex[:12].upper()}"
    qr = f"https://rx.medicorenexus.io/verify/{rx_num}"
    
    rx_dict = {
        "id": rx_id,
        "rx_number": rx_num,
        "digital_signature_hash": sig,
        "qr_code_payload": qr,
        **rx_in.dict(),
        "status": "Active",
        "created_at": datetime.now(timezone.utc),
        "validated_at": None,
        "validated_by_pharmacist": None,
    }
    PRESCRIPTIONS_STORE[rx_id] = rx_dict
    await event_bus.publish(EVENT_PRESCRIPTION_CREATED, rx_dict)
    return PrescriptionResponse(**rx_dict)

@router.put("/{rx_id}/validate", response_model=PrescriptionResponse)
async def validate_prescription(rx_id: str, pharmacist_name: str = "Marcus Vance, PharmD"):
    if rx_id not in PRESCRIPTIONS_STORE:
        raise HTTPException(status_code=404, detail="Prescription not found")
    rx = PRESCRIPTIONS_STORE[rx_id]
    rx["status"] = "Validated"
    rx["validated_at"] = datetime.now(timezone.utc)
    rx["validated_by_pharmacist"] = pharmacist_name
    await event_bus.publish(EVENT_PRESCRIPTION_VALIDATED, rx)
    return PrescriptionResponse(**rx)
