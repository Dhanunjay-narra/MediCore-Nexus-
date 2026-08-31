"""
MediCore Nexus - Doctor Management
"""

import uuid
from typing import List, Optional, Dict
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

class DoctorBase(BaseModel):
    user_id: str
    full_name: str
    license_number: str
    specialization: str
    department_id: str
    hospital_id: str
    consultation_fee: float = 150.00
    telemedicine_fee: float = 100.00
    available_days: List[str] = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    work_start_time: str = "08:30"
    work_end_time: str = "17:00"
    room_number: str = "Suite 304"
    biography: str
    rating: float = 4.9
    total_reviews: int = 142

class DoctorResponse(DoctorBase):
    id: str
    is_available: bool

DOCTORS_STORE: Dict[str, Dict] = {
    "doc-001": {
        "id": "doc-001",
        "user_id": "usr-doc-01",
        "full_name": "Dr. Sarah Chen, MD, FACC",
        "license_number": "MED-MD-883921",
        "specialization": "Interventional Cardiology",
        "department_id": "dept-cardio",
        "hospital_id": "hosp-001",
        "consultation_fee": 220.00,
        "telemedicine_fee": 150.00,
        "available_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "work_start_time": "08:30",
        "work_end_time": "17:00",
        "room_number": "Suite 304 - Cardio Wing",
        "biography": "Board-certified interventional cardiologist with over 15 years experience in coronary disease, cardiac risk stratification, and preventive cardiology.",
        "rating": 4.95,
        "total_reviews": 238,
        "is_available": True,
    },
    "doc-002": {
        "id": "doc-002",
        "user_id": "usr-admin-01",
        "full_name": "Dr. Alexander Wright, MD",
        "license_number": "MED-MD-772910",
        "specialization": "Internal Medicine & Clinical Pharmacology",
        "department_id": "dept-exec",
        "hospital_id": "hosp-001",
        "consultation_fee": 180.00,
        "telemedicine_fee": 120.00,
        "available_days": ["Monday", "Wednesday", "Friday"],
        "work_start_time": "09:00",
        "work_end_time": "16:00",
        "room_number": "Suite 101 - Exec Clinic",
        "biography": "Senior internist and chief medical officer specializing in complex chronic disease management and polypharmacy optimization.",
        "rating": 4.90,
        "total_reviews": 184,
        "is_available": True,
    },
    "doc-003": {
        "id": "doc-003",
        "user_id": "usr-doc-03",
        "full_name": "Dr. Emily Taylor, MD",
        "license_number": "MED-MD-991048",
        "specialization": "Neurology",
        "department_id": "dept-neuro",
        "hospital_id": "hosp-001",
        "consultation_fee": 250.00,
        "telemedicine_fee": 160.00,
        "available_days": ["Tuesday", "Thursday", "Saturday"],
        "work_start_time": "08:00",
        "work_end_time": "15:30",
        "room_number": "Suite 412 - Neuro Wing",
        "biography": "Specialist in neurovascular pathology, migraine disorders, and cognitive neurotherapeutics.",
        "rating": 4.88,
        "total_reviews": 112,
        "is_available": True,
    }
}

router = APIRouter(prefix="/doctors", tags=["Doctor Management"])

@router.get("", response_model=List[DoctorResponse])
async def list_doctors(specialization: Optional[str] = None):
    res = list(DOCTORS_STORE.values())
    if specialization:
        s = specialization.lower()
        res = [d for d in res if s in d["specialization"].lower()]
    return res

@router.get("/{doctor_id}", response_model=DoctorResponse)
async def get_doctor(doctor_id: str):
    if doctor_id not in DOCTORS_STORE:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return DOCTORS_STORE[doctor_id]
