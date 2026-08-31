"""
MediCore Nexus - Patient Management (Master Patient Index & Demographics)
"""

import uuid
from typing import List, Optional, Dict
from datetime import date, datetime, timezone, timedelta
from pydantic import BaseModel, EmailStr, Field
from fastapi import APIRouter, HTTPException, Query, status

class PatientBase(BaseModel):
    first_name: str
    last_name: str
    dob: str
    gender: str  # Male, Female, Other
    blood_group: str  # A+, A-, B+, B-, O+, O-, AB+, AB-
    email: Optional[str] = None
    phone: str
    address: str
    city: str
    state: str
    zip_code: str
    emergency_contact_name: str
    emergency_contact_phone: str
    emergency_contact_relationship: str
    allergies: List[str] = []
    chronic_conditions: List[str] = []
    medical_alerts: List[str] = []
    primary_physician_id: Optional[str] = None
    insurance_policy_number: Optional[str] = None
    insurance_provider: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: str
    mrn: str  # Medical Record Number (Unique Identifier)
    created_at: datetime
    is_active: bool

PATIENTS_STORE: Dict[str, Dict] = {
    "pat-001": {
        "id": "pat-001",
        "mrn": "MRN-2026-004128",
        "first_name": "Eleanor",
        "last_name": "Vance",
        "dob": "1968-04-12",
        "gender": "Female",
        "blood_group": "A+",
        "email": "eleanor.vance@example.com",
        "phone": "+1 (555) 234-5678",
        "address": "45 Beacon Hill Rd",
        "city": "Boston",
        "state": "MA",
        "zip_code": "02108",
        "emergency_contact_name": "Thomas Vance",
        "emergency_contact_phone": "+1 (555) 234-9988",
        "emergency_contact_relationship": "Spouse",
        "allergies": ["Penicillin", "Sulfa Drugs"],
        "chronic_conditions": ["Type 2 Diabetes Mellitus", "Hypertension", "Hyperlipidemia"],
        "medical_alerts": ["Fall Risk Alert", "Diabetic Foot Care Protocol"],
        "primary_physician_id": "usr-doc-01",
        "insurance_policy_number": "POL-BCBS-889104",
        "insurance_provider": "Blue Cross Blue Shield",
        "created_at": datetime.now(timezone.utc) - timedelta(days=120),
        "is_active": True,
    },
    "pat-002": {
        "id": "pat-002",
        "mrn": "MRN-2026-004129",
        "first_name": "Michael",
        "last_name": "Chang",
        "dob": "1985-09-24",
        "gender": "Male",
        "blood_group": "O+",
        "email": "m.chang85@example.com",
        "phone": "+1 (555) 345-6789",
        "address": "88 Commonwealth Ave",
        "city": "Boston",
        "state": "MA",
        "zip_code": "02215",
        "emergency_contact_name": "Grace Chang",
        "emergency_contact_phone": "+1 (555) 345-1122",
        "emergency_contact_relationship": "Sister",
        "allergies": ["Aspirin", "Ibuprofen / NSAIDs"],
        "chronic_conditions": ["Moderate Persistent Asthma", "Seasonal Allergic Rhinitis"],
        "medical_alerts": ["Severe Aspirin-Exacerbated Respiratory Disease (AERD)"],
        "primary_physician_id": "usr-doc-01",
        "insurance_policy_number": "POL-AETNA-449120",
        "insurance_provider": "Aetna Health",
        "created_at": datetime.now(timezone.utc) - timedelta(days=95),
        "is_active": True,
    },
    "pat-003": {
        "id": "pat-003",
        "mrn": "MRN-2026-004130",
        "first_name": "Sophia",
        "last_name": "Martinez",
        "dob": "1992-11-03",
        "gender": "Female",
        "blood_group": "B+",
        "email": "sophia.m@example.com",
        "phone": "+1 (555) 456-7890",
        "address": "210 Tremont Street",
        "city": "Boston",
        "state": "MA",
        "zip_code": "02116",
        "emergency_contact_name": "Carlos Martinez",
        "emergency_contact_phone": "+1 (555) 456-3344",
        "emergency_contact_relationship": "Brother",
        "allergies": ["Codeine"],
        "chronic_conditions": ["Migraine with Aura", "Generalized Anxiety Disorder"],
        "medical_alerts": ["Renal Clearance Monitoring Required"],
        "primary_physician_id": "usr-doc-01",
        "insurance_policy_number": "POL-UHC-992384",
        "insurance_provider": "UnitedHealthcare",
        "created_at": datetime.now(timezone.utc) - timedelta(days=45),
        "is_active": True,
    },
}

