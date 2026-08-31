"""
MediCore Nexus - Electronic Medical Records (EMR)
Encounters, SOAP Notes, Vital Signs, and ICD-10 Diagnoses
"""

import uuid
from typing import List, Optional, Dict
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, status

class VitalSigns(BaseModel):
    temperature_c: float = 37.0
    heart_rate_bpm: int = 74
    blood_pressure_systolic: int = 120
    blood_pressure_diastolic: int = 80
    respiratory_rate_bpm: int = 16
    oxygen_saturation_pct: float = 98.5
    height_cm: float = 168.0
    weight_kg: float = 68.5
    bmi: float = 24.3
    pain_score_10: int = 0

class DiagnosisItem(BaseModel):
    icd10_code: str
    description: str
    is_primary: bool = False
    status: str = "Active"  # Active, In-Remission, Resolved

class ClinicalEncounterBase(BaseModel):
    patient_id: str
    doctor_id: str
    appointment_id: Optional[str] = None
    encounter_type: str = "Outpatient Consultation"  # Outpatient, Inpatient, Emergency, Telehealth
    chief_complaint: str
    subjective_notes: str
    objective_findings: str
    assessment: str
    clinical_plan: str
    vitals: VitalSigns
    diagnoses: List[DiagnosisItem] = []

class ClinicalEncounterCreate(ClinicalEncounterBase):
    pass

class ClinicalEncounterResponse(ClinicalEncounterBase):
    id: str
    encounter_date: datetime
    is_locked: bool = True

ENCOUNTERS_STORE: Dict[str, Dict] = {
    "enc-001": {
        "id": "enc-001",
        "patient_id": "pat-001",
        "doctor_id": "doc-001",
        "appointment_id": "apt-001",
        "encounter_type": "Outpatient Consultation",
        "chief_complaint": "Follow-up on cardiovascular risk reduction and glycemic control.",
        "subjective_notes": "Patient reports adherence to diet and medications. No episodes of chest tightness, orthopnea, or lower extremity edema. Mild morning fatigue noted.",
        "objective_findings": "Alert and oriented x 3. Regular rate and rhythm, no S3/S4 or murmurs. Lungs clear to auscultation bilaterally. Peripheral pulses 2+ symmetric.",
        "assessment": "1. Essential Hypertension - well controlled.\n2. Type 2 Diabetes Mellitus - optimized.\n3. Primary Hyperlipidemia - mild LDL elevation.",
        "clinical_plan": "1. Increase Atorvastatin to 40mg PO QHS.\n2. Maintain Metformin 500mg ER BID with meals.\n3. Order lipid panel and renal function test in 8 weeks.",
        "vitals": {
            "temperature_c": 36.8,
            "heart_rate_bpm": 72,
            "blood_pressure_systolic": 128,
            "blood_pressure_diastolic": 82,
            "respiratory_rate_bpm": 15,
            "oxygen_saturation_pct": 99.0,
            "height_cm": 165.0,
            "weight_kg": 69.2,
            "bmi": 25.4,
            "pain_score_10": 0,
        },
        "diagnoses": [
            {"icd10_code": "I10", "description": "Essential (primary) hypertension", "is_primary": True, "status": "Active"},
            {"icd10_code": "E11.9", "description": "Type 2 diabetes mellitus without complications", "is_primary": False, "status": "Active"},
            {"icd10_code": "E78.0", "description": "Pure hypercholesterolemia", "is_primary": False, "status": "Active"},
        ],
        "encounter_date": datetime.now(timezone.utc) - timedelta(days=3),
        "is_locked": True,
    }
}

router = APIRouter(prefix="/emr", tags=["Electronic Medical Records"])

@router.get("/encounters", response_model=List[ClinicalEncounterResponse])
async def list_encounters(patient_id: Optional[str] = None, doctor_id: Optional[str] = None):
    res = list(ENCOUNTERS_STORE.values())
    if patient_id:
        res = [e for e in res if e["patient_id"] == patient_id]
    if doctor_id:
        res = [e for e in res if e["doctor_id"] == doctor_id]
    return res

@router.get("/encounters/{encounter_id}", response_model=ClinicalEncounterResponse)
async def get_encounter(encounter_id: str):
    if encounter_id not in ENCOUNTERS_STORE:
        raise HTTPException(status_code=404, detail="Clinical encounter record not found")
    return ENCOUNTERS_STORE[encounter_id]

@router.post("/encounters", response_model=ClinicalEncounterResponse, status_code=status.HTTP_201_CREATED)
async def create_encounter(enc_in: ClinicalEncounterCreate):
    eid = f"enc-{uuid.uuid4().hex[:6]}"
    edict = {
        "id": eid,
        **enc_in.dict(),
        "encounter_date": datetime.now(timezone.utc),
        "is_locked": True,
    }
    ENCOUNTERS_STORE[eid] = edict
    return ClinicalEncounterResponse(**edict)
