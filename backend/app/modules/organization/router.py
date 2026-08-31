"""
MediCore Nexus - Organization & Hospital Management
"""

import uuid
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, status
from backend.app.database import Base, TimestampMixin
from sqlalchemy import String, Integer, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column

# Schemas
class OrganizationBase(BaseModel):
    name: str
    code: str
    tax_id: Optional[str] = None
    website: Optional[str] = None
    headquarters: Optional[str] = None

class OrganizationResponse(OrganizationBase):
    id: str
    is_active: bool

class HospitalBase(BaseModel):
    organization_id: str
    name: str
    code: str
    license_number: str
    address: str
    city: str
    state: str
    zip_code: str
    phone: str
    email: str
    total_beds: int = 150
    has_emergency: bool = True
    has_pharmacy: bool = True
    has_laboratory: bool = True
    has_telemedicine: bool = True

class HospitalResponse(HospitalBase):
    id: str
    is_active: bool

class DepartmentBase(BaseModel):
    hospital_id: str
    name: str
    code: str
    department_head: Optional[str] = None
    floor_number: int = 1
    description: Optional[str] = None

class DepartmentResponse(DepartmentBase):
    id: str
    is_active: bool

class BedBase(BaseModel):
    hospital_id: str
    department_id: str
    ward_name: str
    room_number: str
    bed_number: str
    bed_type: str = "Standard Inpatient"  # ICU, Standard, VIP, Recovery
    is_occupied: bool = False
    current_patient_id: Optional[str] = None

class BedResponse(BedBase):
    id: str

# Seed Data Store
ORGANIZATIONS: Dict[str, Dict] = {
    "org-001": {
        "id": "org-001",
        "name": "MediCore Global Healthcare Network",
        "code": "MC-GLOBAL",
        "tax_id": "TAX-99210-USA",
        "website": "https://medicorenexus.io",
        "headquarters": "Boston, MA",
        "is_active": True,
    }
}

HOSPITALS: Dict[str, Dict] = {
    "hosp-001": {
        "id": "hosp-001",
        "organization_id": "org-001",
        "name": "MediCore Central Hospital & Advanced Medical Center",
        "code": "MCH-01",
        "license_number": "MED-LIC-884920",
        "address": "742 Evergreen Healthcare Blvd",
        "city": "Boston",
        "state": "MA",
        "zip_code": "02115",
        "phone": "+1 (555) 019-2000",
        "email": "contact@mch-boston.medicorenexus.io",
        "total_beds": 350,
        "has_emergency": True,
        "has_pharmacy": True,
        "has_laboratory": True,
        "has_telemedicine": True,
        "is_active": True,
    },
    "hosp-002": {
        "id": "hosp-002",
        "organization_id": "org-001",
        "name": "MediCore Westside Community Hospital",
        "code": "MCH-02",
        "license_number": "MED-LIC-884921",
        "address": "1204 Sunset Medical Plaza",
        "city": "Cambridge",
        "state": "MA",
        "zip_code": "02138",
        "phone": "+1 (555) 019-3000",
        "email": "westside@mch-boston.medicorenexus.io",
        "total_beds": 120,
        "has_emergency": True,
        "has_pharmacy": True,
        "has_laboratory": True,
        "has_telemedicine": True,
        "is_active": True,
    }
}

DEPARTMENTS: Dict[str, Dict] = {
    "dept-cardio": {
        "id": "dept-cardio",
        "hospital_id": "hosp-001",
        "name": "Cardiology & Vascular Institute",
        "code": "CARD",
        "department_head": "Dr. Sarah Chen, MD",
        "floor_number": 3,
        "description": "Comprehensive cardiac diagnostics, interventional catheterization, and coronary intensive care.",
        "is_active": True,
    },
    "dept-pharm": {
        "id": "dept-pharm",
        "hospital_id": "hosp-001",
        "name": "Central Pharmacy Operations",
        "code": "PHARM",
        "department_head": "Marcus Vance, PharmD",
        "floor_number": 1,
        "description": "Inpatient, outpatient, and clinical compounding pharmacy services with automated FEFO dispensing.",
        "is_active": True,
    },
    "dept-er": {
        "id": "dept-er",
        "hospital_id": "hosp-001",
        "name": "Emergency & Trauma Medicine",
        "code": "ER",
        "department_head": "Dr. Robert Reynolds, MD",
        "floor_number": 1,
        "description": "24/7 Level 1 Trauma Center, rapid triage, resuscitation, and emergency critical stabilization.",
        "is_active": True,
    },
    "dept-lab": {
        "id": "dept-lab",
        "hospital_id": "hosp-001",
        "name": "Clinical Pathology & Molecular Laboratory",
        "code": "LAB",
        "department_head": "David Kim, MLS",
        "floor_number": 2,
        "description": "Automated biochemistry, hematology, immunology, microbiology, and STAT testing.",
        "is_active": True,
    },
    "dept-neuro": {
        "id": "dept-neuro",
        "hospital_id": "hosp-001",
        "name": "Neurology & Neurosurgery",
        "code": "NEURO",
        "department_head": "Dr. Emily Taylor, MD",
        "floor_number": 4,
        "description": "Stroke unit, neurological critical care, and brain/spine surgical suites.",
        "is_active": True,
    }
}

BEDS: Dict[str, Dict] = {
    "bed-101": {
        "id": "bed-101",
        "hospital_id": "hosp-001",
        "department_id": "dept-cardio",
        "ward_name": "Cardiac Care Ward A",
        "room_number": "301",
        "bed_number": "A",
        "bed_type": "ICU",
        "is_occupied": True,
        "current_patient_id": "pat-001",
    },
    "bed-102": {
        "id": "bed-102",
        "hospital_id": "hosp-001",
        "department_id": "dept-cardio",
        "ward_name": "Cardiac Care Ward A",
        "room_number": "301",
        "bed_number": "B",
        "bed_type": "Standard Inpatient",
        "is_occupied": False,
        "current_patient_id": None,
    },
    "bed-103": {
        "id": "bed-103",
        "hospital_id": "hosp-001",
        "department_id": "dept-er",
        "ward_name": "Emergency Triage Bay",
        "room_number": "104",
        "bed_number": "Bay 1",
        "bed_type": "Emergency Recovery",
        "is_occupied": True,
        "current_patient_id": "pat-002",
    },
}

# Router
router = APIRouter(prefix="/organizations", tags=["Organization & Hospital Management"])

@router.get("", response_model=List[OrganizationResponse])
async def list_organizations():
    return list(ORGANIZATIONS.values())

@router.get("/hospitals", response_model=List[HospitalResponse])
async def list_hospitals():
    return list(HOSPITALS.values())

@router.get("/hospitals/{hospital_id}", response_model=HospitalResponse)
async def get_hospital(hospital_id: str):
    if hospital_id not in HOSPITALS:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return HOSPITALS[hospital_id]

@router.get("/departments", response_model=List[DepartmentResponse])
async def list_departments(hospital_id: Optional[str] = None):
    res = list(DEPARTMENTS.values())
    if hospital_id:
        res = [d for d in res if d["hospital_id"] == hospital_id]
    return res

@router.get("/beds", response_model=List[BedResponse])
async def list_beds(hospital_id: Optional[str] = None, department_id: Optional[str] = None):
    res = list(BEDS.values())
    if hospital_id:
        res = [b for b in res if b["hospital_id"] == hospital_id]
    if department_id:
        res = [b for b in res if b["department_id"] == department_id]
    return res