router = APIRouter(prefix="/patients", tags=["Patient Management"])

@router.get("", response_model=List[PatientResponse])
async def list_patients(
    query: Optional[str] = Query(None, description="Search by name, MRN, phone or email"),
    condition: Optional[str] = Query(None, description="Filter by chronic condition"),
):
    res = list(PATIENTS_STORE.values())
    if query:
        q = query.lower()
        res = [
            p for p in res
            if q in p["first_name"].lower()
            or q in p["last_name"].lower()
            or q in p["mrn"].lower()
            or q in p["phone"].lower()
            or (p["email"] and q in p["email"].lower())
        ]
    if condition:
        c = condition.lower()
        res = [
            p for p in res
            if any(c in cond.lower() for cond in p["chronic_conditions"])
        ]
    return res

@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(patient_id: str):
    if patient_id not in PATIENTS_STORE:
        raise HTTPException(status_code=404, detail="Patient record not found")
    return PATIENTS_STORE[patient_id]

@router.post("", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient(patient_in: PatientCreate):
    pid = f"pat-{uuid.uuid4().hex[:6]}"
    mrn = f"MRN-2026-{uuid.uuid4().hex[:6].upper()}"
    pdict = {
        "id": pid,
        "mrn": mrn,
        **patient_in.dict(),
        "created_at": datetime.now(timezone.utc),
        "is_active": True,
    }
    PATIENTS_STORE[pid] = pdict
    return PatientResponse(**pdict)

@router.get("/{patient_id}/timeline")
async def get_patient_timeline(patient_id: str):
    """Retrieve full chronological medical timeline for patient."""
    if patient_id not in PATIENTS_STORE:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return {
        "patient_id": patient_id,
        "events": [
            {
                "id": "evt-01",
                "type": "ENCOUNTER",
                "date": "2026-08-28T10:30:00Z",
                "title": "Comprehensive Cardiac Follow-up Encounter",
                "doctor": "Dr. Sarah Chen, MD",
                "summary": "Blood pressure regulated at 128/82 mmHg. Adjusted Atorvastatin to 40mg nightly.",
            },
            {
                "id": "evt-02",
                "type": "PRESCRIPTION",
                "date": "2026-08-28T11:00:00Z",
                "title": "E-Prescription Issued (Rx-2026-8891)",
                "doctor": "Dr. Sarah Chen, MD",
                "summary": "Atorvastatin 40mg (30 Tabs), Metformin 500mg ER (60 Tabs)",
            },
            {
                "id": "evt-03",
                "type": "PHARMACY_DISPENSED",
                "date": "2026-08-28T11:45:00Z",
                "title": "Prescription Validated & Dispensed",
                "pharmacist": "Marcus Vance, PharmD",
                "summary": "Dispensed via Smart FEFO from Batch #ATV-2026-B1. Patient counselled on nighttime dosing.",
            },
            {
                "id": "evt-04",
                "type": "LAB_RESULT",
                "date": "2026-08-25T09:15:00Z",
                "title": "Comprehensive Metabolic Panel & Lipid Panel",
                "technician": "David Kim, MLS",
                "summary": "HbA1c: 6.8% (Target Reached), LDL: 92 mg/dL, eGFR: >90 mL/min/1.73m² (Normal).",
            }
        ]
    }
